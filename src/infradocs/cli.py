"""Command-line interface for InfraDocs Generator."""

import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from infradocs import __version__
from infradocs.config import find_config_file, load_config
from infradocs.generator import generate_site
from infradocs.loader import load_data
from infradocs.validator import format_validation_errors, validate_data

app = typer.Typer(
    name="infradocs",
    help="Generate static IT infrastructure documentation websites.",
    add_completion=False,
)

console = Console()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold blue]InfraDocs Generator[/bold blue] v{__version__}")
    console.print(
        "Generate static IT infrastructure documentation from YAML/JSON/CSV files."
    )


@app.command()
def init(
    path: str = typer.Argument(
        "my-it-docs",
        help="Path to create the new documentation directory.",
    ),
) -> None:
    """Initialize a new documentation directory with sample files."""
    init_dir = Path(path)

    if init_dir.exists():
        console.print(
            f"[yellow]Warning:[/yellow] Directory '{init_dir}' already exists."
        )
        response = input(f"Continue and potentially overwrite files? (y/N): ")
        if response.lower() != "y":
            console.print("[red]Aborted.[/red]")
            raise typer.Exit(1)

    console.print(f"[bold]Creating documentation directory:[/bold] {init_dir}")

    # Create directory structure
    init_dir.mkdir(parents=True, exist_ok=True)
    (init_dir / "output").mkdir(exist_ok=True)

    # Create sample config file
    config_content = """# InfraDocs Configuration
# See docs/Customization-Guide.md for all options

site:
  title: "IT Infrastructure Documentation"
  description: "Network and infrastructure documentation for our organization"
  author: "IT Team"
  logo_text: "InfraDocs"

features:
  search: true
  sort_tables: true
  badges: true
  print_css: true

validation:
  require_private_ips: true
  strict_mode: false

output:
  include_timestamp: true
  minify_html: false
"""
    _write_file(init_dir / "config.yaml", config_content)

    # Create sample data files
    _create_sample_data(init_dir)

    # Create README
    readme_content = f"""# IT Infrastructure Documentation

This directory contains your IT infrastructure documentation source files.

## Quick Start

1. Edit the data files in this directory (sites.yaml, devices.yaml, etc.)
2. Run: `infradocs build --input . --output output`
3. Open `output/index.html` in your browser

## Data Files

- `config.yaml` - Site configuration
- `sites.yaml` - Physical locations/sites
- `devices.yaml` - Network devices
- `vlans.yaml` - VLAN configurations
- `subnets.yaml` - IP subnets
- `printers.csv` - Network printers
- `vendors.yaml` - Vendor/supplier information
- `circuits.yaml` - Internet/telecom circuits
- `change-log.yaml` - Change history
- `emergency-procedures.yaml` - Emergency runbooks

## Documentation

See the full documentation at: https://github.com/NexuFrame/infradocs
"""
    _write_file(init_dir / "README.md", readme_content)

    console.print("[green]✓[/green] Documentation directory initialized!")
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"  1. Edit the data files in [cyan]{init_dir}[/cyan]")
    console.print(
        f"  2. Run: [cyan]infradocs build --input {init_dir} --output {init_dir}/output[/cyan]"
    )
    console.print(
        f"  3. Open [cyan]{init_dir}/output/index.html[/cyan] in your browser"
    )


@app.command()
def build(
    input_dir: str = typer.Option(
        "sample-data",
        "--input",
        "-i",
        help="Directory containing input data files.",
    ),
    output_dir: str = typer.Option(
        "output/site",
        "--output",
        "-o",
        help="Directory to write generated site.",
    ),
    validate_only: bool = typer.Option(
        False,
        "--validate-only",
        help="Only validate input files, don't generate site.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors.",
    ),
) -> None:
    """Build the documentation site from input files."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Check input directory
    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input directory does not exist: {input_dir}")
        raise typer.Exit(1)

    # Load configuration
    config_file = find_config_file(str(input_path))
    config = load_config(config_file)

    console.print(f"[bold]InfraDocs Generator[/bold] v{__version__}")
    console.print(f"Input:  [cyan]{input_path.absolute()}[/cyan]")
    console.print(f"Output: [cyan]{output_path.absolute()}[/cyan]")
    if config_file:
        console.print(f"Config: [cyan]{config_file}[/cyan]")
    console.print()

    # Load data
    console.print("[bold]Loading data files...[/bold]")
    data, load_errors, load_warnings = load_data(str(input_path))

    if load_errors:
        console.print(f"[red]✗ Load errors ({len(load_errors)}):[/red]")
        for error in load_errors:
            console.print(f"  - {error}")
        raise typer.Exit(1)

    if load_warnings:
        console.print(f"[yellow]Load warnings ({len(load_warnings)}):[/yellow]")
        for warning in load_warnings:
            console.print(f"  - {warning}")

    console.print(f"[green]✓ Loaded {len(data)} data types[/green]")

    # Validate data
    console.print("\n[bold]Validating data...[/bold]")
    require_private = config.get("validation", "require_private_ips", default=True)
    errors, warnings = validate_data(data, require_private_ips=require_private)

    console.print(format_validation_errors(errors, warnings))

    if errors:
        console.print(f"\n[red]✗ Build failed: {len(errors)} validation error(s)[/red]")
        raise typer.Exit(1)

    if strict and warnings:
        console.print(
            f"\n[red]✗ Build failed (strict mode): {len(warnings)} warning(s)[/red]"
        )
        raise typer.Exit(1)

    if validate_only:
        console.print("\n[green]✓ Validation passed![/green]")
        return

    # Generate site
    console.print("\n[bold]Generating site...[/bold]")
    templates_dir = _get_templates_dir()

    try:
        stats = generate_site(
            data, str(templates_dir), str(output_path), config.to_dict()
        )
    except Exception as e:
        console.print(f"[red]✗ Generation failed: {e}[/red]")
        raise typer.Exit(1)

    # Show summary
    console.print(f"\n[green]✓ Site generated successfully![/green]")
    _show_generation_summary(stats, output_path)


@app.command()
def validate(
    input_dir: str = typer.Argument(
        "sample-data",
        help="Directory containing input data files.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors.",
    ),
) -> None:
    """Validate input data files without generating site."""
    input_path = Path(input_dir)

    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input directory does not exist: {input_dir}")
        raise typer.Exit(1)

    # Load configuration
    config_file = find_config_file(str(input_path))
    config = load_config(config_file)

    console.print(f"[bold]InfraDocs Validator[/bold]")
    console.print(f"Input: [cyan]{input_path.absolute()}[/cyan]\n")

    # Load data
    data, load_errors, load_warnings = load_data(str(input_path))

    if load_errors:
        console.print(f"[red]✗ Load errors ({len(load_errors)}):[/red]")
        for error in load_errors:
            console.print(f"  - {error}")
        raise typer.Exit(1)

    # Validate
    require_private = config.get("validation", "require_private_ips", default=True)
    errors, warnings = validate_data(data, require_private_ips=require_private)

    console.print(format_validation_errors(errors, warnings))

    if errors:
        console.print(f"\n[red]✗ Validation failed: {len(errors)} error(s)[/red]")
        raise typer.Exit(1)

    if strict and warnings:
        console.print(
            f"\n[red]✗ Validation failed (strict mode): {len(warnings)} warning(s)[/red]"
        )
        raise typer.Exit(1)

    console.print(f"\n[green]✓ Validation passed![/green]")


@app.command()
def clean(
    output_dir: str = typer.Option(
        "output/site",
        "--output",
        "-o",
        help="Directory to clean.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be deleted without deleting.",
    ),
) -> None:
    """Clean generated output files."""
    output_path = Path(output_dir)

    if not output_path.exists():
        console.print(f"Output directory does not exist: {output_dir}")
        return

    console.print(f"[bold]Cleaning output directory:[/bold] {output_path}")

    if dry_run:
        console.print("[yellow]Dry run - nothing will be deleted[/yellow]")
        console.print(f"Would delete: {output_path}")
        return

    try:
        shutil.rmtree(str(output_path))
        console.print("[green]✓ Cleaned successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Clean failed: {e}[/red]")
        raise typer.Exit(1)


def _get_templates_dir() -> Path:
    """Get the templates directory path."""
    # Try relative to package first
    package_dir = Path(__file__).parent.parent.parent
    templates_dir = package_dir / "templates"

    if templates_dir.exists():
        return templates_dir

    # Fallback to current directory
    current_templates = Path("templates")
    if current_templates.exists():
        return current_templates

    # Last resort - use the templates in the same directory as this file
    return Path(__file__).parent.parent / "templates"


def _show_generation_summary(stats: dict, output_path: Path) -> None:
    """Display generation summary table."""
    table = Table(title="Generation Summary")
    table.add_column("Content Type", style="cyan")
    table.add_column("Count", justify="right")

    content_types = [
        ("Sites", stats.get("sites", 0)),
        ("Devices", stats.get("devices", 0)),
        ("VLANs", stats.get("vlans", 0)),
        ("Subnets", stats.get("subnets", 0)),
        ("Printers", stats.get("printers", 0)),
        ("Vendors", stats.get("vendors", 0)),
        ("Circuits", stats.get("circuits", 0)),
        ("Change Log", stats.get("change_log", 0)),
        ("Emergency Procedures", stats.get("emergency_procedures", 0)),
    ]

    for name, count in content_types:
        table.add_row(name, str(count))

    console.print(table)
    console.print(
        f"\n[bold]Files generated:[/bold] {len(stats.get('files_generated', []))}"
    )
    console.print(
        f"[bold]Output location:[/bold] [cyan]{output_path.absolute()}/index.html[/cyan]"
    )


def _write_file(path: Path, content: str) -> None:
    """Write content to file, creating directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _create_sample_data(init_dir: Path) -> None:
    """Create minimal sample data files."""
    # Sites
    _write_file(
        init_dir / "sites.yaml",
        """# Physical sites/locations
- id: site-hq
  name: "Headquarters"
  description: "Main office building"
  location: "New York, NY"
  address: "123 Business Ave, New York, NY 10001"
  status: "active"
""",
    )

    # Devices
    _write_file(
        init_dir / "devices.yaml",
        """# Network devices
- id: fw-01
  name: "Main Firewall"
  type: "firewall"
  ip_address: "192.168.1.1"
  model: "Example FW-1000"
  site_id: "site-hq"
  status: "online"
""",
    )

    # VLANs
    _write_file(
        init_dir / "vlans.yaml",
        """# VLAN configurations
- id: vlan-mgmt
  name: "Management"
  vlan_id: 10
  description: "Network management VLAN"
""",
    )

    # Subnets
    _write_file(
        init_dir / "subnets.yaml",
        """# IP subnets
- id: subnet-mgmt
  name: "Management Network"
  cidr: "192.168.1.0/24"
  description: "Management subnet"
  site_id: "site-hq"
""",
    )

    # Printers
    _write_file(
        init_dir / "printers.csv",
        """id,name,ip_address,location,type,status
printer-01,Office Printer,192.168.1.50,Headquarters - Floor 2,Laser,online
""",
    )

    # Vendors
    _write_file(
        init_dir / "vendors.yaml",
        """# Vendors and suppliers
- id: vendor-cisco
  name: "Cisco Systems"
  description: "Network equipment"
  website: "https://www.cisco.com"
  support_phone: "1-800-555-0100"
""",
    )

    # Circuits
    _write_file(
        init_dir / "circuits.yaml",
        """# Internet/telecom circuits
- id: circuit-internet
  name: "Primary Internet"
  provider: "Example ISP"
  type: "fiber"
  speed_mbps: 1000
  site_id: "site-hq"
  status: "active"
""",
    )

    # Change log
    _write_file(
        init_dir / "change-log.yaml",
        """# Change log entries
- id: change-001
  date: "2024-01-15"
  description: "Initial network setup"
  changed_by: "IT Team"
""",
    )

    # Emergency procedures
    _write_file(
        init_dir / "emergency-procedures.yaml",
        """# Emergency procedures
- id: emergency-network-outage
  title: "Network Outage Response"
  description: "Steps to take during a network outage"
  steps:
    - "1. Check main firewall status"
    - "2. Verify internet circuit status"
    - "3. Contact ISP if circuit is down"
    - "4. Escalate to network team if needed"
""",
    )


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
