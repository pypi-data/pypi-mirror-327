import os
import json
from .base import BaseProvider
from ..models import RegionInfo

class OneDriveProvider(BaseProvider):
    """Provider implementation for Microsoft OneDrive."""
    
    def __init__(self):
        """
        Initialize OneDrive provider with region data.
        Loads region information from the onedrive_regions.json mapping file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "mappings", "onedrive_regions.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.region_data = json.load(f)

    def get_region_info(self, region: str) -> dict:
        """
        Get information about a OneDrive region.

        Args:
            region (str): OneDrive region code (e.g., 'nam', 'eur', 'gbr')

        Returns:
            dict: Region information containing:
                - location (str): Human-readable location (e.g., "North America")
                - country (str): Country name (e.g., "United States")
                - flag (str, optional): Unicode flag emoji (e.g., "🇺🇸")
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code

        Example:
            >>> get_region_info("eur")
            {
                "location": "Europe",
                "country": "European Union",
                "flag": "🇪🇺",
                "latitude": 50.8503,
                "longitude": 4.3517,
                "raw": "eur"
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