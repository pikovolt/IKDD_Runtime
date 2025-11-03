"""
Shared utility functions for IKDD Runtime v0.2
"""
import yaml
from typing import Any, Dict

def load_yaml(path: str) -> Dict[str, Any]:
    """Load YAML file and return parsed content."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
