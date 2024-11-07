import os
import openai
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv
import pickle
import streamlit as st

# 환경 변수 로드 및 API 키 설정
load_dotenv()  # .env 파일에서 API 키 로드
openai.api_key = os.getenv("OPENAI_API_KEY")

# 파일 경로 설정
file_path = "data/movie.csv"
embedding_file = "data/embeddings.npy"
faiss_index_file = "data/faiss_index.pkl"

# 데이터 로드
data = pd.read_csv(file_path)

# 텍스트 결합
data['combined_text'] = data.apply(lambda row: f"MOVIE_NM: {row['MOVIE_NM']}, GENRE_NM: {row['GENRE_NM']}, GRAD_NM: {row['GRAD_NM']}, VIEWNG_NMPR_CO: {row['VIEWNG_NMPR_CO']}", axis=1)

# 임베딩 모델 초기화
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 임베딩 로드 또는 생성
if os.path.exists(embedding_file):
    embeddings = np.load(embedding_file)
else:
    embeddings = embedding_model.encode(data['combined_text'].tolist())
    np.save(embedding_file, embeddings)

# FAISS 인덱스 로드 또는 생성
dimension = embeddings.shape[1]
if os.path.exists(faiss_index_file):
    with open(faiss_index_file, "rb") as f:
        index = pickle.load(f)
else:
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    with open(faiss_index_file, "wb") as f:
        pickle.dump(index, f)

# 유사한 문서 검색 함수 (FAISS 기반)
def search_similar_documents(query, top_k=5):
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype(np.float32)
    
    # FAISS 인덱스에서 유사도 검색
    _, top_indices = index.search(query_embedding, top_k)
    
    # 상위 K개의 유사한 문서 반환
    results = data.iloc[top_indices[0]]
    return results['combined_text'].tolist()

# LLM을 통한 답변 생성 함수 (ChatCompletion 사용)
def generate_answer(query):
    # 1. 유사한 문서 검색
    similar_texts = search_similar_documents(query)
    
    # 2. 프롬프트 생성
    context = "\n".join(similar_texts)
    prompt = f"""Here is some information about movie:\n{context}\n\nQuestion,  You must use movie.csv,
    추천 영화의 순서는 컬럼 VIEWNG_NMPR_CO순으로 정리해줘 , always use korean,  대답의 순서는 제목 장르 관람등급 관람객수 줄거리 순으로 해줘: {query}\nAnswer:
    """
    
    # 3. OpenAI ChatCompletion API 호출
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant recommend movie, 줄거리 정보에 대해서 추가해"},
                {"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    
    # 4. 생성된 답변 반환
    answer = response.choices[0].message.content.strip()
    return answer

# Streamlit UI 설정
st.title("영화 추천 Chatbot")
st.write("좋아하는 영화 장르나 원하는 영화 정보를 입력하세요!")

# 질문 입력
question = st.text_input("질문을 입력하세요:")

# 답변 생성 및 출력
if st.button("추천받기"):
    if question:
        with st.spinner("추천 영화를 찾고 있습니다..."):
            answer = generate_answer(question)
        st.write("### 추천 답변")
        st.write(answer)
    else:
        st.warning("질문을 입력해 주세요.")
