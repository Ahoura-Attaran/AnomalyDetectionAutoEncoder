# 09 — Paper Outline

## Proposed title

**CICIDS-2017 Network Anomaly Detection Using Feature-Aware Autoencoders and Semi-Supervised Threshold Calibration**

## 1. Abstract
Problem, dataset, baseline, evolution, V9 method, verified results, contribution and limitations.

## 2. Introduction
- network anomaly detection
- high-dimensional flow data
- autoencoder reconstruction
- threshold limitations
- feature-aware reconstruction
- model ensembling

## 3. Related Work
- autoencoder anomaly detection
- deep autoencoders
- feature weighting
- semi-supervised threshold calibration
- ensemble anomaly detection
- CICIDS-2017 studies

## 4. Dataset
Describe dataset source, processed Parquet files, traffic families, cleaning and split.

## 5. Methodology

### 5.1 Baseline Autoencoders
Shallow and Deep architectures.

### 5.2 Robust Preprocessing
Clipping + RobustScaler.

### 5.3 Skew-Aware Transformation
Selective signed log1p.

### 5.4 Feature Separability
Cohen's-d-style effect sizes.

### 5.5 Feature-Weighted Reconstruction
```text
L = mean_j [w_j * (x_j - xhat_j)^2]
```

### 5.6 Semi-Supervised Threshold Calibration
F1 optimization using normal validation and labeled calibration attacks.

### 5.7 Score-Level Ensemble
```text
S_ensemble =
0.5*(S_shallow/T_shallow)
+
0.5*(S_deep/T_deep)
```

## 6. Experimental Design
V1–V9, V6 ablation, V8 ablation, V9 comparison, multiple seeds, calibration/test separation and chronological holdout.

## 7. Results
Global metrics, per-attack metrics, ROC/PR curves, confusion matrices, training curves, feature weights and model comparison.

## 8. Discussion
Preprocessing, bottleneck, threshold, feature weighting, attack-family behavior and ensemble behavior.

## 9. Limitations
Label-informed weighting, semi-supervised calibration, calibration/test separation, random split, dataset dependence and seed dependence.

## 10. Conclusion and Future Work
Chronological deployment evaluation, adaptive thresholding, temporal models, concept drift and online learning.
