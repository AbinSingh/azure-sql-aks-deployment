import streamlit as st
import requests

st.title("AKS User Registration")

username = st.text_input("Enter username")

if st.button("Submit"):

    response = requests.post(
        "http://backend-service/users",
        json={"username": username}
    )

    st.write(response.json())