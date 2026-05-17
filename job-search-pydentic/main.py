'''
============================================================================
JOB SEARCH AGENT WITH PYDANTIC SCHEMA VALIDATION
============================================================================

Program Description:
--------------------
This program creates an intelligent job search agent that:
1. Uses LangChain to create an AI agent with web search capabilities
2. Leverages TavilySearch for real-time web search
3. Enforces structured output using Pydantic schemas
4. Returns responses with answers and source citations

Key Features:
- Structured data validation using Pydantic
- Real-time web search via Tavily
- Source citation tracking
- Type-safe responses
- ReAct (Reasoning + Acting) pattern

Technology Stack:
- LangChain: Agent framework
- Ollama: Local LLM (qwen2.5:7b)
- Tavily: Web search API
- Pydantic: Data validation and serialization

============================================================================
DETAILED PROCESS FLOW DIAGRAM
============================================================================

┌─────────────────────────────────────────────────────────────────┐
│                    JOB SEARCH AGENT ARCHITECTURE               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   USER INPUT        │
                    │ "Find data science  │
                    │  jobs in Pune"     │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │                     │
                    │   LANGCHAIN AGENT   │
                    │   (ReAct Pattern)   │
                    │                     │
                    │ 1. THOUGHT:         │
                    │    "I need to       │
                    │    search for jobs" │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   LLM REASONING     │
                    │   (qwen2.5:7b)      │
                    │                     │
                    │ "Should I search    │
                    │ the web? Yes, I     │
                    │ need current data"  │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   TOOL SELECTION    │
                    │                     │
                    │ Available:          │
                    │ • TavilySearch()    │
                    │                     │
                    │ Decision:           │
                    │ "Use TavilySearch"  │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   ACTION EXECUTION  │
                    │                     │
                    │ TavilySearch(       │
                    │ "data science jobs  │
                    │ in Pune")          │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   WEB SEARCH        │
                    │                     │
                    │ • Query Tavily API  │
                    │ • Scrape web pages  │
                    │ • Extract job info  │
                    │ • Collect URLs      │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   SEARCH RESULTS    │
                    │                     │
                    │ Raw data:           │
                    │ • Job titles        │
                    │ • Companies         │
                    │ • Requirements      │
                    │ • Source URLs       │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   LLM PROCESSING    │
                    │                     │
                    │ "Now I need to      │
                    │ format this data    │
                    │ according to        │
                    │ Pydantic schema"    │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   PYDANTIC SCHEMA    │
                    │   VALIDATION         │
                    │                     │
                    │ AgentResponse:      │
                    │ • answer: str       │
                    │ • sources: List[Source] │
                    │                     │
                    │ Source:             │
                    │ • url: str          │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   STRUCTURED OUTPUT │
                    │                     │
                    │ {                   │
                    │   "answer": "Found  │
                    │    5 data science   │
                    │    jobs...",        │
                    │   "sources": [      │
                    │     {"url": "..."}, │
                    │     {"url": "..."}  │
                    │   ]                 │
                    │ }                   │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   FINAL RESPONSE    │
                    │   (Type-safe &       │
                    │    Validated)       │
                    └─────────────────────┘


============================================================================
SIMPLIFIED ASCII FLOW
============================================================================

User Input
    ↓
Agent (LangChain + ReAct)
    ↓
LLM (Qwen via Ollama)
    ↓
LLM Decision: "Need web search"
    ↓
Tool Execution (TavilySearch)
    ↓
Web API Call → Job Data
    ↓
Results returned to LLM
    ↓
Pydantic Schema Validation
    ↓
Structured Response (answer + sources)
    ↓
Final Validated Output


============================================================================
REACT PATTERN IN DETAIL
============================================================================

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ THOUGHT  │───▶│  ACTION  │───▶│OBSERVATION│───▶│  THOUGHT  │
│"I need   │    │"Search   │    │"Found 5   │    │"Format   │
│job info" │    │web for   │    │jobs with  │    │with      │
│          │    │jobs"     │    │sources"   │    │Pydantic" │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
      │                                         │
      ▼                                         ▼
┌──────────┐                                 ┌──────────┐
│"What tool│                                 │"Create   │
│to use?"  │                                 │structured│
│          │                                 │response" │
└──────────┘                                 └──────────┘
      │                                         │
      └─────────────────┬───────────────────────┘
                        ▼
                ┌─────────────────────┐
                │   VALIDATED         │
                │   RESPONSE          │
                └─────────────────────┘

============================================================================
DATA FLOW WITH TYPES
============================================================================

str (User Query) → Agent → LLM → Tool → dict (Raw Results) → 
LLM Processing → AgentResponse (Pydantic) → dict (Final Output)

Type Safety:
- Input: str
- Processing: dict (LLM internal)
- Tool Output: dict (Tavily results)
- Final: AgentResponse (validated Pydantic model)

============================================================================
KEY COMPONENTS INTERACTION
============================================================================

1. Agent (Orchestrator)
   - Manages conversation flow
   - Decides when to use tools
   - Coordinates LLM and tools

2. LLM (Brain)
   - Provides reasoning capabilities
   - Understands user intent
   - Formats responses

3. TavilySearch (Tool)
   - Provides real-time web search
   - Returns current job listings
   - Supplies source URLs

4. Pydantic Schemas (Validator)
   - Ensures data consistency
   - Provides type safety
   - Enables structured output

'''

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

# Pydantic imports for data validation and schema definition
from pydantic import BaseModel, Field  # BaseModel for creating data models, Field for field validation
from typing import List  # Type hint for lists

# Environment and configuration
from dotenv import load_dotenv  # Load environment variables from .env file
load_dotenv()  # Load API keys and configuration

# LangChain core imports
from langchain.agents import create_agent  # Agent creation function
from langchain_ollama import ChatOllama  # Ollama integration for local LLMs
from langchain.tools import tool  # Decorator for creating tools (not used here but imported)
from langchain_core.messages import HumanMessage  # Message class for user input
from langchain_tavily import TavilySearch  # Tavily search tool integration   


# =============================================================================
# PYDANTIC SCHEMA DEFINITIONS
# =============================================================================

class Source(BaseModel):
    """
    Schema for a web source used by the agent.
    
    This model represents a single source citation that the agent
    uses to provide transparency and verifiability for its answers.
    
    Attributes:
        url (str): The URL of the source webpage
    """
    url: str = Field(
        description="The URL of the source webpage where information was found"
    )

class AgentResponse(BaseModel):
    """
    Schema for structured agent responses.
    
    This model enforces a consistent response format that includes
    both the answer to the user's query and the sources used.
    
    Attributes:
        answer (str): The main answer to the user's query
        sources (List[Source]): List of sources used to generate the answer
    """
    answer: str = Field(
        description="The answer to the user's query"
    )
    sources: List[Source] = Field(
        default_factory=list,  # Creates empty list by default
        description="The sources used by the agent to generate the answer"
    )

# Schema Usage:
# - Ensures type safety
# - Provides automatic validation
# - Enables structured output from LLM
# - Makes responses predictable and parseable

# =============================================================================
# AGENT CONFIGURATION AND SETUP
# =============================================================================

# Step 1: Initialize the Language Model (LLM)
# Using Ollama with qwen2.5:7b model as the reasoning engine
# temperature=0 ensures deterministic responses (same input = same output)
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# Step 2: Define available tools for the agent
# TavilySearch provides real-time web search capabilities
# The agent will use this to find current job listings
# Note: TavilySearch() is instantiated without parameters - uses default settings
tools = [TavilySearch()]

# Step 3: Create the agent with structured output capability
# The response_format parameter tells the agent to format its output
# according to the AgentResponse Pydantic schema
# This ensures type-safe, validated responses every time
agent = create_agent(
    model=llm, 
    tools=tools, 
    response_format=AgentResponse  # Enforces structured output
)

# Agent Configuration Details:
# - Model: qwen2.5:7b (7 billion parameter model)
# - Tools: TavilySearch (web search)
# - Response Format: AgentResponse (structured with answer + sources)
# - Pattern: ReAct (Reasoning + Acting)
# - Temperature: 0 (deterministic)

# How create_agent works internally:
# 1. Creates a prompt template that includes tool descriptions
# 2. Sets up the ReAct reasoning loop
# 3. Configures the agent to call tools when needed
# 4. Enforces the specified response format
# 5. Handles the conversation flow between user, agent, and tools

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def main():
    """
    Main function that demonstrates the job search agent in action.
    
    Process Flow:
    1. Get user query from stdin
    2. Create HumanMessage with the query
    3. Invoke agent with the message
    4. Agent follows ReAct pattern:
       - THOUGHT: Analyze the query
       - ACTION: Use TavilySearch if needed
       - OBSERVATION: Process search results
       - THOUGHT: Format response according to schema
    5. Return structured AgentResponse
    6. Display results to user
    
    The agent will automatically:
    - Decide if web search is needed
    - Execute the search tool
    - Extract relevant job information
    - Format the response according to AgentResponse schema
    - Include source citations for transparency
    """
    
    # Get user input for job search query
    # Example: "data science jobs in Pune" or "remote Python developer jobs"
    query = input("Enter your job search query: ")
    
    print(f"\n{'='*60}")
    print("JOB SEARCH AGENT - PROCESSING REQUEST")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")
    
    # Invoke the agent with the user's query
    # The agent will:
    # 1. Analyze the query using the LLM
    # 2. Decide if web search is needed (usually yes for job queries)
    # 3. Execute TavilySearch tool with the query
    # 4. Process the search results
    # 5. Format response according to AgentResponse schema
    # 6. Return validated, structured output
    result = agent.invoke({"messages": HumanMessage(content=query)})
    
    print(f"\n{'='*60}")
    print("AGENT RESPONSE - STRUCTURED OUTPUT")
    print(f"{'='*60}")
    
    # Display the complete result (includes both answer and sources)
    # The result is automatically formatted according to AgentResponse schema
    print("\nComplete Agent Response:")
    print(result)
    
    # Alternative: Access specific fields if needed
    # Uncomment the line below to access just the answer
    # print(f"\nAnswer Only: {result['structured_response'].answer}")
    
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETED")
    print(f"{'='*60}\n")
# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    """
    Entry point of the program.
    
    This ensures the main() function only runs when the script is executed
    directly (not when imported as a module).
    
    Usage:
    1. Ensure Ollama is running with qwen2.5:7b model
    2. Set up Tavily API key in .env file
    3. Run: python main.py
    4. Enter job search query when prompted
    5. Receive structured response with sources
    """
    main()
