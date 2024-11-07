import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import faiss

@st.cache_resource
def get_pdf_search():# 저장된 데이터를 로드
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local(
        folder_path="data/faiss_db",
        index_name="faiss_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
    return db.as_retriever(
        search_type="mmr", search_kwargs={"k": 6, "lambda_mult": 0.25, "fetch_k": 10}
)