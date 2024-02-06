import streamlit as st
import requests
import json

if not "BASE_URL" in st.session_state:
    st.session_state.BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Todo App",
    page_icon="👋",
)

st.title("Your Todo")
todos = requests.get(f"{st.session_state.BASE_URL}/todos")
if todos.ok:
    for todo in json.loads(todos.text):
        with st.expander(todo["title"]):
            st.markdown(f"**{todo["description"]}**")
            st.markdown(f"- id {todo["id"]}")
