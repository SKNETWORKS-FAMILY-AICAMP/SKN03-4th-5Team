from langchain_core.messages import HumanMessage
from typing import List, Dict, Generator
from .model import get_chat_openai
from langgraph.types import StreamWriter
from .state import AgentState
from langchain_core.messages import AIMessage
from .chain import get_supervisor_chain, get_checker_chain
from langgraph.graph import START, StateGraph, MessagesState, END
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.callbacks.manager import adispatch_custom_event
from .faiss import get_pdf_search
from .tool import empty_tool, datetime_tool
from .agent import create_agent

def checker_node(state:AgentState):
    check_chain = get_checker_chain('gpt-4o-mini')
    response = check_chain.invoke(state["messages"])

    output = {"next": response['next'], "messages": [HumanMessage(content="테슬라와 관련이 없는 질문입니다." )]}
    return output

def invalid_node(state:AgentState):
    output = {"next": None, "messages": state["messages"]}
    return output

def supervisor_node(state:AgentState):
    supervisor_chain = get_supervisor_chain('gpt-4o-mini')
    response = supervisor_chain.invoke(state["messages"])

    output = {"next": response['next'], "messages": state["messages"]}
    return output

def agent_node(state, agent, name):
    result = agent.invoke(state)

    output = {"messages": [HumanMessage(content=result["output"], name=name)], "next":None}
    return output

def search_pdf_node(state:AgentState):
    search_pdf_chain = get_pdf_search()
    response = search_pdf_chain.invoke(state['messages'][0].content)

    # human_messages = [
    #     HumanMessage(content=doc.page_content, name="document_content") for doc in response  # text_chunks는 Document 객체 리스트
    # ]   
    # 각 메시지의 content를 하나로 결합
    combined_content = "\n".join([doc.page_content for doc in response])

    # 단일 HumanMessage 생성
    combined_human_message = HumanMessage(content=combined_content, name="document_content")

    state['messages'] =[]
    output = {"next": None, "messages": [combined_human_message]}

    return output

def pdf_result_eval(state:AgentState):
    llm = get_chat_openai('gpt-4o-mini')
    eval_agent = create_agent(llm, "Determine whether the data is appropriate for answering the question and answer with YES or NO.", [datetime_tool])

    if not state.get('messages'):
        print("Error: 'messages' key is missing or empty in 'state'.")
        return None
    
    print('type:' ,type(state['messages'][-1]))
    response = eval_agent.invoke(state['messages'][-1])

    output = {"next": response, "messages": state['messages']}
    return output


# https://langchain-ai.github.io/langgraph/how-tos/streaming-content/#stream-content_1
def arrange_node(state: AgentState):
    # Arrange 노드에서 모든 메시지를 정리하여 스트리밍 방식으로 출력
    input_text = state["messages"][-1].content
    response = input_text
    
    chunks = list(input_text)

    return {"messages": [HumanMessage(content=input_text)], "next":None}


