"""
System Assembly & Interface Layer
Tkinter GUI that binds the three serialized models into a single interactive application.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import numpy as np
import joblib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.decomposition import PCA

# Ensure the project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.utils import FEATURE_RANGES, FEATURE_DEFAULTS, validate_inputs, format_report

MODELS_DIR  = os.path.join(PROJECT_ROOT, 'models')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

# ── Colour palette ────────────────────────────────────────────────────────────
C_BG      = '#f1f8e9'
C_HEADER  = '#2e7d32'
C_ACCENT  = '#43a047'
C_PANEL   = '#ffffff'
C_TEXT    = '#1b5e20'
C_BUTTON  = '#388e3c'
C_BTN_FG  = '#ffffff'
FONT_MAIN = ('Segoe UI', 10)
FONT_BOLD = ('Segoe UI', 10, 'bold')
FONT_CODE = ('Consolas', 10)
FONT_MONO = ('Consolas', 9)


# ── Model loader ──────────────────────────────────────────────────────────────

def load_models():
    required = ['decision_tree.pkl', 'kmeans.pkl', 'linear_regression.pkl',
                'scaler.pkl', 'label_encoder.pkl']
    missing = [f for f in required if not os.path.exists(os.path.join(MODELS_DIR, f))]
    if missing:
        return None, (
            f"Missing model files:\n  " + "\n  ".join(missing) +
            "\n\nPlease run  train_models.py  first."
        )
    return {
        'dt': joblib.load(os.path.join(MODELS_DIR, 'decision_tree.pkl')),
        'km': joblib.load(os.path.join(MODELS_DIR, 'kmeans.pkl')),
        'lr': joblib.load(os.path.join(MODELS_DIR, 'linear_regression.pkl')),
        'sc': joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl')),
        'le': joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl')),
    }, None


# ── Main application ──────────────────────────────────────────────────────────

class AgriApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Smart Agriculture Decision Support System")
        self.geometry("1160x760")
        self.minsize(900, 620)
        self.configure(bg=C_BG)

        self.models, err = load_models()
        if err:
            messagebox.showerror("Model Load Error", err)
            self.destroy()
            return

        self._load_metrics()
        self._build_ui()

    # ── Metrics ──────────────────────────────────────────────────────────────

    def _load_metrics(self):
        path = os.path.join(MODELS_DIR, 'metrics.json')
        try:
            with open(path) as f:
                self.metrics = json.load(f)
        except Exception:
            self.metrics = {}

    # ── UI skeleton ───────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header bar
        hdr = tk.Frame(self, bg=C_HEADER, height=56)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr,
                 text="🌾  Smart Agriculture Decision Support System",
                 bg=C_HEADER, fg='white',
                 font=('Segoe UI', 15, 'bold')).pack(side='left', padx=20, pady=12)
        tk.Label(hdr,
                 text="Bahria University  |  AI Lab OEL",
                 bg=C_HEADER, fg='#c8e6c9',
                 font=('Segoe UI', 9)).pack(side='right', padx=20)

        # Notebook
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TNotebook',        background=C_BG)
        style.configure('TNotebook.Tab',    font=FONT_BOLD, padding=[14, 6])
        style.map('TNotebook.Tab',
                  background=[('selected', C_ACCENT), ('active', '#81c784')],
                  foreground=[('selected', 'white')])

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both', expand=True, padx=12, pady=8)

        self._build_input_tab()
        self._build_viz_tab()
        self._build_about_tab()

    # ── Tab 1 — Input & Prediction ────────────────────────────────────────────

    def _build_input_tab(self):
        outer = ttk.Frame(self.nb)
        self.nb.add(outer, text='  Input & Prediction  ')

        # Left: parameter form
        left = tk.LabelFrame(outer, text='  Soil & Climate Parameters  ',
                              bg=C_PANEL, fg=C_TEXT,
                              font=FONT_BOLD, padx=14, pady=12,
                              relief='groove', bd=2)
        left.pack(side='left', fill='y', padx=(14, 6), pady=12)

        self.entry_vars = {}
        for row_idx, (key, (lo, hi, label)) in enumerate(FEATURE_RANGES.items()):
            tk.Label(left, text=label, bg=C_PANEL, fg=C_TEXT,
                     font=FONT_MAIN, anchor='w').grid(
                         row=row_idx, column=0, sticky='w', pady=5, padx=(0, 8))
            var = tk.DoubleVar(value=FEATURE_DEFAULTS[key])
            ent = tk.Entry(left, textvariable=var, width=11,
                           font=FONT_CODE, relief='solid', bd=1)
            ent.grid(row=row_idx, column=1, pady=5)
            tk.Label(left, text=f'({lo} – {hi})',
                     bg=C_PANEL, fg='#888', font=('Segoe UI', 8)).grid(
                         row=row_idx, column=2, sticky='w', padx=(6, 0))
            self.entry_vars[key] = var

        btn = tk.Button(left, text='▶  Run Prediction',
                        bg=C_BUTTON, fg=C_BTN_FG,
                        font=('Segoe UI', 11, 'bold'),
                        relief='flat', cursor='hand2',
                        activebackground='#1b5e20', activeforeground='white',
                        command=self._predict, pady=8)
        btn.grid(row=len(FEATURE_RANGES), column=0, columnspan=3,
                 sticky='ew', pady=(18, 4))

        btn_reset = tk.Button(left, text='↺  Reset Defaults',
                              bg='#e0e0e0', fg='#333',
                              font=FONT_MAIN, relief='flat',
                              cursor='hand2', command=self._reset_defaults)
        btn_reset.grid(row=len(FEATURE_RANGES)+1, column=0, columnspan=3,
                       sticky='ew', pady=(2, 0))

        # Right: output area
        right = tk.Frame(outer, bg=C_BG)
        right.pack(side='left', fill='both', expand=True, padx=(6, 14), pady=12)

        # Result output
        res_frame = tk.LabelFrame(right, text='  Integrated Output  ',
                                  bg=C_PANEL, fg=C_TEXT, font=FONT_BOLD,
                                  relief='groove', bd=2, padx=10, pady=8)
        res_frame.pack(fill='both', expand=True, pady=(0, 8))

        self.result_text = scrolledtext.ScrolledText(
            res_frame, font=FONT_CODE,
            bg='#f9fbe7', fg='#1a237e',
            relief='flat', state='disabled',
            height=14, wrap='word')
        self.result_text.pack(fill='both', expand=True)

        # Metrics panel
        met_frame = tk.LabelFrame(right, text='  Model Performance Summary  ',
                                  bg=C_PANEL, fg=C_TEXT, font=FONT_BOLD,
                                  relief='groove', bd=2, padx=10, pady=6)
        met_frame.pack(fill='x')

        self.metrics_text = tk.Text(met_frame, font=FONT_MONO,
                                    bg='#e8f5e9', fg='#1b5e20',
                                    relief='flat', state='disabled', height=6)
        self.metrics_text.pack(fill='x')
        self._refresh_metrics_panel()

        # Initial placeholder
        self._set_result("Enter soil and climate parameters on the left,\n"
                         "then click  ▶ Run Prediction  to generate the report.")

    def _reset_defaults(self):
        for key, var in self.entry_vars.items():
            var.set(FEATURE_DEFAULTS[key])

    def _refresh_metrics_panel(self):
        if not self.metrics:
            lines = ["  Metrics unavailable — run train_models.py"]
        else:
            dt = self.metrics.get('decision_tree', {})
            km = self.metrics.get('kmeans', {})
            lr = self.metrics.get('linear_regression', {})
            lines = [
                f"  Decision Tree     │  Accuracy : {dt.get('accuracy','N/A'):<8}  "
                f"Precision : {dt.get('precision','N/A'):<8}  Recall : {dt.get('recall','N/A')}",
                f"  K-Means           │  Silhouette Score : {km.get('silhouette_score','N/A'):<8}  "
                f"Clusters : {km.get('n_clusters','N/A')}",
                f"  Linear Regression │  RMSE : {lr.get('RMSE','N/A'):<10}  "
                f"MAE : {lr.get('MAE','N/A'):<10}  R² : {lr.get('R2','N/A')}",
                "",
                "  Visualizations available in the  Visualizations  tab.",
            ]
        self.metrics_text.configure(state='normal')
        self.metrics_text.delete('1.0', 'end')
        self.metrics_text.insert('end', '\n'.join(lines))
        self.metrics_text.configure(state='disabled')

    def _set_result(self, text: str):
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', 'end')
        self.result_text.insert('end', text)
        self.result_text.configure(state='disabled')

    def _predict(self):
        try:
            vals = {k: float(v.get()) for k, v in self.entry_vars.items()}
        except tk.TclError:
            messagebox.showerror("Input Error", "All fields must be numeric.")
            return

        ok, msg = validate_inputs(vals)
        if not ok:
            messagebox.showwarning("Validation Error", msg)
            return

        x_raw    = np.array([[vals[k] for k in FEATURE_RANGES]])
        x_scaled = self.models['sc'].transform(x_raw)

        crop_enc  = self.models['dt'].predict(x_scaled)[0]
        crop_name = self.models['le'].inverse_transform([crop_enc])[0]
        cluster   = int(self.models['km'].predict(x_scaled)[0])

        # Append one-hot crop label (matches training setup)
        ohe_path = os.path.join(MODELS_DIR, 'lr_ohe.pkl')
        if os.path.exists(ohe_path):
            ohe = joblib.load(ohe_path)
            crop_ohe = ohe.transform([[crop_enc]])
            x_lr = np.hstack([x_scaled, crop_ohe])
        else:
            x_lr = x_scaled
        lr_raw = float(self.models['lr'].predict(x_lr)[0])
        # If model was trained on log1p(yield), back-transform
        lr_meta_path = os.path.join(MODELS_DIR, 'lr_meta.json')
        if os.path.exists(lr_meta_path):
            import json as _j
            with open(lr_meta_path) as f:
                meta = _j.load(f)
            if meta.get('log_transform'):
                lr_raw = float(np.expm1(lr_raw))
        yield_val = max(0.0, lr_raw)

        report = format_report(crop_name, cluster, yield_val)
        self._set_result(report)

    # ── Tab 2 — Visualizations ────────────────────────────────────────────────

    def _build_viz_tab(self):
        outer = ttk.Frame(self.nb)
        self.nb.add(outer, text='  Visualizations  ')

        btn_row = tk.Frame(outer, bg=C_BG)
        btn_row.pack(fill='x', padx=14, pady=(10, 4))

        tk.Label(btn_row, text='Select plot:', bg=C_BG,
                 font=FONT_BOLD, fg=C_TEXT).pack(side='left', padx=(0, 8))

        plots = [
            ('Feature Importance',  self._plot_feature_importance),
            ('Soil Cluster Scatter', self._plot_cluster_scatter),
            ('Residual Analysis',   self._plot_residuals),
        ]
        for label, fn in plots:
            tk.Button(btn_row, text=label,
                      bg=C_BUTTON, fg=C_BTN_FG,
                      font=FONT_MAIN, relief='flat',
                      cursor='hand2', padx=10, pady=4,
                      activebackground='#1b5e20',
                      command=fn).pack(side='left', padx=4)

        self._viz_canvas_widget = None
        self.viz_host = tk.Frame(outer, bg=C_BG)
        self.viz_host.pack(fill='both', expand=True, padx=8, pady=4)

        # Show first plot by default when tab is rendered
        outer.bind('<Visibility>', lambda e: self._plot_feature_importance())

    def _clear_viz(self):
        for w in self.viz_host.winfo_children():
            w.destroy()

    def _embed_figure(self, fig):
        self._clear_viz()
        canvas = FigureCanvasTkAgg(fig, master=self.viz_host)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill='both', expand=True)
        self._viz_canvas_widget = widget

    def _plot_feature_importance(self):
        dt = self.models['dt']
        feature_names = list(FEATURE_RANGES.keys())
        importances = dt.feature_importances_
        idx = np.argsort(importances)[::-1]

        fig, ax = plt.subplots(figsize=(8, 4.5))
        colours = plt.cm.Blues(np.linspace(0.4, 0.9, len(feature_names)))
        bars = ax.bar(range(len(feature_names)), importances[idx],
                      color=colours, edgecolor='grey')
        ax.set_xticks(range(len(feature_names)))
        ax.set_xticklabels([feature_names[i] for i in idx], rotation=35, ha='right')
        ax.set_ylabel('Importance Score')
        ax.set_title('Decision Tree — Feature Importance', fontsize=12, fontweight='bold')
        for bar, val in zip(bars, importances[idx]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.002, f'{val:.3f}',
                    ha='center', va='bottom', fontsize=8)
        ax.set_ylim(0, importances.max() * 1.18)
        fig.tight_layout()
        self._embed_figure(fig)
        plt.close(fig)

    def _plot_cluster_scatter(self):
        try:
            from src.preprocessing import load_and_preprocess
            data = load_and_preprocess()
        except Exception as e:
            self._clear_viz()
            tk.Label(self.viz_host, text=f"Error loading data: {e}",
                     fg='red', bg=C_BG, font=FONT_MAIN).pack(pady=30)
            return

        km = self.models['km']
        n_clusters = km.n_clusters

        pca_path = os.path.join(MODELS_DIR, 'pca.pkl')
        if os.path.exists(pca_path):
            pca = joblib.load(pca_path)
        else:
            pca = PCA(n_components=2, random_state=42)
            pca.fit(data['X_scaled'])

        X_2d   = pca.transform(data['X_scaled'])
        labels = km.predict(data['X_scaled'])

        palette = plt.cm.tab10(np.linspace(0, 0.9, n_clusters))
        fig, ax = plt.subplots(figsize=(8, 5.5))
        for i in range(n_clusters):
            mask = labels == i
            ax.scatter(X_2d[mask, 0], X_2d[mask, 1],
                       c=[palette[i]], label=f'Cluster {i+1}',
                       alpha=0.55, s=18, edgecolors='none')
        centers_2d = pca.transform(km.cluster_centers_)
        ax.scatter(centers_2d[:, 0], centers_2d[:, 1],
                   c='black', marker='X', s=160, zorder=10, label='Centroids')

        from src.models import train_kmeans
        sil_str = ''
        metrics_path = os.path.join(MODELS_DIR, 'metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path) as f:
                m = json.load(f)
            sil_str = f"  (Silhouette = {m['kmeans']['silhouette_score']:.3f})"

        ax.set_title(f'K-Means Soil Profile Clusters{sil_str}',
                     fontsize=12, fontweight='bold')
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.legend(fontsize=9)
        fig.tight_layout()
        self._embed_figure(fig)
        plt.close(fig)

    def _plot_residuals(self):
        try:
            from src.preprocessing import load_and_preprocess
            data = load_and_preprocess()
        except Exception as e:
            self._clear_viz()
            tk.Label(self.viz_host, text=f"Error loading data: {e}",
                     fg='red', bg=C_BG, font=FONT_MAIN).pack(pady=30)
            return

        lr = self.models['lr']
        # Append one-hot crop labels (same augmentation as training)
        ohe_path = os.path.join(MODELS_DIR, 'lr_ohe.pkl')
        if os.path.exists(ohe_path):
            _ohe = joblib.load(ohe_path)
            X_lr = np.hstack([data['X_test'], _ohe.transform(data['yc_test'].reshape(-1, 1))])
        else:
            X_lr = data['X_test']
        y_pred_raw = lr.predict(X_lr)
        # Back-transform if model was trained on log1p(yield)
        lr_meta_path = os.path.join(MODELS_DIR, 'lr_meta.json')
        if os.path.exists(lr_meta_path):
            with open(lr_meta_path) as _f:
                if json.load(_f).get('log_transform'):
                    y_pred_raw = np.expm1(y_pred_raw)
        y_pred    = np.maximum(0, y_pred_raw)
        residuals = data['yr_test'] - y_pred

        from sklearn.metrics import r2_score
        r2 = r2_score(data['yr_test'], y_pred)

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
        fig.suptitle('Linear Regression — Residual Analysis', fontsize=12, fontweight='bold')

        axes[0].scatter(y_pred, residuals, alpha=0.45, color='#e57373',
                        edgecolors='#b71c1c', s=20, linewidths=0.4)
        axes[0].axhline(0, color='black', lw=1.5, ls='--')
        axes[0].set_title('Residual vs Fitted')
        axes[0].set_xlabel('Predicted Yield (t/ha)')
        axes[0].set_ylabel('Residuals')

        mn, mx = float(data['yr_test'].min()), float(data['yr_test'].max())
        axes[1].scatter(data['yr_test'], y_pred, alpha=0.45, color='#42a5f5',
                        edgecolors='#0d47a1', s=20, linewidths=0.4)
        axes[1].plot([mn, mx], [mn, mx], 'r--', lw=1.8, label='Ideal fit')
        axes[1].set_title(f'Predicted vs Actual  (R2 = {r2:.3f})')
        axes[1].set_xlabel('Actual Yield (t/ha)')
        axes[1].set_ylabel('Predicted Yield (t/ha)')
        axes[1].legend(fontsize=9)

        fig.tight_layout()
        self._embed_figure(fig)
        plt.close(fig)

    # ── Tab 3 — About ─────────────────────────────────────────────────────────

    def _build_about_tab(self):
        outer = ttk.Frame(self.nb)
        self.nb.add(outer, text='  About  ')

        about = """
  Smart Agriculture Decision Support System
  ══════════════════════════════════════════════════════════════

  Institution  :  Bahria University, Islamabad Campus
  Department   :  Software Engineering
  Course       :  Artificial Intelligence  |  OEL — CLO-2
  Instructor   :  Engr. Saad Mazhar Khan

  ──────────────────────────────────────────────────────────────
  SYSTEM ARCHITECTURE
  ──────────────────────────────────────────────────────────────

   Data Layer       →  Synthetic dataset  (23 crops, 7 soil/climate features)
                        Preprocessing: median imputation · IQR outlier clipping
                        · StandardScaler · LabelEncoder · 80/20 train-test split

   Model Layer      →  ① Decision Tree Classifier   (crop recommendation)
                        ② K-Means Clustering (k=5)  (soil profile segmentation)
                        ③ Linear Regression         (yield prediction, t/ha)

   Interface Layer  →  Tkinter GUI + embedded Matplotlib (FigureCanvasTkAgg)

  ──────────────────────────────────────────────────────────────
  INPUT FEATURES
  ──────────────────────────────────────────────────────────────

   N          Soil nitrogen content          (kg / ha)
   P          Soil phosphorus content        (kg / ha)
   K          Soil potassium content         (kg / ha)
   Temperature  Ambient temperature          (°C)
   Humidity   Relative humidity              (%)
   pH         Soil pH value                  (0 – 14)
   Rainfall   Annual rainfall                (mm)

  ──────────────────────────────────────────────────────────────
  HOW TO USE
  ──────────────────────────────────────────────────────────────

   1.  Enter soil and climate parameters in the  Input & Prediction  tab.
   2.  Click  ▶ Run Prediction  to receive:
         • Recommended crop (Decision Tree)
         • Soil cluster + agronomic guidance (K-Means)
         • Predicted yield with confidence bounds (Linear Regression)
   3.  Switch to the  Visualizations  tab to explore embedded model plots.

  ──────────────────────────────────────────────────────────────
  REPOSITORY STRUCTURE
  ──────────────────────────────────────────────────────────────

   data/        ·  crop_data.csv  (generated on first run)
   src/         ·  preprocessing.py  models.py  gui.py  utils.py
   models/      ·  serialized .pkl artefacts + metrics.json
   results/     ·  evaluation plots (PNG)
   train_models.py   standalone training script
   main.py           GUI entry point
   requirements.txt  dependency manifest

"""
        txt = scrolledtext.ScrolledText(outer, font=FONT_MONO, bg='#f9fbe7',
                                        fg='#1a237e', relief='flat', wrap='word')
        txt.pack(fill='both', expand=True, padx=14, pady=12)
        txt.insert('end', about)
        txt.configure(state='disabled')


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    app = AgriApp()
    app.mainloop()


if __name__ == '__main__':
    main()
