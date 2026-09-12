# Experiment Log

| ID | Version | Main Change | Reason | Result | Decision |
|---|---|---|---|---|---|
| EXP-001 | V1 | StandardScaler baseline | Establish baseline | Pending execution record | Baseline |
| EXP-002 | V2 | Clipping + RobustScaler | Reduce extreme-value influence | Pending execution record | Retained |
| EXP-003 | V3 | Signed log1p | Compress heavy-tailed features | Pending execution record | Retained |
| EXP-004 | V4 | Per-attack evaluation | Reveal attack-family differences | Diagnostic output pending | Retained |
| EXP-005 | V5 | Feature-separation diagnostic | Check feature-level separability | Diagnostic output pending | Retained |
| EXP-006 | V6 | F1 threshold + tighter bottlenecks | Test decision calibration and stronger compression | Pending execution record | To evaluate |

## V6 Control Note

V6 changes:

1. Shallow bottleneck: 16 → 8
2. Deep bottleneck: 8 → 4
3. Threshold: normal P99 → F1-optimized calibration

Therefore V6 is not a one-variable ablation.

## Logging Rule

For future versions record:

- version;
- code revision;
- dataset;
- change;
- motivation;
- hyperparameters;
- threshold;
- global metrics;
- per-attack metrics;
- diagnostic outputs;
- observed problem;
- decision.

Never overwrite historical entries.
