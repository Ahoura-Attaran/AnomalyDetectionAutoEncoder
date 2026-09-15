# 01 — Dataset

## Source

CICIDS-2017 network-flow data.

## Processed Parquet files used by the code

```text
Benign-Monday-no-metadata.parquet
Bruteforce-Tuesday-no-metadata.parquet
DoS-Wednesday-no-metadata.parquet
WebAttacks-Thursday-no-metadata.parquet
Botnet-Friday-no-metadata.parquet
DDoS-Friday-no-metadata.parquet
Portscan-Friday-no-metadata.parquet
```

## Attack families

- Benign
- Bruteforce
- DoS
- WebAttacks
- Botnet
- DDoS
- Portscan

## Cleaning

The loader:
1. reads Parquet files
2. strips whitespace from column names
3. separates `Label`
4. replaces ±inf with NaN
5. drops invalid rows
6. removes constant features
7. enforces a consistent feature-column list

## Normal split

Approximately:
- 70% train
- 15% validation
- 15% normal test

Seed: `42`

The split is randomized and shuffled.

## Attack data

Attack families are evaluated independently.

From V6 onward, up to 2,000 samples per attack family can be used for threshold calibration.

## Exact counts

Exact row counts, feature counts and class distributions must be obtained from actual execution and are therefore not fabricated here.

## Limitation

The current normal split is random. A chronological holdout should be added before deployment/generalization claims.
