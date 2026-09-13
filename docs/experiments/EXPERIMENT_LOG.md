# Experiment Log

| ID | Version | Change | Reason | Result | Decision |
|---|---|---|---|---|---|
| EXP-001 | V1 | Baseline AE + StandardScaler + P99 | Establish baseline | Record from execution | Baseline |
| EXP-002 | V2 | Clipping + RobustScaler | Improve preprocessing robustness | Record from execution | Compare |
| EXP-003 | V3 | Signed log1p | Compress large/skewed values | Record from execution | Compare |
| EXP-004 | V4 | Per-attack evaluation | Reveal family-specific weaknesses | Record from execution | Diagnostic |
| EXP-005 | V5 | Cohen's d feature separation | Determine feature-level separability | Record from execution | Diagnostic |
| EXP-006 | V6 | Bottleneck compression + F1 threshold | Test representation compression and threshold calibration | Record from execution | Requires ablation |
| EXP-007 | V7 | Deep bottleneck 4 → 12 | Test whether V6 Deep model was over-compressed | Record from execution | Compare |
| EXP-008 | V8 | Selective log + feature-weighted MSE | Preserve less-skewed features and emphasize discriminative features | Record from execution | Requires ablation |

## V8 Reproducibility Fields

When V8 is executed, record:

- random seed;
- number of input features;
- number of skewed features;
- skewness threshold;
- feature-weight range;
- top weighted features;
- Shallow best epoch;
- Deep best epoch;
- calibration threshold;
- calibration F1;
- final global metrics;
- per-attack metrics.

## Methodological Note

V8 should not be compared with V7 as if only one variable changed. It changes both the log-transform policy and the training objective.

Therefore a controlled ablation is required before claiming that either change independently caused an improvement.
