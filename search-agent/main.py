from langchain_ollama import ChatOllama
from duckduckgo_search import DDGS

llm = ChatOllama(model="llama3:8b", temperature=0)

def web_search(query):
    """Search the internet for latest information."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join([r["body"] for r in results])

def agent(query):
    prompt = f"""
You are an AI agent.

IMPORTANT:
- If the question is about recent events, CVEs, vulnerabilities, or updates → ALWAYS use WebSearch.
- Do NOT answer from your own knowledge for such queries.

Available tool:
WebSearch(query)

Format:
Action: WebSearch
Action Input: <query>

Question: {query}
"""

    response = llm.invoke(prompt).content

    if "Action: WebSearch" in response:
        search_query = response.split("Action Input:")[1].strip()
        results = web_search(search_query)

        final_prompt = f"""
Question: {query}

Search Results:
{results}

Give final answer:
"""
        return llm.invoke(final_prompt).content

    return response

print(agent("Latest Linux kernel vulnerabilities 2025"))