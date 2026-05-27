from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
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



def main():
    system = SystemMessagePromptTemplate.from_template("You are a helpful translator. Translate the user sentence to {language}.")
    human = HumanMessagePromptTemplate.from_template("I love programming.")
    print(system)
    print(system.format(language='French'))

    messages = [
        system, human
    ]
    template = ChatPromptTemplate(messages)
    prompt = template.invoke({'language': 'Vietnamese'})
    print(prompt)
    res = llm.invoke(prompt)
    print(res)



if __name__ == "__main__":
    main()
