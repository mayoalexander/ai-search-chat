from langgraph.graph import StateGraph, END
from typing import Dict, Any
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from schemas.models import AgentState, QueryType
from tools.cookware_checker import check_cookware_compatibility
from tools.recipe_searcher import search_recipes, get_recipe_suggestions

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

def classify_query(state: AgentState) -> Dict[str, Any]:
    """Node to classify if query is cooking-related or not."""
    logger.info(f"Classifying query: {state.input}")
    
    classification_prompt = ChatPromptTemplate.from_template("""
    You are a cooking assistant. Determine if the following query is related to cooking, recipes, or food preparation.
    
    Query: {query}
    
    Respond with only 'COOKING' if it's cooking-related, or 'NON_COOKING' if it's not.
    
    Examples:
    - "How do I make pancakes?" -> COOKING
    - "What can I cook with chicken?" -> COOKING  
    - "Recipe for pasta" -> COOKING
    - "What's the weather like?" -> NON_COOKING
    - "How do I fix my car?" -> NON_COOKING
    """)
    
    chain = classification_prompt | llm
    result = chain.invoke({"query": state.input})
    
    query_type = QueryType.COOKING if "COOKING" in result.content else QueryType.NON_COOKING
    reasoning = f"Query classified as: {query_type.value}"
    
    logger.info(reasoning)
    
    return {
        "query_type": query_type,
        "reasoning_chain": state.reasoning_chain + [reasoning]
    }

def handle_non_cooking_query(state: AgentState) -> Dict[str, Any]:
    """Handle non-cooking queries with polite refusal."""
    logger.info("Handling non-cooking query")
    
    response = "I'm a cooking assistant specialized in recipes and food preparation. I can help you with cooking questions, recipe suggestions, and checking if you have the right cookware for dishes. Is there anything cooking-related I can help you with?"
    
    reasoning = "Provided polite refusal for non-cooking query"
    
    return {
        "final_response": response,
        "reasoning_chain": state.reasoning_chain + [reasoning]
    }

def search_recipe_content(state: AgentState) -> Dict[str, Any]:
    """Search for recipe content using external tools."""
    logger.info(f"Searching for recipe content: {state.input}")
    
    # Determine if this is an ingredient-based query or recipe search
    if "what can i cook" in state.input.lower() or "ingredients" in state.input.lower():
        recipe_content = get_recipe_suggestions(state.input)
        reasoning = "Used ingredient-based recipe suggestions"
    else:
        recipe_content = search_recipes(state.input)
        reasoning = "Searched recipe database"
    
    logger.info(f"Recipe search reasoning: {reasoning}")
    
    return {
        "recipe_content": recipe_content,
        "reasoning_chain": state.reasoning_chain + [reasoning]
    }

def validate_cookware(state: AgentState) -> Dict[str, Any]:
    """Validate if user can cook the recipe with available cookware."""
    logger.info("Validating cookware compatibility")
    
    if not state.recipe_content:
        reasoning = "No recipe content to validate cookware against"
        return {
            "cookware_check_result": {"can_cook": True, "analysis": "No specific cookware requirements"},
            "reasoning_chain": state.reasoning_chain + [reasoning]
        }
    
    cookware_result = check_cookware_compatibility(state.recipe_content)
    reasoning = f"Cookware validation: {cookware_result['analysis']}"
    
    logger.info(reasoning)
    
    return {
        "cookware_check_result": cookware_result,
        "reasoning_chain": state.reasoning_chain + [reasoning]
    }

def generate_final_response(state: AgentState) -> Dict[str, Any]:
    """Generate the final response combining recipe and cookware information."""
    logger.info("Generating final response")
    
    if not state.recipe_content or not state.cookware_check_result:
        response = "I encountered an issue processing your request. Please try again."
        reasoning = "Error in recipe processing pipeline"
    else:
        cookware_result = state.cookware_check_result
        
        if cookware_result["can_cook"]:
            response = f"{state.recipe_content}\n\n✅ Good news! You have all the required cookware to make this recipe."
            reasoning = "Generated positive response with recipe and cookware confirmation"
        else:
            missing_items = ", ".join(cookware_result["missing_cookware"])
            response = f"{state.recipe_content}\n\n❌ You're missing some cookware: {missing_items}\n\nYou might want to find alternatives or consider a different recipe that uses your available equipment: {', '.join(cookware_result['available_cookware'])}"
            reasoning = f"Generated response noting missing cookware: {missing_items}"
    
    logger.info(reasoning)
    
    return {
        "final_response": response,
        "reasoning_chain": state.reasoning_chain + [reasoning]
    }

def should_search_recipes(state: AgentState) -> str:
    """Determine if we should search for recipes or handle non-cooking query."""
    return "search_recipes" if state.query_type == QueryType.COOKING else "non_cooking_response"

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("classify", classify_query)
workflow.add_node("non_cooking_response", handle_non_cooking_query)
workflow.add_node("search_recipes", search_recipe_content)
workflow.add_node("validate_cookware", validate_cookware)
workflow.add_node("generate_response", generate_final_response)

# Set entry point
workflow.set_entry_point("classify")

# Add conditional edges
workflow.add_conditional_edges(
    "classify",
    should_search_recipes,
    {
        "search_recipes": "search_recipes",
        "non_cooking_response": "non_cooking_response"
    }
)

# Add linear edges
workflow.add_edge("search_recipes", "validate_cookware")
workflow.add_edge("validate_cookware", "generate_response")
workflow.add_edge("generate_response", END)
workflow.add_edge("non_cooking_response", END)

# Compile the graph
recipe_agent = workflow.compile()