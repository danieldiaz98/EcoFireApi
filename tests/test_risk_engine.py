from app.schemas.weather import WeatherData
from app.services.risk_engine import check_30_30_30_rule, calculate_score, get_risk_level, get_recommendation
from app.services.risk_engine import _get_temperature_score, _get_humidity_score, _get_wind_score

def test_check_30_30_30_rule_active():
    weather = WeatherData(
        temperature=35.0,
        humidity_percent=20.0,
        wind_speed=35.0
    )
    assert check_30_30_30_rule(weather) is True

def test_temperature_score():
    temperature = 30.0
    temperature_score = _get_temperature_score(temperature)

    expected_temperature_score = 39.33
    
    assert temperature_score == expected_temperature_score

def test_humidity_score():
    humidity = 20.0
    humidity_score = _get_humidity_score(humidity)

    expected_humidity_score = 30.0

    assert humidity_score == expected_humidity_score

def test_wind_score():
    wind = 40.0
    wind_score = _get_wind_score(wind)

    expected_wind_score = 25.0

    assert wind_score == expected_wind_score

def test_calculate_score_with_rule_30_active():
    weather = WeatherData(
        temperature=35.0,
        humidity_percent=20.0,
        wind_speed=40.0
    )
    rule_30_active = True
    score = calculate_score(weather, rule_30_active)

    expected_score = 85.0

    assert score == expected_score

def test_calculate_score_without_rule_30_not_active():
    weather = WeatherData(
        temperature=25.0,
        humidity_percent=40.0,
        wind_speed=20.0
    )
    rule_30_active = False
    score = calculate_score(weather, rule_30_active)

    expected_score = 35.0

    assert score == expected_score