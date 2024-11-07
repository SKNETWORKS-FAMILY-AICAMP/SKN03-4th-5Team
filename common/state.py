from typing import TypedDict, Sequence,Annotated
from langchain_core.messages import BaseMessage
import operator

# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str