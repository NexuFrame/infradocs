"""Data loader for YAML, JSON, and CSV files."""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class DataLoader:
    """Load infrastructure data from various file formats."""

    SUPPORTED_EXTENSIONS = {".yaml", ".yml", ".json", ".csv"}

    def __init__(self, input_dir: str):
        """Initialize data loader.

        Args:
            input_dir: Directory containing data files.
        """
        self.input_dir = Path(input_dir)
        self.data: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_all(self) -> Dict[str, Any]:
        """Load all data files from the input directory.

        Returns:
            Dictionary containing all loaded data by type.
        """
        if not self.input_dir.exists():
            self.errors.append(f"Input directory does not exist: {self.input_dir}")
            return self.data

        # Define expected file mappings
        file_mappings = {
            "config": ["config.yaml", "config.yml"],
            "sites": ["sites.yaml", "sites.yml", "sites.json"],
            "devices": ["devices.yaml", "devices.yml", "devices.json"],
            "vlans": ["vlans.yaml", "vlans.yml", "vlans.json"],
            "subnets": ["subnets.yaml", "subnets.yml", "subnets.json"],
            "printers": [
                "printers.csv",
                "printers.yaml",
                "printers.yml",
                "printers.json",
            ],
            "vendors": ["vendors.yaml", "vendors.yml", "vendors.json"],
            "circuits": ["circuits.yaml", "circuits.yml", "circuits.json"],
            "change_log": [
                "change-log.yaml",
                "change-log.yml",
                "change-log.csv",
                "changelog.yaml",
                "changelog.yml",
                "changelog.csv",
            ],
            "emergency_procedures": [
                "emergency-procedures.yaml",
                "emergency-procedures.yml",
                "emergency-contacts.yaml",
                "emergency-contacts.yml",
                "emergency.yaml",
                "emergency.yml",
            ],
        }

        for data_type, filenames in file_mappings.items():
            loaded = False
            for filename in filenames:
                file_path = self.input_dir / filename
                if file_path.exists():
                    self._load_file(data_type, file_path)
                    loaded = True
                    break

            if not loaded:
                self.warnings.append(f"No data file found for '{data_type}'")

        return self.data

    def _load_file(self, data_type: str, file_path: Path) -> None:
        """Load a single file and store its data.

        Args:
            data_type: Type of data being loaded.
            file_path: Path to the file.
        """
        try:
            extension = file_path.suffix.lower()

            if extension in {".yaml", ".yml"}:
                data = self._load_yaml(file_path)
            elif extension == ".json":
                data = self._load_json(file_path)
            elif extension == ".csv":
                data = self._load_csv(file_path)
            else:
                self.errors.append(f"Unsupported file extension: {extension}")
                return

            self.data[data_type] = data

        except Exception as e:
            self.errors.append(f"Error loading {file_path}: {str(e)}")

    def _load_yaml(self, file_path: Path) -> Any:
        """Load YAML file, unwrapping single-key dicts like {'sites': [...]}."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        # If the YAML has a single top-level key like 'sites:', unwrap it
        if isinstance(data, dict) and len(data) == 1:
            return list(data.values())[0]
        return data

    def _load_json(self, file_path: Path) -> Any:
        """Load JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_csv(self, file_path: Path) -> List[Dict[str, str]]:
        """Load CSV file and return list of dictionaries."""
        data = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert empty strings to None
                cleaned_row = {k: (v if v != "" else None) for k, v in row.items()}
                data.append(cleaned_row)
        return data

    def load_single(self, filename: str) -> Tuple[Optional[Any], Optional[str]]:
        """Load a single file by name.

        Args:
            filename: Name of the file to load.

        Returns:
            Tuple of (data, error_message).
        """
        file_path = self.input_dir / filename

        if not file_path.exists():
            return None, f"File not found: {filename}"

        try:
            extension = file_path.suffix.lower()

            if extension in {".yaml", ".yml"}:
                data = self._load_yaml(file_path)
            elif extension == ".json":
                data = self._load_json(file_path)
            elif extension == ".csv":
                data = self._load_csv(file_path)
            else:
                return None, f"Unsupported file extension: {extension}"

            return data, None

        except Exception as e:
            return None, f"Error loading {filename}: {str(e)}"


def load_data(input_dir: str) -> Tuple[Dict[str, Any], List[str], List[str]]:
    """Load all infrastructure data from input directory.

    Args:
        input_dir: Directory containing data files.

    Returns:
        Tuple of (data_dict, errors, warnings).
    """
    loader = DataLoader(input_dir)
    data = loader.load_all()
    return data, loader.errors, loader.warnings


def load_single_file(file_path: str) -> Tuple[Optional[Any], Optional[str]]:
    """Load a single data file.

    Args:
        file_path: Path to the file.

    Returns:
        Tuple of (data, error_message).
    """
    path = Path(file_path)

    if not path.exists():
        return None, f"File not found: {file_path}"

    try:
        extension = path.suffix.lower()

        if extension in {".yaml", ".yml"}:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or []
        elif extension == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif extension == ".csv":
            data = []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned_row = {k: (v if v != "" else None) for k, v in row.items()}
                    data.append(cleaned_row)
        else:
            return None, f"Unsupported file extension: {extension}"

        return data, None

    except Exception as e:
        return None, f"Error loading {file_path}: {str(e)}"
