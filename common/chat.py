import streamlit as st
from openai import OpenAI # API 통신용 모듈 


# @st.cache_data # 데이터를 caching 처리 
@st.cache_resource # 객체를 caching 처리 
def get_client():
    return OpenAI()

def response_from_llm(prompt, model_id:str="gpt-4o-mini"):
    responses = get_client().chat.completions.create(
        model=model_id,
        messages=[
            {
                "role":"system",
                "content":"""
                    당신은 어시스턴트입니다.
                """
            },
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return responses.choices[0].message.content


