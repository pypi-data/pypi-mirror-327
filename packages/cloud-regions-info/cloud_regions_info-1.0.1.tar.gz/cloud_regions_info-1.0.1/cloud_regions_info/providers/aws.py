import os
import json
from .base import BaseProvider
from ..models import RegionInfo

class AWSProvider(BaseProvider):
    """Provider implementation for Amazon Web Services (AWS)."""

    def __init__(self):
        """
        Initialize AWS provider with region data.
        Loads region information from the aws_regions.json mapping file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "mappings", "aws_regions.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.region_data = json.load(f)

    def get_region_info(self, region: str) -> dict:
        """
        Get information about an AWS region.

        Args:
            region (str): AWS region code (e.g., 'us-east-1', 'eu-west-1')

        Returns:
            dict: Region information containing:
                - location (str): Human-readable location (e.g., "US East (N. Virginia)")
                - country (str): Country name (e.g., "United States")
                - flag (str, optional): Unicode flag emoji (e.g., "🇺🇸")
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code

        Example:
            >>> get_region_info("us-east-1")
            {
                "location": "US East (N. Virginia)",
                "country": "United States",
                "flag": "🇺🇸",
                "latitude": 37.3719,
                "longitude": -79.8164,
                "raw": "us-east-1"
            }
        """
        info = self.region_data.get(region, {})
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
