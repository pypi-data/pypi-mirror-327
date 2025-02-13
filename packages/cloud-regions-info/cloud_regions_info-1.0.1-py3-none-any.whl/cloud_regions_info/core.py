from .providers import get_provider

def get_region_info(provider: str, region: str) -> dict:
    """
    Retrieve region info in the format:
    {
      "location": str,
      "flag": str,
      "country": str,
      "latitude": float,
      "longitude": float,
      "raw": str
    }
    
    :param provider: name of the provider (e.g. "AWS")
    :param region: region code (e.g. "eu-north-1")
    :return: dict of region information
    """
    provider_instance = get_provider(provider)
    return provider_instance.get_region_info(region)
