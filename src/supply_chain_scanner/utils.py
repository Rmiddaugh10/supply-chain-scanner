"""Utility functions for the supply chain scanner."""

import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON content as dictionary or None if error occurs
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {e}")
        return None

def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path where to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {e}")
        return False

def ensure_directory(directory: str) -> bool:
    """Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Directory path to check/create
        
    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = {
        'scan_intervals': {'containers', 'dependencies'},
        'alert_thresholds': {'high', 'medium', 'low'}
    }
    
    try:
        for section, fields in required_fields.items():
            if section not in config:
                logger.error(f"Missing required section: {section}")
                return False
            
            for field in fields:
                if field not in config[section]:
                    logger.error(f"Missing required field: {section}.{field}")
                    return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating config: {e}")
        return False