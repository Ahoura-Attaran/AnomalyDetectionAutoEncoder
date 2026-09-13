# 04 — Threshold Selection

## 1. Reconstruction Error

For each sample:

```text
error = mean((X - X_reconstructed)^2)
```

In V8, if feature weights are available:

```text
error = mean(weight_j × (X_j - X̂_j)^2)
```

## 2. V1–V5

The threshold is based on the 99th percentile of normal validation reconstruction errors:

```text
Threshold = P99(normal validation errors)
```

This is a normal-only threshold.

## 3. V6–V8 — F1 Calibration

From V6 onward, the implementation also searches for a threshold using:

- all normal validation errors;
- a small labeled sample from each attack family;
- up to 2,000 samples per attack family;
- candidate thresholds between the 50th and 99.9th percentiles;
- maximum F1 as the selection criterion.

The Autoencoder weights are not updated using these attack samples in V6/V7. They are used for threshold selection.

## 4. V8 Specific Point

In V8, attack samples also indirectly affect the feature-weight calculation used by the training loss.

Thus V8 should not be described as purely unsupervised.

A precise description is:

> The system reconstructs normal traffic using an Autoencoder, while attack-labeled data contributes to feature-weight construction and threshold calibration.

## 5. Evaluation Leakage Caveat

The current implementation uses the sampled calibration attack records again in final attack evaluation.

Although the calibration sample is small relative to the complete attack datasets, this is still an overlap between calibration and evaluation data.

For publication-quality evaluation, the attack data should be divided into:

```text
Attack calibration set
        ↓
threshold selection

Attack evaluation set
        ↓
final metrics
```

with no overlap.

## 6. Threshold Independence of ROC-AUC

ROC-AUC is calculated from reconstruction scores and is independent of the selected threshold.

Therefore:

- threshold-dependent metrics: Precision, Recall, F1, confusion matrix;
- threshold-independent metric: ROC-AUC.
