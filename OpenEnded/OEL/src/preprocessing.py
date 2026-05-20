"""
Data Engineering Layer
Generates a synthetic crop-recommendation dataset (mimicking Kaggle Crop Recommendation),
applies comprehensive preprocessing, and returns train/test splits ready for modelling.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

from src.utils import PROJECT_ROOT, FEATURE_COLS


# ── Dataset generation ───────────────────────────────────────────────────────

CROP_PROFILES = {
    'rice':        dict(N=(80,10),  P=(45,8),   K=(42,8),   temp=(23,2),  hum=(82,5),  ph=(6.5,.3), rain=(200,30), yld=(4.5,.8)),
    'wheat':       dict(N=(70,10),  P=(47,8),   K=(41,7),   temp=(22,3),  hum=(65,5),  ph=(6.8,.3), rain=(80,15),  yld=(3.2,.5)),
    'maize':       dict(N=(78,10),  P=(48,8),   K=(20,5),   temp=(21,3),  hum=(65,5),  ph=(6.2,.3), rain=(70,15),  yld=(5.5,1.0)),
    'chickpea':    dict(N=(40,8),   P=(67,8),   K=(79,8),   temp=(18,2),  hum=(17,3),  ph=(7.2,.3), rain=(85,15),  yld=(1.8,.3)),
    'kidneybeans': dict(N=(20,5),   P=(67,8),   K=(20,5),   temp=(20,2),  hum=(20,3),  ph=(5.7,.3), rain=(105,15), yld=(1.5,.3)),
    'pigeonpeas':  dict(N=(20,5),   P=(67,8),   K=(20,5),   temp=(27,2),  hum=(49,5),  ph=(5.7,.3), rain=(149,20), yld=(1.2,.3)),
    'mothbeans':   dict(N=(21,5),   P=(47,8),   K=(20,5),   temp=(28,2),  hum=(53,5),  ph=(6.8,.3), rain=(52,10),  yld=(.9,.2)),
    'mungbean':    dict(N=(20,5),   P=(47,8),   K=(20,5),   temp=(28,2),  hum=(86,5),  ph=(6.7,.3), rain=(49,10),  yld=(.8,.2)),
    'blackgram':   dict(N=(40,8),   P=(67,8),   K=(19,5),   temp=(29,2),  hum=(65,5),  ph=(7.1,.3), rain=(69,15),  yld=(.7,.15)),
    'lentil':      dict(N=(18,4),   P=(67,8),   K=(19,5),   temp=(24,2),  hum=(65,5),  ph=(6.9,.3), rain=(46,10),  yld=(1.3,.2)),
    'pomegranate': dict(N=(18,4),   P=(18,4),   K=(40,5),   temp=(21,2),  hum=(90,5),  ph=(6.4,.3), rain=(110,20), yld=(8.0,1.5)),
    'banana':      dict(N=(100,10), P=(82,8),   K=(50,8),   temp=(27,2),  hum=(80,5),  ph=(5.9,.3), rain=(105,20), yld=(30.,5.)),
    'mango':       dict(N=(20,5),   P=(27,5),   K=(30,5),   temp=(31,3),  hum=(50,5),  ph=(6.2,.3), rain=(95,20),  yld=(6.5,1.2)),
    'grapes':      dict(N=(23,5),   P=(132,10), K=(200,15), temp=(23,2),  hum=(82,5),  ph=(6.1,.3), rain=(70,15),  yld=(12.,2.5)),
    'watermelon':  dict(N=(99,10),  P=(17,4),   K=(50,8),   temp=(27,2),  hum=(85,5),  ph=(6.5,.3), rain=(50,10),  yld=(25.,5.)),
    'muskmelon':   dict(N=(100,10), P=(17,4),   K=(50,8),   temp=(28,2),  hum=(92,5),  ph=(6.3,.3), rain=(25,8),   yld=(15.,3.)),
    'apple':       dict(N=(21,5),   P=(134,10), K=(199,15), temp=(22,2),  hum=(92,5),  ph=(5.9,.3), rain=(113,20), yld=(10.,2.)),
    'orange':      dict(N=(20,5),   P=(16,4),   K=(10,3),   temp=(22,2),  hum=(92,5),  ph=(7.0,.3), rain=(110,20), yld=(14.,3.)),
    'papaya':      dict(N=(49,8),   P=(59,8),   K=(50,8),   temp=(33,3),  hum=(92,5),  ph=(6.7,.3), rain=(145,25), yld=(20.,4.)),
    'coconut':     dict(N=(21,5),   P=(16,4),   K=(30,5),   temp=(27,2),  hum=(94,5),  ph=(5.9,.3), rain=(176,25), yld=(55.,10.)),
    'cotton':      dict(N=(118,10), P=(46,8),   K=(19,5),   temp=(24,2),  hum=(79,5),  ph=(6.9,.3), rain=(80,15),  yld=(1.8,.3)),
    'jute':        dict(N=(78,10),  P=(46,8),   K=(39,7),   temp=(25,2),  hum=(80,5),  ph=(6.7,.3), rain=(175,25), yld=(2.5,.5)),
    'coffee':      dict(N=(101,10), P=(28,5),   K=(29,5),   temp=(25,2),  hum=(58,5),  ph=(6.8,.3), rain=(158,25), yld=(1.5,.3)),
}


def generate_dataset(n_samples: int = 2300, save_path: str = None) -> pd.DataFrame:
    """Generate synthetic agricultural dataset with 23 crop classes."""
    np.random.seed(42)
    per_crop = n_samples // len(CROP_PROFILES)
    rows = []

    for crop, p in CROP_PROFILES.items():
        for _ in range(per_crop):
            rows.append({
                'N':           round(max(0,   np.random.normal(*p['N'])),    2),
                'P':           round(max(0,   np.random.normal(*p['P'])),    2),
                'K':           round(max(0,   np.random.normal(*p['K'])),    2),
                'temperature': round(         np.random.normal(*p['temp']),  2),
                'humidity':    round(np.clip( np.random.normal(*p['hum']),  0, 100), 2),
                'ph':          round(np.clip( np.random.normal(*p['ph']),   0,  14), 2),
                'rainfall':    round(max(0,   np.random.normal(*p['rain'])), 2),
                'crop_yield':  round(max(0,   np.random.normal(*p['yld'])),  2),
                'label':       crop,
            })

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)

    return df


# ── Preprocessing ────────────────────────────────────────────────────────────

def load_and_preprocess(csv_path: str = None) -> dict:
    """
    Load (or generate) the dataset, apply preprocessing, and return a data bundle
    with train/test splits, scaler, and label encoder.
    """
    if csv_path is None:
        csv_path = os.path.join(PROJECT_ROOT, 'data', 'crop_data.csv')

    if not os.path.exists(csv_path):
        print(f"[preprocessing] Generating dataset -> {csv_path}")
        df = generate_dataset(save_path=csv_path)
    else:
        df = pd.read_csv(csv_path)

    # ── Missing value imputation (median) ──
    for col in FEATURE_COLS + ['crop_yield']:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)

    # ── Outlier treatment: IQR clipping ──
    for col in FEATURE_COLS:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        df[col] = df[col].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

    # ── Label encoding ──
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df['label'])

    X = df[FEATURE_COLS].values
    y_class = df['label_encoded'].values
    y_reg   = df['crop_yield'].values

    # ── Feature scaling ──
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── Train / test split ──
    X_tr, X_te, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
        X_scaled, y_class, y_reg,
        test_size=0.2, random_state=42, stratify=y_class,
    )

    return {
        'df':            df,
        'X_scaled':      X_scaled,
        'X_train':       X_tr,  'X_test':  X_te,
        'yc_train':      yc_tr, 'yc_test': yc_te,
        'yr_train':      yr_tr, 'yr_test': yr_te,
        'scaler':        scaler,
        'label_encoder': le,
        'feature_names': FEATURE_COLS,
        'class_names':   list(le.classes_),
    }
