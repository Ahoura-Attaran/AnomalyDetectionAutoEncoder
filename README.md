# CICIDS2017 Network Anomaly Detection Using Feature-Aware Autoencoders

A machine learning project for **network anomaly detection** using Autoencoders on the CICIDS2017 dataset.

The project focuses on detecting anomalous network traffic by learning the reconstruction pattern of benign traffic and identifying samples that produce unusually high reconstruction errors.

The project is developed incrementally through multiple experimental versions (**V1 → V8**), where each version introduces a specific methodological improvement.

---

##  Project Overview

Network intrusion detection systems need to distinguish between normal and malicious network traffic.

In this project, an **Autoencoder-based anomaly detection approach** is used:

> The model is primarily trained to reconstruct benign network traffic.
> Traffic that cannot be reconstructed well is considered potentially anomalous.

The project gradually evolves from a basic Autoencoder into a **feature-aware Autoencoder with semi-supervised threshold calibration**.

### Main objectives

* Detect anomalous network traffic
* Compare different preprocessing strategies
* Investigate the effect of bottleneck dimensionality
* Analyze anomaly detection performance for different attack families
* Investigate feature-level separability
* Improve reconstruction-based anomaly scoring
* Develop a reproducible experimental pipeline
* Document the evolution of the model from V1 to V8

---

#  Dataset

The project is based on the **CICIDS2017** dataset.

Dataset source:

https://huggingface.co/datasets/bvk/CICIDS-2017

The project uses processed Parquet files representing benign traffic and different attack families.

### Processed datasets

| Dataset                                   | Traffic           |
| ----------------------------------------- | ----------------- |
| `Benign-Monday-no-metadata.parquet`       | Benign            |
| `Bruteforce-Tuesday-no-metadata.parquet`  | Brute Force       |
| `DoS-Wednesday-no-metadata.parquet`       | Denial of Service |
| `WebAttacks-Thursday-no-metadata.parquet` | Web Attacks       |
| `Botnet-Friday-no-metadata.parquet`       | Botnet            |
| `DDoS-Friday-no-metadata.parquet`         | DDoS              |
| `Portscan-Friday-no-metadata.parquet`     | Port Scan         |

Exact dataset statistics are intentionally not hard-coded in this README and should be generated from the actual project data.

---

#  Methodology

The general pipeline is:

```text
CICIDS2017
     │
     ▼
Load Parquet Data
     │
     ▼
Feature Cleaning
     │
     ├── Remove ±∞
     ├── Remove NaN
     └── Remove Constant Features
     │
     ▼
Train / Validation / Test
     │
     ▼
Preprocessing
     │
     ├── Outlier Clipping
     ├── Robust Scaling
     └── Log Transformation
     │
     ▼
Autoencoder
     │
     ▼
Reconstruction Error
     │
     ▼
Threshold Selection
     │
     ▼
Normal / Anomaly
     │
     ▼
Global + Per-Attack Evaluation
```

---

#  Model Architecture

Two Autoencoder architectures are evaluated.

## Shallow Autoencoder

Current architecture:

```text
Input
  │
Dense(64, ReLU)
  │
BatchNormalization
  │
Dropout(0.2)
  │
Dense(32, ReLU)
  │
BatchNormalization
  │
Dropout(0.2)
  │
Bottleneck(8)
  │
Dense(32)
  │
Dense(64)
  │
Output
```

## Deep Autoencoder

Current architecture:

```text
Input
  │
Dense(128)
  │
BatchNormalization
  │
Dropout
  │
Dense(64)
  │
BatchNormalization
  │
Dropout
  │
Dense(32)
  │
BatchNormalization
  │
Dropout
  │
Bottleneck(12)
  │
Dense(32)
  │
BatchNormalization
  │
Dropout
  │
Dense(64)
  │
BatchNormalization
  │
Dropout
  │
Dense(128)
  │
Output
```

Both architectures are trained using the Adam optimizer with reconstruction-based loss.

---

# 🔬 Experimental Evolution

The project is intentionally developed as a sequence of experiments.

```text
V1
 │
 ▼
V2
 │
 ▼
V3
 │
 ▼
V4
 │
 ▼
V5
 │
 ▼
V6
 │
 ▼
V7
 │
 ▼
V8
 │
 ▼
V9
```

Each version addresses a specific limitation discovered during experimentation.

---

## V1 — Baseline Autoencoder

The first implementation establishes the baseline pipeline.

### Main components

* Data loading
* Feature cleaning
* Constant-feature removal
* StandardScaler
* 70/15/15 normal-data split
* Shallow Autoencoder
* Deep Autoencoder
* Reconstruction error
* 99th-percentile threshold
* ROC-AUC
* Confusion matrix
* Classification report

The V1 baseline provides the reference point for subsequent experiments.

---

## V2 — Robust Preprocessing

V2 addresses the effect of extreme feature values.

### Changes

* Train-derived percentile clipping
* `RobustScaler`
* Same clipping bounds applied to validation, test and attack data

The clipping boundaries are calculated **only from the training data** to reduce data leakage.

---

## V3 — Signed Log Transformation

V3 introduces a signed logarithmic transformation:

```python
sign(x) * log1p(abs(x))
```

The purpose is to compress highly skewed and large-magnitude features while preserving their sign.

The transformation is applied after clipping and before scaling.

---

## V4 — Per-Attack Evaluation

V4 adds evaluation at the attack-family level.

Instead of reporting only one overall result, the model is evaluated separately on:

* Bruteforce
* DoS
* WebAttacks
* Botnet
* DDoS
* Portscan

Reported metrics include:

* Recall
* Precision
* F1-score
* ROC-AUC
* Number of samples

This allows weaknesses against individual attack families to be identified.

---

## V5 — Feature Separability Analysis

V5 introduces a model-independent feature diagnostic based on a Cohen's-d-style effect size.

For each attack family and feature:

```text
d = | μ_attack - μ_normal | / σ_normal
```

Large values indicate stronger separation between attack and benign traffic.

This analysis is used as a diagnostic rather than directly modifying the model.

The purpose is to distinguish between:

```text
Model problem
      vs.
Feature-information problem
```

---

## V6 — Bottleneck Compression + F1 Threshold

V6 introduces two major changes.

### 1. Smaller bottlenecks

```text
Shallow: 16 → 8
Deep:     8 → 4
```

The goal is to investigate whether stronger compression improves the ability of the Autoencoder to learn the normal-traffic manifold.

### 2. Semi-supervised threshold calibration

Instead of relying only on the benign validation distribution, V6 uses a small labeled calibration set containing:

* Normal validation samples
* Samples from each attack family

The threshold is selected by maximizing F1-score.

The Autoencoder itself is still trained on benign traffic, while attack labels influence the **threshold selection** rather than the model weights.

---

## V7 — Deep Bottleneck Adjustment

The results from V6 suggested that the deep Autoencoder may have been overly compressed.

Therefore:

```text
Deep bottleneck:

V6: 4
V7: 12
```

The shallow bottleneck remains:

```text
8
```

V7 keeps the V6 preprocessing and threshold-calibration strategy and focuses on testing a less restrictive deep representation.

---

#  V8 — Feature-Aware Autoencoder

V8 introduces the most significant methodological change so far.

Two main improvements are added.

---

## 1. Selective Log Transformation

Instead of applying the logarithmic transformation to every feature, V8 calculates feature skewness using the training data.

A feature is considered skewed when:

```text
|skewness| > 1.0
```

Only those features receive the signed `log1p` transformation.

This allows approximately symmetric features to remain unchanged while strongly skewed features are compressed.

The selected feature list is stored in:

```text
Cols/skewed_cols.pkl
```

---

## 2. Feature-Weighted Reconstruction Loss

V8 uses feature separability information to assign different weights to features.

Cohen's-d-style effect sizes are calculated for attack families.

For each feature, the maximum effect size across attack families is obtained.

The values are then mapped to a weight range:

```text
1 ≤ weight ≤ 5
```

Features with stronger attack/normal separation receive larger weights.

The resulting weights are stored in:

```text
Cols/feature_weights.pkl
```

---

## Weighted MSE

Instead of standard reconstruction loss:

```text
MSE = mean((x - x̂)²)
```

V8 uses:

```text
Weighted MSE =
    mean(weight × (x - x̂)²)
```

The same feature weights are also used when calculating the reconstruction-based anomaly score.

This keeps the training objective and anomaly scoring mechanism aligned.

---

#  Important Methodological Note

V8 is not purely unsupervised.

Although the Autoencoder learns to reconstruct benign traffic, attack/normal separation information is used to construct feature weights.

In addition, attack samples are used during threshold calibration.

Therefore the current V8 methodology is better described as:

> **Feature-aware Autoencoder with semi-supervised threshold calibration**

rather than a completely unsupervised anomaly detection system.

This distinction is important for the final academic paper.

---

# 📈 Evaluation

The project evaluates models using both global and attack-specific metrics.

### Global metrics

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion Matrix

### Attack-specific metrics

For every attack family:

```text
Recall
Precision
F1
ROC-AUC
N samples
```

### Additional diagnostics

* Reconstruction error distribution
* Training/validation loss
* ROC curve
* Feature separability
* Feature weights

---

# 🔍 Scientific Considerations

Several methodological issues are explicitly tracked throughout the experiments.

## Data leakage

Preprocessing parameters such as:

* clipping bounds
* scalers
* skewed-feature selection

must be calculated using training data only.

---

## Threshold calibration overlap

The current V6–V8 implementation uses attack samples during threshold calibration.

Those samples are not completely separated from the final attack evaluation.

Therefore, threshold-dependent metrics may be optimistic.

A future experiment should separate:

```text
Training
   ↓
Validation
   ↓
Calibration
   ↓
Final Test
```

with no overlap between calibration and final test samples.

---

## V6 confounding

V6 changes two variables simultaneously:

```text
Bottleneck size
+
Threshold strategy
```

Therefore, a performance change cannot be attributed to only one of them.

A proper ablation should evaluate:

```text
A: Old bottleneck + P99
B: New bottleneck + P99
C: Old bottleneck + F1 threshold
D: New bottleneck + F1 threshold
```

---

## V8 ablation

V8 also introduces multiple changes simultaneously.

A recommended ablation is:

```text
A: All-feature log + standard MSE + F1 threshold

B: Selective log + standard MSE + F1 threshold

C: Selective log + weighted MSE + F1 threshold

D: Selective log + weighted MSE + P99 threshold
```

This allows the contribution of each component to be studied independently.

---

#  Project Structure

```text
project/
│
├── data/
│   └── *.parquet
│
├── Cols/
│   ├── constant_cols.pkl
│   ├── feature_columns.pkl
│   ├── clip_bounds.pkl
│   ├── skewed_cols.pkl
│   └── feature_weights.pkl
│
├── models/
│   ├── scaler.pkl
│   └── *.keras
│
│
├── docs/
│   ├── 00-project-overview.md
│   ├── 01-dataset.md
│   ├── 02-preprocessing.md
│   ├── 03-model.md
│   ├── 04-threshold.md
│   ├── 05-evaluation.md
│   ├── 06-experiment-history.md
│   ├── 07-results-analysis.md
│   ├── 08-discussion.md
│   └── 09-paper-outline.md
|   ├── experiments/
│   └── EXPERIMENT_LOG.md
│
├── autoencoder_anomaly_detection_1.py
├── autoencoder_anomaly_detection_2.py
├── autoencoder_anomaly_detection_3.py
├── autoencoder_anomaly_detection_4.py
├── autoencoder_anomaly_detection_5.py
├── autoencoder_anomaly_detection_6.py
├── autoencoder_anomaly_detection_7.py
├── autoencoder_anomaly_detection_8.py
│
└── README.md
```

---

#  Reproducibility

Experiments use a fixed random seed:

```python
SEED = 42

np.random.seed(SEED)
tf.random.set_seed(SEED)
```

Training uses:

* Adam optimizer
* Mean-squared reconstruction objective
* EarlyStopping
* ReduceLROnPlateau
* ModelCheckpoint

The project stores important preprocessing artifacts so that inference can reproduce the same transformations.

---

#  Experiment Tracking

Every major methodological change is documented as a separate experiment.

| Version | Main contribution                     |
| ------- | ------------------------------------- |
| V1      | Baseline Autoencoder                  |
| V2      | Clipping + RobustScaler               |
| V3      | Signed Log Transformation             |
| V4      | Per-Attack Evaluation                 |
| V5      | Feature Separability Analysis         |
| V6      | Bottleneck Compression + F1 Threshold |
| V7      | Deep Bottleneck 4 → 12                |
| V8      | Selective Log + Feature-Weighted Loss |

Detailed experiment history is available in:

```text
experiments/EXPERIMENT_LOG.md
```

---

#  Documentation

Detailed technical documentation is available under:

```text
docs/
```

Recommended reading order:

1. `00-project-overview.md`
2. `01-dataset.md`
3. `02-preprocessing.md`
4. `03-model.md`
5. `04-threshold.md`
6. `05-evaluation.md`
7. `06-experiment-history.md`
8. `07-results-analysis.md`
9. `08-discussion.md`
10. `09-paper-outline.md`

---

#  Future Work

The next stage of the project focuses on controlled experimentation rather than simply adding more complexity.

Planned work includes:

* Controlled ablation studies
* Strict calibration/test separation
* Comparison of threshold strategies
* Investigation of unseen attack families
* Analysis of feature weights
* Statistical comparison between models
* Robustness testing
* Final model selection
* Reproducible experiment tables
* Preparation of the final academic paper

---

#  Research Direction

The current research direction can be summarized as:

```text
CICIDS2017
     ↓
Benign Traffic Representation
     ↓
Autoencoder
     ↓
Feature Separability Analysis
     ↓
Feature-Aware Reconstruction
     ↓
Semi-Supervised Threshold Calibration
     ↓
Attack-Family Evaluation
```

A working title for the eventual paper is:

> **CICIDS2017 Network Anomaly Detection Using Feature-Aware Autoencoders and Semi-Supervised Threshold Calibration**

---

#  Project Status

**Current version:** V8

**Status:** Experimental / Research Development

The project is currently focused on evaluating the contribution of preprocessing, representation compression, feature-aware reconstruction, and threshold calibration.

Final performance claims will be reported only after the controlled experiments and ablation studies are completed.

---

## License

What is a license?😂
