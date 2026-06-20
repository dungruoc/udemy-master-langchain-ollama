from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.runnables import (
    RunnableLambda
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


def review_chain():
    template = ChatPromptTemplate.from_template('''
    Given the user review below, classify it as either being about "Positive" or "Negative".
    Respond in one word only, either "Positive" or "Negative".

    Review: {review}
    Classification:''')
    return template | llm | StrOutputParser()

def positive_replier_chain():
    template = ChatPromptTemplate.from_template('''
    You are expert in writing reply for positive reviews.
    You may encourage the user to share their experience on scocial media.

    Review: {review}
    Answer:''')
    return template | llm | StrOutputParser()

def negative_replier_chain():
    template = ChatPromptTemplate.from_template('''
    You are expert in writing reply for negative reviews.
    You need first to apologize for the inconvenience caused to the user.
    You need to encourage the user to share their concern to the following email: "udemy@course.com"

    Review: {review}
    Answer:''')
    return template | llm | StrOutputParser()

def route_chain(review):
    if 'positive' in review['sentiment'].lower():
        return positive_replier_chain()
    else:
        return negative_replier_chain()


def full_chain():
    return {'sentiment': review_chain(), 'review': lambda x: x['review']} | RunnableLambda(route_chain)

def debug():
    review = {'review': 'Thank you so much for providing such a greate platform for learning. I am really happy with it.'}
    chain = review_chain()
    output = chain.invoke(review)
    print(output)

    chain = positive_replier_chain()
    output = chain.invoke(review)
    print(output)

    chain = negative_replier_chain()
    output = chain.invoke(review)
    print(output)

    print(route_chain({'sentiment': 'Negative'}))
    print(route_chain({'sentiment': 'Positive'}))

    chain = full_chain()
    output = chain.invoke(review)
    print(output)

    output = chain.invoke({'review': 'The service is not good. To avoid.'})
    print(output)

def main():
    debug()


if __name__ == '__main__':
    main()