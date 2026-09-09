# Experiment Log

| ID | Version | Main Change | Reason | Result | Decision |
|---|---|---|---|---|---|
| EXP-001 | V1 | StandardScaler baseline | Establish baseline pipeline | Numerical result pending | Baseline retained for comparison |
| EXP-002 | V2 | Percentile clipping + RobustScaler | Reduce effect of extreme values | Numerical result pending | Retained |
| EXP-003 | V3 | Signed log1p transformation | Compress heavy-tailed feature magnitudes | Numerical result pending | Retained |
| EXP-004 | V4 | Per-attack-type evaluation | Detect attack-family-specific weaknesses | Diagnostic output pending | Retained |

## Logging Rule

For every new experiment record:

- Version
- Date
- Code revision
- Dataset version
- Main change
- Motivation
- Hyperparameters
- Training configuration
- Threshold
- Global metrics
- Per-attack metrics
- Observed problem
- Decision

Do not replace old experiment entries. Add a new row so the evolution remains traceable.
