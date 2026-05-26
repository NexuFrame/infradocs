"""Utility functions for InfraDocs Generator."""

import ipaddress
import re
from datetime import datetime
from typing import Any, Optional


def validate_ip_address(ip: str) -> bool:
    """Validate an IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_cidr(cidr: str) -> bool:
    """Validate a CIDR notation (IPv4 or IPv6)."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def validate_mac_address(mac: str) -> bool:
    """Validate a MAC address format."""
    patterns = [
        r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",  # 00:11:22:33:44:55 or 00-11-22-33-44-55
        r"^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$",  # 0011.2233.4455
        r"^[0-9A-Fa-f]{12}$",  # 001122334455
    ]
    return any(re.match(pattern, mac) for pattern in patterns)


def validate_date(date_str: str) -> bool:
    """Validate a date string in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_datetime(datetime_str: str) -> bool:
    """Validate a datetime string in ISO format."""
    try:
        datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def normalize_mac_address(mac: str) -> str:
    """Normalize MAC address to colon-separated uppercase format."""
    # Remove all separators
    clean = re.sub(r"[:-.]", "", mac)
    # Format as XX:XX:XX:XX:XX:XX
    return ":".join(clean[i : i + 2] for i in range(0, 12, 2)).upper()


def is_private_ip(ip: str) -> bool:
    """Check if an IP address is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private
    except ValueError:
        return False


def format_bytes(size_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if size_bytes < 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date() -> str:
    """Get current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = text.replace(" ", "-")
    # Remove special characters
    text = re.sub(r"[^a-z0-9\-_]", "", text)
    # Remove multiple hyphens
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary values."""
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        else:
            return default
    return result


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
