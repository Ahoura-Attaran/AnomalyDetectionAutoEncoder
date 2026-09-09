# Autoencoder Model

## 1. Objective

The Autoencoder learns to reconstruct normal network-flow feature vectors.

During inference, a high reconstruction error indicates that the sample differs from the learned normal representation and may therefore be anomalous.

## 2. Reconstruction Objective

For an input vector \(x\), the Autoencoder produces:

\[
\hat{x}=f_	heta(x)
\]

The training objective is Mean Squared Error:

\[
L(x,\hat{x}) =
rac{1}{n}\sum_{i=1}^{n}(x_i-\hat{x}_i)^2
\]

## 3. Shallow Autoencoder

The architecture is:

```text
Input
  ↓
Dense(64, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(32, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Bottleneck(16, ReLU)
  ↓
Dense(32, ReLU)
  ↓
Dense(64, ReLU)
  ↓
Linear Output
```

The bottleneck has 16 dimensions.

## 4. Deep Autoencoder

The architecture is:

```text
Input
  ↓
Dense(128, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(64, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(32, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Bottleneck(8, ReLU)
  ↓
Dense(32, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(64, ReLU)
  ↓
BatchNormalization
  ↓
Dropout(0.2)
  ↓
Dense(128, ReLU)
  ↓
Linear Output
```

The bottleneck has 8 dimensions.

## 5. Training Configuration

Both architectures use:

- Optimizer: Adam
- Loss: MSE
- Maximum epochs: 100
- Batch size: 512
- Shuffle: enabled

Validation data is passed separately during training.

## 6. Training Callbacks

Three callbacks are used:

### EarlyStopping

```text
monitor = val_loss
patience = 10
restore_best_weights = True
```

### ReduceLROnPlateau

```text
monitor = val_loss
factor = 0.5
patience = 5
min_lr = 1e-6
```

### ModelCheckpoint

The best validation-loss model is saved.

## 7. Reproducibility

The code sets:

```python
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
```

This is intended to improve reproducibility across runs.

## 8. Model Artifacts

The pipeline saves:

```text
models/
├── shallow_autoencoder.keras
├── deep_autoencoder.keras
├── scaler.pkl
├── shallow_threshold.pkl
└── deep_threshold.pkl
```

The exact artifact set may evolve in later versions.

## 9. Model Evolution

V1–V4 do not introduce a new Autoencoder architecture after the initial baseline.

The major changes in these versions are preprocessing and evaluation.

This controlled structure is useful for determining whether performance changes originate from data transformation rather than architecture changes.
