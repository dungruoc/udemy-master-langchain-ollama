import streamlit as st

st.title("Text Inputs")

input_name = st.text_input(label="Enter your name:")
st.write(input_name)

feedback = st.text_area("Enter your feedbacks:")
st.write(feedback)

age = st.number_input("Enter your age:", step=1)
print(type(age))

input_date = st.date_input("Select a date:")
st.write(input_date)

input_time = st.time_input("selec time:")
st.write(input_time)

input_color = st.color_picker("select a color:", "#ff0000")
st.write(input_color)
