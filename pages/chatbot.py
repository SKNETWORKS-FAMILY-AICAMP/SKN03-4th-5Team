
from common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from common.message import create_message
from common.llm_handler import response_from_llm

# web ui/ux
import streamlit as st

st.title("Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현 
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])


# 사용자 입력
prompt = st.chat_input("입력해주세요")
# 사용자 입력이 있다면,
if prompt:
    message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    
    # 입력값이 존재한다며, 
    if message:
        # 화면에 표현
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        
        # 이력 추가 

        st.session_state.messages.append(message)

        # 챗봇 답변 
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            answer = response_from_llm(prompt=prompt)
            st.write(answer)
            #stream방식
            assistant_response = answer

        # 이력 추가 
        st.session_state.messages.append(
            create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))
