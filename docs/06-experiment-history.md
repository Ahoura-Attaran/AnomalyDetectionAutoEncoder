# 06 — Experiment History

The project should be interpreted as an iterative sequence:

```text
V1 → observed problem → V2 → observed problem → ... → V8
```

## V1 — Baseline

**Method**
- StandardScaler
- normal-only 70/15/15 split
- Shallow and Deep Autoencoders
- ordinary MSE
- P99 normal validation threshold

**Purpose**
Establish the baseline.

## V2 — Robust Preprocessing

**Change**
- training-only 0.001/0.999 clipping
- RobustScaler

**Reason**
Extreme finite values could distort preprocessing and contribute to unstable losses.

## V3 — Magnitude Compression

**Change**
- signed log1p on all features.

**Reason**
Compress highly skewed and very large values.

## V4 — Attack-Specific Evaluation

**Change**
- per-attack Recall, Precision, F1 and AUC.

**Reason**
Aggregate metrics can hide weaknesses on individual attack families.

## V5 — Feature Separability Diagnostic

**Change**
- Cohen's-d-style analysis between normal and each attack family.

**Reason**
Determine whether poor detection is caused by the model or by weak feature-level separability.

## V6 — Stronger Compression + Threshold Calibration

**Changes**
- Shallow bottleneck: 16 → 8
- Deep bottleneck: 8 → 4
- F1-optimized threshold using labeled attack samples.

**Reason**
Test stronger representation compression and reduce the limitations of a normal-only P99 threshold.

**Important**
Two variables changed simultaneously, so causal attribution requires an ablation study.

## V7 — Deep Bottleneck Revision

**Change**
- Deep bottleneck: 4 → 12
- Shallow remains 8.

**Reason**
The V6 Deep bottleneck was considered potentially over-compressed. V7 tests whether a larger latent representation improves preservation of normal traffic patterns and anomaly separability.

**Unchanged**
- clipping
- RobustScaler
- signed log transform
- Cohen's d diagnostic
- F1 threshold calibration
- per-attack evaluation

## V8 — Feature-Aware Autoencoder

V8 contains two major methodological changes.

### A. Selective Log Transform

Instead of transforming every feature, V8 calculates training-set skewness and applies signed log1p only when:

```text
|skewness| > 1.0
```

### B. Feature-Weighted MSE

Cohen's d values from V8's feature-separation analysis are converted into weights from 1 to 5.

The weighted loss is:

```text
L = mean_j [w_j (x_j - x̂_j)^2]
```

The same weights are used in reconstruction error.

### V8 Hypothesis

Features that are more informative for separating attacks from normal traffic should receive greater influence in the reconstruction objective and anomaly score.

## Version Comparison

| Version | Preprocessing | Model change | Threshold | Evaluation |
|---|---|---|---|---|
| V1 | StandardScaler | Baseline | P99 | Global |
| V2 | Clip + RobustScaler | None | P99 | Global |
| V3 | + log1p | None | P99 | Global |
| V4 | Same as V3 | None | P99 | Per-attack |
| V5 | Same as V3 | None | P99 | Cohen's d |
| V6 | Same | Bottleneck 8/4 | F1 calibration | Per-attack |
| V7 | Same | Deep 12 | F1 calibration | Per-attack |
| V8 | Selective log + weighted features | Same as V7 | F1 calibration | Weighted reconstruction + per-attack |

## Next Scientific Step

V8 should be followed by controlled ablations to determine whether improvement comes from:

1. selective log transformation;
2. feature weighting;
3. their interaction.
