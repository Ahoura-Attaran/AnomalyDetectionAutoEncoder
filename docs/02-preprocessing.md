# 02 — Preprocessing Evolution

## 1. Common Preprocessing

Across versions, the project performs:

1. Remove `Label` from model features.
2. Replace `inf/-inf` with NaN.
3. Drop rows containing NaN.
4. Remove constant columns based on normal training data.
5. Enforce the same feature-column order for all datasets.

The selected feature list is stored in:

```text
Cols/feature_columns.pkl
```

## 2. V1 — StandardScaler

V1 uses:

```text
Normal data
   ↓
NaN/Inf cleaning
   ↓
constant-feature removal
   ↓
70/15/15 split
   ↓
StandardScaler
```

The scaler is fitted only on training data.

## 3. V2 — Outlier Clipping + RobustScaler

V2 introduces per-feature clipping.

Bounds are computed only from the training data:

```text
lower = train.quantile(0.001)
upper = train.quantile(0.999)
```

The same training-derived bounds are then applied to validation, normal test, and attack data.

The scaler changes from `StandardScaler` to `RobustScaler`.

The bounds are saved in:

```text
Cols/clip_bounds.pkl
```

## 4. V3 — Signed Log Transform

V3 adds:

```text
x' = sign(x) * log(1 + |x|)
```

after clipping and before scaling.

The goal is to compress very large magnitudes while retaining the sign.

## 5. V5/V7 — Log Transform on All Features

The earlier implementation applies signed log transformation to every feature after clipping.

This is later reconsidered because some relatively symmetric/count-like features may lose useful information.

## 6. V8 — Selective Log Transform

V8 introduces:

```python
compute_skewed_columns(train_df, skew_threshold=1.0)
```

A feature is selected for transformation when:

```text
|skewness| > 1.0
```

Only those features receive signed log1p transformation.

The selected columns are stored in:

```text
Cols/skewed_cols.pkl
```

This creates the following V8 pipeline:

```text
Raw features
   ↓
NaN / Inf cleaning
   ↓
Constant-feature removal
   ↓
Train / Val / Test split
   ↓
Train-derived clipping
   ↓
Skewness analysis on Train
   ↓
Selective signed log1p
   ↓
RobustScaler
   ↓
Autoencoder
```

## 7. Leakage Control

The intended rule is:

> Parameters learned from data must be derived from training data only.

This applies to:

- constant feature selection;
- clipping bounds;
- skewed-feature selection;
- RobustScaler parameters.

The same transformations are then applied to validation and test/attack data.

## 8. Important V8 Methodological Change

V8 uses attack/normal separation information to derive feature weights. This is not a preprocessing-only change. The resulting weights influence the Autoencoder training loss.

Therefore V8 introduces supervised information into the training objective even though the Autoencoder reconstructs normal data.
