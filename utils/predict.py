import os
import joblib
import pandas as pd

# Get the parent directory
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load models using relative path from the parent
dt_model = joblib.load(os.path.join(PARENT_DIR, 'model', 'wine_quality_dt_model.pkl'))
rf_model = joblib.load(os.path.join(PARENT_DIR, 'model', 'wine_quality_rf_model.pkl'))


def predict_wine_quality_hybrid(input_data, rf_conf_thresh=0.8, dt_conf_thresh_minor=0.4):
    feature_order = ['Alc', 'Cl', 'TSO2', 'VA', 'FSO2', 'FA']

    input_df = pd.DataFrame([input_data])
    
    # Reorder columns to match training features
    print("Input DataFrame columns:", input_df.columns.tolist())
    input_df = input_df[feature_order]
    
    # Random Forest predictions
    rf_probs = rf_model.predict_proba(input_df)[0]
    rf_pred = rf_model.predict(input_df)[0]
    rf_conf = rf_probs[rf_pred]
    
    # Decision Tree predictions
    dt_probs = dt_model.predict_proba(input_df)[0]
    dt_pred = dt_model.predict(input_df)[0]
    dt_conf = dt_probs[dt_pred]

    # Hybrid Decision Logic
    if rf_pred == 1 and rf_conf >= rf_conf_thresh:
        final_pred = rf_pred  # Trust RF on medium class with high confidence
    elif dt_pred in [0, 2] and dt_conf >= dt_conf_thresh_minor:
        final_pred = dt_pred  # Trust DT on minority classes with good confidence
    else:
        final_pred = rf_pred  # Default to Random Forest prediction

    return final_pred, rf_conf, dt_conf

