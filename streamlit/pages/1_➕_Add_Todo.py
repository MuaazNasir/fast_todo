import streamlit as st
import requests
import json


st.set_page_config(
    page_title="Add Todo",
    page_icon="➕"
)

st.title("create todo")
title = st.text_input("Enter Todo Title")
description = st.text_area("Enter Todo Description")
if st.button("Add Todo"):
    response = requests.post(f"{st.session_state.BASE_URL}/todos/", json={"title": title, "description": description})
    if response.status_code == 200:
        st.success("Todo added successfully")
        st.info(f"New Todo Id is {json.loads(response.text)["id"]}",icon="ℹ️")