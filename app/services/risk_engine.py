from app.schemas import weather


def check_30_30_30_rule(weather: WeatherData) -> bool:
    if weather.Temperature > 30 and weather.humidity_percent < 30 and weather.wind_speed > 30:
        return True