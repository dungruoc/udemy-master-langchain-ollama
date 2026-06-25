import streamlit as st
from pypdf import PdfReader

import chat_tools

st.title("Chat with your documents")

st.session_state.uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

def init_state():

    if "upload_id" not in st.session_state:
        st.session_state.upload_id = None

    if "pdf_pages" not in st.session_state:
        st.session_state.pdf_pages = []

    if "context_data" not in st.session_state:
        st.session_state.context_data = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "context_summary" not in st.session_state:
        st.session_state.context_summary = None

init_state()

def clean_conversation():
    st.session_state.chat_history = []

def clean_all():
    st.session_state.upload_id = None
    st.session_state.pdf_pages = []
    st.session_state.text_summary.text("Summary")
    st.session_state.context_data = None
    clean_conversation()

def display_pdf(tab, uploaded_pdf):
    with tab:
        st.subheader("Native PDF Viewer")
        # 2. Render the PDF directly using Streamlit's native st.pdf
        st.pdf(uploaded_pdf)

def read_pdf_content(uploaded_pdf):
    pdf_reader = PdfReader(uploaded_pdf)
    return [page.extract_text() for page in pdf_reader.pages]

def display_parsed_pdf(tab, pdf_pages):
    with tab:
        st.subheader("Extracted Text Content")
        # 3. Read and parse the file object using pypdf
        
        # Loop through pages and extract text
        for page_num, page in enumerate(pdf_pages):
            with st.expander(f"Page {page_num + 1}"):
                if page:
                    st.write(page)
                else:
                    st.info("No extractable text found on this page.")


# Create two tabs: one to view the PDF structure, one to read text
view_tab, parsed_tab = st.tabs(["View PDF Document", "Extract Text Content"])

st.session_state.text_summary = st.empty()
st.session_state.text_summary.markdown("# Summary")

if st.session_state.uploaded_pdf is not None:
    if st.session_state.upload_id is None or st.session_state.upload_id != st.session_state.uploaded_pdf.file_id:
        st.session_state.pdf_pages = read_pdf_content(st.session_state.uploaded_pdf)
        st.session_state.context_data = chat_tools.multiround_shorten_text([page for page in st.session_state.pdf_pages if page is not None])
        print("{0} chars, {1} pages".format(len(st.session_state.context_data), len(st.session_state.pdf_pages)))
        st.session_state.upload_id = st.session_state.uploaded_pdf.file_id
        st.session_state.context_summary = chat_tools.make_text_summary(st.session_state.context_data)
    st.session_state.text_summary.markdown(st.session_state.context_summary)
    display_pdf(view_tab, st.session_state.uploaded_pdf)
    display_parsed_pdf(parsed_tab, st.session_state.pdf_pages)
    st.markdown(st.session_state.context_data)
else:
    clean_all()

if st.button("Reset Conversation"):
    clean_conversation()

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

input_prompt = st.chat_input("Enter your question here!")
if input_prompt:
    st.session_state.chat_history.append({'role': 'user', 'content': input_prompt})

    with st.chat_message("user"):
        st.markdown(input_prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chat_tools.chat_with_document(st.session_state.context_data, input_prompt))

    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
