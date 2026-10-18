from app.schemas.weather import WeatherData
from app.services.risk_engine import check_30_30_30_rule, calculate_score, get_risk_level, get_recommendation

def test_check_30_30_30_rule_active():
    weather = WeatherData(
        temperature=35.0,
        humidity_percent=20.0,
        wind_speed=35.0
    )
    assert check_30_30_30_rule(weather) is True

def test_temperature_score():
    temperature = 30.0

    score = calculate_score(WeatherData(temperature=temperature, humidity_percent=50.0, wind_speed=10.0), rule_30_active=False)
    
    assert score == 39.33
