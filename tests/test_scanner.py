"""Test cases for the supply chain scanner."""

import pytest
from datetime import datetime
from supply_chain_scanner.scanner import SupplyChainScanner, SecurityAlert

@pytest.fixture
def scanner():
    """Create a scanner instance for testing."""
    return SupplyChainScanner()

@pytest.fixture
def sample_alert():
    """Create a sample security alert for testing."""
    return SecurityAlert(
        timestamp=datetime.now().isoformat(),
        severity="HIGH",
        category="Container Security",
        description="Test alert",
        affected_component="Test Component",
        recommendation="Test recommendation"
    )

def test_scanner_initialization(scanner):
    """Test scanner initialization."""
    assert scanner is not None
    assert hasattr(scanner, 'alerts')
    assert isinstance(scanner.alerts, list)

def test_container_manifest_scanning(scanner, tmp_path):
    """Test container manifest scanning functionality."""
    # Create a temporary manifest file
    manifest_path = tmp_path / "manifest.json"
    manifest_content = {
        "baseImage": "ubuntu:latest",
        "imageSources": ["registry.fedex.com/base-image"]
    }
    manifest_path.write_text(json.dumps(manifest_content))
    
    alerts = scanner.scan_container_manifest(str(manifest_path))
    assert isinstance(alerts, list)

def test_package_dependency_checking(scanner, tmp_path):
    """Test package dependency checking functionality."""
    # Create a temporary dependencies file
    deps_path = tmp_path / "dependencies.json"
    deps_content = {
        "requests": "2.25.1",
        "pytest": "6.2.4"
    }
    deps_path.write_text(json.dumps(deps_content))
    
    alerts = scanner.check_package_dependencies(str(deps_path))
    assert isinstance(alerts, list)

def test_network_connection_monitoring(scanner, tmp_path):
    """Test network connection monitoring functionality."""
    # Create a temporary log file
    log_path = tmp_path / "network.log"
    log_content = [
        "2024-02-13 12:00:00 - Suspicious connection from 192.168.1.100",
        "2024-02-13 12:01:00 - Normal traffic"
    ]
    log_path.write_text("\n".join(log_content))
    
    alerts = scanner.monitor_network_connections(str(log_path))
    assert isinstance(alerts, list)

def test_report_generation(scanner, sample_alert):
    """Test security report generation."""
    scanner.alerts.append(sample_alert)
    report = scanner.generate_report()
    
    assert isinstance(report, str)
    assert "Supply Chain Security Scan Report" in report
    assert sample_alert.severity in report
    assert sample_alert.description in report