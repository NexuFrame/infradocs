# Contributing to InfraDocs Generator

Thank you for your interest in contributing to InfraDocs Generator! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in [Issues](https://github.com/NexuFrame/infradocs/issues)
- If not, create a new issue with:
  - A clear description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment (Python version, OS)

### Suggesting Features

- Open an issue with the `enhancement` label
- Describe the feature and its use case
- Be specific about the expected behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass (`pytest`)
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your fork (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/infradocs.git
cd infradocs

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=infradocs
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and modular

### Testing

- All new features should include tests
- Aim for high test coverage
- Use pytest fixtures for reusable test data

## Questions?

Feel free to open an issue or reach out to support@nexuframe.com

Thank you for contributing! 🎉
