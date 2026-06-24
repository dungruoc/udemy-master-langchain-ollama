import streamlit as st

from chat_module import stream_chat, clear_history

st.title("My Chatbot")

ollama_base_url = 'http://localhost:11434'
# model = 'lfm2.5'
model = 'nemotron3:33b'
# model = 'qwen3.5:35b'

st.write(f"Chat with me, powered by Ollama/{model}")

user_id = "hello_user"

if st.button("Reset Conversation"):
    print("cleaning history")
    clear_history(user_id)
    st.session_state.chat_history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


input_prompt = st.chat_input("what is going?")
st.write(f"sesssion chat {user_id}")

if input_prompt:
    st.session_state.chat_history.append({'role': 'user', 'content': input_prompt})

    with st.chat_message("user"):
        st.markdown(input_prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(stream_chat(user_id, input_prompt))

    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
