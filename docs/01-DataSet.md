# Dataset

## 1. Dataset Source

The project is based on CICIDS2017-derived network-flow data.

The Autoencoder implementation loads processed Parquet subsets rather than the original daily CSV files.

## 2. Experimental Files

| Group | File |
|---|---|
| Normal | `Benign-Monday-no-metadata.parquet` |
| Brute Force | `Bruteforce-Tuesday-no-metadata.parquet` |
| DoS | `DoS-Wednesday-no-metadata.parquet` |
| Web Attacks | `WebAttacks-Thursday-no-metadata.parquet` |
| Botnet | `Botnet-Friday-no-metadata.parquet` |
| DDoS | `DDoS-Friday-no-metadata.parquet` |
| PortScan | `Portscan-Friday-no-metadata.parquet` |

## 3. Loading

Each Parquet file is loaded using `pandas.read_parquet()`. Column names are normalized with:

```python
df.columns = df.columns.str.strip()
```

## 4. Cleaning

The pipeline:

1. separates `Label` when present;
2. replaces `±inf` with NaN;
3. drops NaN rows;
4. removes constant columns;
5. applies the fixed feature list.

## 5. Normal Split

Normal data is split into:

- 70% training
- 15% validation
- 15% normal test

with `random_state=42` and shuffling.

## 6. Attack Groups

The six attack groups remain separate:

- BruteForce
- DoS
- WebAttacks
- Botnet
- DDoS
- PortScan

V6 samples up to 2,000 records from each attack group for threshold calibration. These samples do not train the Autoencoder.

## 7. Dataset Verification

Before publication, exact row counts, feature counts, labels, constant columns, and post-cleaning counts should be extracted from the actual Parquet files.

They are not fabricated here from source code.

## 8. Leakage Considerations

Preprocessing parameters are derived from normal training data:

- constant-feature selection;
- clipping bounds;
- RobustScaler parameters.

V6 additionally uses labeled attack samples for threshold calibration. Therefore the training remains normal-only, but the overall decision procedure is no longer purely unsupervised.

For rigorous final evaluation, calibration samples should be excluded from the final test set.
