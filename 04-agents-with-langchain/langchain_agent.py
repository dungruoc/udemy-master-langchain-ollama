from langchain_ollama import ChatOllama

from langchain.agents import create_agent

import agent_tools

ollama_base_url = 'http://localhost:11434'
llm_model = 'qwen3.5:35b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=llm_model,
    validate_model_on_init=True,
    temperature=0.8,
)

system_prompt = """
You are a helpful AI assistant. Use the available tools when needed to answer questions accurately.
If you need search for information, use web_search tool.
Always provide clear and consise answers.
"""

agent = create_agent(model=llm, tools=[agent_tools.web_search], system_prompt=system_prompt)

res = agent.invoke({"messages": "what is the top global news right now about Agentic AI?"})

print(res)
print(res['messages'][-1].content)

