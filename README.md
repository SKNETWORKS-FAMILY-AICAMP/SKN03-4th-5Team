# 🤖 LangChain & RAG 사전 🤖
**LangChain과 RAG에 대해 궁금한 점이나 더 알고 싶은 부분을 질문해보아요 !**
<br/><br/>

### <mark> 개발자 </mark>
👩🏻‍💻 SKN 3기 4조 서민정

<br/><br/>

### <mark>개발 기간</mark>
📅 2024.11.06 ~ 2024.11.07 (총 2일)

<br/><br/>

### <mark>프로젝트 배경</mark>
 본 과정을 수행하며 강사님께서는 "저의 강의자료를 사전처럼 사용하세요."라 말씀하시곤 하셨다. 그러나 막상 특정 내용을 찾으려 하니 강의 자료의 주제와 내용이 다양하고, 파일 경로가 복잡하여 원하는 부분을 찾는 데 시간이 오래 걸렸다.

 이에 RAG를 활용하여 강사님의 강의자료를 기반으로, **궁금한 내용이나 그 내용이 담긴 파일의 경로를 쉽게 찾을 수 있도록 도와주는 챗봇 시스템**을 개발하고자 한다.

<br/><br/>

### <mark>프로젝트 목표</mark>
 강의 자료를 효율적으로 활용하기 위한 챗봇 개발을 목표로 한다.

 이때, 기간과 리소스를 고려하여 개발자가 최근 공부중인 LangChain과 RAG에 대한 폴더 두개로 대상을 좁히기로 한다.

<br/><br/>
 
### <mark>데이터 정보</mark>
**💽 LangChain & RAG 강의 자료 데이터** 
> [SKN 3기 강사님 깃허브](https://github.com/good593/course_ai/tree/main/3.%20Large%20Language%20Models)
 
<br/><br/>

### <mark>프로젝트 수행 과정</mark>
**① 강의 자료 벡터 추출** 

> FAISS를 활용하여 `db/faiss` 생성
> 
> 이때, 메타데이터(부모 폴더와 파일 명)를 함께 저장하여 검색 시 해당 파일 경로를 제공할 수 있도록 함

<br/>

**② 강의 자료 벡터를 활용한 챗봇 구현** 

> 추출된 벡터를 기반으로 사용자 prompt가 입력되면, 그와 관련된 답변을 주는 챗봇 구현
>
> 이때, 가장 많이 활용된 강의 자료의 파일 경로를 제공하여 사용자가 추가적으로 학습할 수 있도록 함

<br/><br/>

### <mark>프로젝트 수행 결과</mark>
<details> <summary>🤖 챗봇 질의 예시</summary>
  
![image](https://github.com/user-attachments/assets/98925a68-2453-4b26-8a44-a08305bdd714)![image](https://github.com/user-attachments/assets/9c1a6fd9-d5fa-41a1-b6f8-163b8556be0d)

</details>

<details> <summary>📃 강의자료 발췌 내용</summary>

![image](https://github.com/user-attachments/assets/18ee7dad-68a4-4d95-a3b3-9a274d534907) 

</details>

<br/><br/>

### <mark>프로젝트 의의</mark>
**⏱️ 탐색 시간 절약** 

> 복잡한 경로와 다양한 주제를 가진 자료들 속에서 사용자가 필요한 내용을 신속하게 찾아낼 수 있다.

<br/>

**📚 학습 효율성을 극대화** 

> 탐색 시간 절약을 통해 사용자가 더 많은 시간을 학습에 집중할 수 있게 돕는다.
>
> 챗봇의 기능을 통해 강의 내용에 대한 이해를 높이고, 추가적인 학습 자료를 쉽게 찾아볼 수 있다.

<br/>

**🌐 확장 가능성** 

> 본 프로젝트에서는 LangChain과 RAG에 대해서만 다루고 있지만, 다른 강의 자료나 주제들을 추가하여 VectorDB에 저장하면 시스템을 확장할 수 있다.
>
> 또한, 다양한 데이터 소스와 연결하여 보다 범용적인 학습 지원 시스템으로 발전시킬 수 있다.

<br/><br/>
