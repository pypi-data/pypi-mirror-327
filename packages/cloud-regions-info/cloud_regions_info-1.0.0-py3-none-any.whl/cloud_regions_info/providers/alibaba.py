import os
import json
from .base import BaseProvider
from ..models import RegionInfo

class AlibabaProvider(BaseProvider):
    """Provider implementation for Alibaba Cloud (Aliyun)."""
    
    def __init__(self):
        """
        Initialize Alibaba Cloud provider with region data.
        Loads region information from the alibaba_regions.json mapping file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "mappings", "alibaba_regions.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.region_data = json.load(f)

    def get_region_info(self, region: str) -> dict:
        """
        Get information about an Alibaba Cloud region.

        Args:
            region (str): Alibaba Cloud region code (e.g., 'cn-hangzhou', 'ap-southeast-1')

        Returns:
            dict: Region information containing:
                - location (str): Human-readable location (e.g., "Hangzhou")
                - country (str): Country name (e.g., "China")
                - flag (str, optional): Unicode flag emoji (e.g., "🇨🇳")
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code

        Example:
            >>> get_region_info("cn-hangzhou")
            {
                "location": "Hangzhou",
                "country": "China",
                "flag": "🇨🇳",
                "latitude": 30.2741,
                "longitude": 120.1551,
                "raw": "cn-hangzhou"
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