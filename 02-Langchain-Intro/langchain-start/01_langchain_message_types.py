from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

ollama_base_url = 'http://localhost:11434'
model = 'gpt-oss:20b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=model,
    validate_model_on_init=True,
    temperature=0.8,
    num_predict=256
)

print(llm.invoke("Hello"))

def main():
    messages = [
        SystemMessage(content="You are a helpful translator. Translate the user sentence to French."),
        HumanMessage(content="I love programming.")
    ]
    res = llm.invoke(messages)
    print(res)



if __name__ == "__main__":
    main()
