from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

from langchain_core.runnables import (
    RunnableParallel
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


def fact_chain():
    system = SystemMessagePromptTemplate.from_template('''
        You are a {school} teacher. Your answer in short sentences.
    ''')
    human = HumanMessagePromptTemplate.from_template('''
        Tell me a bout the {topics} in {points} points.
    ''')
    messages = [
        system, human
    ]
    template = ChatPromptTemplate(messages)
    return template | llm | StrOutputParser()

def poem_chain():
    prompt = ChatPromptTemplate.from_template('''
        Write a poem on {topics} in {sentences} lines.
    ''')
    return prompt | llm | StrOutputParser()


def main():
    chain = RunnableParallel(fact=fact_chain(), poem=poem_chain())
    output = chain.invoke({
        'topics': 'solar system',
        'sentences': 5,
        'school': 'phd',
        'points': 5
    })
    print(output['fact'])
    print(output['poem'])


if __name__ == '__main__':
    main()