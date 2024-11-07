import streamlit as st
import faiss
import numpy as np
import pickle
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
# OpenAI API Key 설정
# 테스트
load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
# LangChain의 OpenAI 모델 클라이언트 설정
client = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")

# 광고 문구 생성 함수
def ask_chatgpt(prompt):
    chat_prompt = ChatPromptTemplate.from_template(prompt)
    response = client.invoke(chat_prompt.format_messages())  # .invoke()로 변경
    return response.content

# FAISS 인덱스 초기화
def initialize_faiss_index():
    index = faiss.IndexFlatL2(768)  # 벡터의 차원 수에 맞게 수정하세요
    return index

# 벡터를 FAISS에 추가하는 함수
def add_to_faiss(index, vectors, ad_copies):
    index.add(np.array(vectors, dtype=np.float32))  # 벡터를 FAISS 인덱스에 추가
    return ad_copies  # 광고 문구를 반환

# Streamlit 페이지 구성
st.set_page_config(page_title="광고 문구 생성 프로그램")
st.header("🎸광고 문구 생성 프로그램")
st.markdown('---')

# 사용자 입력 폼 구성
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("제품명", placeholder=" ")
    strength = st.text_input("제품 특징", placeholder=" ")
    keyword = st.text_input("필수 포함 키워드", placeholder=" ")
with col2:
    com_name = st.text_input("브랜드 명", placeholder="Apple, 올리브영..")
    tone_manner = st.text_input("톤앤 매너", placeholder="발랄하게, 유머러스하게, 감성적으로..")
    value = st.text_input("브랜드 핵심 가치", placeholder="필요 시 입력")

# 광고 문구 생성 버튼
if st.button("광고 문구 생성"):
    prompt = f'''
    아래 내용을 참고해서 광고 문구를 1~2줄짜리 광고 문구 5개 작성해줘:
    - 제품명: {name}
    - 브랜드 명: {com_name}
    - 브랜드 핵심 가치: {value}
    - 제품 특징: {strength}
    - 톤앤 매너: {tone_manner}
    - 필수 포함 키워드: {keyword}
    '''
    ad_copy = ask_chatgpt(prompt)

    # 생성된 광고 문구를 FAISS에 추가
    index = initialize_faiss_index()
    vectors = np.random.rand(5, 768)  # 예시로 랜덤 벡터 생성, 실제로는 모델을 통해 생성한 벡터 사용
    ad_copies = add_to_faiss(index, vectors, ad_copy)

    # 광고 문구를 파일로 저장
    with open("ad_copies.pkl", "wb") as f:
        pickle.dump(ad_copies, f)

    st.info(ad_copy)

# 저장된 광고 문구 불러오기
if st.button("저장된 광고 문구 불러오기"):
    try:
        with open("ad_copies.pkl", "rb") as f:
            loaded_ad_copies = pickle.load(f)
        st.success("광고 문구를 성공적으로 불러왔습니다.")
        st.write(loaded_ad_copies)
    except FileNotFoundError:
        st.warning("ad_copies.pkl 파일이 존재하지 않습니다.") 