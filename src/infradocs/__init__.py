"""InfraDocs Generator - Static IT infrastructure documentation generator."""

__version__ = "1.0.0"
__author__ = "InfraDocs"

from infradocs.loader import load_data
from infradocs.validator import validate_data
from infradocs.generator import generate_site

__all__ = ["load_data", "validate_data", "generate_site", "__version__"]
