# Autoencoder Model

## 1. Objective

The Autoencoder learns a compact representation of normal network-flow data and reconstructs the input.

\[
E(x)=rac{1}{n}\sum_{i=1}^{n}(x_i-\hat{x}_i)^2
\]

The reconstruction error is the anomaly score.

## 2. Shallow Autoencoder

### V1–V5

```text
Input
 ↓ Dense(64, ReLU)
 ↓ BatchNorm
 ↓ Dropout(0.2)
 ↓ Dense(32, ReLU)
 ↓ BatchNorm
 ↓ Dropout(0.2)
 ↓ Dense(16, ReLU)  [bottleneck]
 ↓ Dense(32, ReLU)
 ↓ Dense(64, ReLU)
 ↓ Linear Output
```

### V6

Only the bottleneck is changed:

```text
Dense(8, ReLU) [bottleneck]
```

Thus V6 doubles the compression relative to V1–V5.

## 3. Deep Autoencoder

### V1–V5

```text
Input
 ↓ 128 → BN → Dropout
 ↓ 64 → BN → Dropout
 ↓ 32 → BN → Dropout
 ↓ Dense(8) [bottleneck]
 ↓ 32 → BN → Dropout
 ↓ 64 → BN → Dropout
 ↓ 128
 ↓ Linear Output
```

### V6

The bottleneck is reduced:

```text
Dense(4, ReLU) [bottleneck]
```

## 4. Bottleneck Evolution

| Model | V1–V5 | V6 |
|---|---:|---:|
| Shallow | 16 | 8 |
| Deep | 8 | 4 |

The hypothesis is that stronger compression may force the model to learn a more compact representation of normal traffic. It may also hurt reconstruction if compression becomes excessive; this must be determined experimentally.

## 5. Training

Both models use:

- Adam
- MSE loss
- maximum 100 epochs
- batch size 512
- shuffled training

## 6. Callbacks

- EarlyStopping: `val_loss`, patience 10, restore best weights
- ReduceLROnPlateau: factor 0.5, patience 5, minimum LR `1e-6`
- ModelCheckpoint: best validation-loss model

## 7. Reproducibility

```python
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
```
