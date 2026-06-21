from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    PromptTemplate
)

from langchain_core.output_parsers import (
    CommaSeparatedListOutputParser
)


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


parser = CommaSeparatedListOutputParser()
print("format instruction:\n", parser.get_format_instructions())


prompt = PromptTemplate(
    template='''
        Answer the user query with a list of values. Here is your formatting instruction:
        {format_instruction}

        Query: {query}

        Answer:''',
    input_variables=['query'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

print("prompt:\n", prompt)

chain = prompt | llm | parser

output = chain.invoke({'query': '''Generate seo keywords for my website. The site's content is about NLP and LLLM'''})
print(output)
