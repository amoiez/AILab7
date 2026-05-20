# Smart Agriculture Decision Support System

> **Bahria University, Islamabad Campus** — Department of Software Engineering  
> **Course:** Artificial Intelligence | **OEL — CLO-2**  
> **Instructor:** Engr. Saad Mazhar Khan

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer (GUI)                      │
│          Tkinter + Matplotlib (FigureCanvasTkAgg)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ user inputs / predictions
┌──────────────────────────▼──────────────────────────────────────┐
│                      Model Layer                                 │
│  ┌──────────────────┐ ┌────────────────┐ ┌──────────────────┐  │
│  │ Decision Tree    │ │  K-Means       │ │ Linear           │  │
│  │ Classifier       │ │  Clustering    │ │ Regression       │  │
│  │ (crop recommend) │ │  (soil zones)  │ │ (yield predict)  │  │
│  └──────────────────┘ └────────────────┘ └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ preprocessed features
┌──────────────────────────▼──────────────────────────────────────┐
│                      Data Layer                                  │
│  CSV Dataset → Imputation → IQR Outlier Clip → StandardScaler  │
│  LabelEncoder → 80/20 Train-Test Split                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train models

```bash
python train_models.py
```

This generates the dataset, trains all three models, serializes them to `models/`, and saves evaluation plots to `results/`.

### 3. Launch the GUI

```bash
python main.py
```

---

## Repository Structure

```
repository/
├── data/
│   └── crop_data.csv           # Auto-generated on first run
├── src/
│   ├── __init__.py
│   ├── preprocessing.py        # Dataset generation & preprocessing pipeline
│   ├── models.py               # Model training, evaluation & serialization
│   ├── gui.py                  # Tkinter GUI application
│   └── utils.py                # Constants, validators, report formatter
├── models/
│   ├── decision_tree.pkl       # Serialized Decision Tree
│   ├── kmeans.pkl              # Serialized K-Means model
│   ├── linear_regression.pkl   # Serialized Linear Regression
│   ├── scaler.pkl              # Fitted StandardScaler
│   ├── label_encoder.pkl       # Fitted LabelEncoder
│   ├── pca.pkl                 # Fitted PCA (for cluster viz)
│   └── metrics.json            # Saved evaluation metrics
├── results/
│   ├── feature_importance.png  # Decision Tree feature importances
│   ├── cluster_scatter.png     # K-Means PCA scatter plot
│   └── residual_plot.png       # Linear Regression residual analysis
├── train_models.py             # Standalone training script
├── main.py                     # GUI entry point
├── requirements.txt            # Dependency manifest
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## Dataset

A **synthetic agricultural dataset** (2,300 samples, 23 crop classes) is generated automatically on first run. It models real-world distributions drawn from the Kaggle *Crop Recommendation Dataset* and UCI agricultural repositories.

### Data Dictionary

| Feature       | Description                           | Unit    | Range      |
|---------------|---------------------------------------|---------|------------|
| `N`           | Soil nitrogen content                 | kg/ha   | 0 – 140    |
| `P`           | Soil phosphorus content               | kg/ha   | 5 – 145    |
| `K`           | Soil potassium content                | kg/ha   | 5 – 205    |
| `temperature` | Ambient temperature                   | °C      | 8 – 44     |
| `humidity`    | Relative humidity                     | %       | 14 – 100   |
| `ph`          | Soil pH                               | —       | 3.5 – 9.9  |
| `rainfall`    | Annual rainfall                       | mm      | 20 – 300   |
| `crop_yield`  | Crop yield (regression target)        | t/ha    | 0.7 – 55   |
| `label`       | Crop class (classification target)    | —       | 23 classes |

### Preprocessing Rationale

- **Missing value imputation** — median imputation (robust to skewed distributions)
- **Outlier treatment** — IQR clipping (±1.5× IQR) to prevent distortion of model boundaries
- **Feature scaling** — `StandardScaler` (zero mean, unit variance) required by KNN/KMeans and improves regression conditioning
- **Label encoding** — ordinal integer encoding for 23 crop classes

---

## Algorithmic Core

### 1. Decision Tree Classifier

**Purpose:** Crop recommendation from soil and climate features.

- `max_depth=12`, `min_samples_split=4`, `min_samples_leaf=2`
- **Metrics:** Accuracy, Precision (weighted), Recall (weighted)
- **Visualization:** Feature importance bar chart

### 2. K-Means Clustering (k=5)

**Purpose:** Soil profile segmentation to identify homogeneous farm zones.

> *Note: The specification uses "K-Nearest Neighbors Clustering" as a label; K-Means is the appropriate centroid-based clustering algorithm for this unsupervised soil segmentation task.*

- `n_clusters=5`, `n_init=15`
- **Metrics:** Silhouette Score, Cluster size distribution
- **Visualization:** PCA-reduced 2-D cluster scatter plot

### 3. Linear Regression

**Purpose:** Quantitative crop yield prediction (tonnes/hectare).

- Standard OLS with `StandardScaler`-preprocessed features
- **Metrics:** RMSE, MAE, R²
- **Visualization:** Residual vs Fitted + Predicted vs Actual plots

---

## Performance Summary

| Model                  | Metric              | Typical Value |
|------------------------|---------------------|---------------|
| Decision Tree          | Accuracy            | ~0.97+        |
| Decision Tree          | Weighted Precision  | ~0.97+        |
| Decision Tree          | Weighted Recall     | ~0.97+        |
| K-Means (k=5)          | Silhouette Score    | ~0.40 – 0.50  |
| Linear Regression      | R²                  | ~0.88 – 0.93  |
| Linear Regression      | RMSE (t/ha)         | ~2.5 – 4.0    |

*Exact values printed to console by `train_models.py` and stored in `models/metrics.json`.*

---

## GUI Features

- **Tab 1 — Input & Prediction:** Enter 7 soil/climate parameters and receive integrated outputs: recommended crop, soil cluster with agronomic guidance, and predicted yield with confidence bounds.
- **Tab 2 — Visualizations:** Three embedded Matplotlib plots (Feature Importance, Cluster Scatter, Residual Analysis) rendered live inside the Tkinter window.
- **Tab 3 — About:** System architecture, data dictionary, and usage instructions.

---

## Industrial Application

This system maps directly to commercial agri-tech deployment:

1. **Field Advisory Apps** — smartphone input of sensor readings → instant crop recommendation without internet connectivity.
2. **Variable-Rate Fertilization** — soil cluster assignment drives prescription maps for precision nutrient application, reducing input costs by 15–25%.
3. **Yield Forecasting** — regression output feeds procurement and logistics planning for agri-supply chains.
4. **Insurance & Credit Scoring** — yield predictions with confidence bounds support parametric crop insurance products.

---

## Future Work

**1. IoT Sensor Integration**  
Replace manual input with live MQTT feeds from in-field soil sensors (e.g., EC/pH probes, weather stations). A streaming inference pipeline (Apache Kafka + FastAPI) would enable real-time decision support at scale, with automatic model retraining as new seasonal data accumulates.

**2. Ensemble Deep Learning with Satellite Imagery Fusion**  
Augment the tabular feature set with multi-spectral vegetation indices (NDVI, EVI) derived from Sentinel-2 imagery. A hybrid architecture combining a 1-D CNN for tabular features with a lightweight ResNet branch for patch-level imagery, fused via attention gating, could capture spatial heterogeneity invisible to point-sample sensors.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
