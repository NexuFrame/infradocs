"""Search index generation for InfraDocs Generator."""

import json
from typing import Any, Dict, List, Optional, Set


class SearchIndex:
    """Build and export search index for client-side search."""
    
    def __init__(self):
        """Initialize search index."""
        self.index: List[Dict[str, Any]] = []
    
    def build(self, data: Dict[str, Any]) -> None:
        """Build search index from infrastructure data.
        
        Args:
            data: Dictionary containing all loaded data.
        """
        self.index = []
        
        # Index sites
        for site in data.get('sites', []):
            if isinstance(site, dict):
                self._add_item({
                    'id': site.get('id', ''),
                    'type': 'site',
                    'title': site.get('name', ''),
                    'description': site.get('description', ''),
                    'location': site.get('location', ''),
                    'url': f"sites.html#{site.get('id', '')}",
                })
        
        # Index devices
        for device in data.get('devices', []):
            if isinstance(device, dict):
                self._add_item({
                    'id': device.get('id', ''),
                    'type': 'device',
                    'title': device.get('name', ''),
                    'description': device.get('description', device.get('type', '')),
                    'ip_address': device.get('ip_address', ''),
                    'mac_address': device.get('mac_address', ''),
                    'model': device.get('model', ''),
                    'url': f"devices.html#{device.get('id', '')}",
                })
        
        # Index VLANs
        for vlan in data.get('vlans', []):
            if isinstance(vlan, dict):
                self._add_item({
                    'id': vlan.get('id', ''),
                    'type': 'vlan',
                    'title': f"VLAN {vlan.get('vlan_id', '')} - {vlan.get('name', '')}",
                    'description': vlan.get('description', ''),
                    'url': f"vlans.html#{vlan.get('id', '')}",
                })
        
        # Index subnets
        for subnet in data.get('subnets', []):
            if isinstance(subnet, dict):
                self._add_item({
                    'id': subnet.get('id', ''),
                    'type': 'subnet',
                    'title': subnet.get('name', ''),
                    'description': subnet.get('description', subnet.get('cidr', '')),
                    'cidr': subnet.get('cidr', ''),
                    'url': f"subnets.html#{subnet.get('id', '')}",
                })
        
        # Index printers
        for printer in data.get('printers', []):
            if isinstance(printer, dict):
                self._add_item({
                    'id': printer.get('id', ''),
                    'type': 'printer',
                    'title': printer.get('name', ''),
                    'description': printer.get('location', printer.get('type', '')),
                    'ip_address': printer.get('ip_address', ''),
                    'url': f"printers.html#{printer.get('id', '')}",
                })
        
        # Index vendors
        for vendor in data.get('vendors', []):
            if isinstance(vendor, dict):
                self._add_item({
                    'id': vendor.get('id', ''),
                    'type': 'vendor',
                    'title': vendor.get('name', ''),
                    'description': vendor.get('description', ''),
                    'url': f"vendors.html#{vendor.get('id', '')}",
                })
        
        # Index circuits
        for circuit in data.get('circuits', []):
            if isinstance(circuit, dict):
                self._add_item({
                    'id': circuit.get('id', ''),
                    'type': 'circuit',
                    'title': circuit.get('name', ''),
                    'description': circuit.get('description', circuit.get('provider', '')),
                    'provider': circuit.get('provider', ''),
                    'url': f"circuits.html#{circuit.get('id', '')}",
                })
        
        # Index change log entries
        for entry in data.get('change_log', []):
            if isinstance(entry, dict):
                self._add_item({
                    'id': entry.get('id', ''),
                    'type': 'change_log',
                    'title': entry.get('description', '')[:50],
                    'description': entry.get('description', ''),
                    'date': entry.get('date', ''),
                    'url': f"change-log.html#{entry.get('id', '')}",
                })
        
        # Index emergency procedures
        for proc in data.get('emergency_procedures', []):
            if isinstance(proc, dict):
                self._add_item({
                    'id': proc.get('id', ''),
                    'type': 'emergency',
                    'title': proc.get('title', ''),
                    'description': proc.get('description', ''),
                    'url': f"emergency.html#{proc.get('id', '')}",
                })
    
    def _add_item(self, item: Dict[str, Any]) -> None:
        """Add an item to the search index."""
        # Build searchable text
        searchable_parts = []
        for key in ['title', 'description', 'ip_address', 'mac_address', 
                    'model', 'location', 'cidr', 'provider', 'date']:
            if key in item and item[key]:
                searchable_parts.append(str(item[key]))
        
        item['searchable'] = ' '.join(searchable_parts).lower()
        self.index.append(item)
    
    def to_json(self) -> str:
        """Export index as JSON string."""
        # Remove the searchable field from output (used only for matching)
        output = []
        for item in self.index:
            output_item = {k: v for k, v in item.items() if k != 'searchable'}
            output.append(output_item)
        
        return json.dumps(output, indent=2)
    
    def save(self, output_path: str) -> None:
        """Save search index to file.
        
        Args:
            output_path: Path to save the JSON file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search the index for a query.
        
        Args:
            query: Search query string.
            
        Returns:
            List of matching items.
        """
        query_lower = query.lower()
        results = []
        
        for item in self.index:
            searchable = item.get('searchable', '')
            if query_lower in searchable:
                results.append(item)
        
        return results


def build_search_index(data: Dict[str, Any]) -> SearchIndex:
    """Build search index from infrastructure data.
    
    Args:
        data: Dictionary containing all loaded data.
        
    Returns:
        SearchIndex object with built index.
    """
    index = SearchIndex()
    index.build(data)
    return index


def generate_search_index_json(data: Dict[str, Any]) -> str:
    """Generate search index JSON string.
    
    Args:
        data: Dictionary containing all loaded data.
        
    Returns:
        JSON string of the search index.
    """
    index = build_search_index(data)
    return index.to_json()
