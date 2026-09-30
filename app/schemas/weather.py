from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    temperature: float = Field(
        ...,
        description="Temperature in Celsius")
    humidity_percent: float = Field(
        ...,
        ge = 0.0,
        le = 100.0,
        description = "Relative humidity in percentage (0-100%)"
    )
    wind_speed: float = Field(
        ...,
        ge = 0.0,
        description = "Wind Speed around 10 meters measures in km/h"
    )