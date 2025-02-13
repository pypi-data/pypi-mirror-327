import os
import json
from .base import BaseProvider
from ..models import RegionInfo

class OCIProvider(BaseProvider):
    """Provider implementation for Oracle Cloud Infrastructure (OCI)."""
    
    def __init__(self):
        """
        Initialize OCI provider with region data.
        Loads region information from the oci_regions.json mapping file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "mappings", "oci_regions.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.region_data = json.load(f)

    def get_region_info(self, region: str) -> dict:
        """
        Get information about an OCI region.

        Args:
            region (str): OCI region code (e.g., 'us-ashburn-1', 'eu-frankfurt-1')

        Returns:
            dict: Region information containing:
                - location (str): Human-readable location (e.g., "Ashburn, VA")
                - country (str): Country name (e.g., "United States")
                - flag (str, optional): Unicode flag emoji (e.g., "🇺🇸")
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code

        Example:
            >>> get_region_info("us-ashburn-1")
            {
                "location": "Ashburn, VA",
                "country": "United States",
                "flag": "🇺🇸",
                "latitude": 39.0438,
                "longitude": -77.4874,
                "raw": "us-ashburn-1"
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