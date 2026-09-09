# Discussion

## 1. Research Perspective

The project follows an iterative engineering-to-research workflow.

Each version is treated as an experiment in which a specific limitation is addressed while unnecessary changes to other components are avoided.

## 2. Preprocessing as a Critical Component

The first four versions show that anomaly detection performance is not determined only by the neural-network architecture.

V1 established a baseline using StandardScaler.

V2 addressed the influence of extreme values using train-based clipping and RobustScaler.

V3 further addressed heavy-tailed distributions through signed log1p transformation.

This sequence motivates a central discussion point:

> Stable numerical representation of network-flow features is a prerequisite for reliable Autoencoder reconstruction.

## 3. Model Architecture vs Data Representation

The Autoencoder architecture remains unchanged through V4.

This is useful experimentally because improvements observed between V1, V2, and V3 can be investigated primarily as preprocessing effects rather than architecture effects.

However, numerical performance must still be measured before claiming that one preprocessing strategy is superior.

## 4. Evaluation Granularity

V4 adds per-attack-type analysis.

This changes the interpretation of model performance from:

```text
Can the model detect attacks?
```

to:

```text
Which attack families can the learned normal representation distinguish?
```

This is particularly relevant for anomaly detection because attack families can have substantially different statistical characteristics.

## 5. Threshold Sensitivity

The current threshold is the 99th percentile of normal validation reconstruction error.

This provides a reproducible calibration rule, but the threshold represents a particular operating point.

Later experiments should investigate whether different thresholds change:

- False-positive rate
- Attack recall
- Precision
- F1
- Operational usefulness

## 6. Reproducibility and Leakage

The project explicitly saves preprocessing artifacts and derives data-dependent preprocessing parameters from training data.

This is important because using test or attack data to determine scaling or clipping parameters would make the evaluation optimistic.

## 7. Limitations to Address Later

Potential limitations requiring later investigation include:

- Numerical distribution differences between attack families
- Threshold selection strategy
- Class imbalance in evaluation
- Dependence of results on the chosen feature set
- Stability across random seeds
- Generalization to unseen traffic
- Comparison with non-neural anomaly detectors
- Computational cost
- Interpretability of reconstruction errors

These are discussion topics, not established experimental findings.

## 8. Current Scientific Position

V1–V4 establish a progressively refined anomaly-detection pipeline.

The current evidence from source code supports the claim that the implementation evolved from a basic scaled Autoencoder toward a pipeline with more robust preprocessing and more detailed evaluation.

Performance superiority between versions must be established from experimental results.
