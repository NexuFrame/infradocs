"""Smoke tests for InfraDocs Generator."""

import infradocs


def test_version_exists():
    """Test that the package has a version."""
    assert hasattr(infradocs, '__version__')
    assert isinstance(infradocs.__version__, str)


def test_import_cli():
    """Test that CLI module can be imported."""
    from infradocs.cli import app
    assert app is not None


def test_import_config():
    """Test that config module can be imported."""
    from infradocs.config import Config, load_config
    assert Config is not None
    assert load_config is not None


def test_import_generator():
    """Test that generator module can be imported."""
    from infradocs.generator import generate_site
    assert generate_site is not None


def test_import_loader():
    """Test that loader module can be imported."""
    from infradocs.loader import DataLoader, load_data
    assert DataLoader is not None
    assert load_data is not None


def test_import_validator():
    """Test that validator module can be imported."""
    from infradocs.validator import DataValidator, validate_data
    assert DataValidator is not None
    assert validate_data is not None
