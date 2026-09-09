# Threshold Selection

## 1. Purpose

The Autoencoder produces a continuous reconstruction error rather than a binary prediction.

A threshold is therefore required to convert reconstruction error into a normal/attack decision.

## 2. Reconstruction Error

For each sample:

\[
E(x)=rac{1}{n}\sum_{i=1}^{n}(x_i-\hat{x}_i)^2
\]

The implementation calculates the mean squared reconstruction error across all input features.

## 3. Validation-Based Threshold

The current V1–V4 implementation calculates the threshold from normal validation reconstruction errors.

For each model:

```python
threshold = np.percentile(val_errors, 99)
```

Therefore:

\[
T = P_{99}(E_{validation})
\]

A sample is classified as anomalous when:

\[
E(x)>T
\]

## 4. Why Validation Data Is Used

The normal dataset is separated into training, validation, and test subsets.

The validation set is used for:

- EarlyStopping / model selection
- Threshold calibration

The normal test set is not used to calculate the threshold.

This is an improvement over an earlier approach where validation data was reused without a separate untouched normal test set.

## 5. Interpretation of the 99th Percentile

The 99th percentile means that, under the validation distribution, approximately the highest 1% of normal reconstruction errors lie above the threshold.

This does not guarantee a 1% false-positive rate on a different test distribution. It is a calibration rule based on the validation distribution.

## 6. Separate Thresholds

The shallow and deep models receive separate thresholds:

```text
shallow_threshold.pkl
deep_threshold.pkl
```

This is necessary because the two architectures can produce different reconstruction-error distributions.

## 7. Threshold and ROC-AUC

Threshold-based metrics depend on the selected threshold.

ROC-AUC is different: it uses the continuous reconstruction error as an anomaly score and evaluates ranking performance independently of a single threshold.

Therefore both threshold-dependent metrics and ROC-AUC are reported.

## 8. Future Experimental Extensions

Later versions may compare the 99th percentile with alternative calibration methods. Such methods should be added only when supported by the corresponding experimental version and results.
