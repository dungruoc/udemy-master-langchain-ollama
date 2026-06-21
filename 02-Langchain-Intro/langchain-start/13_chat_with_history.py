from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

from langchain_core.messages import (
    HumanMessage,
)

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

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

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id=session_id, connection="sqlite:///chat_history.db")


user_id = 'master_langchain_ollama'
history = get_session_history(user_id)
print(history.get_messages())

template = ChatPromptTemplate.from_template("{prompt}")

chain = template | llm | StrOutputParser()

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history
)

config = {
    "configurable": {"session_id": user_id}
}

output = runnable.invoke({'prompt': 'My name is Toto. I am learning Agentic AI.'}, config=config)
print(output)

output = runnable.invoke({'prompt': 'Do you remember my name?'}, config=config)
print("Next message:\n", output)

print(history.get_messages())
history.clear()
print(history.get_messages())


