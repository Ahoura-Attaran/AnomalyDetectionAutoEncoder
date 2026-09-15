# 04 — Threshold Strategy

## V1–V5

Normal-only threshold:

```text
99th percentile of normal validation reconstruction errors
```

## V6–V9

F1-based calibration uses:
- normal validation errors
- sampled attack errors
- up to 2,000 samples per attack family
- candidate percentile thresholds approximately 50–99.9

The selected threshold maximizes F1.

## V9

Separate scores are calibrated for:
- Shallow
- Deep
- Ensemble

Shallow and Deep are normalized by their calibrated thresholds before fusion.

```text
Ensemble =
0.5*(ShallowScore/ShallowThreshold)
+
0.5*(DeepScore/DeepThreshold)
```

The ensemble receives an independent threshold.

## Important validity issue

Calibration attack samples may also appear in final evaluation. This creates calibration/evaluation overlap.

For the final study, split attack data into:
1. calibration set
2. untouched test set

## ROC-AUC

ROC-AUC does not depend on a selected threshold and is therefore useful for comparing score ranking.
