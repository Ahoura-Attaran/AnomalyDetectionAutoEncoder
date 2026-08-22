import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# --------------------------------------------------------------------------
# برای تکرارپذیری نتایج (Reproducibility) -
# --------------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

# مسیر های مورد نیاز پروژه
# --------------------------------------------------------------------------
DATA_DIR = "data"
os.makedirs("Cols", exist_ok=True)
os.makedirs("models", exist_ok=True)

DATA_FILES = {
    "normal":     "Benign-Monday-no-metadata.parquet",
    "botnet":     "Botnet-Friday-no-metadata.parquet",
    "ddos":       "DDoS-Friday-no-metadata.parquet",
    "dos":        "DoS-Wednesday-no-metadata.parquet",
    "portscan":   "Portscan-Friday-no-metadata.parquet",
    "webattacks": "WebAttacks-Thursday-no-metadata.parquet",
    "bruteforce": "Bruteforce-Tuesday-no-metadata.parquet",
}


# 1) Loading data
# ============================================================================
def load_datasets():
    # read and strip()
    dfs = {}
    for key, filename in DATA_FILES.items():
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_parquet(path)
        df.columns = df.columns.str.strip()   
        dfs[key] = df
    return dfs


# 2) Preprocessing
# ============================================================================
def clean_features(df, label_col="Label", constant_cols=None, feature_columns=None):
    #pre proccessing All Data Frames 
    y = df[label_col] if label_col in df.columns else None
    X = df.drop(columns=[label_col]) if label_col in df.columns else df.copy()

    # Deleting nan's
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.dropna()
    if y is not None:
        y = y.loc[X.index]

    # Deleting Constant columns 
    if constant_cols is not None:
        X = X.drop(columns=[c for c in constant_cols if c in X.columns], errors="ignore")

    # Ensuring all columns dfs have exact same columns
    if feature_columns is not None:
        X = X[feature_columns]

    return X, y


# 3) Autoencoder and Deep Autoencoder artitecture
# ============================================================================
def build_shallow_autoencoder(input_dim):

    input_layer = Input(shape=(input_dim,))

    x = Dense(64, activation="relu")(input_layer)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    x = Dense(32, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    encoded = Dense(16, activation="relu", name="bottleneck")(x)

    x = Dense(32, activation="relu")(encoded)
    x = Dense(64, activation="relu")(x)

    output_layer = Dense(input_dim, activation="linear")(x)

    model = Model(input_layer, output_layer, name="shallow_autoencoder")
    model.compile(optimizer="adam", loss="mse")
    return model


def build_deep_autoencoder(input_dim):

    input_layer = Input(shape=(input_dim,))

    # ---- Encoder ----
    x = Dense(128, activation="relu")(input_layer)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    x = Dense(64, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    x = Dense(32, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    encoded = Dense(8, activation="relu", name="bottleneck")(x)

    # ---- Decoder ----
    x = Dense(32, activation="relu")(encoded)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    x = Dense(64, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    x = Dense(128, activation="relu")(x)

    output_layer = Dense(input_dim, activation="linear")(x)

    model = Model(input_layer, output_layer, name="deep_autoencoder")
    model.compile(optimizer="adam", loss="mse")
    return model


def get_callbacks(checkpoint_path):
    
    early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1)
    checkpoint = ModelCheckpoint(checkpoint_path, monitor="val_loss", save_best_only=True, verbose=1)
    return [early_stop, reduce_lr, checkpoint]


# 4) Treshold and reconstruction error
# ============================================================================
def reconstruction_error(model, X):
    # Mean square error 
    pred = model.predict(X, verbose=0)
    return np.mean(np.square(X - pred), axis=1)


def plot_history(history, title):
    plt.figure(figsize=(8, 4))
    plt.plot(history.history["loss"], label="Train")
    plt.plot(history.history["val_loss"], label="Validation")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()


def plot_error_histogram(errors, threshold, title):
    plt.figure(figsize=(8, 4))
    plt.hist(errors, bins=100)
    plt.axvline(threshold, color="red", linestyle="--", label=f"Threshold = {threshold:.4f}")
    plt.xlabel("Reconstruction Error")
    plt.ylabel("Count")
    plt.title(title)
    plt.legend()
    plt.show()


# 5) Evaluating on real attack data
# ============================================================================
def evaluate_model(model, threshold, scaler, constant_cols, feature_columns,
                    test_normal_X, attack_dfs, model_name):

    X_parts = [test_normal_X]
    y_true_parts = [np.zeros(len(test_normal_X))]  # 0 = normal

    for name, df in attack_dfs.items():
        X_att, _ = clean_features(df, constant_cols=constant_cols, feature_columns=feature_columns)
        if len(X_att) == 0:
            continue
        X_att_scaled = scaler.transform(X_att)
        X_parts.append(X_att_scaled)
        y_true_parts.append(np.ones(len(X_att_scaled)))  # 1 = attack

    X_test_all = np.vstack(X_parts)
    y_true_all = np.concatenate(y_true_parts)

    errors = reconstruction_error(model, X_test_all)
    y_pred_all = (errors > threshold).astype(int)

    print(f"\nEvaluaring results ================ {model_name} ================")
    print(classification_report(y_true_all, y_pred_all, target_names=["Normal", "Attack"]))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true_all, y_pred_all))
    try:
        auc = roc_auc_score(y_true_all, errors)
        print(f"ROC-AUC (بر اساس خطای خام، مستقل از آستانه): {auc:.4f}")
    except ValueError:
        pass

    return y_true_all, y_pred_all, errors


# 6) exeuting pipline 
# ============================================================================
def main():
    # ---- loading data----
    dfs = load_datasets()
    df_normal = dfs.pop("normal")
    attack_dfs = dfs  

    # ---- preprocessing normal df and feature----
    y_all = df_normal["Label"]
    X_all = df_normal.drop(columns=["Label"])

    X_all = X_all.replace([np.inf, -np.inf], np.nan).dropna()
    y_all = y_all.loc[X_all.index]

    constant_cols = X_all.columns[X_all.nunique() <= 1].tolist()
    X_all = X_all.drop(columns=constant_cols)
    feature_columns = X_all.columns.tolist()

    joblib.dump(constant_cols, "Cols/constant_cols.pkl")
    joblib.dump(feature_columns, "Cols/feature_columns.pkl")

    # --------------------------------------------------------------
    # نکته‌ی مهم درباره‌ی نشت داده (Data Leakage):
    # در نوت‌بوک اصلی، همان مجموعه‌ی Validation که برای EarlyStopping
    # استفاده می‌شد، برای تعیین Threshold هم استفاده شده بود. اینجا
    # داده‌ی نرمال را به سه بخش تقسیم می‌کنیم:
    #   train        -> فقط برای آموزش مدل
    #   val           -> فقط برای EarlyStopping / انتخاب بهترین وزن‌ها
    #   test (normal) -> کاملاً دست‌نخورده، فقط برای ارزیابی نهایی
    # --------------------------------------------------------------
    train_data, temp_data = train_test_split(X_all, test_size=0.3, random_state=SEED, shuffle=True)
    val_data, test_normal_data = train_test_split(temp_data, test_size=0.5, random_state=SEED, shuffle=True)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_data)
    X_val = scaler.transform(val_data)
    X_test_normal = scaler.transform(test_normal_data)
    joblib.dump(scaler, "models/scaler.pkl")

    print(f"Train: {X_train.shape} | Val: {X_val.shape} | Test(normal): {X_test_normal.shape}")

    input_dim = X_train.shape[1]

    # ============================================================
    # مدل ۱: اتوانکودر ساده
    # ============================================================
    shallow_model = build_shallow_autoencoder(input_dim)
    shallow_model.summary()

    shallow_history = shallow_model.fit(
        X_train, X_train,
        validation_data=(X_val, X_val),
        epochs=100,
        batch_size=512,
        shuffle=True,
        callbacks=get_callbacks("models/shallow_autoencoder.keras"),
        verbose=1,
    )
    plot_history(shallow_history, "Shallow Autoencoder - Loss")

    shallow_val_errors = reconstruction_error(shallow_model, X_val)
    shallow_threshold = np.percentile(shallow_val_errors, 99)
    plot_error_histogram(shallow_val_errors, shallow_threshold, "Shallow AE - Validation Reconstruction Error")
    joblib.dump(shallow_threshold, "models/shallow_threshold.pkl")

    evaluate_model(
        shallow_model, shallow_threshold, scaler, constant_cols, feature_columns,
        X_test_normal, attack_dfs, "Shallow Autoencoder"
    )

    # ============================================================
    # مدل ۲: اتوانکودر عمیق
    # ============================================================
    deep_model = build_deep_autoencoder(input_dim)
    deep_model.summary()

    deep_history = deep_model.fit(
        X_train, X_train,
        validation_data=(X_val, X_val),
        epochs=100,
        batch_size=512,
        shuffle=True,
        callbacks=get_callbacks("models/deep_autoencoder.keras"),
        verbose=1,
    )
    plot_history(deep_history, "Deep Autoencoder - Loss")

    deep_val_errors = reconstruction_error(deep_model, X_val)
    deep_threshold = np.percentile(deep_val_errors, 99)
    plot_error_histogram(deep_val_errors, deep_threshold, "Deep AE - Validation Reconstruction Error")
    joblib.dump(deep_threshold, "models/deep_threshold.pkl")

    evaluate_model(
        deep_model, deep_threshold, scaler, constant_cols, feature_columns,
        X_test_normal, attack_dfs, "Deep Autoencoder"
    )


if __name__ == "__main__":
    main()
