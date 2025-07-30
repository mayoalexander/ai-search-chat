from typing import Dict, List, Any
import re

AVAILABLE_COOKWARE = [
    "Spatula",
    "Frying Pan", 
    "Little Pot",
    "Stovetop",
    "Whisk",
    "Knife",
    "Ladle",
    "Spoon"
]

def check_cookware_compatibility(recipe_text: str) -> Dict[str, Any]:
    """
    Analyze recipe text to determine required cookware and check availability.
    Returns compatibility status and missing items.
    """
    recipe_lower = recipe_text.lower()
    
    # Simple keyword matching for required cookware
    cookware_requirements = {
        "frying pan": ["fry", "sauté", "pan-fry", "frying pan"],
        "little pot": ["boil", "simmer", "pot", "saucepan"],
        "stovetop": ["cook", "heat", "boil", "fry", "simmer"],
        "knife": ["chop", "dice", "cut", "slice", "mince"],
        "spatula": ["flip", "turn", "spatula"],
        "whisk": ["whisk", "beat", "mix thoroughly"],
        "ladle": ["ladle", "serve soup"],
        "spoon": ["stir", "mix", "spoon"]
    }
    
    required_items = []
    for cookware, keywords in cookware_requirements.items():
        if any(keyword in recipe_lower for keyword in keywords):
            required_items.append(cookware.title())
    
    # Check availability
    available_set = set([item.lower() for item in AVAILABLE_COOKWARE])
    required_set = set([item.lower() for item in required_items])
    
    missing_items = [item.title() for item in required_set if item not in available_set]
    can_cook = len(missing_items) == 0
    
    return {
        "can_cook": can_cook,
        "required_cookware": required_items,
        "available_cookware": AVAILABLE_COOKWARE,
        "missing_cookware": missing_items,
        "analysis": f"Recipe requires: {', '.join(required_items)}. Missing: {', '.join(missing_items) if missing_items else 'None'}"
    }