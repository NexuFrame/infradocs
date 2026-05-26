"""Data validation for InfraDocs Generator."""

from typing import Any, Dict, List, Optional, Set, Tuple

from infradocs.utils import (
    validate_ip_address,
    validate_cidr,
    validate_mac_address,
    validate_date,
    validate_datetime,
    is_private_ip,
)


class DataValidator:
    """Validate infrastructure data for correctness and consistency."""
    
    # Required fields for each data type
    REQUIRED_FIELDS = {
        'sites': ['id', 'name'],
        'devices': ['id', 'name', 'type', 'ip_address'],
        'vlans': ['id', 'name', 'vlan_id'],
        'subnets': ['id', 'name', 'cidr'],
        'printers': ['id', 'name', 'ip_address'],
        'vendors': ['id', 'name'],
        'circuits': ['id', 'name', 'provider'],
        'change_log': ['id', 'date', 'description'],
        'emergency_procedures': ['id', 'title', 'steps'],
    }
    
    # Field types for validation
    FIELD_TYPES = {
        'ip_address': 'ip',
        'gateway': 'ip',
        'cidr': 'cidr',
        'mac_address': 'mac',
        'date': 'date',
        'datetime': 'datetime',
        'vlan_id': 'vlan_id',
        'port': 'port',
    }
    
    def __init__(self, data: Dict[str, Any], require_private_ips: bool = True):
        """Initialize validator.
        
        Args:
            data: Dictionary containing all loaded data.
            require_private_ips: If True, validate that IPs are in private ranges.
        """
        self.data = data
        self.require_private_ips = require_private_ips
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
    
    def validate_all(self) -> Tuple[List[Dict], List[Dict]]:
        """Run all validations.
        
        Returns:
            Tuple of (errors, warnings).
        """
        # Validate each data type
        for data_type in self.REQUIRED_FIELDS.keys():
            if data_type in self.data:
                self._validate_data_type(data_type)
        
        # Cross-reference validations
        self._validate_cross_references()
        
        return self.errors, self.warnings
    
    def _add_error(self, data_type: str, item_id: str, field: str, message: str) -> None:
        """Add an error."""
        self.errors.append({
            'type': data_type,
            'id': item_id,
            'field': field,
            'message': message,
        })
    
    def _add_warning(self, data_type: str, item_id: str, field: str, message: str) -> None:
        """Add a warning."""
        self.warnings.append({
            'type': data_type,
            'id': item_id,
            'field': field,
            'message': message,
        })
    
    def _validate_data_type(self, data_type: str) -> None:
        """Validate a specific data type."""
        items = self.data.get(data_type, [])
        
        if not isinstance(items, list):
            items = [items]
        
        required = self.REQUIRED_FIELDS.get(data_type, [])
        seen_ids: Set[str] = set()
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            item_id = item.get('id', 'unknown')
            
            # Check for duplicate IDs
            if item_id in seen_ids:
                self._add_error(data_type, item_id, 'id', f"Duplicate ID: {item_id}")
            seen_ids.add(item_id)
            
            # Check required fields
            for field in required:
                if field not in item or item[field] is None or item[field] == '':
                    self._add_error(data_type, item_id, field, f"Missing required field: {field}")
            
            # Validate field types
            for field, value in item.items():
                if value is None or value == '':
                    continue
                
                if field in self.FIELD_TYPES:
                    self._validate_field_type(data_type, item_id, field, value)
    
    def _validate_field_type(self, data_type: str, item_id: str, field: str, value: Any) -> None:
        """Validate a field's value type."""
        field_type = self.FIELD_TYPES.get(field)
        
        if field_type == 'ip':
            if not validate_ip_address(str(value)):
                self._add_error(data_type, item_id, field, f"Invalid IP address: {value}")
            elif self.require_private_ips and not is_private_ip(str(value)):
                self._add_warning(data_type, item_id, field, 
                    f"IP address {value} is not in a private range")
        
        elif field_type == 'cidr':
            if not validate_cidr(str(value)):
                self._add_error(data_type, item_id, field, f"Invalid CIDR notation: {value}")
        
        elif field_type == 'mac':
            if not validate_mac_address(str(value)):
                self._add_error(data_type, item_id, field, f"Invalid MAC address: {value}")
        
        elif field_type == 'date':
            if not validate_date(str(value)):
                self._add_error(data_type, item_id, field, f"Invalid date format: {value} (expected YYYY-MM-DD)")
        
        elif field_type == 'datetime':
            if not validate_datetime(str(value)):
                self._add_error(data_type, item_id, field, f"Invalid datetime format: {value}")
        
        elif field_type == 'vlan_id':
            try:
                vlan_id = int(value)
                if not (1 <= vlan_id <= 4094):
                    self._add_error(data_type, item_id, field, 
                        f"VLAN ID must be between 1 and 4094: {value}")
            except (ValueError, TypeError):
                self._add_error(data_type, item_id, field, f"VLAN ID must be a number: {value}")
        
        elif field_type == 'port':
            try:
                port = int(value)
                if not (1 <= port <= 65535):
                    self._add_error(data_type, item_id, field, 
                        f"Port must be between 1 and 65535: {value}")
            except (ValueError, TypeError):
                self._add_error(data_type, item_id, field, f"Port must be a number: {value}")
    
    def _validate_cross_references(self) -> None:
        """Validate cross-references between data types."""
        # Build ID lookups
        site_ids = self._get_ids('sites')
        vlan_ids = self._get_ids('vlans')
        subnet_ids = self._get_ids('subnets')
        device_ids = self._get_ids('devices')
        vendor_ids = self._get_ids('vendors')
        
        # Validate device references
        for device in self.data.get('devices', []):
            if not isinstance(device, dict):
                continue
            
            device_id = device.get('id', 'unknown')
            
            # Check site reference
            site_id = device.get('site_id')
            if site_id and site_id not in site_ids:
                self._add_error('devices', device_id, 'site_id', 
                    f"Referenced site not found: {site_id}")
            
            # Check VLAN references
            vlans = device.get('vlans', [])
            if isinstance(vlans, list):
                for vlan in vlans:
                    if vlan not in vlan_ids:
                        self._add_warning('devices', device_id, 'vlans', 
                            f"Referenced VLAN not found: {vlan}")
            
            # Check vendor reference
            vendor_id = device.get('vendor_id')
            if vendor_id and vendor_id not in vendor_ids:
                self._add_warning('devices', device_id, 'vendor_id', 
                    f"Referenced vendor not found: {vendor_id}")
        
        # Validate subnet references
        for subnet in self.data.get('subnets', []):
            if not isinstance(subnet, dict):
                continue
            
            subnet_id = subnet.get('id', 'unknown')
            
            site_id = subnet.get('site_id')
            if site_id and site_id not in site_ids:
                self._add_error('subnets', subnet_id, 'site_id', 
                    f"Referenced site not found: {site_id}")
        
        # Validate circuit references
        for circuit in self.data.get('circuits', []):
            if not isinstance(circuit, dict):
                continue
            
            circuit_id = circuit.get('id', 'unknown')
            
            site_id = circuit.get('site_id')
            if site_id and site_id not in site_ids:
                self._add_error('circuits', circuit_id, 'site_id', 
                    f"Referenced site not found: {site_id}")
    
    def _get_ids(self, data_type: str) -> Set[str]:
        """Get all IDs for a data type."""
        items = self.data.get(data_type, [])
        
        if not isinstance(items, list):
            items = [items]
        
        return {item.get('id') for item in items if isinstance(item, dict) and item.get('id')}


def validate_data(data: Dict[str, Any], require_private_ips: bool = True) -> Tuple[List[Dict], List[Dict]]:
    """Validate infrastructure data.
    
    Args:
        data: Dictionary containing all loaded data.
        require_private_ips: If True, validate that IPs are in private ranges.
        
    Returns:
        Tuple of (errors, warnings).
    """
    validator = DataValidator(data, require_private_ips)
    return validator.validate_all()


def format_validation_errors(errors: List[Dict], warnings: List[Dict]) -> str:
    """Format validation errors and warnings for display.
    
    Args:
        errors: List of error dictionaries.
        warnings: List of warning dictionaries.
        
    Returns:
        Formatted string for terminal output.
    """
    output = []
    
    if errors:
        output.append(f"\n❌ Validation Errors ({len(errors)}):")
        for err in errors:
            output.append(f"  [{err['type']}] {err['id']}.{err['field']}: {err['message']}")
    
    if warnings:
        output.append(f"\n⚠️  Validation Warnings ({len(warnings)}):")
        for warn in warnings:
            output.append(f"  [{warn['type']}] {warn['id']}.{warn['field']}: {warn['message']}")
    
    if not errors and not warnings:
        output.append("\n✅ All validations passed!")
    
    return '\n'.join(output)
