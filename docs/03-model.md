# 03 — Model Architecture

## 1. Models

The project compares:

- Shallow Autoencoder
- Deep Autoencoder

Both reconstruct the input vector and use reconstruction error as the anomaly score.

## 2. Shallow Autoencoder

Current V7/V8 architecture:

```text
Input
  ↓
Dense(64, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Dense(32, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Bottleneck(8, ReLU)
  ↓
Dense(32, ReLU)
  ↓
Dense(64, ReLU)
  ↓
Linear Output
```

## 3. Deep Autoencoder

Current V8 architecture:

```text
Input
  ↓
Dense(128, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Dense(64, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Dense(32, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Bottleneck(12, ReLU)
  ↓
Dense(32, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Dense(64, ReLU)
  ↓
BatchNorm
  ↓
Dropout(0.2)
  ↓
Dense(128, ReLU)
  ↓
Linear Output
```

## 4. Bottleneck Evolution

| Version | Shallow | Deep |
|---|---:|---:|
| V1–V5 | 16 | 8 |
| V6 | 8 | 4 |
| V7 | 8 | 12 |
| V8 | 8 | 12 |

V6 attempted stronger compression. V7 reversed the Deep bottleneck from 4 to 12 after the previous experiment suggested that excessive compression could harm representation quality.

## 5. Training

Both models use:

- Adam optimizer
- up to 100 epochs
- batch size 512
- shuffled training data
- validation loss monitoring

Callbacks:

- EarlyStopping: patience 10, restore best weights
- ReduceLROnPlateau: factor 0.5, patience 5, minimum LR `1e-6`
- ModelCheckpoint: save best validation-loss model

## 6. Loss Evolution

V1–V7 primarily use ordinary MSE.

V8 introduces a feature-weighted MSE:

```text
Weighted MSE =
mean( feature_weight_j × (y_j - ŷ_j)^2 )
```

The same feature weights are also used in the reconstruction error so that the training objective and anomaly score remain aligned.

## 7. Scientific Interpretation

The key V8 hypothesis is:

> Features that exhibit stronger normal-vs-attack separation should contribute more strongly to reconstruction-based anomaly scoring.

This hypothesis must be validated experimentally rather than assumed to improve detection.
