import pytest
from infradocs.validator import validate_device, validate_vlan

def test_valid_device_passes():
    device = {"id": "d1", "hostname": "sw-test", "ip": "192.168.1.1", "site": "hq", "role": "switch"}
    errors = validate_device(device)
    assert errors == []

def test_missing_hostname_fails():
    device = {"id": "d1", "ip": "192.168.1.1", "site": "hq", "role": "switch"}
    errors = validate_device(device)
    assert any("hostname" in e for e in errors)

def test_missing_ip_fails():
    device = {"id": "d1", "hostname": "sw-test", "site": "hq", "role": "switch"}
    errors = validate_device(device)
    assert any("ip" in e for e in errors)

def test_valid_vlan_passes():
    vlan = {"id": 10, "name": "Servers"}
    errors = validate_vlan(vlan)
    assert errors == []
