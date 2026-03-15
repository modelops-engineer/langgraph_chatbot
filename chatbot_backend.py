from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages


load_dotenv()

model = ChatOpenAI()

class QAState(TypedDict):

    messages : str = Annotated[list[BaseMessage], add_messages]


def chatnode(state : QAState) -> QAState:
    messages = state['messages']

    response = model.invoke(messages)

    return {'messages': [response]}


checkpointer = InMemorySaver()

graph = StateGraph(QAState)

node1 = graph.add_node('chatnode', chatnode)

edge1 = graph.add_edge(START, 'chatnode')
edge2 = graph.add_edge('chatnode', END)


chatbot = graph.compile(checkpointer=checkpointer)