from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """Base class for cloud provider implementations."""

    @abstractmethod
    def get_region_info(self, region: str) -> dict:
        """
        Get information about a cloud region.

        Args:
            region (str): The region code (e.g., 'us-east-1' for AWS, 'eastus' for Azure)

        Returns:
            dict: A dictionary containing region information with the following keys:
                - location (str): Human-readable location name
                - country (str): Country name
                - flag (str, optional): Unicode flag emoji
                - latitude (float, optional): Geographic latitude
                - longitude (float, optional): Geographic longitude
                - raw (str): Original region code as provided

        Example:
            >>> provider.get_region_info("us-east-1")
            {
                "location": "US East (N. Virginia)",
                "country": "United States",
                "flag": "🇺🇸",
                "latitude": 37.3719,
                "longitude": -79.8164,
                "raw": "us-east-1"
            }
        """
        raise NotImplementedError("Provider must implement get_region_info method")
