# Preprocessing

## 1. Final Pipeline Through V6

```text
Cleaning
   ↓
Constant-feature removal
   ↓
Normal Train / Validation / Test split
   ↓
Train-based clipping
   ↓
Signed log1p
   ↓
RobustScaler
```

## 2. Cleaning

Infinite values are converted to NaN and missing rows are removed.

Constant features are removed from the normal data and the resulting feature list is reused across datasets.

Artifacts:

```text
Cols/constant_cols.pkl
Cols/feature_columns.pkl
```

## 3. Split

Normal data uses a 70/15/15 train/validation/test split.

The normal test set is reserved for final evaluation.

## 4. V1 — StandardScaler

V1 used `StandardScaler` without explicit clipping.

This was the baseline.

## 5. V2 — Clipping + RobustScaler

V2 introduced train-derived percentile clipping:

```text
lower = 0.001
upper = 0.999
```

and replaced `StandardScaler` with `RobustScaler`.

The bounds are calculated only from training data and then reused for validation, normal test, and attack data.

## 6. V3 — Signed Log1p

V3 added:

```python
np.sign(X_df) * np.log1p(np.abs(X_df))
```

after clipping and before RobustScaler.

\[
x' = sign(x)\log(1+|x|)
\]

The purpose is to compress large magnitudes in highly skewed network-flow features.

## 7. V4

V4 kept the V3 preprocessing unchanged.

Its primary contribution was per-attack evaluation.

## 8. V5 — Feature-Separation Diagnostic

V5 kept the V3 preprocessing unchanged but added a model-independent diagnostic.

For each attack family, transformed attack means are compared with transformed normal means:

\[
d_j =
\left|
rac{\mu_{attack,j}-\mu_{normal,j}}
{\sigma_{normal,j}}
ight|
\]

The largest values are reported as the most separated features.

This diagnostic does not modify model training.

## 9. V6

V6 keeps exactly the same preprocessing pipeline as V5.

Its main changes are:

- tighter Autoencoder bottlenecks;
- semi-supervised threshold calibration.

## 10. Leakage Control

Clipping bounds and scaler parameters remain training-derived.

Attack samples used by V6 for threshold calibration do not affect preprocessing or Autoencoder weights.
