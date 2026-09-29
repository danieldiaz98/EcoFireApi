from  fastapi import FastAPI
from app.schemas.location import CoordinateRequest

app = FastAPI()

@app.post("/api/v1/risk/check")
async def check_location_validity(coordinate: CoordinateRequest):
    return {"status": "valid", "lat": coordinate.latitude, "lon": coordinate.longitude}