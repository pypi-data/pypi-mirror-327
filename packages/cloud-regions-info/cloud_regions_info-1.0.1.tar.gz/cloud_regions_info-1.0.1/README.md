# Cloud Regions Info

A Python package that provides detailed information about cloud regions across different cloud providers.

[![PyPI version](https://badge.fury.io/py/cloud-regions-info.svg)](https://badge.fury.io/py/cloud-regions-info)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🌍 **Region Information Lookup**: Pass any cloud region code and provider name to get detailed geographic information:
  ```python
  get_region_info(provider="aws", region="eu-north-1")
  ```

- 📍 **Comprehensive Region Details**: For each region, get:
  - Human-readable location name (e.g., "Europe (Stockholm)")
  - Country information with flag emoji (e.g., "Sweden 🇸🇪")
  - Precise geographic coordinates (latitude/longitude)
  - Original region code as used by the provider

- 🔍 **Simple and Intuitive API**: Single function call to get all region details
  ```python
  region_info.location    # "Europe (Stockholm)"
  region_info.country    # "Sweden"
  region_info.flag       # "🇸🇪"
  region_info.latitude   # 59.3293
  region_info.longitude  # 18.0686
  region_info.raw        # "eu-north-1"
  ```

## Installation

Install using pip:
```bash
pip install cloud-regions-info
```

Or with Poetry:
```bash
poetry add cloud-regions-info
```

## Usage

```python
from cloud_regions_info import get_region_info

region_info = get_region_info(provider="aws", region="eu-north-1")

# Access region information
print(region_info.location)    # Europe (Stockholm)
print(region_info.flag)        # 🇸🇪
print(region_info.country)     # Sweden
print(region_info.latitude)    # 59.3293
print(region_info.longitude)   # 18.0686
print(region_info.raw)         # eu-north-1
```
## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ditikrushna/cloud-regions-info.git
cd cloud-regions-info
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Run tests:
```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`poetry run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Areas for Contribution

- Expanding Azure and GCP support
- Adding more region information
- Improving documentation
- Adding new cloud providers
- Bug fixes and improvements

## Data Sources

The region information is sourced from:
- AWS: Official AWS documentation and APIs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/cloud-regions-info/issues) page
2. Create a new issue if your problem isn't already listed

## Project Status

### Cloud Providers
| Provider | Status | Implementation |
|----------|--------|----------------|
| AWS      | ✅     | Complete       |
| Azure    | ✅     | Complete       |
| GCP      | ✅     | Complete       |
| Oracle Cloud | ✅  | Complete      |
| DigitalOcean | ✅  | Complete      |
| IBM Cloud    | ✅  | Complete      |
| Alibaba Cloud| ✅  | Complete      |
| Vultr        | ✅  | Complete      |

### SaaS Applications
| Application | Status | Implementation |
|-------------|--------|----------------|
| Microsoft 365 | 🚧   | In Progress    |
| - OneDrive   | ✅   | Complete       |
| - SharePoint | 📅   | Planned        |
| - Teams      | 📅   | Planned        |
| Atlassian    | 📅   | Planned        |
| - Jira       | 📅   | Planned        |
| - Confluence | 📅   | Planned        |
| Salesforce   | 📅   | Planned        |
| ServiceNow   | 📅   | Planned        |
| Workday      | 📅   | Planned        |

Status Legend:
- ✅ Complete
- 🚧 In Progress
- 📅 Planned
- ❌ Not Started

Made with ❤️ by [Ditikrushna Giri](https://ditikrushna.xyz/)
