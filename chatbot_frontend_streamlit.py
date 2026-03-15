import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage



CONFIG = {'configurable' : {'thread_id' : 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input("Please write your query")

if user_input:

    st.session_state['message_history'].append({'role' : 'user', 'content':user_input})

    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({
        'messages' : [HumanMessage(content=user_input)]
    },
    config=CONFIG
    )

    ai_message = response['messages'][-1].content

    st.session_state['message_history'].append({'role' : 'assistant', 'content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)

    