# Experiment Log — V1 to V9

This is the operational record. Fill numerical fields only after executing the corresponding version.

## EXP-001 — V1
Objective: baseline autoencoders.
Changes: StandardScaler, P99 threshold, Shallow 16, Deep 8.
Results: TBD

## EXP-002 — V2
Objective: robust preprocessing.
Changes: clipping + RobustScaler.
Results: TBD

## EXP-003 — V3
Objective: reduce skew/extreme-value influence.
Change: signed log1p.
Results: TBD

## EXP-004 — V4
Objective: expose family-specific weaknesses.
Change: per-attack metrics.
Results: TBD

## EXP-005 — V5
Objective: measure feature separability.
Change: Cohen's-d-style diagnostic.
Results: TBD

## EXP-006 — V6
Objective: test bottleneck compression and F1 calibration.
Changes: Shallow 16→8, Deep 8→4, P99→F1.
Required: 2×2 bottleneck × threshold ablation.
Results: TBD

## EXP-007 — V7
Objective: test larger Deep latent space.
Change: Deep 4→12.
Results: TBD

## EXP-008 — V8
Objective: feature-aware preprocessing and reconstruction.
Changes: selective log, feature weighting, weighted loss/score.
Required: 2×2 log policy × loss ablation.
Results: TBD

## EXP-009 — V9
Objective: combine Shallow and Deep scores.
Change: score-level ensemble.
Formula:
`0.5*(ShallowScore/ShallowThreshold) + 0.5*(DeepScore/DeepThreshold)`
Results: TBD

## Required result fields

- code version
- dataset version
- feature count
- normal count
- attack counts
- seed
- epochs
- training time
- inference time
- threshold
- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC
- FPR
- confusion matrix
- per-attack metrics

## Required next experiments

1. V6 2×2 ablation.
2. V8 2×2 ablation.
3. Calibration/test separation.
4. Multiple seeds.
5. Chronological holdout.
6. Final Shallow vs Deep vs Ensemble comparison.
