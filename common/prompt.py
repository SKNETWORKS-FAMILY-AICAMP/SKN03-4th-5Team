from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
def get_promt(system_prompt:str):    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    return prompt

def get_supervisor_prompt():
    members = ["SearchPDF", "CurrentTime"]
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers:  {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )
    options = ["FINISH"] + members

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))
    return prompt

def get_checker_prompt():
    members = ["YES", "NO"]
    system_prompt = (
        """
        You are an assistant that helps classify questions. If a question is related to Tesla, respond with "Yes." 
        If the question is not related to Tesla, respond with "No." Answer only with {{members}} based on whether 
        the question is related to Tesla or not. Do not provide any explanations.
        """
    )    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next? "
                "Select one of: {{options}}",
            ),
        ]
    ).partial(options=str(members), members=", ".join(members))
    return prompt
