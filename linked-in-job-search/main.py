from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools  import tool
from langchain_core.messages import HumanMessage
from tavily import TavilyClient

tavily = TavilyClient()

@tool
def search_query(query: str) -> dict:
    """Search for information on the web"""
    print(f"[TOOL] Searching for: {query}")
    return tavily.search(query=query)   # return dict directly

llm = ChatOllama(model="qwen2.5:7b", temperature=0)
agent = create_agent(model=llm, tools=[search_query])


def main():
    result = agent.invoke({"messages": [HumanMessage(content="Search for top 5 jobs in India as an AI Engineer")]})
    print(result)


if __name__ == "__main__":
    main()