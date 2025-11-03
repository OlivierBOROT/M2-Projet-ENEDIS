from pydantic import BaseModel
from typing import Union

class PredictionRequest(BaseModel):
    qualite_isolation_murs: str
    type_batiment: str
    type_installation_ecs: str
    type_energie_principale_chauffage: str
    qualite_isolation_plancher_bas: str
    type_installation_chauffage: str
    surface_habitable_logement: float
    hauteur_sous_plafond: float
    nombre_niveau_logement: float
    isolation_toiture: int
    type_generateur_n1_ecs_n1: str
    type_generateur_chauffage_principal: str
    periode_construction: str
    code_postal_ban: int

class PredictionResponse(BaseModel):
    status: str
    prediction_type: str
    model_used: str
    prediction: Union[str, float]
