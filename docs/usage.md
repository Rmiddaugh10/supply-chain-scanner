# Usage Guide

## Basic Usage

1. Start a scan:
```bash
python -m supply_chain_scanner --config config.json
```

2. Generate a report:
```bash
python -m supply_chain_scanner --report
```

## Configuration Options

### Scan Intervals
- containers: Frequency of container scans (in seconds)
- dependencies: Frequency of dependency checks (in seconds)
- network: Frequency of network monitoring (in seconds)

### Alert Thresholds
- high: Threshold for high severity alerts
- medium: Threshold for medium severity alerts
- low: Threshold for low severity alerts

## Features

### Container Manifest Scanning
Scans container manifests for:
- Outdated base images
- Unauthorized sources
- Security vulnerabilities

### Package Dependency Checking
Checks dependencies for:
- Known vulnerabilities
- Version compatibility
- Security updates

### Network Connection Monitoring
Monitors for:
- Suspicious connections
- Unauthorized access attempts
- Unusual traffic patterns

## Examples

1. Scan a specific container manifest:
```bash
python -m supply_chain_scanner --manifest path/to/manifest.json