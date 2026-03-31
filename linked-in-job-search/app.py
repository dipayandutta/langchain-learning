from flask import Flask, request, render_template_string
import json
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

app = Flask(__name__)

# -------------------------------
# Setup
# -------------------------------
tavily = TavilyClient()

@tool
def search_query(query: str) -> dict:
    """Search for information on the web using Tavily"""
    return tavily.search(query=query)

llm = ChatOllama(model="qwen2.5:7b", temperature=0)
agent = create_agent(model=llm, tools=[search_query])


# -------------------------------
# Extract Tool Output
# -------------------------------
def extract_tool_json(messages):
    for msg in messages:
        if isinstance(msg, ToolMessage):
            try:
                return json.loads(msg.content)
            except:
                return None
    return None


# -------------------------------
# Process Results
# -------------------------------
def process_results(data):
    results = []

    for item in data.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content")
        })

    return results


# -------------------------------
# HTML Template
# -------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Job Results</title>
</head>
<body>

<h2>Results for: {{ query }}</h2>
<hr>

{% for item in results %}
    <h1>{{ item.title }}</h1>
    <h2>{{ item.url }}</h2>
    <h4>{{ item.content }}</h4>
    <hr>
{% endfor %}

</body>
</html>
"""


# -------------------------------
# Route
# -------------------------------
@app.route("/")
def home():
    query = request.args.get("q", "AI jobs in India")

    result = agent.invoke({
        "messages": [
            HumanMessage(content=f"Search for {query}")
        ]
    })

    tool_data = extract_tool_json(result.get("messages", []))

    if not tool_data:
        return "<h2>Error fetching data</h2>"

    results = process_results(tool_data)

    return render_template_string(
        HTML_TEMPLATE,
        results=results,
        query=query
    )


# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)