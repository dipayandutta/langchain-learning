from dotenv import load_dotenv
import json
import ast

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from tavily import TavilyClient

tavily = TavilyClient()


@tool
def search_query(query: str) -> dict:
    """Search for information on the web"""
    print(f"[TOOL] Searching for: {query}")
    return tavily.search(query=query)   # return dict directly


llm = ChatOllama(model="qwen2.5:7b", temperature=0)
agent = create_agent(model=llm, tools=[search_query])


# -----------------------------
# RESPONSE PARSER
# -----------------------------
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


# -----------------------------
# TOOL OUTPUT PARSER (IMPORTANT)
# -----------------------------
def extract_weather(tool_outputs):
    if not tool_outputs:
        return None

    raw = tool_outputs[0]

    # Step 1: Ensure dict
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except:
            return {"error": "Invalid JSON"}
    else:
        data = raw  # already dict

    # Step 2: Get first result
    results = data.get("results", [])
    if not results:
        return {"error": "No results found"}

    content_str = results[0].get("content")

    # Step 3: Parse inner content safely
    try:
        content = ast.literal_eval(content_str)
    except Exception:
        return {"error": "Failed to parse content"}

    location = content.get("location", {})
    current = content.get("current", {})

    city_name = location.get("name")
    temp_c    = current.get("temp_c")
    condition = current.get("condition",{}).get("text")
    humidity  = current.get("humidity")
    wind_kph  = current.get("wind_kph")
    
    print("City:", city_name)
    print("Temp:", temp_c)
    print("Condition:", condition)
    print("Humidity:", humidity)
    print("Wind:", wind_kph)
    '''
    # Step 4: Extract exact data
    return {
        "city": city_name,
        "temp_c": temp_c,
        "condition": condition,
        "humidity": humidity,
        "wind_kph": wind_kph,
    }
    '''


def parse_tools(tools_used):
    return [tool["name"] for tool in tools_used]


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("Web Search Agent")

    response = agent.invoke(
        {"messages": [HumanMessage(content="What is the weather in Pune?")]}
    )

    final, tools, outputs = parse_response(response)

    print("\nFinal Answer:", final)

    print("\nTools Used:", parse_tools(tools))

    print("\nRaw Tool Output:", outputs[0])

    # Extract structured data
    weather = extract_weather(outputs)

    print("\nParsed Weather Data:", weather)


if __name__ == "__main__":
    main()