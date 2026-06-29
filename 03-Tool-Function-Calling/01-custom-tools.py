from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.messages import (
    HumanMessage
)

from langchain_core.tools import tool


from langchain_core.output_parsers import StrOutputParser

ollama_base_url = 'http://localhost:11434'
llm_model = 'qwen3.5:35b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=llm_model,
    validate_model_on_init=True,
    temperature=0.8,
)

@tool
def add(a: int, b:int) -> int:
    """
    Add two integer numbers

    Args:
    a: int - first integer
    b: int - second integer
    """
    return a + b

@tool
def multiply(a: int, b:int) -> int:
    """
    Multiply two integer numbers

    Args:
    a: int - first integer
    b: int - second integer
    """
    return a * b


print(add)
print(add.invoke({'a': 1, 'b': 2}))

tool_list = [add, multiply]
tool_map = {t.name: t for t in tool_list}

llm_with_tools = llm.bind_tools(tool_list)

# response = llm_with_tools.invoke("what is 2 plus 4?")
# print(response)

# response = llm_with_tools.invoke("what is the production of 3 and 4?")
# print(response)

messages = [HumanMessage("what is 2 plus 4, and what is the production of 3 and 4?")]

need_tool = True

while need_tool:
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    need_tool = False
    tool_calls = response.tool_calls

    for tool in tool_calls:
        ret = tool_map[tool['name']].invoke(tool)
        messages.append(ret)
        need_tool = True

print(messages)