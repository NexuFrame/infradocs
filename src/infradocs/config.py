"""Configuration management for InfraDocs Generator."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from infradocs.utils import safe_get

# Default configuration values
DEFAULT_CONFIG = {
    "site": {
        "title": "IT Infrastructure Documentation",
        "description": "Network and infrastructure documentation",
        "author": "IT Team",
        "logo_text": "InfraDocs",
    },
    "features": {
        "search": True,
        "sort_tables": True,
        "badges": True,
        "print_css": True,
    },
    "validation": {
        "require_private_ips": True,
        "strict_mode": False,
    },
    "output": {
        "include_timestamp": True,
        "minify_html": False,
    },
}


class Config:
    """Configuration handler for InfraDocs."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to configuration YAML file. If None, uses defaults.
        """
        self.config = DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)

    def _load_config(self, path: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(path, "r") as f:
                user_config = yaml.safe_load(f) or {}

            # Deep merge user config with defaults
            self._deep_merge(self.config, user_config)
        except Exception as e:
            # Log warning but continue with defaults
            print(f"Warning: Could not load config from {path}: {e}")

    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Recursively merge override dict into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get configuration value by nested keys."""
        return safe_get(self.config, *keys, default=default)

    def set(self, *keys: str, value: Any) -> None:
        """Set configuration value by nested keys."""
        if len(keys) < 1:
            return

        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config.copy()


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or use defaults.

    Args:
        config_path: Path to configuration YAML file.

    Returns:
        Config object with merged defaults and user configuration.
    """
    return Config(config_path)


def find_config_file(input_dir: str) -> Optional[str]:
    """Find configuration file in input directory.

    Args:
        input_dir: Directory to search for configuration file.

    Returns:
        Path to config.yaml if found, None otherwise.
    """
    config_names = ["config.yaml", "config.yml", ".infradocs.yaml", ".infradocs.yml"]

    for name in config_names:
        config_path = os.path.join(input_dir, name)
        if os.path.exists(config_path):
            return config_path

    return None
