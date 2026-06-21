from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.messages import (
    HumanMessage,
    SystemMessage
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
history.clear()
print(history.get_messages())

system_template = SystemMessagePromptTemplate.from_template("You are a helpful assistant")
human_template = HumanMessagePromptTemplate.from_template("{input_prompt}")

messages = [system_template, MessagesPlaceholder(variable_name='history'), human_template]
prompt = ChatPromptTemplate(messages=messages)

chain = prompt | llm | StrOutputParser()

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input_prompt',
    history_messages_key='history'
)

config = {
    "configurable": {"session_id": user_id}
}

output = runnable.invoke({'input_prompt': 'My name is Toto. I am learning Agentic AI.'}, config=config)
print(output)

output = runnable.invoke({'input_prompt': 'Do you remember my name?'}, config=config)
print("Next message:\n", output)

print(history.get_messages())
history.clear()
print(history.get_messages())


