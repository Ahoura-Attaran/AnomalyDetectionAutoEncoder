import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, auc as auc_score

import tensorflow as tf #type:ignore
from tensorflow.keras.models import Model #type: ignore
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization #type: ignore
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint #type: ignore

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


# 2b) Outlier clipping (fixes the scaler-distortion / exploding-loss problem)
# ============================================================================
# 
def compute_clip_bounds(train_df, lower_q=0.001, upper_q=0.999):
    lower = train_df.quantile(lower_q)
    upper = train_df.quantile(upper_q)
    return lower, upper


def clip_outliers(X_df, lower, upper):
    return X_df.clip(lower=lower, upper=upper, axis=1)


def log_transform(X_df):

    return np.sign(X_df) * np.log1p(np.abs(X_df))


# 2c) Diagnostic: is each attack type separable from normal at all?
# ============================================================================

def analyze_feature_separation(train_data_raw, attack_dfs, constant_cols, feature_columns,
                                clip_lower, clip_upper, top_n=5):
    normal_log = log_transform(clip_outliers(train_data_raw, clip_lower, clip_upper))
    normal_mean = normal_log.mean()
    normal_std = normal_log.std().replace(0, 1e-9)

    print("\n================feature sepration analysis================")
    for name, df in attack_dfs.items():
        X_att, _ = clean_features(df, constant_cols=constant_cols, feature_columns=feature_columns)
        if len(X_att) == 0:
            continue
        att_log = log_transform(clip_outliers(X_att, clip_lower, clip_upper))
        att_mean = att_log.mean()

        # Cohen's d: تفاوت میانگین بر حسب انحراف معیار داده‌ی نرمال؛
        # هر چه بزرگ‌تر، آن ویژگی برای این نوع حمله تفکیک‌کننده‌تر است.
        effect_size = ((att_mean - normal_mean) / normal_std).abs().sort_values(ascending=False)

        print(f"\n{name} -- {top_n} feature with highest difference with normal")
        print(effect_size.head(top_n).to_string())


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

    encoded = Dense(8, activation="relu", name="bottleneck")(x)

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

    encoded = Dense(4, activation="relu", name="bottleneck")(x)

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


# 4b) Threshold calibration using a small labeled sample (semi-supervised)
# ============================================================================
def find_best_threshold(model, normal_errors, attack_dfs, scaler, constant_cols, feature_columns,
                         clip_lower, clip_upper, sample_size=2000, seed=SEED):
    errors_parts = [normal_errors]
    labels_parts = [np.zeros(len(normal_errors))]

    for name, df in attack_dfs.items():
        X_att, _ = clean_features(df, constant_cols=constant_cols, feature_columns=feature_columns)
        if len(X_att) == 0:
            continue
        n = min(sample_size, len(X_att))
        X_sample = X_att.sample(n=n, random_state=seed)
        X_sample = clip_outliers(X_sample, clip_lower, clip_upper)
        X_sample = log_transform(X_sample)
        X_sample_scaled = scaler.transform(X_sample)

        errs = reconstruction_error(model, X_sample_scaled)
        errors_parts.append(errs)
        labels_parts.append(np.ones(n))

    errors_all = np.concatenate(errors_parts)
    labels_all = np.concatenate(labels_parts)

    # به‌جای امتحان کردن تمام مقادیر ممکن، فقط صدک‌های ۵۰ تا ۹۹.۹ را
    # به‌عنوان کاندید Threshold بررسی می‌کنیم (کافی و سریع است).
    candidates = np.unique(np.percentile(errors_all, np.linspace(50, 99.9, 200)))

    best_threshold, best_f1 = candidates[0], -1.0
    for thr in candidates:
        preds = (errors_all > thr).astype(int)
        tp = np.sum((preds == 1) & (labels_all == 1))
        fp = np.sum((preds == 1) & (labels_all == 0))
        fn = np.sum((preds == 0) & (labels_all == 1))
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        if f1 > best_f1:
            best_f1, best_threshold = f1, thr

    print(f"Calibrated F1 score on small test data set "
          f"{best_threshold:.4f}  |  Calibreated F1 = {best_f1:.3f}")
    # نکته: همین چند هزار نمونه‌ی کالیبراسیون دوباره در evaluate_model هم
    # جزو ارزیابی نهایی حساب می‌شوند. چون نسبت به حجم کل هر دیتاست حمله
    # (ده‌ها تا صدها هزار ردیف) بسیار کوچک‌اند، تأثیرشان بر متریک نهایی
    # ناچیز است؛ برای گزارش کاملاً دقیق می‌توان این نمونه‌ها را پیش از
    # ارزیابی نهایی از attack_dfs حذف کرد.
    return best_threshold


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


def plot_roc_curve(y_true, errors, title):
    """
    منحنی ROC مستقل از Threshold است و نشون میده مدل به‌طور کلی چقدر
    توانایی جدا کردن نرمال از حمله داره (ناحیه‌ی زیر منحنی = AUC).
    برای گزارش/ارائه بسیار گویاتر از یک عدد تنها است.
    """
    fpr, tpr, _ = roc_curve(y_true, errors)
    roc_area = auc_score(fpr, tpr)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {roc_area:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Guess")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()


# 5) Evaluating on real attack data
# ============================================================================
def evaluate_model(model, threshold, scaler, constant_cols, feature_columns,
                    clip_lower, clip_upper, test_normal_X, attack_dfs, model_name):

    X_parts = [test_normal_X]
    y_true_parts = [np.zeros(len(test_normal_X))]  # 0 = normal

    for name, df in attack_dfs.items():
        X_att, _ = clean_features(df, constant_cols=constant_cols, feature_columns=feature_columns)
        if len(X_att) == 0:
            continue
        # همان کلیپِ محاسبه‌شده روی Train را اینجا هم اعمال می‌کنیم تا
        # پیش‌پردازش داده‌ی حمله دقیقاً مثل داده‌ی آموزش باشد.
        X_att = clip_outliers(X_att, clip_lower, clip_upper)
        X_att = log_transform(X_att)
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
        print(f"ROC-AUC : {auc:.4f}")
    except ValueError:
        pass

    return y_true_all, y_pred_all, errors


# 5b) Diagnostic: per-attack-type breakdown
# ============================================================================
def evaluate_per_attack_type(model, threshold, scaler, constant_cols, feature_columns,
                              clip_lower, clip_upper, test_normal_X, attack_dfs, model_name):
    normal_errors = reconstruction_error(model, test_normal_X)
    y_normal = np.zeros(len(normal_errors))

    print(f"\n================ sepration based on Attack type: {model_name} ================")
    print(f"{'Attack Type':<15}{'Recall':>10}{'Precision':>12}{'F1':>10}{'AUC':>10}{'N samples':>12}")

    rows = []
    for name, df in attack_dfs.items():
        X_att, _ = clean_features(df, constant_cols=constant_cols, feature_columns=feature_columns)
        if len(X_att) == 0:
            continue
        X_att = clip_outliers(X_att, clip_lower, clip_upper)
        X_att = log_transform(X_att)
        X_att_scaled = scaler.transform(X_att)

        att_errors = reconstruction_error(model, X_att_scaled)

        # مقایسه‌ی این یک نوع حمله در برابر همان مجموعه‌ی تست نرمال
        y_true = np.concatenate([y_normal, np.ones(len(att_errors))])
        errors_combined = np.concatenate([normal_errors, att_errors])
        y_pred = (errors_combined > threshold).astype(int)

        att_recall = (y_pred[len(y_normal):] == 1).mean()  # recall فقط برای همین نوع حمله
        try:
            auc = roc_auc_score(y_true, errors_combined)
        except ValueError:
            auc = float("nan")

        tp = ((y_pred == 1) & (y_true == 1)).sum()
        fp = ((y_pred == 1) & (y_true == 0)).sum()
        fn = ((y_pred == 0) & (y_true == 1)).sum()
        precision = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
        f1 = 2 * precision * att_recall / (precision + att_recall) if (precision + att_recall) > 0 else float("nan")

        print(f"{name:<15}{att_recall:>10.3f}{precision:>12.3f}{f1:>10.3f}{auc:>10.3f}{len(att_errors):>12}")
        rows.append({
            "model": model_name, "attack_type": name, "recall": att_recall,
            "precision": precision, "f1": f1, "auc": auc, "n_samples": len(att_errors),
        })

    return pd.DataFrame(rows)


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

    train_data, temp_data = train_test_split(X_all, test_size=0.3, random_state=SEED, shuffle=True)
    val_data, test_normal_data = train_test_split(temp_data, test_size=0.5, random_state=SEED, shuffle=True)

    # ---- کلیپ کردن outlier ها -- فقط بر اساس Train محاسبه می‌شود ----
    clip_lower, clip_upper = compute_clip_bounds(train_data)
    joblib.dump((clip_lower, clip_upper), "Cols/clip_bounds.pkl")

    # ---- تشخیص زودهنگام: قبل از صرف وقت روی آموزش مدل، ببینیم اصلاً
    # هر نوع حمله در سطح ویژگی‌های خام قابل تفکیک هست یا نه ----
    analyze_feature_separation(train_data, attack_dfs, constant_cols, feature_columns,
                                clip_lower, clip_upper)

    train_data = clip_outliers(train_data, clip_lower, clip_upper)
    val_data = clip_outliers(val_data, clip_lower, clip_upper)
    test_normal_data = clip_outliers(test_normal_data, clip_lower, clip_upper)

    # ---- فشرده‌سازی دامنه‌ی مقادیر بزرگ با log1p علامت‌دار ----
    train_data = log_transform(train_data)
    val_data = log_transform(val_data)
    test_normal_data = log_transform(test_normal_data)

    # RobustScaler بر اساس میانه و IQR کار می‌کند، پس نسبت به outlierهای
    # باقی‌مانده هم مقاوم‌تر از StandardScaler است.
    scaler = RobustScaler()
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
    reference_percentile_threshold = np.percentile(shallow_val_errors, 99)
    shallow_threshold = find_best_threshold(
        shallow_model, shallow_val_errors, attack_dfs, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper
    )
    print(f"(For comparison (example 99percentile treshhold)= {reference_percentile_threshold:.4f})")
    plot_error_histogram(shallow_val_errors, shallow_threshold, "Shallow AE - Validation Reconstruction Error")
    joblib.dump(shallow_threshold, "models/shallow_threshold.pkl")

    y_true_shallow, y_pred_shallow, errors_shallow = evaluate_model(
        shallow_model, shallow_threshold, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper, X_test_normal, attack_dfs, "Shallow Autoencoder"
    )
    plot_roc_curve(y_true_shallow, errors_shallow, "ROC Curve - Shallow Autoencoder")
    shallow_summary = evaluate_per_attack_type(
        shallow_model, shallow_threshold, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper, X_test_normal, attack_dfs, "Shallow Autoencoder"
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
    reference_percentile_threshold = np.percentile(deep_val_errors, 99)
    deep_threshold = find_best_threshold(
        deep_model, deep_val_errors, attack_dfs, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper
    )
    print(f"(For comparison (example 99percentile treshhold)= {reference_percentile_threshold:.4f})")
    plot_error_histogram(deep_val_errors, deep_threshold, "Deep AE - Validation Reconstruction Error")
    joblib.dump(deep_threshold, "models/deep_threshold.pkl")

    y_true_deep, y_pred_deep, errors_deep = evaluate_model(
        deep_model, deep_threshold, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper, X_test_normal, attack_dfs, "Deep Autoencoder"
    )
    plot_roc_curve(y_true_deep, errors_deep, "ROC Curve - Deep Autoencoder")
    deep_summary = evaluate_per_attack_type(
        deep_model, deep_threshold, scaler, constant_cols, feature_columns,
        clip_lower, clip_upper, X_test_normal, attack_dfs, "Deep Autoencoder"
    )

    # ============================================================
    # جدول مقایسه‌ی نهایی: Shallow در برابر Deep، برای هر نوع حمله
    # ============================================================
    comparison = shallow_summary.merge(
        deep_summary, on="attack_type", suffixes=("_shallow", "_deep")
    )
    comparison["better_model"] = np.where(
        comparison["recall_deep"] > comparison["recall_shallow"], "Deep", "Shallow"
    )
    print("\n================ final comparison Shallow vs Deep (بر اساس Recall) ================")
    print(comparison[[
        "attack_type", "recall_shallow", "recall_deep",
        "auc_shallow", "auc_deep", "better_model"
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
