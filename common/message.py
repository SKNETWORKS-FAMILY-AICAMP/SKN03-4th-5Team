# 아래와 같은걸 만들 예정임
"""
{
        CHATBOT_MESSAGE.role.name: CHATBOT_ROLE.assistant.name,
        CHATBOT_MESSAGE.content.name: assistant_prompt
}
"""

from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE

def __check_message(role:CHATBOT_ROLE, prompt:str):
    result = False
    if role not in CHATBOT_ROLE:
        result = True
    elif not isinstance(prompt, str) and not len(prompt):
        result = True
    
    return result

def create_message(role:CHATBOT_ROLE, prompt:str):
    if __check_message(role, prompt):
        return

    return {
        CHATBOT_MESSAGE.role.name: role.name,
        CHATBOT_MESSAGE.content.name: prompt
    }