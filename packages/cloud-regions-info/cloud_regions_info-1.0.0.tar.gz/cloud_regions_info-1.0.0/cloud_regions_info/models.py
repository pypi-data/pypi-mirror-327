from pydantic import BaseModel, Field
from typing import Optional

class RegionInfo(BaseModel):
    location: str = Field(..., description="Human-readable location name, e.g. 'Europe (Stockholm)'")
    flag: Optional[str] = Field(None, description="Unicode flag emoji, e.g. '🇸🇪'")
    country: str = Field(..., description="Country name, e.g. 'Sweden'")
    latitude: Optional[float] = Field(None, description="Approximate latitude")
    longitude: Optional[float] = Field(None, description="Approximate longitude")
    raw: str = Field(..., description="The raw region code, e.g. 'eu-north-1'")
