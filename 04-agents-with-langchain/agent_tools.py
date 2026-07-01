from ddgs import DDGS

from langchain_core.tools import tool
import json


@tool
def web_search(query: str, num_results: int = 10) -> str:
    """Search the web using DuckDuckGo for getting information from internet

    Args:
        query: search query string
        num_results: number of results to be returned (default: 10)

    Returns:
        Formatted search results, each with the fields:
          - title: for result title
          - href: the hyperlink to the source
          - body: the extracted text
    """

    try:
        results = list(DDGS().text(query, max_results = num_results))
        if results:
            return "\n".join([json.dumps(ret) for ret in results])
        else:
            return "Nothing Found"
    except:
        return "Search Failed"
    

if __name__ == "__main__":
    print(web_search.invoke({"query": "Python programming", "num_results": 3}))