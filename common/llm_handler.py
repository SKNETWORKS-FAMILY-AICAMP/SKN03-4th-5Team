import time
from .langgraph import get_workflow
from langchain_core.messages import HumanMessage

def response_from_llm(prompt, message_history=[], model_id:str="gpt-4o-mini"):
    llm_string = model_id
    
    agent = get_workflow()
    config = {"configurable": {"thread_id": "abc123"}}
    streaming = agent.invoke({"messages": [HumanMessage(content = prompt)]})

    print('streaming',type(streaming))

    end_time = time.time()

    response_text = streaming['messages'][-1].content
    
    return response_text

