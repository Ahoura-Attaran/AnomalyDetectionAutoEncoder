# 02 — Preprocessing Evolution

## V1 — StandardScaler

Fit on training data only and apply to validation/test/attack data.

No clipping or log transformation.

## V2 — Clipping + RobustScaler

Training-derived clipping:
- lower quantile = 0.001
- upper quantile = 0.999

The same bounds are applied to later splits.

`StandardScaler` is replaced by `RobustScaler`.

## V3 — Signed log1p

```text
sign(x) * log1p(abs(x))
```

Applied after clipping to compress extreme magnitudes while preserving sign.

## V4–V7

The broad log transformation remains while the project adds attack-family evaluation, feature separability diagnostics, bottleneck experiments and threshold calibration.

## V8 — Selective log

Training-set skewness determines which features receive signed log1p:

```text
abs(skewness) > 1.0
```

Selected columns are saved as `Cols/skewed_cols.pkl`.

## V8 — Feature weighting

For feature j:

```text
d_j = abs((mu_attack,j - mu_normal,j) / sigma_normal,j)
```

The maximum effect size across attack families is used, then weights are mapped approximately to `[1, 5]`.

Saved as `Cols/feature_weights.pkl`.

## V8/V9 — Weighted reconstruction

```text
WeightedMSE = mean(w_j * (x_j - xhat_j)^2)
```

The same weights are used for anomaly scoring.

## Caveat

Attack/normal information contributes to feature weights. Therefore V8/V9 are label-informed/semi-supervised components rather than purely unsupervised anomaly detection.
