# 03 — Model Architecture

## Shallow Autoencoder

```text
Input
→ Dense(64, ReLU)
→ BatchNormalization
→ Dropout(0.2)
→ Dense(32, ReLU)
→ BatchNormalization
→ Dropout(0.2)
→ Bottleneck
→ Dense(32)
→ Dense(64)
→ Linear Output
```

Bottleneck:
- V1–V5: 16
- V6–V9: 8

## Deep Autoencoder

```text
Input
→ Dense(128)
→ BatchNormalization
→ Dropout
→ Dense(64)
→ BatchNormalization
→ Dropout
→ Dense(32)
→ BatchNormalization
→ Dropout
→ Bottleneck
→ Dense(32)
→ BatchNormalization
→ Dropout
→ Dense(64)
→ BatchNormalization
→ Dropout
→ Dense(128)
→ Linear Output
```

Bottleneck:
- V1–V5: 8
- V6: 4
- V7–V9: 12

## Training

Uses:
- Adam
- EarlyStopping
- ReduceLROnPlateau
- ModelCheckpoint

ReduceLROnPlateau:
- factor 0.5
- patience 5
- minimum learning rate 1e-6

## V8/V9 weighted objective

```text
L = mean_j [w_j * (x_j - xhat_j)^2]
```

Weights are reused in scoring, calibration and evaluation.

## V9 ensemble

```text
ShallowNorm = ShallowScore / ShallowThreshold
DeepNorm    = DeepScore / DeepThreshold

EnsembleScore =
    0.5 * ShallowNorm +
    0.5 * DeepNorm
```

The ensemble has its own F1-calibrated threshold.
