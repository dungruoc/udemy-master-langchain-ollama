import streamlit as st
import time

st.title("Status & Progress")

placeholder = st.empty()
placeholder.text("This will be changed after a while")
time.sleep(2.0)
placeholder.text("Text changed")

progress = st.progress(0)
status_text = st.empty()
for i in range(100):
    time.sleep(0.05)
    progress.progress(i)
    status_text.text(f"Progress: {i}")
status_text.text(f"Progress: Done")