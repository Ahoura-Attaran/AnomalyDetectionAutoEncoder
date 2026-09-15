# 05 — Evaluation

## Global metrics

- Precision
- Recall
- F1
- ROC-AUC
- Average Precision / PR-AUC
- Confusion Matrix

## Per-attack metrics

- Bruteforce
- DoS
- WebAttacks
- Botnet
- DDoS
- Portscan

## V9 comparison

Compare:
1. Shallow
2. Deep
3. Ensemble

Mean attack-family ROC-AUC is an important ranking criterion. Recall is reported but should not be the only selection metric.

## Recommended final metrics

Also report:
- False Positive Rate
- Specificity
- Balanced Accuracy
- PR-AUC
- threshold
- training time
- inference time
- parameter count
- calibration size
- mean ± standard deviation across seeds

## Results template

| Model | Attack | Precision | Recall | F1 | ROC-AUC | PR-AUC | N |
|---|---|---:|---:|---:|---:|---:|---:|
| Shallow | Bruteforce | TBD | TBD | TBD | TBD | TBD | TBD |
| Deep | Bruteforce | TBD | TBD | TBD | TBD | TBD | TBD |
| Ensemble | Bruteforce | TBD | TBD | TBD | TBD | TBD | TBD |

Repeat for all attack families. Never insert unverified numerical results.
