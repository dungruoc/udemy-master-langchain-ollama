from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    PromptTemplate
)

from langchain_core.output_parsers import (
    JsonOutputParser
)

from typing import (
    Optional
)

from pydantic import (
    BaseModel,
    Field
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

class Joke(BaseModel):
    """
        Joke to tell people
    """

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(description="The rating of the joke, from 1 to 10")


parser = JsonOutputParser(pydantic_object=Joke)
print(parser.get_format_instructions())


prompt = PromptTemplate(
    template='''
        Answer the user query with a joke. Here is your formatting instruction:
        {format_instruction}

        Query: {query}

        Answer:''',
    input_variables=['query'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

print(prompt)

chain = prompt | llm

output = chain.invoke({'query': 'Tell me a joke about the dog'})
print("output content:\n", output.content)


chain = prompt | llm | parser
output = chain.invoke({'query': 'Tell me a joke about the dog'})
print("output:\n", output)
