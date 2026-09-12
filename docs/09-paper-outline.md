# Paper Outline

## Proposed Title

**Network Anomaly Detection Using Autoencoders with Robust Feature Preprocessing and Semi-Supervised Threshold Calibration**

The title should be finalized after V9.

## Abstract

To be completed after the final experiment.

Include:

1. problem;
2. dataset;
3. methodology;
4. preprocessing contribution;
5. threshold strategy;
6. best quantitative result;
7. conclusion.

## 1. Introduction

- Network intrusion and anomaly detection
- Problem definition
- Motivation for Autoencoder-based anomaly detection
- Research objectives
- Contributions

Potential contributions:

- reproducible Autoencoder pipeline;
- train-only preprocessing parameter estimation;
- robust treatment of heavy-tailed flow features;
- model-independent feature-separation analysis;
- per-attack-family evaluation;
- semi-supervised threshold calibration;
- systematic V1→V9 experimentation.

## 2. Related Work

Research:

- network intrusion detection;
- CICIDS2017;
- Autoencoder anomaly detection;
- reconstruction-error methods;
- robust preprocessing;
- threshold calibration;
- semi-supervised anomaly detection.

## 3. Dataset

Describe:

- CICIDS2017;
- flow representation;
- experimental Parquet subsets;
- normal traffic;
- six selected attack groups;
- feature representation.

Exact counts must be verified from data.

## 4. Methodology

### 4.1 Cleaning

Inf/NaN handling and constant-feature removal.

### 4.2 Data Split

70/15/15 normal split.

### 4.3 Clipping

Train-derived 0.001 and 0.999 quantile bounds.

### 4.4 Signed Log1p

\[
x'=sign(x)\log(1+|x|)
\]

### 4.5 RobustScaler

Fitted only on training data.

### 4.6 Autoencoders

Shallow and deep architectures with V6 bottleneck changes.

### 4.7 Reconstruction Error

\[
E(x)=rac{1}{n}\sum_i(x_i-\hat{x}_i)^2
\]

### 4.8 Thresholding

Compare normal-only P99 and semi-supervised F1 calibration.

### 4.9 Feature Separability

Describe V5's standardized mean-difference diagnostic.

## 5. Experimental Design

Describe V1→V9.

Explicitly identify versions with multiple simultaneous changes.

V6 should be presented as a combined bottleneck and threshold experiment.

## 6. Results

- Global results
- Per-attack results
- Feature-separation results
- Threshold comparison
- Ablation results if implemented

## 7. Discussion

Discuss preprocessing, latent representation, thresholding, attack-family differences, calibration/test separation, and deployment implications.

## 8. Conclusion

Only conclusions supported by verified experiments.

## 9. Future Work

- strict calibration/test separation;
- threshold sensitivity;
- alternative anomaly detectors;
- feature selection;
- temporal modeling;
- cross-dataset validation;
- real-network validation;
- explainability.

## Appendix

- hyperparameters;
- feature list;
- preprocessing parameters;
- experiment log;
- threshold values;
- confusion matrices;
- per-attack tables;
- training curves.
