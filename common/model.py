import streamlit as st
from langchain_openai import ChatOpenAI

@st.cache_resource
def get_chat_openai(model_id:str="gpt-4o-mini"):
    model = ChatOpenAI(
        model=model_id
        )
    return model
