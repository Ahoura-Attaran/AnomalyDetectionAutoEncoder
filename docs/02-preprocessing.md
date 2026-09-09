# Preprocessing

## 1. Objective

The preprocessing pipeline was developed incrementally to address numerical instability, inconsistent feature sets, and extreme feature distributions.

The final pipeline currently represented by V3/V4 is:

```text
Raw Data
   ↓
Remove Inf / NaN
   ↓
Remove constant columns
   ↓
Select fixed feature columns
   ↓
Normal Train / Validation / Test split
   ↓
Train-based percentile clipping
   ↓
Signed log1p transformation
   ↓
RobustScaler
   ↓
Autoencoder
```

## 2. Cleaning NaN and Infinite Values

Infinite values are replaced with missing values:

```python
X = X.replace([np.inf, -np.inf], np.nan)
```

Rows containing missing values are then removed:

```python
X = X.dropna()
```

Labels, when present, are aligned with the remaining feature indices.

## 3. Constant Feature Removal

Constant columns are detected using:

```python
X_all.columns[X_all.nunique() <= 1]
```

These columns contain no variation in the normal training source and therefore provide no useful information for reconstruction.

The selected constant columns are saved to:

```text
Cols/constant_cols.pkl
```

## 4. Feature Consistency

A fixed feature list is saved to:

```text
Cols/feature_columns.pkl
```

Other datasets are subsequently restricted to these same columns.

This is important because the Autoencoder input dimension must remain identical between training and evaluation.

## 5. Train / Validation / Test Split

Normal data is divided using two `train_test_split` operations:

- 70% training
- 15% validation
- 15% normal test

The split uses:

```python
random_state=42
shuffle=True
```

The training set is used to fit the preprocessing and train the Autoencoder.

The validation set is used for model-selection callbacks and threshold calibration.

The normal test set remains untouched until final evaluation.

## 6. V1 — StandardScaler

V1 used `StandardScaler`.

This established the baseline preprocessing approach but was vulnerable to the influence of extreme values.

## 7. V2 — Clipping + RobustScaler

V2 introduced percentile clipping.

For each feature, the lower and upper bounds are calculated from training data:

```python
lower_q = 0.001
upper_q = 0.999
```

The resulting bounds are then applied to train, validation, normal test, and attack data.

V2 also replaced `StandardScaler` with `RobustScaler`.

The motivation was to reduce the influence of extreme values.

The clipping bounds are saved to:

```text
Cols/clip_bounds.pkl
```

## 8. V3 — Signed Logarithmic Transformation

V3 introduced:

```python
np.sign(X_df) * np.log1p(np.abs(X_df))
```

This transformation compresses large magnitudes while preserving the sign.

It is applied after clipping and before `RobustScaler`.

The motivation documented in the source code is to reduce the dynamic range of highly skewed, zero-inflated rate-based features such as `Flow Bytes/s` and `Flow Packets/s`.

## 9. Final Preprocessing State in V3/V4

The effective transformation is:

\[
x_{clip} = clip(x, q_{0.001}, q_{0.999})
\]

followed by:

\[
x_{log}=sign(x_{clip})\log(1+|x_{clip}|)
\]

and finally RobustScaler transformation.

The scaler is fitted only on the transformed training set and saved to:

```text
models/scaler.pkl
```

## 10. Leakage Control

The following parameters are training-derived:

- Constant-feature selection
- Clipping bounds
- RobustScaler parameters

They are reused for validation, normal test, and attack data.

This is a central preprocessing rule of the experiment.

## 11. Evolution Summary

| Version | Cleaning | Clipping | Transformation | Scaling |
|---|---|---|---|---|
| V1 | Yes | No | None | StandardScaler |
| V2 | Yes | Train-based | None | RobustScaler |
| V3 | Yes | Train-based | Signed log1p | RobustScaler |
| V4 | Same as V3 | Same | Same | Same |
