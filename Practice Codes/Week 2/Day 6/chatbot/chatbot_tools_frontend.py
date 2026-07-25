import uuid
import streamlit as st

from chatbot_backend_with_tools import (
    chatbot,
    get_all_conversations,
    save_conversation_name,
)

from langchain_core.messages import HumanMessage, AIMessage

# ==========================================================
# Helper Functions
# ==========================================================

def generate_thread_id():
    return str(uuid.uuid4())


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    if state is None or state.values is None:
        return []

    return state.values.get("messages", [])


def reset_chat():
    st.session_state.thread_id = generate_thread_id()
    st.session_state.message_history = []


# ==========================================================
# Session State
# ==========================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state.message_history = []


# ==========================================================
# Sidebar
# ==========================================================

st.title("ImranGPT 💀")

st.sidebar.title("Conversations")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_chat()
    st.rerun()


st.sidebar.divider()

conversations = get_all_conversations()

for thread_id, title in conversations:

    if st.sidebar.button(
        title,
        key=thread_id,
        use_container_width=True,
    ):

        st.session_state.thread_id = thread_id

        history = load_conversation(thread_id)

        messages = []

        for msg in history:

            if isinstance(msg, HumanMessage):
                role = "user"

            elif isinstance(msg, AIMessage):
                role = "assistant"

            else:
                continue

            messages.append(
                {
                    "role": role,
                    "content": msg.content
                }
            )

        st.session_state.message_history = messages
        st.rerun()


# ==========================================================
# Config
# ==========================================================

CONFIG = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


# ==========================================================
# Existing Chat
# ==========================================================

for message in st.session_state.message_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================================
# User Input
# ==========================================================

user_input = st.chat_input("Ask Anything...")

if user_input:

    st.session_state.message_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
                
            ai_message = st.write_stream(

                chunk.content

                for chunk, metadata in chatbot.stream(

                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },

                    config=CONFIG,

                    stream_mode="messages"

                )

                if chunk.content and isinstance(chunk, AIMessage)
            )

    # --------------------------------------------------
    # Save title (only once)
    # --------------------------------------------------

    state = chatbot.get_state(config=CONFIG)

    title = state.values.get("conversation_name")

    if title:
        save_conversation_name(
            st.session_state.thread_id,
            title,
        )

    st.session_state.message_history.append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )

    st.rerun()