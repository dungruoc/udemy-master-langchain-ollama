from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    PromptTemplate
)

from langchain_core.output_parsers import (
    PydanticOutputParser
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


def debug():
    parser = PydanticOutputParser(pydantic_object=Joke)
    instruction = parser.get_format_instructions()
    print(instruction)

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

    chain1 = prompt | llm
    output = chain1.invoke({'query': 'Tell me a joke about the cat'})
    print('ouput content:\n', output.content)

    chain2 = prompt | llm | parser
    output2 = chain2.invoke({'query': 'Tell me a joke about the cat'})
    print('ouput2:\n', output2)

    structured_llm = llm.with_structured_output(Joke)
    output3 = structured_llm.invoke("Tell me a joke about the cat")
    print("output3:\n", output3)

def main():
    debug()

if __name__ == "__main__":
    main()
