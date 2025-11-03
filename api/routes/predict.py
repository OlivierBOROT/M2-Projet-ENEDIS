# api/routes/predict.py
import os
import re
import pickle
import joblib
import pandas as pd
from fastapi import APIRouter, Query, HTTPException
from core.config import settings
from models.schemas import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["Prediction"])

# Default models
DEFAULT_MODELS = {
    "DPE": "DPE_model.pkl",
    "CONSO": "CONSO_model.pkl"
}
def preprocess_input(data: PredictionRequest, prediction_type="DPE"):
    df = pd.DataFrame([data.dict()])

    # Fill missing values
    for col in df.columns:
        if df[col].dtype in ["float64","int64"]:
            df[col] = df[col].fillna(df[col].mean())
        else:
            df[col] = df[col].fillna("non spécifié")

    # Categorical columns for one-hot encoding
    if prediction_type=="DPE":
        categorical_cols = [
            'qualite_isolation_murs',
            'type_batiment',
            'type_installation_ecs',
            'type_energie_principale_chauffage',
            'qualite_isolation_plancher_bas',
            'type_installation_chauffage',
            'type_generateur_n1_ecs_n1',
            'type_generateur_chauffage_principal',
            'periode_construction'
        ]
    else:  # CONSO
        categorical_cols = [
            'qualite_isolation_murs',
            'type_batiment',
            'type_installation_ecs',
            'type_energie_principale_chauffage',
            'qualite_isolation_plancher_bas',
            'type_installation_chauffage',
            'type_generateur_n1_ecs_n1',
            'type_generateur_chauffage_principal',
            'periode_construction',
            'code_postal_ban'
        ]

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df_encoded

@router.post("/", response_model=PredictionResponse)
async def predict(
    data: PredictionRequest,
    prediction_type: str = Query("DPE", description="DPE or CONSO"),
    model_name: str = Query(None, description="Optional model filename")
):
    # ---------------------
    # Validate inputs
    # ---------------------
    prediction_type = prediction_type.upper()
    if prediction_type not in DEFAULT_MODELS:
        raise HTTPException(status_code=400, detail="prediction_type must be 'DPE' or 'CONSO'")

    # Determine model
    model_name = model_name or DEFAULT_MODELS[prediction_type]
    if not model_name.endswith(".pkl") and not model_name.endswith(".joblib"):
        model_name += ".pkl"

    if not re.fullmatch(r"[A-Za-z0-9_\-\.]+", model_name):
        raise HTTPException(status_code=400, detail="Invalid model name")
    model_name = os.path.basename(model_name)

    # Load model
    model_path = os.path.join(settings.LOCAL_MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
    try:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

    # -----------------------
    # Preprocess input
    # -----------------------
    df_input = preprocess_input(data, prediction_type)

    # ---------------------
    # Fill missing columns if model expects them
    # ---------------------
    if hasattr(model, "get_booster"):
        model_features = model.get_booster().feature_names
        for col in model_features:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[model_features]  # Ensure correct order

    # ---------------------
    # Predict
    # ---------------------
    try:
        y_pred = model.predict(df_input)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Decode DPE labels if multi-class
    if prediction_type=="DPE" and hasattr(model, "classes_"):
        y_pred = model.classes_[y_pred] if isinstance(y_pred,int) else y_pred

    return {
        "status":"success",
        "prediction_type": prediction_type,
        "model_used": model_name,
        "prediction": y_pred
    }
