import requests
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

def search_recipes(query: str) -> str:
    """
    Simple recipe search using a mock API or basic web search.
    In a real implementation, this would use SERP API or a recipe API.
    """
    
    # For demo purposes, return mock recipe data based on common queries
    mock_recipes = {
        "pancakes": """
        Simple Pancakes Recipe:
        
        Ingredients:
        - 1 cup flour
        - 1 egg
        - 1 cup milk
        - 2 tbsp sugar
        - 1 tsp baking powder
        - Pinch of salt
        
        Instructions:
        1. Mix dry ingredients in a bowl
        2. Whisk wet ingredients separately
        3. Combine wet and dry ingredients
        4. Heat frying pan on stovetop
        5. Pour batter and cook until bubbles form
        6. Flip with spatula and cook other side
        
        Equipment needed: Frying pan, stovetop, whisk, spatula
        """,
        
        "pasta": """
        Basic Pasta Recipe:
        
        Ingredients:
        - 200g pasta
        - Salt
        - Water
        - Olive oil
        
        Instructions:
        1. Boil water in a pot with salt
        2. Add pasta and cook according to package directions
        3. Stir occasionally with spoon
        4. Drain using ladle or strainer
        
        Equipment needed: Little pot, stovetop, spoon, ladle
        """,
        
        "stir fry": """
        Vegetable Stir Fry Recipe:
        
        Ingredients:
        - Mixed vegetables
        - Oil
        - Soy sauce
        - Garlic
        
        Instructions:
        1. Heat oil in frying pan on stovetop
        2. Add chopped vegetables (use knife to chop)
        3. Stir frequently with spatula
        4. Add sauce and mix
        
        Equipment needed: Frying pan, stovetop, knife, spatula
        """
    }
    
    query_lower = query.lower()
    
    # Find matching recipe
    for recipe_key, recipe_content in mock_recipes.items():
        if recipe_key in query_lower:
            return recipe_content
    
    # If no specific match, return a general cooking response
    return """
    I can help you with recipes! I have information about pancakes, pasta, and stir fry dishes. 
    You can also ask me "What can I cook with [ingredients]?" and I'll suggest recipes based on your available cookware.
    
    Your available cookware includes: Spatula, Frying Pan, Little Pot, Stovetop, Whisk, Knife, Ladle, Spoon
    """

def get_recipe_suggestions(ingredients: str) -> str:
    """
    Suggest recipes based on available ingredients and cookware.
    """
    ingredients_lower = ingredients.lower()
    
    suggestions = []
    
    if any(ingredient in ingredients_lower for ingredient in ["egg", "flour", "milk"]):
        suggestions.append("Pancakes - requires frying pan, stovetop, whisk, spatula")
    
    if any(ingredient in ingredients_lower for ingredient in ["pasta", "noodles"]):
        suggestions.append("Pasta - requires little pot, stovetop, spoon, ladle")
    
    if any(ingredient in ingredients_lower for ingredient in ["vegetables", "veggies", "onion", "pepper"]):
        suggestions.append("Vegetable Stir Fry - requires frying pan, stovetop, knife, spatula")
    
    if suggestions:
        return f"Based on your ingredients, you can make:\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions)
    else:
        return "I'd be happy to suggest recipes! Could you tell me what specific ingredients you have available?"