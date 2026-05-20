import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_COLS = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

FEATURE_RANGES = {
    'N':           (0,   140, 'Nitrogen (kg/ha)'),
    'P':           (5,   145, 'Phosphorus (kg/ha)'),
    'K':           (5,   205, 'Potassium (kg/ha)'),
    'temperature': (8,    44, 'Temperature (°C)'),
    'humidity':    (14,  100, 'Humidity (%)'),
    'ph':          (3.5, 9.9, 'Soil pH'),
    'rainfall':    (20,  300, 'Rainfall (mm)'),
}

FEATURE_DEFAULTS = {
    'N': 90, 'P': 42, 'K': 43,
    'temperature': 21, 'humidity': 82,
    'ph': 6.5, 'rainfall': 202,
}

CLUSTER_GUIDANCE = {
    0: ("High-Fertility Zone",
        "Rich in NPK with optimal moisture. Ideal for high-yield cereals (wheat, rice) "
        "and cash crops. Maintain soil organic matter with periodic compost application."),
    1: ("Acidic Sandy Zone",
        "Low pH and poor water retention. Lime application (2–4 t/ha) recommended. "
        "Suitable for acid-tolerant legumes (groundnut, soybean). Drip irrigation advised."),
    2: ("Moderate Loam Zone",
        "Balanced nutrient profile with good drainage. Versatile for most crops including "
        "vegetables and pulses. Minimal corrective intervention needed."),
    3: ("Alkaline Clay Zone",
        "High pH and dense clay texture. Gypsum treatment (3–5 t/ha) improves structure. "
        "Well-suited for paddy and sugarcane. Avoid over-irrigation."),
    4: ("Nutrient-Deficient Zone",
        "Low NPK reserves require targeted fertilization. Start with nitrogen-fixing cover "
        "crops (clover, lucerne). Micro-nutrient foliar sprays recommended."),
}


def validate_inputs(values: dict):
    """Return (True, None) on success or (False, message) on failure."""
    for key, val in values.items():
        lo, hi, label = FEATURE_RANGES[key]
        if not (lo <= val <= hi):
            return False, f"{label} must be between {lo} and {hi}."
    return True, None


def format_report(crop: str, cluster_id: int, yield_pred: float) -> str:
    zone_name, guidance = CLUSTER_GUIDANCE.get(
        cluster_id, ("Unknown Zone", "No guidance available.")
    )
    conf_lo = max(0.0, yield_pred - 0.5)
    conf_hi = yield_pred + 0.5
    lines = [
        "=" * 55,
        "     AGRICULTURAL INTELLIGENCE REPORT",
        "=" * 55,
        "",
        f"  Recommended Crop  :  {crop.upper()}",
        f"  Soil Cluster      :  {cluster_id + 1} — {zone_name}",
        f"  Agronomic Guidance:  {guidance[:52]}",
        f"                       {guidance[52:]} " if len(guidance) > 52 else "",
        f"  Predicted Yield   :  {yield_pred:.2f} tonnes / hectare",
        f"  Confidence Range  :  {conf_lo:.2f} – {conf_hi:.2f}  t/ha",
        "",
        "=" * 55,
    ]
    return "\n".join(lines)
