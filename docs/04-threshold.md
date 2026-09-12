# Threshold Selection

## 1. Reconstruction Error

For each sample:

\[
E(x)=rac{1}{n}\sum_{i=1}^{n}(x_i-\hat{x}_i)^2
\]

The decision rule is:

\[
\hat y =
egin{cases}
1 & E(x)>T\
0 & E(x)\le T
\end{cases}
\]

## 2. V1–V5: Normal-Only P99

The threshold was:

\[
T=P_{99}(E_{normal,val})
\]

Only normal validation reconstruction errors were used.

## 3. V6: Semi-Supervised Calibration

V6 introduces `find_best_threshold()`.

The Autoencoder is still trained only on normal traffic.

For threshold selection, the calibration set contains:

```text
Normal validation reconstruction errors
+
Up to 2,000 sampled errors from each attack family
```

The attack samples are randomly selected with the reproducibility seed.

## 4. F1 Optimization

Candidate thresholds are generated from the 50th through 99.9th percentiles of the combined calibration error distribution.

For each candidate:

- TP
- FP
- FN
- Precision
- Recall
- F1

are calculated.

The selected threshold is:

\[
T^*=rg\max_T F1(T)
\]

## 5. Reference Threshold

V6 still calculates the old P99 threshold:

```python
reference_percentile_threshold = np.percentile(val_errors, 99)
```

This enables direct comparison between the old and new operating points.

## 6. Correct Terminology

V6 should be described as:

> Unsupervised Autoencoder training with semi-supervised threshold calibration.

The attack labels influence the threshold, not the Autoencoder weights.

## 7. Methodological Limitation

The V6 source code does not remove the sampled calibration attack records from the attack datasets before final evaluation.

Therefore threshold-dependent final metrics may contain calibration/evaluation overlap.

A rigorous later version should use:

```text
Training attacks: none
Calibration attacks: separate subset
Final test attacks: disjoint subset
```
