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
    response = requests.post("{}/todos/".format(st.session_state.BASE_URL), json={"title": title, "description": description})
    if response.status_code == 200:
        id = json.loads(response.text)["id"]
        st.success("Todo added successfully")
        st.info("New Todo Id is {}".format(id),icon="ℹ️")