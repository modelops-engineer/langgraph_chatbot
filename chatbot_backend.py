from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()

model = ChatOpenAI()

class QAState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]


def chatnode(state : QAState) -> QAState:
    messages = state['messages']

    response = model.invoke(messages)

    return {'messages': [response]}


conn = sqlite3.connect(database ='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(QAState)

node1 = graph.add_node('chatnode', chatnode)

edge1 = graph.add_edge(START, 'chatnode')
edge2 = graph.add_edge('chatnode', END)


def retrieve_threads():
    all_threads= set()
    for check_point in checkpointer.list(None):
        all_threads.add(check_point.config['configurable']['thread_id'])

    return list(all_threads)


chatbot = graph.compile(checkpointer=checkpointer)