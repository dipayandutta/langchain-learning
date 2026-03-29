from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


@tool
def search_query(query: str) -> str:
    """Search for information on the web
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    print(f"[TOOL] Searching for: {query}")
    return "Pune weather is sunny"


llm = ChatOllama(model="qwen2.5:7b", temperature=0)

agent = create_agent(model=llm, tools=[search_query])


def parse_response(response):
    messages = response["messages"]

    final = messages[-1].content
    tools_used = []
    tool_outputs = []

    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tools_used.extend(msg.tool_calls)

        if msg.__class__.__name__ == "ToolMessage":
            tool_outputs.append(msg.content)

    return final, tools_used, tool_outputs


def parse_tools(tools_used):
    return [tool["name"] for tool in tools_used]


def main():
    print("Web Search Agent")

    response = agent.invoke(
        {"messages": [HumanMessage(content="What is the weather in Pune?")]}
    )

    final, tools, outputs = parse_response(response)

    print("\nFinal Answer:", final)
    parsed_tools = parse_tools(tools)
    print("\nTools Used:", parsed_tools)

    print("\nTool Outputs:", outputs)


if __name__ == "__main__":
    main()
