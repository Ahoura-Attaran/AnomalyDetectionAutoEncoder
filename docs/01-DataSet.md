# 01 — Dataset

## 1. Dataset Source

The project is based on CICIDS2017-derived network flow data.

The external source used during the project is the Hugging Face CICIDS2017 repository:

https://huggingface.co/datasets/bvk/CICIDS-2017

The project code does not directly train on the five raw daily CSV files. Instead, it loads processed Parquet files grouped by traffic/attack family.

## 2. Experimental Files

```text
Benign-Monday-no-metadata.parquet
Bruteforce-Tuesday-no-metadata.parquet
DoS-Wednesday-no-metadata.parquet
WebAttacks-Thursday-no-metadata.parquet
Botnet-Friday-no-metadata.parquet
DDoS-Friday-no-metadata.parquet
Portscan-Friday-no-metadata.parquet
```

## 3. Role of Each Dataset

| Group | Role |
|---|---|
| Benign | Normal traffic used for model development |
| Bruteforce | Attack evaluation/calibration |
| DoS | Attack evaluation/calibration |
| WebAttacks | Attack evaluation/calibration |
| Botnet | Attack evaluation/calibration |
| DDoS | Attack evaluation/calibration |
| Portscan | Attack evaluation/calibration |

## 4. Normal Data Split

The normal dataset is split into:

- 70% training
- 15% validation
- 15% untouched normal test

using `train_test_split`, `random_state=42`, and shuffling.

The validation set is used for model training control such as EarlyStopping. The normal test set is reserved for final evaluation.

## 5. Feature Preparation

The code:

- removes the `Label` column from model inputs;
- replaces positive/negative infinity with NaN;
- removes rows containing NaN;
- identifies constant columns using `nunique() <= 1`;
- stores the resulting feature list for consistent processing.

## 6. Reproducibility and Verification

Exact row counts, feature counts, and label distributions should be generated from the actual Parquet files and recorded as experiment outputs. They should not be inferred from the external dataset description.
