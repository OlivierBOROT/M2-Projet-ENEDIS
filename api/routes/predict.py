# api/routes/predict.py
import re
import os
import pickle
import joblib
from fastapi import APIRouter, Query, HTTPException

from core.config import settings
from models.schemas import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["Prediction"])

# Default model filename
DEFAULT_MODEL = "default_model.pkl"

@router.post("/", response_model=PredictionResponse)
async def predict(
    data: PredictionRequest,
    model_name: str = Query(DEFAULT_MODEL, description="Model filename to use")
):
    """Run prediction using the specified or default model."""

    # make sur e that model_name is a good thing and not an attack
    try:
        # Allow only letters, numbers, underscores, dashes, and dots
        if not re.fullmatch(r"[A-Za-z0-9_\-\.]+", model_name):
            raise ValueError("Invalid model name")
        # Prevent path traversal
        model_name = os.path.basename(model_name)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid model name")

    # Determine model path (local or S3 not implemented yet)
    if settings.USE_S3:
        # Here you would fetch the model from S3
        raise NotImplementedError("S3 model loading not implemented yet")
    else:
        model_path = os.path.join(settings.LOCAL_MODEL_DIR, model_name)
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found locally")

    # Load model based on extension
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

    # Convert input to feature vector (example — adjust for your model)
    features = [
        1 if data.type_logement.lower() == "maison" else 0,
        data.surface,
        # to do: add other fields and preprocessing here
    ]

    # Run prediction
    try:
        prediction = model.predict([features])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Return raw input + model used + prediction
    return {
        "status": "success",
        "model_used": model_name,
        "prediction": prediction
    }
