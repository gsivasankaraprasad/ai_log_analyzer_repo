
import streamlit as st

st.set_page_config(page_title="Streamlit Test")

st.title("Hello! Streamlit is Working")
st.success("Your Streamlit application is running successfully.")

st.write("Testing the AI Log Analyzer environment.")

number = st.number_input("Enter a number", min_value=1, value=10)

st.write("Your number is:", number)
