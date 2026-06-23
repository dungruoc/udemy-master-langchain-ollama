import streamlit as st

st.title("Working with interactive widget")

if "clicked_count" not in st.session_state:
    st.session_state.clicked_count = 0

def button_clicked():
    st.session_state.clicked_count += 1

st.button("Click me", on_click = button_clicked)
st.write("Button clicked", st.session_state.clicked_count)

if "check_box_status" not in st.session_state:
    st.session_state.check_box_status = False

def checkbox_changed_hdl():
    st.session_state.check_box_status = not st.session_state.check_box_status

checked = st.checkbox("Check option", value=st.session_state.check_box_status, key="my_checkbox", on_change=checkbox_changed_hdl)
st.write("checked:", st.session_state.check_box_status)
st.write("checked:", checked)


multiselected = st.multiselect("Choose multiple options:", [
    "NLP", "GenAI", "DL", "Agentic"
])

st.write("your selections:", multiselected)

rating = st.slider("Give your rating:", min_value=1, max_value=5, step=1)
st.write("your rating:", rating)