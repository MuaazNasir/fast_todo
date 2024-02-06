import streamlit as st
import requests
import json

if not "BASE_URL" in st.session_state:
    st.session_state.BASE_URL = "https://fast-todo-seven.vercel.app"

st.set_page_config(
    page_title="Todo App",
    page_icon="👋",
)

st.title("Your Todo")
todos = requests.get("{}/todos".format(st.session_state.BASE_URL))
if todos.ok:
    for todo in json.loads(todos.text):
        with st.expander(todo["title"]):
            st.markdown("**{}**".format(todo["title"]))
            st.markdown("- id {}".format(todo["id"]))
