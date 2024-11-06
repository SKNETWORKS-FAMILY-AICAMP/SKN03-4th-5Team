
from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE

def __check_message(role:CHATBOT_ROLE, prompt:str):
    result = False
    if role not in CHATBOT_ROLE:
        result = True 
    elif not isinstance(prompt, str) and not len(prompt.strip()):
        result = True 

    return result

def create_message(role: CHATBOT_ROLE, prompt: str):
    if __check_message(role, prompt):
        return None 

    return {
        CHATBOT_MESSAGE.role.name: role.name,
        CHATBOT_MESSAGE.content.name: f"{prompt}"
    }

def generate_rag_prompt(prompt: str, search_results):

    prompt = f"사용자 질문: {prompt}\n\n"

    prompt += "## 관련 정보:\n"

    prompt += (
        "아래의 내용은 LangChain 혹은 RAG에 대한 관련 정보와 정보의 장소입니다. \n"
        "이 정보들로 ""사용자의 궁금증을 풀 수 있는"" 신뢰성 있는 설명을 제공해 주세요. \n\n\n"
    )

    for i, result in enumerate(search_results):
        content = result['content'].replace("'", "").strip()  
        metadata = result['metadata']
        
        prompt += f"### 결과 {i + 1}\n"
        prompt += f"- **내용**: {content}\n"
        prompt += f"- **출처 파일**: {metadata['source_file']}\n"
        prompt += f"- **출처 폴더**: {metadata['source_folder']}\n"
        prompt += "--------------------------------------------------\n"


    prompt += (
        "\n\n이상 관련 정보입니다.\
        꼭 마지막에 사용자의 질문과 가장 연관된 정보를 얻을 수 있는 파일 경로를 아래와 같이 제공해주세요.\
        생성한 결과에 가장 많이 관여한 파일의 위치를 작성해야 합니다."
        f"> **📜 참조 파일 위치**: `출처 폴더 명/출처 파일 명` <"
    )  

    return prompt