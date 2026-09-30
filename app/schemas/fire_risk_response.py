from pydantic import BaseModel, Field
from app.schemas.risk import Risklevel
from app.schemas.weather import WeatherData

class FireRiskResponse(BaseModel):
    location: CoordinateRequest = Field(
        ...,
        description = "Geographical coordinates evaluated in Canarias"
    )
    risk_score: float = Field(
        ...,
        ge = 0.0,
        le = 100.0,
        description = "Accumulate fire risk score (0-100)"
    )
    risk_level: RiskLevel = Field(
        ...,
        description = "Cualitative fire risk level"
    )
    rule_30_active: bool = Field(
        ..., 
        description="Validates critical rule 30-30-30"
    )
    weather: WeatherData = Field(
        ..., 
        description="Current weather data for the location"
    )
    recommendation: str = Field(
        ..., 
        description="Recommendations or alerts for prevention and safety"
    )