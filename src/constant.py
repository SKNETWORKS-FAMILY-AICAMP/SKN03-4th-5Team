import enum 

class CHATBOT_ROLE(enum.Enum):
    user = (enum.auto, "User")
    assistant = (enum.auto, "LLM Model")

class CHATBOT_MESSAGE(enum.Enum):
    role = (enum.auto, "Author")
    content = (enum.auto, "Message")