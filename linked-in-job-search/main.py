from dotenv import load_dotenv
import json 
load_dotenv()
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools  import tool
from langchain_core.messages import HumanMessage,ToolMessage
from tavily import TavilyClient

tavily = TavilyClient()

@tool
def search_query(query: str) -> dict:
    """Search for information on the web"""
    print(f"[TOOL] Searching for: {query}")
    #return tavily.search(query=query)   # return dict directly
    response = tavily.search(query=query)
    '''
    return {
        "results": [
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"]
            }
            for result in response["results"]
        ]
    }
    '''
    return  response 

llm = ChatOllama(model="qwen2.5:7b", temperature=0)
agent = create_agent(model=llm, tools=[search_query])


#----------------
# JSON Extractor
#----------------

def extract_tool_json(messages):
    for message in messages:
        if isinstance(message,ToolMessage):
            try:
                return json.loads(message.content)
            except Exception as e:
                print(f"Error parsing tool message: {e}")
                return None
    return None

def relavent_data(data):
    # TODO: Implement logic to extract relevant data from the tool output
    if isinstance(data,str):
        data = json.loads(data)
    results = []

    for item in data.get("results",[]):
        results.append({
            "title":item.get("title"),
            "url": item.get("url"),
            "content": item.get("content"),
            "score": item.get("score")
        })
    
    return results

def main():
    query = "Search for top 2 jobs in India as an AI Engineer"
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    #print(result)
    messages = result.get("messages",[])
    tool_data = extract_tool_json(messages)
    if not tool_data:
        print("No tool data found")
        return
    else:
        output = json.dumps(tool_data, indent=2)
        result = relavent_data(output)
    print(result)
    #print(json.dumps(tool_data, indent=2)) # This will print the output in the JSON format


if __name__ == "__main__":
    main()