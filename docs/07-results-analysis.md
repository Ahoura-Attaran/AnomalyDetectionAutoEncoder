# 07 — Results Analysis

## Rule

No numerical result is inserted unless it was produced by an actual experiment.

## Comparison template

| Version | Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| V1 | Shallow | TBD | TBD | TBD | TBD | TBD |
| V1 | Deep | TBD | TBD | TBD | TBD | TBD |
| V6 | Shallow | TBD | TBD | TBD | TBD | TBD |
| V6 | Deep | TBD | TBD | TBD | TBD | TBD |
| V8 | Shallow | TBD | TBD | TBD | TBD | TBD |
| V8 | Deep | TBD | TBD | TBD | TBD | TBD |
| V9 | Ensemble | TBD | TBD | TBD | TBD | TBD |

## Interpretation

### ROC-AUC increases
Attack scores are ranked above normal scores more effectively.

### ROC-AUC increases but F1 does not
Ranking improved, but the decision threshold did not necessarily improve.

### Recall increases while Precision decreases
The detector catches more attacks at the cost of more false alarms.

### PR-AUC increases
Ranking improves under class imbalance.

### One attack family remains weak
Inspect V5 separability results and feature weights.

## Required final studies

1. V6 2×2 ablation.
2. V8 2×2 ablation.
3. V9 Shallow vs Deep vs Ensemble.
4. Separate calibration/test attack samples.
5. Multiple seeds.
6. Chronological holdout.
