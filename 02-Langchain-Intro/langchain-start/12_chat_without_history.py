from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import StrOutputParser

ollama_base_url = 'http://localhost:11434'
# model = 'lfm2.5'
model = 'nemotron3:33b'
# model = 'qwen3.5:35b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=model,
    validate_model_on_init=True,
    temperature=0.8,
)

template = ChatPromptTemplate.from_template("{prompt}")

chain = template | llm | StrOutputParser()

output = chain.invoke({'prompt': 'My name is Toto. I am learning Agentic AI.'})
print(output)

output = chain.invoke({'prompt': 'Do you remember my name?'})
print("Next message:\n", output)
