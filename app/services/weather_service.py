import asyncio
import httpx
from fastapi import HTTPException
from app.schemas.location import Location
from app.schemas.weather import WeatherData

async def fetch_weather_data(lat: float, long: float):
    location = Location(latitude=lat, longitude=long)
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Weather data not found")
    data = response.json()
    data.get("current")
    weather_data = WeatherData(
        temperature=data["current"]["temperature_2m"],
        humidity_percent=data["current"]["relative_humidity_2m"],
        wind_speed=data["current"]["wind_speed_10m"]
    )
    return weather_data
