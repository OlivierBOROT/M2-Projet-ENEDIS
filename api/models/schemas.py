# api/models/schema.py
from pydantic import BaseModel
from typing import Optional

class PredictionRequest(BaseModel):
    type_logement: str
    surface: float
    code_postal: str
    commune: str
    type_chauffage: str
    energie_chauffage: str

class PredictionResponse(BaseModel):
    status: str
    data: dict

class ModelUploadResponse(BaseModel):
    status: str
    message: str
