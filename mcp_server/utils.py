import json
from typing import Any, Dict

def format_response(data: Any) -> Dict:
    """Format response for MCP protocol"""
    if hasattr(data, "dict"):
        return data.dict()
    elif isinstance(data, dict):
        return data
    elif isinstance(data, list):
        return {"data": data}
    else:
        return {"result": str(data)}

def validate_user_id(user_id: str) -> bool:
    """Basic user ID validation"""
    if not user_id or not isinstance(user_id, str):
        return False
    if len(user_id) > 100:  # Reasonable length limit
        return False
    return True