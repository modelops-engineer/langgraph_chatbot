import streamlit as st
from chatbot_backend import chatbot, retrieve_threads
from langchain_core.messages import HumanMessage
import uuid





# ************************** Utility func ************************

def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    thread_id = generate_thread_id()
    add_thread(thread_id)
    # st.session_state['thread_history'] = thread_id
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['thread_history']:
        st.session_state['thread_history'].append(thread_id)


def load_messages(thread_id):
    config = {'configurable' : {'thread_id' : thread_id}}
    return chatbot.get_state(config=config).values.get('messages',[])

# ******************** Session State ****************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'thread_history' not in st.session_state:
    st.session_state['thread_history'] = retrieve_threads()

add_thread(st.session_state['thread_id'])



# *****************Side bar of the UI *************************

st.sidebar.title('Chatbot')

if st.sidebar.button('New chat'):
    reset_chat()

st.sidebar.text('Your chats')


for thread in st.session_state['thread_history'][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = load_messages(thread)

        message_list = []   
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            message_list.append({'role' : role, 'content' : message.content})

        st.session_state['message_history'] = message_list


# ************************ UI **************************

for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])





user_input = st.chat_input("Please write your query")

if user_input:

    st.session_state['message_history'].append({'role' : 'user', 'content':user_input})

    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({
    #     'messages' : [HumanMessage(content=user_input)]
    # },
    # config=CONFIG
    # )

    # ai_message = response['messages'][-1].content

    CONFIG = {'configurable' : {'thread_id' : st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream({
            'messages' : [HumanMessage(content=user_input)]
            },
            config=CONFIG,
            stream_mode='messages'
    ))

    st.session_state['message_history'].append({'role' : 'assistant', 'content':ai_message})