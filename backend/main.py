from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from schemas.models import ChatRequest, ChatResponse, AgentState, QueryType
from graphs.recipe_agent import recipe_agent

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Recipe Chatbot API",
    description="LangGraph-powered recipe assistant with cookware validation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "message": "AI Recipe Chatbot API is running",
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user queries through the LangGraph agent.
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Initialize agent state
        initial_state = AgentState(
            input=request.message,
            reasoning_chain=[]
        )
        
        # Run the agent
        result = recipe_agent.invoke(initial_state)
        
        # Extract response
        response_text = result.get("final_response", "I'm sorry, I couldn't process your request.")
        query_type = result.get("query_type")
        reasoning_chain = result.get("reasoning_chain", [])
        cookware_validated = result.get("cookware_check_result", {}).get("can_cook") if result.get("cookware_check_result") else None
        
        logger.info(f"Agent response generated successfully. Query type: {query_type}")
        
        return ChatResponse(
            response=response_text,
            query_type=query_type,
            reasoning_chain=reasoning_chain,
            cookware_validated=cookware_validated
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/cookware")
async def get_available_cookware():
    """Get the list of available cookware."""
    from tools.cookware_checker import AVAILABLE_COOKWARE
    return {
        "available_cookware": AVAILABLE_COOKWARE,
        "count": len(AVAILABLE_COOKWARE)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Enable reload for development
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        reload_dirs=["./"]
    )