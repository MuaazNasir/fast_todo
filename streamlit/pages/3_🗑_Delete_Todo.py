import streamlit as st
import requests


st.set_page_config(
    page_title="Delete Todo",
    page_icon="🗑",
)

st.title("Delete Todo")
todo_id = st.number_input("Todo ID", step=1,min_value=1)

if st.button("Delete"):
    todo = requests.get(f"{st.session_state.BASE_URL}/todos/{todo_id}")
    if todo.ok:
        response = requests.delete(f"{st.session_state.BASE_URL}/todos/{todo_id}")
        if response.ok:
            st.success("Todo deleted successfully")
    else :
        st.error("Invalid ID")
