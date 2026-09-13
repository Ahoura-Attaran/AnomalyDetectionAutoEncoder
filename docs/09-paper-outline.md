# 09 — Paper Outline

## Proposed Title

**CICIDS2017 Network Anomaly Detection Using Feature-Aware Autoencoders and Semi-Supervised Threshold Calibration**

## 1. Abstract

Describe:

- network anomaly detection problem;
- CICIDS2017-derived flow data;
- normal-traffic Autoencoder training;
- preprocessing evolution;
- feature-separation analysis;
- selective log transformation;
- feature-weighted reconstruction;
- threshold calibration;
- attack-family evaluation.

The final abstract must contain actual measured results after the experiments are finalized.

## 2. Introduction

Discuss:

- importance of network anomaly detection;
- limitations of purely signature-based methods;
- motivation for Autoencoders;
- challenges caused by heterogeneous flow features;
- importance of threshold selection.

## 3. Related Work

Potential themes:

- Autoencoder anomaly detection;
- CICIDS2017;
- reconstruction-error thresholding;
- robust preprocessing;
- feature weighting;
- semi-supervised anomaly detection.

## 4. Dataset

Document:

- CICIDS2017 source;
- processed Parquet subsets;
- normal and attack groups;
- feature preparation;
- train/validation/test protocol.

## 5. Methodology

### 5.1 Preprocessing

- NaN/Inf handling
- constant feature removal
- clipping
- RobustScaler
- selective signed log transform

### 5.2 Autoencoders

- Shallow architecture
- Deep architecture
- bottleneck evolution

### 5.3 Feature Separation

Explain Cohen's-d-style analysis.

### 5.4 Feature-Weighted Loss

Define:

```text
L = mean_j [w_j (x_j - x̂_j)^2]
```

and explain how weights are derived.

### 5.5 Threshold Calibration

Explain:

- normal validation reconstruction errors;
- attack calibration samples;
- candidate thresholds;
- F1 optimization.

## 6. Experimental Design

Describe V1–V8 as controlled evolution.

Explicitly identify where multiple variables changed simultaneously.

## 7. Results

Report:

- global metrics;
- per-attack metrics;
- ROC curves;
- reconstruction-error distributions;
- feature weights;
- training curves.

## 8. Ablation Study

At minimum compare:

- all-feature log vs selective log;
- ordinary MSE vs weighted MSE;
- P99 vs F1 threshold.

## 9. Discussion

Discuss:

- representation capacity;
- feature separability;
- threshold sensitivity;
- feature weighting;
- attack-specific weaknesses;
- leakage controls.

## 10. Limitations

At minimum:

1. Current threshold calibration/evaluation overlap.
2. V8 uses attack information for feature-weight construction.
3. V6 changed bottleneck and threshold simultaneously.
4. Exact generalization to unseen attack families requires separate testing.

## 11. Conclusion

Summarize the final evidence rather than claiming improvement without measured results.

## 12. Future Work

Possible directions:

- strict calibration/test separation;
- ablation experiments;
- unseen-attack testing;
- temporal evaluation;
- adaptive thresholding;
- comparison with additional anomaly-detection baselines.
