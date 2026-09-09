# Paper Outline

## Proposed Title

**Network Anomaly Detection in CICIDS2017 Using Autoencoders with Robust Feature Preprocessing**

The title can be revised after the final model and results are established.

## Abstract

### To be completed after V9

The abstract should contain:

1. Problem
2. Dataset
3. Proposed method
4. Main preprocessing contribution
5. Main experimental finding
6. Best quantitative results
7. Conclusion

No final numerical claim should be inserted until the experiments are complete.

## 1. Introduction

### 1.1 Background
Network intrusion and anomaly detection.

### 1.2 Problem
Detection of anomalous network-flow behavior without requiring a multi-class supervised classifier.

### 1.3 Motivation
Learning normal traffic patterns through Autoencoders and identifying deviations through reconstruction error.

### 1.4 Contributions

Potential contributions, to be confirmed after the final experiments:

- A reproducible Autoencoder anomaly-detection pipeline.
- Train-only preprocessing parameter estimation.
- Robust handling of heavy-tailed flow features.
- Per-attack-family diagnostic evaluation.
- Systematic experimental evolution from baseline to final model.

## 2. Related Work

To be completed with external literature research.

Suggested areas:

- Network intrusion detection
- CICIDS2017
- Autoencoder-based anomaly detection
- Reconstruction-error thresholding
- Robust preprocessing of network-flow features
- Unsupervised and semi-supervised intrusion detection

## 3. Dataset

Describe:

- CICIDS2017
- Data collection structure
- Flow representation
- Experimental Parquet subsets
- Normal traffic
- Six selected attack groups
- Feature representation

Exact sample counts and feature counts should be inserted from verified data.

## 4. Methodology

### 4.1 Data Cleaning

Inf/NaN handling and constant-feature removal.

### 4.2 Data Splitting

70/15/15 normal split.

### 4.3 Outlier Clipping

Train-derived 0.1% and 99.9% bounds.

### 4.4 Signed Log Transformation

\[
x'=sign(x)\log(1+|x|)
\]

### 4.5 Robust Scaling

RobustScaler fitted only on training data.

### 4.6 Autoencoder Architecture

Shallow and deep architectures.

### 4.7 Reconstruction Error

\[
E(x)=rac{1}{n}\sum_i(x_i-\hat{x}_i)^2
\]

### 4.8 Threshold

99th percentile of normal validation reconstruction errors.

## 5. Experimental Design

Describe the V1→V9 evolution.

A key principle is controlled experimentation:

- Identify problem.
- Introduce one main change.
- Keep other components stable where possible.
- Measure effect.
- Decide whether to retain the change.

## 6. Results

### 6.1 Global Results

Comparison of versions and models.

### 6.2 Per-Attack Results

Comparison across:

- BruteForce
- DoS
- WebAttacks
- Botnet
- DDoS
- PortScan

### 6.3 Threshold Analysis

Evaluate operating points.

### 6.4 Error Distribution

Compare normal and attack reconstruction-error distributions.

## 7. Discussion

Interpret:

- Why the final preprocessing works.
- Which attack families remain difficult.
- Difference between shallow and deep Autoencoders.
- Practical limitations.

## 8. Conclusion

Summarize the validated contribution and the final experimental result.

## 9. Future Work

Potential directions:

- Alternative threshold calibration
- Isolation Forest comparison
- Random Forest baseline
- Other Autoencoder architectures
- Variational Autoencoder
- Feature selection
- Temporal modeling
- Cross-dataset validation
- Real industrial traffic validation

## Appendix

Include:

- Hyperparameters
- Feature list
- Preprocessing parameters
- Experiment log
- Confusion matrices
- Additional per-attack results
