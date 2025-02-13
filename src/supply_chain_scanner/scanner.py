#!/usr/bin/env python3
"""
Supply Chain Security Scanner
A tool designed to monitor and analyze supply chain security risks.
Features:
- Container manifest validation
- Package dependency checking
- Network connection monitoring
- Suspicious pattern detection
"""

import json
import re
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SecurityAlert:
    """Data class for security alerts."""
    timestamp: str
    severity: str
    category: str
    description: str
    affected_component: str
    recommendation: str

class SupplyChainScanner:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the scanner with configuration."""
        self.alerts: List[SecurityAlert] = []
        self.config = self._load_config(config_path)
        self.vulnerability_patterns = [
            r"password\s*=\s*['|\"](?![*]+)[^'\"]+['|\"]",  # Hardcoded passwords
            r"aws_access_key.*=.*['|\"][A-Za-z0-9+/=]+['|\"]",  # AWS keys
            r"api[_-]key.*=.*['|\"][A-Za-z0-9+/=]+['|\"]"  # API keys
        ]

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return {
                "scan_intervals": {"containers": 3600, "dependencies": 86400},
                "alert_thresholds": {"high": 8, "medium": 5, "low": 2}
            }

    def scan_container_manifest(self, manifest_path: str) -> List[SecurityAlert]:
        """Scan container manifest for security issues."""
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            alerts = []
            
            # Check for outdated base images
            if 'baseImage' in manifest:
                if self._is_outdated_base_image(manifest['baseImage']):
                    alerts.append(
                        SecurityAlert(
                            timestamp=datetime.now().isoformat(),
                            severity="HIGH",
                            category="Container Security",
                            description=f"Outdated base image detected: {manifest['baseImage']}",
                            affected_component="Container Base Image",
                            recommendation="Update to latest secure base image version"
                        )
                    )

            # Check for unauthorized sources
            if 'imageSources' in manifest:
                for source in manifest['imageSources']:
                    if not self._is_approved_source(source):
                        alerts.append(
                            SecurityAlert(
                                timestamp=datetime.now().isoformat(),
                                severity="MEDIUM",
                                category="Supply Chain Security",
                                description=f"Unauthorized image source detected: {source}",
                                affected_component="Container Image Source",
                                recommendation="Use only approved container registries"
                            )
                        )

            return alerts
        except Exception as e:
            logger.error(f"Error scanning container manifest: {e}")
            return []

    def check_package_dependencies(self, dependencies_file: str) -> List[SecurityAlert]:
        """Check package dependencies for known vulnerabilities."""
        try:
            with open(dependencies_file, 'r') as f:
                dependencies = json.load(f)
            
            alerts = []
            
            for pkg, version in dependencies.items():
                vulns = self._check_vulnerability_database(pkg, version)
                for vuln in vulns:
                    alerts.append(
                        SecurityAlert(
                            timestamp=datetime.now().isoformat(),
                            severity=vuln['severity'],
                            category="Dependency Security",
                            description=f"Vulnerability found in {pkg} version {version}",
                            affected_component=f"Package: {pkg}",
                            recommendation=f"Upgrade to version {vuln['safe_version']}"
                        )
                    )
            
            return alerts
        except Exception as e:
            logger.error(f"Error checking dependencies: {e}")
            return []

    def monitor_network_connections(self, log_file: str) -> List[SecurityAlert]:
        """Monitor network connections for suspicious patterns."""
        try:
            with open(log_file, 'r') as f:
                logs = f.readlines()
            
            alerts = []
            suspicious_patterns = {
                r'\b(?:\d{1,3}\.){3}\d{1,3}\b': "Suspicious IP address",
                r'((wget|curl)\s+http)': "Unauthorized download attempt",
                r'(\\x[0-9a-fA-F]{2}){4,}': "Potential shellcode detected"
            }
            
            for line in logs:
                for pattern, alert_type in suspicious_patterns.items():
                    if re.search(pattern, line):
                        alerts.append(
                            SecurityAlert(
                                timestamp=datetime.now().isoformat(),
                                severity="HIGH",
                                category="Network Security",
                                description=f"{alert_type} detected",
                                affected_component="Network Traffic",
                                recommendation="Investigate suspicious network activity"
                            )
                        )
            
            return alerts
        except Exception as e:
            logger.error(f"Error monitoring network connections: {e}")
            return []

    def _is_outdated_base_image(self, image: str) -> bool:
        """Check if container base image is outdated."""
        # Implementation would include version checking against known good versions
        return False

    def _is_approved_source(self, source: str) -> bool:
        """Verify if image source is from approved registry."""
        approved_sources = [
            "registry.fedex.com",
            "gcr.io/fedex-prod",
            "docker.io/fedex"
        ]
        return any(approved in source for approved in approved_sources)

    def _check_vulnerability_database(self, package: str, version: str) -> List[Dict]:
        """Check package against vulnerability database."""
        # This would typically query a vulnerability database (e.g., NVD)
        # Mockup implementation for demonstration
        return []

    def generate_report(self) -> str:
        """Generate a security report from collected alerts."""
        report = ["Supply Chain Security Scan Report", "=" * 30, ""]
        
        severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for alert in self.alerts:
            severity_counts[alert.severity] += 1
            
        report.append("Summary:")
        for severity, count in severity_counts.items():
            report.append(f"- {severity} severity alerts: {count}")
        
        report.append("\nDetailed Alerts:")
        for alert in self.alerts:
            report.extend([
                f"\nTimestamp: {alert.timestamp}",
                f"Severity: {alert.severity}",
                f"Category: {alert.category}",
                f"Description: {alert.description}",
                f"Affected Component: {alert.affected_component}",
                f"Recommendation: {alert.recommendation}",
                "-" * 30
            ])
        
        return "\n".join(report)

def main():
    """Main execution function."""
    scanner = SupplyChainScanner()
    
    # Scan container manifests
    container_alerts = scanner.scan_container_manifest("manifest.json")
    scanner.alerts.extend(container_alerts)
    
    # Check dependencies
    dependency_alerts = scanner.check_package_dependencies("dependencies.json")
    scanner.alerts.extend(dependency_alerts)
    
    # Monitor network
    network_alerts = scanner.monitor_network_connections("network.log")
    scanner.alerts.extend(network_alerts)
    
    # Generate and print report
    report = scanner.generate_report()
    print(report)
    
    # Save report to file
    with open(f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
        f.write(report)

if __name__ == "__main__":
    main()
