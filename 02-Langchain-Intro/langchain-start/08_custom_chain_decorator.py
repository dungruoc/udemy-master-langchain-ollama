from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

from langchain_core.runnables import (
    chain
)

from langchain_core.output_parsers import (
    StrOutputParser
)

ollama_base_url = 'http://localhost:11434'
# model = 'lfm2.5'
model = 'nemotron3:33b'
# model = 'qwen3.5:35b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=model,
    validate_model_on_init=True,
    # temperature=0.8,
    # reasoning=False,
    # num_predict=256
)


def fact_chain():
    system = SystemMessagePromptTemplate.from_template('''
        You are a {school} teacher. Answer in concise and short sentences.
    ''')

    human = HumanMessagePromptTemplate.from_template('''
        Tell me a bout the {topics} in {points} bullet points.
    ''')

    messages = [
        system,
        human
    ]
    
    template = ChatPromptTemplate(messages)
    return template | llm | StrOutputParser()

def poem_chain():
    prompt = ChatPromptTemplate.from_template('''
        Write a poem on {topics} in {sentences} lines.
    ''')
    return prompt | llm | StrOutputParser()

@chain
def custom_chain(params):
    return {
        'fact': fact_chain().invoke(params),
        'poem': poem_chain().invoke(params)
    }


def main():
    output = custom_chain.invoke({
        'topics': 'solar system',
        'sentences': '5',
        'school': 'phd',
        'points': 'five'
    })
    print('fact:\n', output['fact'])
    print('poem:\n', output['poem'])

if __name__ == '__main__':
    main()