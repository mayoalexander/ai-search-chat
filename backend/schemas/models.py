from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class QueryType(str, Enum):
    COOKING = "cooking"
    NON_COOKING = "non_cooking"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    query_type: Optional[QueryType] = None
    reasoning_chain: Optional[List[str]] = None
    cookware_validated: Optional[bool] = None

class AgentState(BaseModel):
    input: str
    query_type: Optional[QueryType] = None
    reasoning_chain: List[str] = []
    recipe_content: Optional[str] = None
    cookware_check_result: Optional[Dict[str, Any]] = None
    final_response: Optional[str] = None