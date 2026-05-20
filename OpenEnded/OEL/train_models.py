"""
Training script — run this once before launching the GUI.
Generates the dataset, trains all three models, saves artefacts, and prints metrics.

Usage:
    python train_models.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing import load_and_preprocess
from src.models import train_all


def main():
    print("=" * 55)
    print("  Smart Agriculture Decision Support System")
    print("  Model Training Pipeline")
    print("=" * 55)

    print("\n[1/2] Loading & preprocessing data …")
    data = load_and_preprocess()
    df = data['df']
    print(f"  Samples    : {len(df)}")
    print(f"  Features   : {data['feature_names']}")
    print(f"  Crop classes ({len(data['class_names'])}): {', '.join(data['class_names'])}")
    print(f"  Train size : {len(data['X_train'])}   Test size : {len(data['X_test'])}")

    print("\n[2/2] Training models …")
    results = train_all(data)

    dt, dt_m = results['decision_tree']
    km, km_m = results['kmeans']
    lr, lr_m = results['linear_regression']

    print("\n" + "=" * 55)
    print("  RESULTS SUMMARY")
    print("=" * 55)
    print(f"\n  Decision Tree Classifier")
    print(f"    Accuracy  : {dt_m['accuracy']}")
    print(f"    Precision : {dt_m['precision']}")
    print(f"    Recall    : {dt_m['recall']}")

    print(f"\n  K-Means Clustering")
    print(f"    Silhouette Score : {km_m['silhouette_score']}")
    print(f"    Clusters         : {km_m['n_clusters']}")
    sizes = km_m.get('cluster_sizes', {})
    for cid, sz in sizes.items():
        print(f"      Cluster {int(cid)+1} : {sz} samples")

    print(f"\n  Linear Regression")
    print(f"    RMSE : {lr_m['RMSE']}")
    print(f"    MAE  : {lr_m['MAE']}")
    print(f"    R²   : {lr_m['R2']}")

    print("\n  Classification Report (Decision Tree):")
    print(dt_m.get('report', '  (not available)'))

    print("=" * 55)
    print("  Serialized models  -> models/")
    print("  Evaluation plots   -> results/")
    print("  Run  python main.py  to launch the GUI.")
    print("=" * 55)


if __name__ == '__main__':
    main()
