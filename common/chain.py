import streamlit as st
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from .model import get_chat_openai
from .prompt import get_supervisor_prompt, get_checker_prompt
from .tool import get_tools, execute_tool_calls
from langchain_openai import ChatOpenAI

@st.cache_resource
def get_supervisor_chain(model_id="gpt-4o-mini"):
    model = get_chat_openai(model_id)
    if model is None:
            raise ValueError("get_chat_openai returned None; ensure model_id is valid and model is loaded correctly.")
    

    options = ["FINISH", "SearchPDF", "CurrentTime"]
        # Using openai function calling can make output parsing easier for us
    function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    }
                },
                "required": ["next"],
            },
        }

    # llm = ChatOpenAI(model="gpt-4o-mini")
    tool_binded_model = model.bind_functions(functions=[function_def], function_call="route")
    # tool_binded_model = llm.bind_fnctions(functions=[function_def], function_call="route")

    prompt = get_supervisor_prompt()
    if prompt is None:
        raise ValueError("get_promt returned None; ensure prompt template is correctly defined.")
        
    # chain = LLMChain(llm=llm, prompt=prompt) # Deprecated since version 0.1.17: Use RunnableSequence, e.g., `prompt | llm` instead.
    # chain = Chain(tool_binded_model, prompt)
    chain = prompt | tool_binded_model | JsonOutputFunctionsParser()
    return chain


@st.cache_resource
def get_checker_chain(model_id="gpt-4o-mini"):
    model = get_chat_openai(model_id)
    if model is None:
            raise ValueError("get_chat_openai returned None; ensure model_id is valid and model is loaded correctly.")
    
    options = ["YES", "NO"]
        # Using openai function calling can make output parsing easier for us
    function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    }
                },
                "required": ["next"],
            },
        }

    # llm = ChatOpenAI(model="gpt-4o-mini")
    tool_binded_model = model.bind_functions(functions=[function_def], function_call="route")
    # tool_binded_model = llm.bind_fnctions(functions=[function_def], function_call="route")

    prompt = get_checker_prompt()
    if prompt is None:
        raise ValueError("get_promt returned None; ensure prompt template is correctly defined.")
        
    # chain = LLMChain(llm=llm, prompt=prompt) # Deprecated since version 0.1.17: Use RunnableSequence, e.g., `prompt | llm` instead.
    # chain = Chain(tool_binded_model, prompt)
    chain = prompt | tool_binded_model | JsonOutputFunctionsParser()
    return chain