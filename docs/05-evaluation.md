# 05 — Evaluation

## 1. Global Evaluation

The system combines:

- untouched normal test data;
- all attack datasets.

It calculates:

- classification report;
- confusion matrix;
- ROC-AUC.

The anomaly score is the reconstruction error.

## 2. Per-Attack Evaluation

V4 introduced evaluation separately for:

- Bruteforce
- DoS
- WebAttacks
- Botnet
- DDoS
- Portscan

For every attack family the code reports:

- Recall
- Precision
- F1
- ROC-AUC
- number of samples

The attack family is evaluated against the same normal test set.

## 3. Feature Separation Diagnostic

V5 introduced Cohen's-d-style feature separation analysis.

For each attack:

```text
d_j =
abs((mean_attack_j - mean_normal_j) / std_normal_j)
```

The largest values identify features with stronger attack/normal separation.

This is a diagnostic and not an Autoencoder performance metric.

## 4. V8 Weighted-Loss Evaluation

V8 converts the feature-separation analysis into feature weights.

The maximum Cohen's d for each feature across attack families is normalized and mapped to:

```text
[min_weight, max_weight] = [1, 5]
```

These weights affect:

1. model training loss;
2. reconstruction error;
3. threshold calibration;
4. final classification metrics.

## 5. Recommended Final Reporting

For every final experiment, report:

| Level | Metrics |
|---|---|
| Global | Precision, Recall, F1, ROC-AUC, confusion matrix |
| Attack family | Recall, Precision, F1, ROC-AUC, sample count |
| Threshold | threshold value and calibration F1 |
| Training | best epoch / validation loss |
| Feature analysis | selected skewed features and feature-weight distribution |

No numerical result should be added to the documentation unless it comes from an actual run.
