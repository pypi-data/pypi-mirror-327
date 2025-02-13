"""
cloud_regions_info
~~~~~~~~~~~~~~~~~~

A Python package for retrieving cloud region information.
"""

__version__ = "0.1.0"

from .core import get_region_info
from .providers.aws import AWSProvider
from .providers.azure import AzureProvider
from .providers.gcp import GCPProvider
from .providers.oci import OCIProvider
from .providers.digitalocean import DigitalOceanProvider
from .providers.ibm import IBMProvider
from .providers.alibaba import AlibabaProvider
from .providers.vultr import VultrProvider
from .providers.onedrive import OneDriveProvider

PROVIDER_MAP = {
    "aws": AWSProvider,
    "azure": AzureProvider,
    "gcp": GCPProvider,
    "oci": OCIProvider,
    "digitalocean": DigitalOceanProvider,
    "ibm": IBMProvider,
    "alibaba": AlibabaProvider,
    "vultr": VultrProvider,
    "onedrive": OneDriveProvider
}

def get_provider(provider_name: str):
    """Get the provider class for a given provider name."""
    key = provider_name.strip().lower()
    if key not in PROVIDER_MAP:
        raise ValueError(f"Provider '{provider_name}' is not supported")
    return PROVIDER_MAP[key]()
