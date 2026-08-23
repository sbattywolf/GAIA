# GAIA Target Inventory

This directory contains the target inventory system that defines targets and their configurations for the engineering loop.

## Structure

```
gaia_target_inventory/
├── targets/
│   └── gaia-1070/
│       ├── declared_config.json
│       └── evidence_templates/
├── transports/
│   └── ssh/
│       └── gaia-1070.json
└── README.md
```

## Target Configuration

Each target has a `declared_config.json` file that specifies:
- Target identification and role
- Hostname and connection details  
- Runner script path
- Resource requirements
- Execution characteristics

## Transport Configuration

Transport configurations define how to connect to targets:
- SSH alias or direct connection parameters
- Authentication methods
- Port numbers
- Connection timeouts

## Future Expansion

This structure supports:
- Multiple target types (physical, simulated, cloud)
- Multiple transport mechanisms (SSH, HTTP, etc.)
- Dynamic inventory loading
- Target health monitoring