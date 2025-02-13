import os
import json
from .base import BaseProvider
from ..models import RegionInfo

class DigitalOceanProvider(BaseProvider):
    """Provider implementation for DigitalOcean."""
    
    def __init__(self):
        """
        Initialize DigitalOcean provider with region data.
        Loads region information from the digitalocean_regions.json mapping file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "mappings", "digitalocean_regions.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.region_data = json.load(f)

    def get_region_info(self, region: str) -> dict:
        """
        Get information about a DigitalOcean region.

        Args:
            region (str): DigitalOcean region code (e.g., 'nyc1', 'ams3')

        Returns:
            dict: Region information containing:
                - location (str): Human-readable location (e.g., "New York City")
                - country (str): Country name (e.g., "United States")
                - flag (str, optional): Unicode flag emoji (e.g., "🇺🇸")
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code

        Example:
            >>> get_region_info("nyc1")
            {
                "location": "New York City",
                "country": "United States",
                "flag": "🇺🇸",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "raw": "nyc1"
            }
        """
        region_key = region.lower().replace(" ", "")
        info = self.region_data.get(region_key, {})
        
        if not info:
            model = RegionInfo(
                location="Unknown",
                country="Unknown",
                raw=region
            )
            return model.dict()
            
        model = RegionInfo(
            location=info.get("location", "Unknown"),
            flag=info.get("flag", None),
            country=info.get("country", "Unknown"),
            latitude=info.get("latitude", None),
            longitude=info.get("longitude", None),
            raw=region
        )
        return model.dict() 