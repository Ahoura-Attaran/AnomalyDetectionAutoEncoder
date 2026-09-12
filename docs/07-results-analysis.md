# Results Analysis

## 1. Purpose

This document interprets measured results. It is separate from `06-experiment-history.md`, which records implementation changes.

## 2. Global Results

| Version | Model | Precision | Recall | F1 | ROC-AUC | Threshold |
|---|---|---:|---:|---:|---:|---|
| V1 | Shallow | — | — | — | — | P99 |
| V1 | Deep | — | — | — | — | P99 |
| V2 | Shallow | — | — | — | — | P99 |
| V2 | Deep | — | — | — | — | P99 |
| V3 | Shallow | — | — | — | — | P99 |
| V3 | Deep | — | — | — | — | P99 |
| V4 | Shallow | — | — | — | — | P99 |
| V4 | Deep | — | — | — | — | P99 |
| V5 | Shallow | — | — | — | — | P99 |
| V5 | Deep | — | — | — | — | P99 |
| V6 | Shallow | — | — | — | — | F1-calibrated |
| V6 | Deep | — | — | — | — | F1-calibrated |

## 3. Per-Attack Results

Record separately for:

- BruteForce
- DoS
- WebAttacks
- Botnet
- DDoS
- PortScan

Metrics:

- Recall
- Precision
- F1
- ROC-AUC

## 4. V5 Feature-Separation Results

V5 results should record the strongest standardized mean differences per attack type.

| Attack | Feature | Effect Size | Rank |
|---|---|---:|---:|
| BruteForce | — | — | — |
| DoS | — | — | — |
| WebAttacks | — | — | — |
| Botnet | — | — | — |
| DDoS | — | — | — |
| PortScan | — | — | — |

## 5. V6 Threshold Comparison

| Model | Normal P99 | F1 Threshold | Calibration F1 | Final Test F1 |
|---|---:|---:|---:|---:|
| Shallow | — | — | — | — |
| Deep | — | — | — | — |

## 6. Interpretation Questions

For each version:

1. Did global detection improve?
2. Did false positives decrease?
3. Did false negatives decrease?
4. Did AUC change?
5. Which attacks improved?
6. Which attacks worsened?
7. Did V5 show weak feature-level separation?
8. Did the tighter V6 bottleneck improve anomaly separation?
9. Did threshold calibration improve F1?
10. Did it increase false positives?
11. Can V6 improvement be attributed to threshold, bottleneck, or both?

## 7. Scientific Rule

No numerical result should be inferred from source code.
