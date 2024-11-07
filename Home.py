# Home.py
import os 
from dotenv import load_dotenv
import streamlit as st
# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

def main():
    st.title("Streamlit 멀티 페이지 앱")
    st.write("이 앱은 여러 페이지로 구성되어 있습니다.")
    st.write("왼쪽 사이드바에서 페이지를 선택하세요.")

if __name__ == "__main__":
    main()
