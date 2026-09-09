# Experiment History

## V1 → V2

---

## Version 1 — Baseline Autoencoder

### Objective

The first implementation established the baseline Autoencoder anomaly-detection pipeline.

The objective was to determine whether an Autoencoder trained on benign network traffic could distinguish malicious network flows based on reconstruction error.

### Pipeline

```text
Load Parquet Data
      ↓
Clean NaN / Inf
      ↓
Remove Constant Features
      ↓
Train / Validation / Test Split
      ↓
StandardScaler
      ↓
Train Autoencoders
      ↓
Calculate Reconstruction Error
      ↓
99th Percentile Threshold
      ↓
Evaluate Normal vs Attack
```

### Models

Two architectures were implemented:

**Shallow Autoencoder**

```text
Input
 ↓
64
 ↓
32
 ↓
16  ← Bottleneck
 ↓
32
 ↓
64
 ↓
Output
```

**Deep Autoencoder**

```text
Input
 ↓
128
 ↓
64
 ↓
32
 ↓
8   ← Bottleneck
 ↓
32
 ↓
64
 ↓
128
 ↓
Output
```

Both models use ReLU activations in hidden layers and a linear output layer. The reconstruction objective is Mean Squared Error (MSE).

### Threshold

The anomaly threshold is defined as:

```python
threshold = np.percentile(validation_errors, 99)
```

Therefore, observations whose reconstruction error exceeds the 99th percentile of benign validation errors are classified as anomalies.

### Evaluation

V1 evaluates the combined normal test and attack data using:

* Classification Report
* Confusion Matrix
* ROC-AUC

The anomaly score is the reconstruction error.

---

# Problem Identified After V1

The main issue addressed after V1 was the influence of extreme numerical values.

The dataset contains flow-based numerical features with potentially very large values.

The initial pipeline used:

```text
Raw Data
 ↓
StandardScaler
 ↓
Autoencoder
```

Without an explicit outlier-handling stage.

This created a risk that extreme observations could dominate the scaling statistics and produce unusually large transformed values.

The second implementation therefore introduced a dedicated outlier-handling mechanism.

---

# Version 2 — Robust Preprocessing

## Objective

The objective of V2 was to improve the numerical stability of the preprocessing pipeline and reduce the effect of extreme feature values.

Two changes were introduced:

1. Train-based percentile clipping
2. Replacement of StandardScaler with RobustScaler

---

## Change 1 — Train-Based Outlier Clipping

V2 calculates feature-wise clipping boundaries from the training dataset.

```python
lower_q = 0.001
upper_q = 0.999
```

For each feature:

```text
Lower Bound = 0.1th percentile
Upper Bound = 99.9th percentile
```

The bounds are calculated only using training data.

The same bounds are then applied to validation, normal test, and attack observations.

### Why?

The objective is to prevent extreme numerical values from disproportionately affecting the preprocessing pipeline while preserving the same transformation for all datasets.

---

## Change 2 — StandardScaler → RobustScaler

V1:

```python
StandardScaler()
```

V2:

```python
RobustScaler()
```

This change was motivated by the presence of extreme values.

The resulting preprocessing sequence became:

```text
Clean Data
   ↓
Remove Constant Features
   ↓
Split Normal Data
   ↓
Compute Train Clip Bounds
   ↓
Clip Train / Val / Test
   ↓
RobustScaler
   ↓
Autoencoder
```

---

# V1 vs V2

| Component            | V1                | V2                  |
| -------------------- | ----------------- | ------------------- |
| Data cleaning        | NaN / Inf removal | Same                |
| Constant features    | Removed           | Removed             |
| Normal split         | 70/15/15          | 70/15/15            |
| Scaler               | StandardScaler    | RobustScaler        |
| Outlier handling     | None              | Percentile clipping |
| Clip bounds          | —                 | Train-derived       |
| Attack preprocessing | Scaling           | Clipping + scaling  |
| Shallow bottleneck   | 16                | 16                  |
| Deep bottleneck      | 8                 | 8                   |
| Loss                 | MSE               | MSE                 |
| Threshold            | 99th percentile   | 99th percentile     |
| Evaluation           | Binary            | Binary              |

---

# Scientific Interpretation

V2 should not be considered a completely new model.

Instead, it is a **preprocessing refinement of the baseline architecture**.

The Autoencoder architectures and thresholding strategy remain unchanged.

The controlled variable is primarily the preprocessing strategy:

```text
V1:
StandardScaler
     ↓
Autoencoder

V2:
Outlier Clipping
     ↓
RobustScaler
     ↓
Autoencoder
```

Therefore, the V1 → V2 comparison can later be interpreted as an experiment measuring the effect of robust preprocessing on Autoencoder-based anomaly detection.

---

# Reproducibility

Both versions use:

```python
SEED = 42
```

and initialize NumPy and TensorFlow random generators using this seed.

The preprocessing artifacts are also persisted to disk, allowing the transformation pipeline to be reproduced.

---

# Status

**V1:** Baseline established.

**V2:** Robust preprocessing introduced.

**Main hypothesis of V2:**

> Reducing the influence of extreme numerical values before scaling should produce a more stable representation of network-flow features and improve Autoencoder training behavior.

**Next step:** Analyze V3 and determine whether the improvement is sufficient or whether the model requires additional changes.

## V3 — Log Transformation for Heavy-Tailed Features

### Motivation

Version 2 introduced train-based percentile clipping and `RobustScaler` to reduce the effect of extreme values. However, the preprocessing pipeline could still produce excessively large scaled values for some highly skewed and zero-inflated features.

Rate-based network-flow features such as `Flow Bytes/s` and `Flow Packets/s` can contain a large concentration of values near zero together with a long tail of very large values. In such cases, the IQR used by `RobustScaler` may remain very small, causing otherwise normal observations to be mapped to very large scaled values.

The code comments associated this behavior with extremely large reconstruction losses and thresholds.

### Change

V3 introduced a signed logarithmic transformation before scaling:

$$
x' = sign(x)\log(1+|x|)
$$

implemented as:

```python
def log_transform(X_df):
    return np.sign(X_df) * np.log1p(np.abs(X_df))
```

The transformation compresses large magnitudes while preserving the sign of the original value.

### Updated preprocessing pipeline

The V3 preprocessing pipeline became:

```text
Normal Data
    ↓
Train / Validation / Test split
    ↓
Compute clipping bounds from Train only
    ↓
Percentile clipping
    ↓
Signed log1p transformation
    ↓
RobustScaler fitted on Train only
    ↓
Autoencoder
```

The same train-derived clipping bounds and the same fitted scaler are applied to validation, normal test, and attack data.

### What remained unchanged

V3 intentionally kept the following components unchanged from V2:

* Shallow Autoencoder architecture
* Deep Autoencoder architecture
* Bottleneck dimensions
* Batch Normalization
* Dropout
* Adam optimizer
* MSE reconstruction loss
* EarlyStopping
* ReduceLROnPlateau
* ModelCheckpoint
* 70/15/15 normal-data split
* 99th-percentile validation threshold
* Binary Normal vs Attack evaluation

Therefore, V3 should primarily be interpreted as a **preprocessing refinement**, rather than a model-architecture experiment.

---

## V4 — Per-Attack-Type Evaluation

### Motivation

Previous versions evaluated all attack samples together as a single `Attack` class.

Although this provides an overall binary anomaly-detection result, it can hide important differences between attack families.

For example, a model may detect volumetric attacks effectively while failing to detect attacks whose flow-level characteristics are closer to normal traffic.

Therefore, V4 introduced a diagnostic evaluation stage that evaluates each attack family separately.

### Change

A new function was introduced:

```python
evaluate_per_attack_type(...)
```

For every attack dataset, the function:

1. Loads and cleans the attack data.
2. Applies the same train-derived clipping bounds.
3. Applies the signed `log1p` transformation.
4. Applies the fitted `RobustScaler`.
5. Calculates reconstruction error.
6. Compares attack samples against the same untouched normal test set.
7. Calculates attack-specific detection metrics.

The reported metrics are:

* Recall
* Precision
* F1-score
* ROC-AUC
* Number of attack samples

### Evaluation structure

V4 therefore contains two complementary evaluation levels:

#### Global evaluation

```text
Normal Test + All Attack Types
            ↓
      Normal vs Attack
            ↓
 Classification Report
 Confusion Matrix
 ROC-AUC
```

#### Per-attack evaluation

```text
Normal Test + Attack Type A → Metrics
Normal Test + Attack Type B → Metrics
Normal Test + Attack Type C → Metrics
...
```

### Scientific significance

This change does not modify the trained model. Instead, it increases the diagnostic resolution of the experiment.

V4 allows the research to answer not only:

> Can the autoencoder detect attacks?

but also:

> Which attack types can the autoencoder detect reliably, and which attack types remain difficult?

This distinction is important for interpreting the practical effectiveness of the anomaly-detection approach.
