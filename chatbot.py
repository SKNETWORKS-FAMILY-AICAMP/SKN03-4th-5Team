import streamlit as st
from src import *
from dotenv import load_dotenv

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<h1 style="text-align: center;">🤖 LangChain & RAG 사전 🤖</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center;">
        <a href="https://github.com/good593/course_ai/tree/main/3.%20Large%20Language%20Models" 
            style="color: rgba(76, 175, 80, 0.7); text-decoration: none; margin-right: 10px;">
            『📗 SKN 3기 강의 자료 원본』
        </a>
        <div class="tooltip" style="display: inline;">
            ℹ️ 
            <span class="tooltiptext">본 챗봇은 SKN 3기 조경원 강사님의 강의 자료를 기반으로 합니다 :)</span>
        </div>
    </div>
    <style>
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 260px;
            background-color: black;
            color: #fff;
            text-align: center;
            border-radius: 5px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* 아이콘 위에 위치 */
            left: 50%;
            margin-left: -110px; /* 가운데 정렬 */
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
    <br>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

prompt = st.chat_input("LangChain과 RAG의 어떤 부분이 헷갈리나요? 🤔")

if prompt:
    message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    
    if message:
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        
        st.session_state.messages.append(message)

        with st.chat_message(CHATBOT_ROLE.assistant.name):
            assistant_response = st.write_stream(response_from_llm(prompt=generate_rag_prompt(prompt, retrieve_similar_documents(prompt))))

        st.session_state.messages.append(
            create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))

