# Evaluation

## 1. Global Evaluation

The primary task is binary:

```text
Normal = 0
Attack = 1
```

The normal test set is combined with the attack datasets after applying the same train-derived preprocessing pipeline.

Metrics:

- Precision
- Recall
- F1
- Confusion Matrix
- ROC-AUC

## 2. Confusion Matrix

| | Predicted Normal | Predicted Attack |
|---|---:|---:|
| Actual Normal | TN | FP |
| Actual Attack | FN | TP |

## 3. ROC-AUC

ROC-AUC uses continuous reconstruction error rather than thresholded predictions.

Higher reconstruction error represents a stronger anomaly score.

## 4. Per-Attack Evaluation

V4 introduced independent evaluation of each attack family against the same normal test set:

\[
Normal \quad vs \quad Attack_i
\]

Reported metrics:

- Recall
- Precision
- F1
- ROC-AUC
- sample count

## 5. V5 — Feature-Level Diagnostic

V5 adds a separate, model-independent diagnostic before training.

For each attack family it reports the top features with the largest standardized mean difference from normal traffic after the selected transformations.

This is not an Autoencoder performance metric.

It answers:

> Is this attack family distinguishable in the selected feature representation at all?

This helps distinguish a model problem from a feature-information problem.

## 6. V6 — Threshold-Aware Evaluation

V6 keeps the global and per-attack evaluation procedures but supplies the F1-optimized threshold instead of the normal-only P99 threshold.

The old P99 threshold is also calculated as a reference.

## 7. V6 Evaluation Caveat

Attack samples used for threshold calibration remain in the attack datasets used for evaluation.

Therefore V6 threshold-dependent final metrics are not based on a perfectly disjoint calibration/test split.

This limitation must be reported in the final paper unless corrected in a later version.

## 8. Required Final Results

Numerical values should be populated from actual execution logs:

- global Precision/Recall/F1/AUC;
- confusion matrices;
- per-attack metrics;
- threshold values;
- calibration F1;
- validation loss and training epochs.

No numerical result should be inferred from source code.
