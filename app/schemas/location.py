from pydantic import BaseModer, Field

class CoordinateRequest (BaseModel):
    latitude: float = Field(ge= 27.5, le= 29.5, description="Latitude must be between 27.5 and 29.5")
    longitude: float = Field(ge=-18.5, le=-13.0, description="Longitude must be between -18.5 and -13.0")