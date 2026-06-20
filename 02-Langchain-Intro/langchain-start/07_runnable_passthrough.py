from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)

from langchain_core.output_parsers import (
    StrOutputParser
)

ollama_base_url = 'http://localhost:11434'
model = 'gpt-oss:20b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=model,
    validate_model_on_init=True,
    temperature=0.8,
    num_predict=256
)


def char_counts(text: str) -> int:
    return len(text)

def word_counts(text: str) -> int:
    return len(text.split(' '))

def full_chain():
    prompt = ChatPromptTemplate.from_template(
        '''Explain these inputs in 5 sentences:
        {input1}
        and {input2}
        '''
    )
    chain = prompt | llm | StrOutputParser() | {
        "char_count": RunnableLambda(char_counts),
        "word_count": RunnableLambda(word_counts),
        "description": RunnablePassthrough()
    }
    return chain

def debug():
    chain = full_chain()
    output = chain.invoke({
        'input1': 'Earth planet',
        'input2': 'Sun star'
    })
    print(output)

def main():
    debug()


if __name__ == '__main__':
    main()