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
llm_model = 'nemotron3:33b'
# llm_model = 'qwen3.5:35b'

llm = ChatOllama(
    base_url=ollama_base_url,
    model=llm_model,
    validate_model_on_init=True,
    temperature=0.8,
)

def make_text_summary(content):
    template = ChatPromptTemplate.from_template("Make a concise summary for the following text. Text: {content}")
    chain = template | llm | StrOutputParser()
    return chain.invoke({'content': content})


def chat_with_document(document, question, words=200):
    system_prompt = SystemMessagePromptTemplate.from_template(
        """You are a helpful assistant, using the provided context to answer the question.
        Use only data from the context to answer. If the question is not relevant to the context, reply that it's out of context.
        Your answer need to be no more than {words} words.
        """
    )
    prompt_template = """
        ### Context:
        {context}
        
        ### Question
        {question}

        ### Answer:"""

    human_prompt = HumanMessagePromptTemplate.from_template(prompt_template)

    messages = [system_prompt, human_prompt]
    prompt = ChatPromptTemplate(messages=messages)
    chain = prompt | llm | StrOutputParser()
    for output in chain.stream({'context': document, 'question': question, "words": words}):
        yield output


def shorten_text(content, max_words):
    simple_model = ChatOllama(
        base_url=ollama_base_url,
        model=llm_model,
        validate_model_on_init=True,
        temperature=0.0,
        think=False
    )

    template = ChatPromptTemplate.from_template(f"Rewrite the following text in less than {max_words} words." +  "Text: {content}")
    chain = template | simple_model | StrOutputParser()
    return chain.invoke({'content': content})


def multiround_shorten_text(pages, max_len=10000):
    content = ""
    i = 0
    shorten_pages = []
    total_len = sum([len(page) for page in pages])
    while total_len > max_len:
        total_len = 0
        while i < len(pages):
            content += ("\n" + pages[i])
            i += 1
            if len(content) >= max_len:
                chunk = shorten_text(content, max_len//20)
                print(f"page {i}: shorten: {len(content)} -> {len(chunk)}")
                shorten_pages.append(chunk)
                total_len += len(chunk)
                content = ""
        pages = shorten_pages
        print(f"new round {len(pages)}/{total_len}")
    return shorten_text("\n".join(pages), max_len//4)
