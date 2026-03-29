'''
Program :- To create a basic web search agent
Description: This program demonstrates how to create a simple AI agent using LangChain
that can use tools to perform web searches. The agent uses the ReAct pattern
(Reasoning + Acting) to decide when and how to use tools.

Architecture Overview:
- LLM (Ollama) serves as the reasoning engine
- Tool (search_query) provides web search capability
- Agent orchestrates the interaction between LLM and tools

Flow: User Query → Agent Reasoning → Tool Usage → Result → Final Answer
'''

# =============================================================================
# IMPORTS AND ENVIRONMENT SETUP
# =============================================================================

from dotenv import load_dotenv  # Load environment variables from .env file

load_dotenv()  # Load API keys and configuration from environment

from langchain.agents import create_agent  # LangChain agent creator function
from langchain.tools import tool  # Decorator to convert functions to agent tools
from langchain_core.messages import HumanMessage  # Message class for user input
from langchain_ollama import ChatOllama  # Ollama integration for local LLMs


# =============================================================================
# TOOL DEFINITION
# =============================================================================

# The @tool decorator converts a regular Python function into a LangChain tool
# Tools are functions that agents can use to interact with external systems
# Each tool must have a docstring that describes what it does - this helps the LLM
# understand when and how to use the tool
@tool
def search_query(query: str) -> str:
    """Search for information on the web
    
    Args:
        query (str): The search query string
        
    Returns:
        str: Search results as a string
        
    Note: This is a mock implementation that returns a fixed response.
          In a real implementation, this would connect to a search API like Tavily.
    """
    print(f"[TOOL] Searching for: {query}")  # Debug output to show tool usage
    # Mock response - in real scenario, this would call an actual search API
    return "Pune weather is sunny"


# =============================================================================
# AGENT SETUP AND CONFIGURATION
# =============================================================================

# Step 1: Initialize the Language Model (LLM)
# We're using Ollama with qwen2.5:7b model as our reasoning engine
# temperature=0 makes the model deterministic (same input = same output)
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# Step 2: Define the tools available to the agent
# The agent can only use tools that are explicitly provided to it
# Here we're giving it access to our search_query tool
tools = [search_query]

# Step 3: Create the agent
# The create_agent function combines:
# - The LLM (for reasoning)
# - The tools (for acting)
# - Built-in prompt templates for ReAct (Reasoning + Acting)
agent = create_agent(model=llm, tools=[search_query])

# What happens inside create_agent:
# 1. Creates a prompt template that includes tool descriptions
# 2. Sets up the ReAct reasoning loop
# 3. Configures the agent to call tools when needed
# 4. Handles the conversation flow between user, agent, and tools


# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def main():
    """
    Main function that demonstrates the agent in action.
    
    Process Flow:
    1. User question is wrapped in a HumanMessage
    2. Agent receives the message and starts reasoning
    3. Agent decides if it needs to use a tool
    4. If needed, agent calls the search_query tool
    5. Agent receives tool results and continues reasoning
    6. Agent provides final answer based on available information
    """
    
    # Create a human message with the user's question
    # The agent will process this message and decide whether to use tools
    user_question = "What is the weather in Pune?"
    
    print(f"\n{'='*60}")
    print("AGENT EXECUTION STARTED")
    print(f"{'='*60}")
    print(f"User Question: {user_question}")
    print(f"{'='*60}\n")
    
    # Invoke the agent with the user's question
    # The agent will:
    # 1. Analyze the question
    # 2. Decide if it needs to use the search tool
    # 3. Execute the tool if needed
    # 4. Process the tool results
    # 5. Generate a final response
    result = agent.invoke({"messages": HumanMessage(content=user_question)})
    
    print(f"\n{'='*60}")
    print("AGENT EXECUTION COMPLETED")
    print(f"{'='*60}")
    print("Final Result:")
    print(result)
    print(f"{'='*60}\n")

# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    """
    Entry point of the program.
    This ensures the main() function only runs when the script is executed directly.
    """
    main()


# =============================================================================
# FLOWCHART OF THE AGENT PROCESS
# =============================================================================

'''
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT EXECUTION FLOWCHART                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   User Question     │
                    │ "What is weather    │
                    │  in Pune?"          │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │                     │
                    │   AGENT THINKING    │
                    │ "I need to find     │
                    │ weather info for    │
                    │ Pune"              │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   AVAILABLE TOOLS   │
                    │ • search_query()   │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   AGENT DECIDES     │
                    │ "I should use       │
                    │ search_query tool"  │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │     ACTION          │
                    │   search_query(     │
                    │ "Pune weather")    │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   TOOL EXECUTION    │
                    │ [TOOL] Searching    │
                    │ for: Pune weather   │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   TOOL RESULT       │
                    │ "Pune weather is    │
                    │ sunny"             │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   AGENT THINKING    │
                    │ "Based on search    │
                    │ result, I can now   │
                    │ answer the user"   │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   FINAL ANSWER      │
                    │ "The weather in     │
                    │ Pune is sunny"     │
                    └─────────────────────┘


ReAct Pattern in Action:
------------------------

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ THOUGHT  │───▶│  ACTION  │───▶│OBSERVATION│───▶│  THOUGHT  │
│"I need   │    │"Search   │    │"Pune is  │    │"I can    │
│weather"  │    │weather"  │    │sunny"    │    │answer"   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
      │                                         │
      ▼                                         ▼
┌──────────┐                                 ┌──────────┐
│"What tool│                                 │"What did  │
│to use?"  │                                 │I learn?"  │
└──────────┘                                 └──────────┘
      │                                         │
      └─────────────────┬───────────────────────┘
                        ▼
                ┌─────────────────────┐
                │   PROVIDE ANSWER    │
                └─────────────────────┘


Key Components:
---------------

1. LLM (qwen2.5:7b) - The brain that reasons
2. Tool (search_query) - The hands that act
3. Agent - The coordinator that connects brain and hands
4. ReAct Pattern - The thinking process: Thought → Action → Observation


Data Flow:
----------

User Query → Agent → LLM Reasoning → Tool Call → Tool Result → 
           LLM Processing → Final Answer → User


Error Handling:
---------------

- If tool fails, agent tries alternative approaches
- If no tools available, agent answers from general knowledge
- Agent can ask for clarification if query is ambiguous


Extensibility:
-------------

To add more tools:
1. Create new functions with @tool decorator
2. Add them to the tools list
3. Agent will automatically discover and use them

Example additional tools:
- calculator() for math operations
- weather_api() for real weather data
- database_query() for information retrieval
'''
