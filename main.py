import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
import streamlit as st
from common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE  # CHATBOT_ROLE 클래스 import
from common.message import create_message

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
api_key = os.getenv("API_KEY")
print("API Key 로드 완료")

# PDF 및 벡터 스토어 로드 함수 정의
def load_pdf_and_create_vector_store():
    # PDF 로드
    folder_path = 'documents'
    documents = [] 
    # 모든 PDF 파일 불러오기
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load()) 

    print("PDF 로드 완료")
    
    # 문서 텍스트 분할
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # 벡터베이스로 변환하여 저장
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
    vector_store.persist()
    return vector_store

# 최초 실행시에만 PDF 및 벡터 스토어 로드
if "vector_store" not in st.session_state:
    st.session_state.vector_store = load_pdf_and_create_vector_store()
    st.session_state.retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 2})

# Streamlit 설정
st.title("LLM을 연동한 내외부 문서 기반 질의 응답 시스템")

# role -> user(사용자)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# 사용자 입력 처리
prompt = st.chat_input("입력해주세요:")

if prompt:
    message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    if message[CHATBOT_MESSAGE.content.name].strip():
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append(message)
        
        # 프롬프트 개선
        system_template = """
        Use the following pieces of context to answer the users question shortly.
        Given the following summaries of a long document and a question, create a final answer with references ("SOURCES"), use "SOURCES" in capital letters regardless of the number of sources.
        If you don't know the answer, just say that "I don't know", don't try to make up an answer.
        ----------------
        {summaries}
        You MUST answer in Korean and in Markdown format:
        """
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # ChatGPT 모델을 사용하여 학습
        chain_type_kwargs = {"prompt": prompt_template}
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=st.session_state.retriever,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )

        # 질문 처리
        query = prompt
        result = chain.invoke(query)
        
        with st.chat_message("assistant"):
            # st.write(f"질문: {query}")
            st.markdown(result['answer'])
        
        # 이력 추가
        st.session_state.messages.append(
            create_message(role=CHATBOT_ROLE.assistant, prompt=result['answer'])
        )
