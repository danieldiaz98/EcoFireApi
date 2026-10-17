from app.schemas.location import CoordinateRequest
from app.schemas.risk import RiskLevel
from app.schemas.fire_risk_response import FireRiskResponse
from app.schemas.weather import WeatherData


def check_30_30_30_rule(weather: WeatherData) -> bool:
    return (
        weather.temperature >= 30.0
        and weather.humidity_percent <= 30.0
        and weather.wind_speed >= 30.0
    )


def _get_temperature_score(temp: float) -> float:
    raw = (temp - 15.0) * 1.4 
    return max(0.0, min(35.0, raw))

def _get_humidity_score(humidity: float) -> float:
    raw = (80.0 - humidity) * 0.5
    return max(0.0, min(35.0, raw))

def _get_wind_score(wind: float) -> float:
    raw = (wind - 5.0) * (30.0 / 45.0)
    return max(0.0, min(30.0, raw))


def calculate_score(weather: WeatherData, rule_30_active: bool) -> float:
    temperature_score = _get_temperature_score(weather.temperature)
    humidity_score = _get_humidity_score(weather.humidity_percent)
    wind_score = _get_wind_score(weather.wind_speed)

    total = temperature_score + humidity_score + wind_score

    if rule_30_active:
        return max(85.0, round(total, 2))
    
    return round(total, 2)


def get_risk_level(score: float) -> RiskLevel:
    if score < 25.0:
        return RiskLevel.LOW
    elif score < 50.0:
        return RiskLevel.MODERATE
    elif score < 70.0:
        return RiskLevel.HIGH
    elif score < 85.0:
        return RiskLevel.VERY_HIGH
    else:
        return RiskLevel.EXTREME


def get_recommendation(level: RiskLevel, rule_30_active: bool) -> str:
    if rule_30_active:
        return "ALERTA MÁXIMA: Se cumple la regla del 30-30-30. Prohibición absoluta de fuegos, maquinaria y actividades de riesgo en monte."
    
    recommendations = {
        RiskLevel.LOW: "Riesgo bajo. Condiciones normales de prevención.",
        RiskLevel.MODERATE: "Riesgo moderado. Mantener precaución en zonas forestales y evitar arrojar colillas o basura.",
        RiskLevel.HIGH: "Riesgo alto. Restricción de quemas agrícolas y extremar precauciones en uso de barbacoas.",
        RiskLevel.VERY_HIGH: "Riesgo muy alto. Prohibición de quemas agrícolas y uso de maquinaria pirotécnica o cortacéspedes en zonas de monte.",
        RiskLevel.EXTREME: "Riesgo extremo. Prohibición total de acceso a zonas forestales y uso de fogones."
    }
    return recommendations.get(level, "Precaución general.")


async def calculate_fire_risk(location: CoordinateRequest, weather: WeatherData) -> FireRiskResponse:
    rule_30 = check_30_30_30_rule(weather)
    score = calculate_score(weather, rule_30)
    level = get_risk_level(score)
    recommendation = get_recommendation(level, rule_30)
    
    return FireRiskResponse(
        location=location,
        risk_score=score,
        risk_level=level,
        rule_30_active=rule_30,
        weather=weather,
        recommendation=recommendation
    )