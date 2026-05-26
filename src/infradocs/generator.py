"""Site generator for InfraDocs Generator."""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from infradocs.search_index import build_search_index
from infradocs.templates import TemplateRenderer
from infradocs.utils import get_timestamp


class SiteGenerator:
    """Generate static HTML site from infrastructure data."""
    
    def __init__(self, templates_dir: str, output_dir: str):
        """Initialize site generator.
        
        Args:
            templates_dir: Directory containing HTML templates.
            output_dir: Directory to write generated site.
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.renderer: Optional[TemplateRenderer] = None
    
    def generate(self, data: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate the complete static site.
        
        Args:
            data: Dictionary containing all infrastructure data.
            config: Optional configuration dictionary.
            
        Returns:
            Dictionary with generation statistics.
        """
        config = config or {}
        
        # Ensure output directory exists and is clean
        self._prepare_output_dir()
        
        # Initialize renderer
        assets_dir = self.templates_dir / 'assets'
        self.renderer = TemplateRenderer(str(self.templates_dir), str(assets_dir))
        
        stats = {
            'sites': 0,
            'devices': 0,
            'vlans': 0,
            'subnets': 0,
            'printers': 0,
            'vendors': 0,
            'circuits': 0,
            'change_log': 0,
            'emergency_procedures': 0,
            'files_generated': [],
        }
        
        # Build context with all data and config
        context = self._build_context(data, config)
        
        # Generate index page
        self._generate_index(context)
        stats['files_generated'].append('index.html')
        
        # Generate section pages
        if data.get('sites'):
            self._generate_sites_page(context)
            stats['sites'] = len(data['sites']) if isinstance(data['sites'], list) else 1
            stats['files_generated'].append('sites.html')
        
        if data.get('devices'):
            self._generate_devices_page(context)
            stats['devices'] = len(data['devices']) if isinstance(data['devices'], list) else 1
            stats['files_generated'].append('devices.html')
        
        if data.get('vlans'):
            self._generate_vlans_page(context)
            stats['vlans'] = len(data['vlans']) if isinstance(data['vlans'], list) else 1
            stats['files_generated'].append('vlans.html')
        
        if data.get('subnets'):
            self._generate_subnets_page(context)
            stats['subnets'] = len(data['subnets']) if isinstance(data['subnets'], list) else 1
            stats['files_generated'].append('subnets.html')
        
        if data.get('printers'):
            self._generate_printers_page(context)
            stats['printers'] = len(data['printers']) if isinstance(data['printers'], list) else 1
            stats['files_generated'].append('printers.html')
        
        if data.get('vendors'):
            self._generate_vendors_page(context)
            stats['vendors'] = len(data['vendors']) if isinstance(data['vendors'], list) else 1
            stats['files_generated'].append('vendors.html')
        
        if data.get('circuits'):
            self._generate_circuits_page(context)
            stats['circuits'] = len(data['circuits']) if isinstance(data['circuits'], list) else 1
            stats['files_generated'].append('circuits.html')
        
        if data.get('change_log'):
            self._generate_change_log_page(context)
            stats['change_log'] = len(data['change_log']) if isinstance(data['change_log'], list) else 1
            stats['files_generated'].append('change-log.html')
        
        if data.get('emergency_procedures'):
            self._generate_emergency_page(context)
            stats['emergency_procedures'] = len(data['emergency_procedures']) if isinstance(data['emergency_procedures'], list) else 1
            stats['files_generated'].append('emergency.html')
        
        # Generate search index
        self._generate_search_index(data)
        stats['files_generated'].append('search-index.json')
        
        # Copy assets
        self._copy_assets()
        stats['files_generated'].extend(['assets/style.css', 'assets/search.js'])
        
        return stats
    
    def _prepare_output_dir(self) -> None:
        """Prepare output directory."""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create assets directory
        (self.output_dir / 'assets').mkdir(exist_ok=True)
    
    def _build_context(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Build template context."""
        site_config = config.get('site', {})
        
        # Calculate summary statistics
        summary = {
            'total_sites': len(data.get('sites', [])) if isinstance(data.get('sites'), list) else (1 if data.get('sites') else 0),
            'total_devices': len(data.get('devices', [])) if isinstance(data.get('devices'), list) else (1 if data.get('devices') else 0),
            'total_vlans': len(data.get('vlans', [])) if isinstance(data.get('vlans'), list) else (1 if data.get('vlans') else 0),
            'total_subnets': len(data.get('subnets', [])) if isinstance(data.get('subnets'), list) else (1 if data.get('subnets') else 0),
            'total_printers': len(data.get('printers', [])) if isinstance(data.get('printers'), list) else (1 if data.get('printers') else 0),
            'total_vendors': len(data.get('vendors', [])) if isinstance(data.get('vendors'), list) else (1 if data.get('vendors') else 0),
            'total_circuits': len(data.get('circuits', [])) if isinstance(data.get('circuits'), list) else (1 if data.get('circuits') else 0),
        }
        
        return {
            'site': site_config,
            'data': data,
            'summary': summary,
            'config': config,
            'generated_at': get_timestamp(),
        }
    
    def _generate_index(self, context: Dict[str, Any]) -> None:
        """Generate index.html."""
        self.renderer.render_to_file(
            'index.html',
            context,
            str(self.output_dir / 'index.html')
        )
    
    def _generate_sites_page(self, context: Dict[str, Any]) -> None:
        """Generate sites.html."""
        self.renderer.render_to_file(
            'site.html',
            context,
            str(self.output_dir / 'sites.html')
        )
    
    def _generate_devices_page(self, context: Dict[str, Any]) -> None:
        """Generate devices.html."""
        self.renderer.render_to_file(
            'device.html',
            context,
            str(self.output_dir / 'devices.html')
        )
    
    def _generate_vlans_page(self, context: Dict[str, Any]) -> None:
        """Generate vlans.html."""
        self.renderer.render_to_file(
            'vlan.html',
            context,
            str(self.output_dir / 'vlans.html')
        )
    
    def _generate_subnets_page(self, context: Dict[str, Any]) -> None:
        """Generate subnets.html."""
        self.renderer.render_to_file(
            'subnet.html',
            context,
            str(self.output_dir / 'subnets.html')
        )
    
    def _generate_printers_page(self, context: Dict[str, Any]) -> None:
        """Generate printers.html."""
        self.renderer.render_to_file(
            'printer.html',
            context,
            str(self.output_dir / 'printers.html')
        )
    
    def _generate_vendors_page(self, context: Dict[str, Any]) -> None:
        """Generate vendors.html."""
        self.renderer.render_to_file(
            'vendor.html',
            context,
            str(self.output_dir / 'vendors.html')
        )
    
    def _generate_circuits_page(self, context: Dict[str, Any]) -> None:
        """Generate circuits.html."""
        self.renderer.render_to_file(
            'circuit.html',
            context,
            str(self.output_dir / 'circuits.html')
        )
    
    def _generate_change_log_page(self, context: Dict[str, Any]) -> None:
        """Generate change-log.html."""
        self.renderer.render_to_file(
            'change-log.html',
            context,
            str(self.output_dir / 'change-log.html')
        )
    
    def _generate_emergency_page(self, context: Dict[str, Any]) -> None:
        """Generate emergency.html."""
        self.renderer.render_to_file(
            'emergency.html',
            context,
            str(self.output_dir / 'emergency.html')
        )
    
    def _generate_search_index(self, data: Dict[str, Any]) -> None:
        """Generate search-index.json."""
        index = build_search_index(data)
        index.save(str(self.output_dir / 'search-index.json'))
    
    def _copy_assets(self) -> None:
        """Copy CSS and JS assets to output directory."""
        assets_dir = self.templates_dir / 'assets'
        output_assets = self.output_dir / 'assets'
        
        if assets_dir.exists():
            for asset_file in assets_dir.iterdir():
                if asset_file.is_file():
                    shutil.copy2(str(asset_file), str(output_assets / asset_file.name))


def generate_site(data: Dict[str, Any], templates_dir: str, output_dir: str,
                  config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate static site from infrastructure data.
    
    Args:
        data: Dictionary containing all infrastructure data.
        templates_dir: Directory containing HTML templates.
        output_dir: Directory to write generated site.
        config: Optional configuration dictionary.
        
    Returns:
        Dictionary with generation statistics.
    """
    generator = SiteGenerator(templates_dir, output_dir)
    return generator.generate(data, config)
