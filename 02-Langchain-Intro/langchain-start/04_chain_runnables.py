from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
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


def get_first_chain():
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

def get_second_chain():
    analysis_prompt = ChatPromptTemplate.from_template('''
        Analyse the following text: {response}
        Your need to tell me that how difficult it is to understand.
        Answer in one sentence only.
    ''')

    return analysis_prompt | llm | StrOutputParser()


def debug():
    story_chain = get_first_chain()
    output = story_chain.invoke({
        'school': 'phd',
        'topics': 'solar system',
        'points': 5
    })
    print(output)
    fact_check_chain = get_second_chain()
    output = fact_check_chain.invoke({'response': output})
    print(output)

def chain_chain():
    story_chain = get_first_chain()
    fact_check_chain = get_second_chain()
    chain = {'response': story_chain} | fact_check_chain
    output = chain.invoke({
        'school': 'phd',
        'topics': 'solar system',
        'points': 5
    })
    print(output)

def main():
    debug()
    chain_chain()


if __name__ == '__main__':
    main()