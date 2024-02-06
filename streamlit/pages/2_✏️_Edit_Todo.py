import streamlit as st
import requests
from json import loads


st.set_page_config(
    page_title="Edit Todo",
    page_icon="📝",
)

if 'step' not in st.session_state:
    st.session_state.step = 0
if "todo_data" not in st.session_state:
    st.session_state.todo_data = {"title" : "", "description" : ""}


st.title("Edit a Todo")
todo_id = st.number_input("Enter ID",min_value=1,step=1)


if st.button("Go"):
    todo_data = requests.get(f"{st.session_state.BASE_URL}/todos/{todo_id}")
    if not todo_data.ok:
        st.error("Invalid ID")
    else :
        st.session_state.todo_data = todo_data
        st.session_state.step = 1

if st.session_state.step == 1 :
    todo_data = loads(st.session_state.todo_data.text)
    title = st.text_input("Enter New Title",value=todo_data["title"])
    description = st.text_input("Enter New Description",value=todo_data["description"])
    submit = st.button("Submit")
    if  submit:
        response = requests.put(f"{st.session_state.BASE_URL}/todos/{todo_id}",json={"title":title,"description" : description})
        if response.ok :
            st.success("Successfully updated your Todo !")
        else :
            st.error("Failed to update !!")


