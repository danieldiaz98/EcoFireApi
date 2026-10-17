from fastapi import FastAPI

from app.schemas.fire_risk_response import FireRiskResponse
from app.schemas.risk import RiskLevel
from app.schemas.location import CoordinateRequest
from app.services.risk_engine import calculate_fire_risk
from app.services.weather_service import fetch_weather_data

app = FastAPI(
    title="EcoFire API",
    description="API para el cálculo de índice de riesgo de incendios en Canarias",
    version="1.0.0"
)

@app.post("/api/v1/risk/check_location")
async def check_location_validity(coordinate: CoordinateRequest):
    return {"status": "valid", "lat": coordinate.latitude, "lon": coordinate.longitude}

@app.post("/api/v1/risk/fire_risk", response_model=FireRiskResponse)
async def fire_risk_assessment(location: CoordinateRequest):
    weather = await fetch_weather_data(location.latitude, location.longitude)
    return await calculate_fire_risk(location, weather)