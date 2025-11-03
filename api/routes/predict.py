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

# Example: DPE model features (one-hot columns)
# Replace these with the exact columns from your trained model X.columns
DPE_FEATURES = [
    "surface_habitable_logement", "hauteur_sous_plafond", "nombre_niveau_logement",
    "qualite_isolation_murs_Très bonne", "qualite_isolation_murs_Bonne", "qualite_isolation_murs_Moyenne",
    "qualite_isolation_plancher_bas_Très bonne", "qualite_isolation_plancher_bas_Bonne", "qualite_isolation_plancher_bas_Moyenne",
    "isolation_toiture_Oui",
    "type_batiment_maison",
    "type_installation_ecs_individuel",
    "type_installation_chauffage_individuel",
    "type_energie_principale_chauffage_Électricité",
    "type_generateur_n1_ecs_n1_boiler",
    "type_generateur_chauffage_principal_gaz",
    "periode_construction_Avant 1960",
    "periode_construction_1961-1970",
    "periode_construction_1971-1980",
    "periode_construction_1981-1990",
    "periode_construction_1991-2000",
    "periode_construction_2001-2010",
    "periode_construction_Après 2010"
]

# Example: CONSO numeric features
CONSO_FEATURES = [
    "surface_habitable_logement", "hauteur_sous_plafond", "nombre_niveau_logement",
    "qualite_isolation_murs", "qualite_isolation_plancher_bas",
    "type_batiment", "type_installation_ecs", "type_installation_chauffage",
    "type_energie_principale_chauffage", "type_generateur_n1_ecs_n1",
    "type_generateur_chauffage_principal", "isolation_toiture",
    "periode_construction", "code_postal_ban"
]

# Ordinal mappings
ISOLATION_MAP = {"Très bonne":3, "Bonne":2, "Moyenne":1, "Insuffisante":0}
TOITURE_MAP = {"Oui":1, "Non":0}
TYPE_LOGEMENT_MAP = {"Maison":1, "Appartement":0}
YES_NO_MAP = {"Oui":1, "Non":0}

# Periode construction mapping
PERIODE_MAP = {
    "Avant 1960":0, "1961-1970":1, "1971-1980":2, "1981-1990":3,
    "1991-2000":4, "2001-2010":5, "Après 2010":6
}

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
    ext = os.path.splitext(model_path)[1].lower()
    try:
        if ext == ".pkl":
            with open(model_path, "rb") as f:
                model = pickle.load(f)
        elif ext == ".joblib":
            model = joblib.load(model_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported model format: {ext}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

    # ---------------------
    # Build input vector
    # ---------------------
    if prediction_type == "DPE":
        # One-hot encoded for DPE
        input_dict = {}

        # Numeric
        input_dict["surface_habitable_logement"] = data.surface
        input_dict["hauteur_sous_plafond"] = data.hauteur_sous_plafond
        input_dict["nombre_niveau_logement"] = data.nombre_niveau_logement

        # Isolation murs
        for val in ["Très bonne", "Bonne", "Moyenne"]:
            input_dict[f"qualite_isolation_murs_{val}"] = 1 if data.qualite_isolation_murs==val else 0

        # Isolation plancher
        for val in ["Très bonne", "Bonne", "Moyenne"]:
            input_dict[f"qualite_isolation_plancher_bas_{val}"] = 1 if data.isolation_plancher==val else 0

        # Isolation toiture
        input_dict["isolation_toiture_Oui"] = 1 if data.isolation_toiture=="Oui" else 0

        # Type logement
        input_dict["type_batiment_maison"] = 1 if data.type_logement=="Maison" else 0

        # Installation ECS
        input_dict["type_installation_ecs_individuel"] = 1 if data.type_ecs=="Individuel" else 0

        # Installation chauffage
        input_dict["type_installation_chauffage_individuel"] = 1 if data.type_chauffage=="Individuel" else 0

        # Energie principale
        input_dict["type_energie_principale_chauffage_Électricité"] = 1 if data.energie_chauffage=="Électricité" else 0

        # Generateur ECS principal (example mapping)
        input_dict["type_generateur_n1_ecs_n1_boiler"] = 1 if "boiler" in data.type_generateur_ecs.lower() else 0

        # Generateur chauffage principal (example mapping)
        input_dict["type_generateur_chauffage_principal_gaz"] = 1 if "gaz" in data.type_generateur_chauffage.lower() else 0

        # Periode construction
        for val in ["Avant 1960","1961-1970","1971-1980","1981-1990","1991-2000","2001-2010","Après 2010"]:
            input_dict[f"periode_construction_{val}"] = 1 if data.annee_construction==val else 0

        df_input = pd.DataFrame([input_dict], columns=DPE_FEATURES)

    else:
        # CONSO numeric features
        df_input = pd.DataFrame([{
            "surface_habitable_logement": data.surface,
            "hauteur_sous_plafond": data.hauteur_sous_plafond,
            "nombre_niveau_logement": data.nombre_niveau_logement,
            "qualite_isolation_murs": ISOLATION_MAP.get(data.qualite_isolation_murs,0),
            "qualite_isolation_plancher_bas": ISOLATION_MAP.get(data.isolation_plancher,0),
            "type_batiment": TYPE_LOGEMENT_MAP.get(data.type_logement,0),
            "type_installation_ecs": 1 if data.type_ecs=="Individuel" else 0,
            "type_installation_chauffage": 1 if data.type_chauffage=="Individuel" else 0,
            "type_energie_principale_chauffage": 1 if data.energie_chauffage=="Électricité" else 0,
            "type_generateur_n1_ecs_n1": 1 if "boiler" in data.type_generateur_ecs.lower() else 0,
            "type_generateur_chauffage_principal": 1 if "gaz" in data.type_generateur_chauffage.lower() else 0,
            "isolation_toiture": TOITURE_MAP.get(data.isolation_toiture,0),
            "periode_construction": PERIODE_MAP.get(data.annee_construction,0),
            "code_postal_ban": str(data.code_postal) if hasattr(data,"code_postal") else 0
        }], columns=CONSO_FEATURES)

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
