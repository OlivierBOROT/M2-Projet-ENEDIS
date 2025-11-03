# api/models/schema.py
from pydantic import BaseModel
from typing import Optional

# api/models/schemas.py
from pydantic import BaseModel
from typing import Optional

class PredictionRequest(BaseModel):
    # Logement
    type_logement: str
    surface: float
    code_postal: Optional[str] = None  # only needed for CONSO
    annee_construction: str
    nombre_niveau_logement: int
    hauteur_sous_plafond: float
    isolation_toiture: str
    isolation_plancher: str
    qualite_isolation_murs: str

    # Installations énergétiques
    type_chauffage: str
    energie_chauffage: str
    type_ecs: str
    type_generateur_chauffage: str
    type_generateur_ecs: str


class PredictionResponse(BaseModel):
    status: str
    data: dict

class ModelUploadResponse(BaseModel):
    status: str
    message: str
