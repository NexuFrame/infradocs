"""Template rendering for InfraDocs Generator."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


class TemplateRenderer:
    """Render HTML templates using Jinja2."""

    def __init__(self, templates_dir: str, assets_dir: Optional[str] = None):
        """Initialize template renderer.

        Args:
            templates_dir: Directory containing HTML templates.
            assets_dir: Directory containing CSS/JS assets (optional).
        """
        self.templates_dir = Path(templates_dir)
        self.assets_dir = (
            Path(assets_dir) if assets_dir else self.templates_dir / "assets"
        )

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "htm", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters
        self.env.filters["format_date"] = self._format_date
        self.env.filters["format_datetime"] = self._format_datetime
        self.env.filters["status_badge"] = self._status_badge
        self.env.filters["truncate"] = self._truncate

        # Load assets
        self.css_content = self._load_asset("style.css")
        self.js_content = self._load_asset("search.js")

    def _load_asset(self, filename: str) -> str:
        """Load an asset file content."""
        asset_path = self.assets_dir / filename
        if asset_path.exists():
            with open(asset_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _format_date(self, date_str: str) -> str:
        """Format date string for display."""
        if not date_str:
            return ""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%B %d, %Y")
        except ValueError:
            return date_str

    def _format_datetime(self, dt_str: str) -> str:
        """Format datetime string for display."""
        if not dt_str:
            return ""
        try:
            # Handle ISO format with or without timezone
            dt_str_clean = dt_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(dt_str_clean)
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except ValueError:
            return dt_str

    def _status_badge(self, status: str) -> str:
        """Generate HTML badge for status."""
        status_lower = status.lower() if status else ""

        badge_classes = {
            "online": "badge-success",
            "active": "badge-success",
            "up": "badge-success",
            "operational": "badge-success",
            "offline": "badge-danger",
            "down": "badge-danger",
            "error": "badge-danger",
            "warning": "badge-warning",
            "maintenance": "badge-warning",
            "pending": "badge-warning",
            "expired": "badge-danger",
            "expiring": "badge-warning",
            "unknown": "badge-secondary",
        }

        badge_class = badge_classes.get(status_lower, "badge-secondary")
        return f'<span class="badge {badge_class}">{status or "Unknown"}</span>'

    def _truncate(self, text: str, length: int = 50) -> str:
        """Truncate text to specified length."""
        if not text or len(text) <= length:
            return text or ""
        return text[:length] + "..."

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with given context.

        Args:
            template_name: Name of the template file.
            context: Dictionary of template variables.

        Returns:
            Rendered HTML string.
        """
        # Add global assets to context
        context["css_content"] = self.css_content
        context["js_content"] = self.js_content
        context["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_to_file(
        self, template_name: str, context: Dict[str, Any], output_path: str
    ) -> None:
        """Render template and save to file.

        Args:
            template_name: Name of the template file.
            context: Dictionary of template variables.
            output_path: Path to save the rendered HTML.
        """
        html = self.render(template_name, context)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)


def create_renderer(
    templates_dir: str, assets_dir: Optional[str] = None
) -> TemplateRenderer:
    """Create a template renderer instance.

    Args:
        templates_dir: Directory containing HTML templates.
        assets_dir: Directory containing CSS/JS assets (optional).

    Returns:
        TemplateRenderer instance.
    """
    return TemplateRenderer(templates_dir, assets_dir)
