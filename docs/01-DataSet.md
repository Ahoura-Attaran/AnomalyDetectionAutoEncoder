# CICIDS2017 Dataset

**Project Documentation — Stage 2: Dataset**

---

## 1. Dataset Overview

This project uses the **CICIDS2017** intrusion detection dataset as the primary source of network traffic data.

The dataset was developed by the Canadian Institute for Cybersecurity (CIC) and contains network traffic representing both benign behavior and multiple types of malicious activities.

The dataset is used in this project to investigate whether an Autoencoder trained on benign traffic can identify malicious network flows through reconstruction error.

The external dataset source used during this project is:

**Hugging Face:** `bvk/CICIDS-2017`

The original dataset is organized according to traffic collected over five working days:

```text
Monday
Tuesday
Wednesday
Thursday
Friday
```

The project, however, does not directly train on the original daily files. Instead, the experimental pipeline uses processed Parquet files in which benign and attack traffic are separated.

---

# 2. Dataset Organization

The experimental dataset used by the project contains the following traffic groups:

| Category    | File                                      |
| ----------- | ----------------------------------------- |
| Normal      | `Benign-Monday-no-metadata.parquet`       |
| Botnet      | `Botnet-Friday-no-metadata.parquet`       |
| DDoS        | `DDoS-Friday-no-metadata.parquet`         |
| DoS         | `DoS-Wednesday-no-metadata.parquet`       |
| Port Scan   | `Portscan-Friday-no-metadata.parquet`     |
| Web Attacks | `WebAttacks-Thursday-no-metadata.parquet` |
| Brute Force | `Bruteforce-Tuesday-no-metadata.parquet`  |

This exact file mapping is defined in both the first and second implementations of the project.

The project therefore treats the dataset as two major groups:

```text
                    CICIDS2017
                        │
              ┌─────────┴─────────┐
              │                   │
           Normal              Attacks
              │                   │
     Benign-Monday         ┌──────┼───────────────┐
                           │      │       │       │
                         DoS    DDoS   Botnet   ...
```

---

# 3. Traffic Categories

The current experimental pipeline evaluates the following attack families.

### 3.1 Normal Traffic

Normal traffic is represented by:

```text
Benign-Monday-no-metadata.parquet
```

This dataset forms the basis of Autoencoder training.

The Autoencoder does not learn an explicit representation of each attack class during the training stage. Instead, it learns to reconstruct benign traffic.

---

### 3.2 Brute Force

```text
Bruteforce-Tuesday-no-metadata.parquet
```

This traffic is treated as malicious traffic during evaluation.

---

### 3.3 DoS

```text
DoS-Wednesday-no-metadata.parquet
```

Denial-of-Service traffic is used to evaluate whether the learned normal representation can identify DoS behavior as anomalous.

---

### 3.4 Web Attacks

```text
WebAttacks-Thursday-no-metadata.parquet
```

This category represents malicious web-related traffic.

---

### 3.5 Botnet

```text
Botnet-Friday-no-metadata.parquet
```

Botnet traffic is evaluated as an attack category.

---

### 3.6 DDoS

```text
DDoS-Friday-no-metadata.parquet
```

Distributed Denial-of-Service traffic is evaluated separately from other DoS traffic.

---

### 3.7 Port Scan

```text
Portscan-Friday-no-metadata.parquet
```

Port scanning traffic is evaluated as another attack category.

---

# 4. Why the Dataset Is Suitable for Anomaly Detection

The dataset is particularly useful for this project because it contains both benign and malicious network-flow observations.

The experimental methodology uses this structure differently from a conventional supervised classification problem.

Instead of performing:

```text
Input → Multi-class Classifier → Attack Class
```

the project uses:

```text
Benign Traffic
      │
      ▼
Autoencoder Training
      │
      ▼
Learn Normal Representation
      │
      ▼
Reconstruction Error
      │
      ▼
Normal / Anomaly
```

The attack datasets are primarily used after model training to determine whether malicious observations generate larger reconstruction errors than benign observations.

---

# 5. Data Loading

The project loads all Parquet files using Pandas:

```python
df = pd.read_parquet(path)
```

After loading, whitespace is removed from column names:

```python
df.columns = df.columns.str.strip()
```

The files are stored in a dictionary according to their traffic category.

Conceptually:

```python
DATA_FILES = {
    "normal": "...",
    "botnet": "...",
    "ddos": "...",
    "dos": "...",
    "portscan": "...",
    "webattacks": "...",
    "bruteforce": "..."
}
```

This same loading structure is present in V1 and V2.

---

# 6. Feature and Label Separation

The dataset contains a `Label` column.

During preprocessing, the label is separated from the feature matrix.

Conceptually:

```python
y = df["Label"]
X = df.drop(columns=["Label"])
```

The Autoencoder receives only the numerical feature matrix `X`.

The label is not used as an input feature.

This distinction is important because the objective of the model is anomaly detection rather than direct supervised attack classification.

---

# 7. Initial Data Cleaning

The preprocessing pipeline performs several basic cleaning operations.

### 7.1 Infinite Values

Positive and negative infinity values are replaced with missing values:

```python
X = X.replace([np.inf, -np.inf], np.nan)
```

### 7.2 Missing Values

Rows containing missing values are subsequently removed:

```python
X = X.dropna()
```

If labels are available, the labels are aligned with the remaining rows:

```python
y = y.loc[X.index]
```

This cleaning procedure is implemented in both V1 and V2.

---

# 8. Constant Feature Removal

The first implementation identifies constant features from the benign dataset:

```python
constant_cols = X_all.columns[
    X_all.nunique() <= 1
].tolist()
```

These columns are removed before model training.

The remaining feature names are stored as:

```text
Cols/feature_columns.pkl
```

while the removed constant columns are stored as:

```text
Cols/constant_cols.pkl
```

This ensures that the same feature structure can later be applied to attack datasets.

---

# 9. Train / Validation / Test Strategy

A major methodological decision in V1 is separating benign traffic into three subsets.

The benign dataset is divided as follows:

```text
                 Normal Dataset
                       │
                 ┌─────┴─────┐
                 │           │
              Train         Temp
               70%           30%
                             │
                       ┌─────┴─────┐
                       │           │
                     Val          Test
                     15%          15%
```

The first split uses:

```python
test_size=0.3
```

and the temporary set is then divided equally:

```python
test_size=0.5
```

Both operations use:

```python
random_state=42
shuffle=True
```

Therefore, relative to the original benign dataset:

* Training = 70%
* Validation = 15%
* Normal Test = 15%

This separation was introduced specifically to avoid using the same validation data for both model selection and final evaluation.

---

# 10. Feature Scaling

## V1

The first implementation uses:

```python
StandardScaler()
```

The scaler is fitted exclusively on the training data:

```python
X_train = scaler.fit_transform(train_data)
```

and then applied to validation and normal test data:

```python
X_val = scaler.transform(val_data)
X_test_normal = scaler.transform(test_normal_data)
```

The fitted scaler is saved as:

```text
models/scaler.pkl
```

This prevents information from the validation and test sets from influencing the scaling parameters.

---

# 11. Outlier Problem Identified in V1

During the evolution of the project, the first implementation exposed a preprocessing problem.

Some network-flow features can contain extremely large numerical values.

Such values can strongly affect the statistics used by conventional scaling methods.

This can result in:

```text
Extreme values
      │
      ▼
Scaling distortion
      │
      ▼
Large transformed values
      │
      ▼
Large reconstruction loss
      │
      ▼
Unstable / exploding validation loss
```

This issue motivated the changes introduced in V2.

---

# 12. V2: Outlier Clipping

V2 introduces an explicit outlier-clipping stage before scaling.

The clipping bounds are calculated using:

```python
lower_q = 0.001
upper_q = 0.999
```

Therefore, for each feature, the lower and upper limits correspond to the 0.1th and 99.9th percentiles of the training data.

The important methodological decision is that these bounds are calculated **only from the training set**:

```python
clip_lower, clip_upper = compute_clip_bounds(train_data)
```

The same bounds are then applied to:

* Training data
* Validation data
* Normal test data
* Attack data

This avoids calculating preprocessing statistics from the evaluation data.

The clipping parameters are stored in:

```text
Cols/clip_bounds.pkl
```

V2 explicitly introduces this mechanism to reduce the influence of extreme numerical values.

---

# 13. V2: Robust Scaling

After clipping, V2 replaces `StandardScaler` with:

```python
RobustScaler()
```

The scaler is still fitted only on the training set:

```python
X_train = scaler.fit_transform(train_data)
```

and then applied to validation, test, and attack data.

The resulting pipeline becomes:

```text
Raw Features
     │
     ▼
Clean NaN / Inf
     │
     ▼
Remove Constant Features
     │
     ▼
Train-based Outlier Clipping
     │
     ▼
RobustScaler
     │
     ▼
Autoencoder
```

This represents the main methodological improvement from V1 to V2.

---

# 14. Data Leakage Considerations

The project explicitly considers data leakage during dataset preparation.

The preprocessing parameters are derived from training data wherever possible.

In particular:

### Scaling

```text
Scaler.fit()
      │
      ▼
Training data only
```

### Outlier Clipping

```text
Clip bounds
      │
      ▼
Training data only
```

The resulting parameters are then reused on validation, normal test, and attack data.

This separation is important because using information from test or attack traffic to construct preprocessing statistics could artificially improve the measured performance.

---

# 15. Experimental Dataset Pipeline

The complete dataset-processing pipeline in V2 can therefore be summarized as:

```text
CICIDS2017
    │
    ▼
Processed Parquet Files
    │
    ├───────────────┐
    │               │
 Normal           Attacks
    │               │
    ▼               ├── Brute Force
Clean Features     ├── DoS
    │               ├── Web Attacks
    ▼               ├── Botnet
Remove Constants   ├── DDoS
    │               └── Port Scan
    ▼
Train / Validation / Test
    │
    ▼
Train-based Outlier Clipping
    │
    ▼
Robust Scaling
    │
    ▼
Autoencoder
```

---

# 16. Dataset Preparation Decisions

The major dataset-related decisions made during the first two project versions are summarized below.

| Decision          | V1               | V2               |
| ----------------- | ---------------- | ---------------- |
| File format       | Parquet          | Parquet          |
| Data loading      | Pandas           | Pandas           |
| Label separation  | Yes              | Yes              |
| Inf handling      | Replace with NaN | Replace with NaN |
| Missing rows      | Removed          | Removed          |
| Constant features | Removed          | Removed          |
| Train/Val/Test    | 70/15/15         | 70/15/15         |
| Scaling           | StandardScaler   | RobustScaler     |
| Outlier clipping  | No               | Yes              |
| Clip statistics   | —                | Train only       |
| Reproducibility   | Seed 42          | Seed 42          |

---

# 17. Important Dataset Questions for Later Verification

The following values should be extracted directly from the actual Parquet files before being included as definitive numerical statements in the paper:

* Number of rows in each file
* Number of original features
* Number of features after constant-column removal
* Number of rows removed because of NaN/Inf values
* Number of constant features
* Exact distribution of labels
* Minimum and maximum values of important features
* Number of observations affected by clipping
* Final training, validation, and normal-test sample counts

These statistics should be generated directly from the experimental data rather than estimated from external descriptions of CICIDS2017.

---

# 18. Dataset Role in the Research

The dataset is not merely used as a generic benchmark.

Its structure enables the project to evaluate three different aspects of the anomaly detector:

### Normality Learning

The model learns normal traffic from benign observations.

### Binary Anomaly Detection

The model is evaluated on:

```text
Normal vs Attack
```

### Attack-Specific Behavior

The reconstruction errors can additionally be analyzed separately for:

```text
Brute Force
DoS
Web Attacks
Botnet
DDoS
Port Scan
```

This third level becomes particularly important in later project versions, where per-attack metrics are introduced.

---

## 19. Dataset Documentation Status

**Dataset:** CICIDS2017

**External Source:** Hugging Face `bvk/CICIDS-2017`

**Experimental Format:** Parquet

**Traffic Groups:** 1 benign + 6 attack categories

**Primary Training Data:** Benign traffic

**Primary Evaluation Data:** Benign test + attack traffic

**Feature Processing:** Cleaning → Constant Feature Removal → Outlier Handling → Scaling

**Current Scaling Method:** RobustScaler (V2)

**Current Outlier Strategy:** Train-derived percentile clipping (V2)

**Train / Validation / Test:** 70% / 15% / 15% of benign data

**Random Seed:** 42
