# Evaluation

## 1. Evaluation Objective

The evaluation determines how effectively the Autoencoder separates normal network traffic from anomalous attack traffic.

The primary task is binary anomaly detection:

```text
Normal = 0
Attack = 1
```

## 2. Global Evaluation

The untouched normal test set is combined with all available attack datasets.

For every attack dataset:

1. Clean the features.
2. Apply the fixed feature list.
3. Apply train-derived clipping bounds.
4. Apply signed log1p transformation.
5. Apply the scaler fitted on training data.
6. Calculate reconstruction error.

The combined data is then classified using the selected threshold.

## 3. Reported Metrics

The global evaluation reports:

- Classification report
- Confusion matrix
- ROC-AUC

The classification report provides precision, recall, and F1-score for Normal and Attack.

## 4. Confusion Matrix

The confusion matrix is interpreted as:

| | Predicted Normal | Predicted Attack |
|---|---:|---:|
| Actual Normal | TN | FP |
| Actual Attack | FN | TP |

This allows false positives and false negatives to be inspected separately.

## 5. ROC-AUC

ROC-AUC is calculated from the raw reconstruction error.

A larger reconstruction error represents a stronger anomaly score.

This means ROC-AUC evaluates the ranking quality of the anomaly score without fixing the operating point to one threshold.

## 6. V4 — Per-Attack-Type Evaluation

V4 adds a second evaluation layer.

Instead of combining all attack groups into one class, each attack type is evaluated separately against the same normal test set.

For attack type \(i\):

\[
Normal \quad vs \quad Attack_i
\]

The following metrics are calculated:

- Attack Recall
- Precision
- F1-score
- ROC-AUC
- Number of attack samples

## 7. Attack Recall

For a specific attack type:

\[
Recall_i =
rac{TP_i}{TP_i+FN_i}
\]

This measures the proportion of samples from that attack family detected as anomalous.

## 8. Why Per-Attack Analysis Matters

An aggregate Attack metric can hide differences between attack families.

For example, strong detection of one attack family may dominate the aggregate result while another attack family remains poorly detected.

Per-attack evaluation therefore provides diagnostic information about the weaknesses and strengths of the learned normal representation.

## 9. Current Evaluation Structure

```text
                 ┌── Global Normal vs All Attacks
Model → Score ───┤
                 └── Normal vs Each Attack Type
```

## 10. Current Limitation

The available source code does not provide the numerical outputs of these experiments. Therefore this document defines the evaluation methodology but does not claim specific accuracy, precision, recall, F1, or AUC values.

Those values should be populated from actual experiment logs/results.

## 11. Future Evaluation Extensions

Potential later additions include:

- Threshold sensitivity analysis
- False-positive rate analysis
- Attack-wise confusion analysis
- Error-distribution comparison
- Statistical comparison between model versions
- Precision-recall curves
- Detection-performance comparison across versions

These should be documented only when implemented and experimentally verified.
