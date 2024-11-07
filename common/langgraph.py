import functools
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
import streamlit as st
from .state import AgentState
from .agent import create_agent
from .model import get_chat_openai
from .tool import wikipedia_tool, datetime_tool, empty_tool
from .node import agent_node, supervisor_node, checker_node, search_pdf_node, pdf_result_eval
from .chain import get_supervisor_chain

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import datetime
from langchain.tools import Tool

@st.cache_resource
def get_workflow():
    workflow = StateGraph(AgentState)
    
    llm = get_chat_openai('gpt-4o-mini')

    research_agent = create_agent(llm, "You are a web researcher.", [wikipedia_tool()])
    research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

    currenttime_agent = create_agent(llm, "You can tell the current time at", [datetime_tool])
    currenttime_node = functools.partial(agent_node, agent=currenttime_agent, name = "CurrentTime")
    
    arrange_agent = create_agent(llm, "Organize the following sentences", [datetime_tool])
    arrange_node = functools.partial(agent_node, agent=arrange_agent, name = "Arrange")

    # workflow.add_node("Researcher", research_node)
    workflow.add_node("Invalid", checker_node)
    workflow.add_node("CurrentTime", currenttime_node)
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Arrange", arrange_node)
    workflow.add_node("Checker", checker_node)
    workflow.add_node("SearchPDF", search_pdf_node)
    # workflow.add_node('Eval_PDF', pdf_result_eval)

    # Add an entry point. This tells our graph where to start its work each time we run it.
    workflow.add_edge(START, "Checker")

    # workflow.add_edge("Researcher", "Arrange")
    workflow.add_edge("CurrentTime", "Arrange")
    workflow.add_edge("SearchPDF", "Arrange")
    workflow.add_edge("Arrange", END)
    workflow.add_edge("Invalid", END)

    conditional_map = {k: k for k in ["SearchPDF", "CurrentTime"]}
    conditional_map["FINISH"] = END

    conditional_map2= {}
    conditional_map2["YES"] = 'Supervisor'
    conditional_map2["NO"] = "Invalid"

    # conditional_map3= {}
    # conditional_map3["YES"] = 'Arrange'
    # conditional_map3["NO"] = "Researcher"
    
    workflow.add_conditional_edges("Checker", lambda x: x["next"], conditional_map2)
    workflow.add_conditional_edges("Supervisor", lambda x: x["next"], conditional_map)
    # workflow.add_conditional_edges("Eval_PDF", lambda x: x["next"], conditional_map3)

    graph_2 = workflow.compile()

    return graph_2