# Input Formats

InfraDocs reads YAML, JSON, and CSV files from your `input_dir`.

## YAML files

### devices.yaml
List of network devices. Each device:
```yaml
devices:
  - id: unique-id        # required
    hostname: hostname   # required
    ip: 192.168.1.1      # required
    site: site-id        # required (matches sites.yaml)
    role: switch         # required
    mac: aa:bb:cc:...    # optional
    os: Cisco IOS 15.2   # optional
    location: Rack A     # optional
    vlan_ids: [10, 20]   # optional
    notes: ""            # optional
```

### sites.yaml, vlans.yaml, subnets.yaml, printers.yaml, vendors.yaml, circuits.yaml, emergency-contacts.yaml
All follow the same pattern: a top-level key with a list of objects.

## CSV files

### change-log.csv
Required columns: `date, engineer, description, systems_affected, rollback_plan, outcome`
