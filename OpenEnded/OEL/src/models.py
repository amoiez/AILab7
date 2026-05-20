"""
Algorithmic Core
Trains and evaluates three models:
  1. Decision Tree Classifier  — crop recommendation
  2. K-Means Clustering        — soil profile segmentation
  3. Linear Regression         — crop yield prediction
All trained artefacts are serialized via joblib and evaluation plots saved to results/.
"""

import os
import json
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    classification_report, silhouette_score,
    mean_squared_error, mean_absolute_error, r2_score,
)

from src.utils import PROJECT_ROOT

MODELS_DIR  = os.path.join(PROJECT_ROOT, 'models')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')


def _dirs():
    os.makedirs(MODELS_DIR,  exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)


# ── 1. Decision Tree Classifier ──────────────────────────────────────────────

def train_decision_tree(X_train, X_test, yc_train, yc_test,
                        feature_names, label_encoder) -> tuple:
    clf = DecisionTreeClassifier(max_depth=12, min_samples_split=4,
                                  min_samples_leaf=2, random_state=42)
    clf.fit(X_train, yc_train)

    y_pred = clf.predict(X_test)
    metrics = {
        'accuracy':  round(accuracy_score(yc_test, y_pred), 4),
        'precision': round(precision_score(yc_test, y_pred, average='weighted', zero_division=0), 4),
        'recall':    round(recall_score(yc_test, y_pred, average='weighted', zero_division=0), 4),
        'report':    classification_report(yc_test, y_pred,
                         target_names=label_encoder.classes_, zero_division=0),
    }

    joblib.dump(clf, os.path.join(MODELS_DIR, 'decision_tree.pkl'))

    # Feature importance bar chart
    importances = clf.feature_importances_
    idx = np.argsort(importances)[::-1]

    fig, ax = plt.subplots(figsize=(8, 5))
    colours = plt.cm.Blues(np.linspace(0.4, 0.9, len(feature_names)))
    bars = ax.bar(range(len(feature_names)), importances[idx], color=colours, edgecolor='grey')
    ax.set_xticks(range(len(feature_names)))
    ax.set_xticklabels([feature_names[i] for i in idx], rotation=40, ha='right', fontsize=10)
    ax.set_ylabel('Importance Score', fontsize=11)
    ax.set_xlabel('Feature', fontsize=11)
    ax.set_title('Decision Tree — Feature Importance', fontsize=13, fontweight='bold')
    for bar, val in zip(bars, importances[idx]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax.set_ylim(0, importances.max() * 1.18)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, 'feature_importance.png'), dpi=150)
    plt.close(fig)

    print(f"  [DT]  Accuracy={metrics['accuracy']:.4f}  "
          f"Precision={metrics['precision']:.4f}  Recall={metrics['recall']:.4f}")
    return clf, metrics


# ── 2. K-Means Clustering ────────────────────────────────────────────────────

def train_kmeans(X_scaled, n_clusters: int = 5) -> tuple:
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=15, max_iter=300)
    labels = km.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)

    joblib.dump(km, os.path.join(MODELS_DIR, 'kmeans.pkl'))

    # PCA → 2-D scatter
    pca = PCA(n_components=2, random_state=42)
    X_2d = pca.fit_transform(X_scaled)
    joblib.dump(pca, os.path.join(MODELS_DIR, 'pca.pkl'))

    palette = plt.cm.tab10(np.linspace(0, 0.9, n_clusters))
    fig, ax = plt.subplots(figsize=(8, 6))
    for i in range(n_clusters):
        mask = labels == i
        ax.scatter(X_2d[mask, 0], X_2d[mask, 1],
                   c=[palette[i]], label=f'Cluster {i+1}',
                   alpha=0.55, s=18, edgecolors='none')
    centers_2d = pca.transform(km.cluster_centers_)
    ax.scatter(centers_2d[:, 0], centers_2d[:, 1],
               c='black', marker='X', s=180, zorder=10, label='Centroids')
    ax.set_title(f'K-Means Soil Profile Clusters  (Silhouette = {sil:.3f})',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Principal Component 1', fontsize=11)
    ax.set_ylabel('Principal Component 2', fontsize=11)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, 'cluster_scatter.png'), dpi=150)
    plt.close(fig)

    metrics = {
        'silhouette_score': round(sil, 4),
        'n_clusters':       n_clusters,
        'cluster_sizes':    {int(i): int(np.sum(labels == i)) for i in range(n_clusters)},
    }
    print(f"  [KM]  Silhouette Score={sil:.4f}  n_clusters={n_clusters}")
    return km, metrics


# ── 3. Linear Regression ─────────────────────────────────────────────────────

def train_linear_regression(X_train, X_test, yr_train, yr_test,
                             yc_train=None, yc_test=None) -> tuple:
    from sklearn.preprocessing import OneHotEncoder

    # One-hot-encode the crop label so the model can learn a per-crop yield offset
    if yc_train is not None:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        ohe_tr = ohe.fit_transform(yc_train.reshape(-1, 1))
        ohe_te = ohe.transform(yc_test.reshape(-1, 1))
        X_tr   = np.hstack([X_train, ohe_tr])
        X_te   = np.hstack([X_test,  ohe_te])
        joblib.dump(ohe, os.path.join(MODELS_DIR, 'lr_ohe.pkl'))
    else:
        X_tr, X_te = X_train, X_test

    # Log-transform the target so linear regression handles the wide yield range
    log_yr_train = np.log1p(yr_train)

    reg = LinearRegression()
    reg.fit(X_tr, log_yr_train)

    log_pred = reg.predict(X_te)
    y_pred   = np.expm1(log_pred)          # back-transform to original scale
    residuals = yr_test - y_pred

    metrics = {
        'RMSE': round(float(np.sqrt(mean_squared_error(yr_test, y_pred))), 4),
        'MAE':  round(float(mean_absolute_error(yr_test, y_pred)), 4),
        'R2':   round(float(r2_score(yr_test, y_pred)), 4),
    }

    # Save the log-space model; inference code must also apply log1p/expm1
    joblib.dump(reg, os.path.join(MODELS_DIR, 'linear_regression.pkl'))
    # Flag so GUI knows to back-transform
    import json as _json
    _flag = {'log_transform': True}
    with open(os.path.join(MODELS_DIR, 'lr_meta.json'), 'w') as f:
        _json.dump(_flag, f)

    # Residual plot (two sub-plots)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Linear Regression — Residual Analysis', fontsize=13, fontweight='bold')

    axes[0].scatter(y_pred, residuals, alpha=0.45, color='#e57373',
                    edgecolors='#b71c1c', s=25, linewidths=0.4)
    axes[0].axhline(0, color='black', linewidth=1.5, linestyle='--')
    axes[0].set_title('Residual vs Fitted', fontsize=11)
    axes[0].set_xlabel('Predicted Yield  (t/ha)')
    axes[0].set_ylabel('Residuals')

    mn, mx = float(yr_test.min()), float(yr_test.max())
    axes[1].scatter(yr_test, y_pred, alpha=0.45, color='#42a5f5',
                    edgecolors='#0d47a1', s=25, linewidths=0.4)
    axes[1].plot([mn, mx], [mn, mx], 'r--', linewidth=1.8, label='Ideal fit')
    axes[1].set_title(f'Predicted vs Actual  (R2 = {metrics["R2"]:.3f})', fontsize=11)
    axes[1].set_xlabel('Actual Yield  (t/ha)')
    axes[1].set_ylabel('Predicted Yield  (t/ha)')
    axes[1].legend(fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, 'residual_plot.png'), dpi=150)
    plt.close(fig)

    print(f"  [LR]  RMSE={metrics['RMSE']:.4f}  MAE={metrics['MAE']:.4f}  R2={metrics['R2']:.4f}")
    return reg, metrics


# ── Orchestrator ─────────────────────────────────────────────────────────────

def train_all(data: dict) -> dict:
    _dirs()

    print("\nTraining Decision Tree Classifier …")
    dt, dt_m = train_decision_tree(
        data['X_train'], data['X_test'],
        data['yc_train'], data['yc_test'],
        data['feature_names'], data['label_encoder'],
    )

    print("Training K-Means Clustering …")
    km, km_m = train_kmeans(data['X_scaled'])

    print("Training Linear Regression …")
    lr, lr_m = train_linear_regression(
        data['X_train'], data['X_test'],
        data['yr_train'], data['yr_test'],
        yc_train=data['yc_train'], yc_test=data['yc_test'],
    )

    # Persist ancillary artefacts
    joblib.dump(data['scaler'],        os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(data['label_encoder'], os.path.join(MODELS_DIR, 'label_encoder.pkl'))

    # Save metrics summary as JSON for GUI display
    summary = {
        'decision_tree':      dt_m,
        'kmeans':             km_m,
        'linear_regression':  lr_m,
    }
    # Remove non-serialisable classification report
    summary['decision_tree'] = {k: v for k, v in dt_m.items() if k != 'report'}
    with open(os.path.join(MODELS_DIR, 'metrics.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    return {
        'decision_tree':     (dt, dt_m),
        'kmeans':            (km, km_m),
        'linear_regression': (lr, lr_m),
    }
