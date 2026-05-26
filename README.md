# InfraDocs Generator

> Generate beautiful, static IT infrastructure documentation websites from YAML, JSON, and CSV files.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)]()

## Features

- **Multiple Input Formats** — Reads YAML, JSON, and CSV files
- **Beautiful HTML Output** — Clean, modern templates with dark mode support
- **Built-in Search** — JavaScript-powered search, no server required
- **Mobile Friendly** — Responsive design works on all devices
- **Print Ready** — Dedicated print stylesheet for hard copies
- **Fully Offline** — Generated sites work without internet connectivity
- **Customizable** — Jinja2 templates, easy to theme

## Quick Start

### Installation

```bash
pip install infradocs
```

Or install from source:

```bash
git clone https://github.com/NexuFrame/infradocs.git
cd infradocs
pip install -e .
```

### Usage

```bash
# Initialize a new project with sample data
infradocs init my-network
cd my-network

# Edit your data files
# See docs/input-formats.md for the data schema

# Generate the documentation site
infradocs build --input . --output site

# View the result
open site/index.html
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `infradocs init <path>` | Create a new project with sample data |
| `infradocs build` | Generate the static site |
| `infradocs validate` | Validate data files without building |
| `infradocs version` | Show version information |

## Data Structure

InfraDocs organizes your infrastructure data into these categories:

- **Sites** — Physical locations and facilities
- **Devices** — Network equipment (routers, switches, firewalls, servers)
- **VLANs** — Virtual LAN configurations
- **Subnets** — IP address allocations
- **Printers** — Network printer inventory
- **Vendors** — Supplier and contractor information
- **Circuits** — Internet and telecom connections
- **Change Log** — Historical changes and updates
- **Emergency Procedures** — Runbooks and contact information

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Input Formats](docs/input-formats.md)
- [Templates](docs/templates.md)
- [Troubleshooting](docs/troubleshooting.md)
- [FAQ](docs/faq.md)

## Pricing

InfraDocs Generator is available under three license tiers:

| Tier | Price | Use Case |
|------|-------|----------|
| Personal | $19 | Single IT admin, internal use only |
| Consultant | $49 | Up to 5 client engagements per year |
| MSP/White-label | $99 | Unlimited clients, rebrand HTML output |

See [EULA.md](EULA.md) for full license terms.

## Development

```bash
# Clone the repository
git clone https://github.com/NexuFrame/infradocs.git

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=infradocs
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License — see [LICENSE.txt](LICENSE.txt) for details.

The MIT license covers the source code. Commercial usage is governed by the [EULA](EULA.md).

## Support

- 📧 Email: support@infradocs.io
- 🐛 Issues: [GitHub Issues](https://github.com/NexuFrame/infradocs/issues)
- 📖 Docs: See the `docs/` directory

---

Made with ❤️ by [NexuFrame](https://github.com/NexuFrame)
