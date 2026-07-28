import asyncio
import uuid

import streamlit as st

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from chatbot_backend_with_mcp import (
    get_chatbot,
    get_all_conversations,
    save_conversation_name,
)


# ==========================================================
# Helper Functions
# ==========================================================

def generate_thread_id():

    return str(
        uuid.uuid4()
    )


def reset_chat():

    st.session_state.thread_id = (
        generate_thread_id()
    )

    st.session_state.message_history = []


# ==========================================================
# Streamlit Setup
# ==========================================================

st.set_page_config(
    page_title="ImranGPT",
    page_icon="💀",
)

st.title(
    "ImranGPT 💀"
)


# ==========================================================
# Session State
# ==========================================================

if (
    "thread_id"
    not in st.session_state
):

    st.session_state.thread_id = (
        generate_thread_id()
    )


if (
    "message_history"
    not in st.session_state
):

    st.session_state.message_history = []


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title(
    "Conversations"
)


if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True,
):

    reset_chat()

    st.rerun()


st.sidebar.divider()


# ==========================================================
# Load Saved Conversations
# ==========================================================

conversations = asyncio.run(
    get_all_conversations()
)


for (
    thread_id,
    title,
) in conversations:

    if st.sidebar.button(

        title,

        key=thread_id,

        use_container_width=True,

    ):

        st.session_state.thread_id = (
            thread_id
        )


        # --------------------------------------------------
        # Load old conversation
        # --------------------------------------------------

        async def load_conversation():

            async with get_chatbot() as chatbot:

                state = (
                    await chatbot.aget_state(

                        config={

                            "configurable": {

                                "thread_id":
                                    thread_id

                            }

                        }

                    )
                )


                if (
                    state is None
                    or state.values is None
                ):

                    return []


                return state.values.get(

                    "messages",

                    [],

                )


        history = asyncio.run(

            load_conversation()

        )


        messages = []


        for msg in history:


            if isinstance(

                msg,

                HumanMessage,

            ):

                role = "user"


            elif isinstance(

                msg,

                AIMessage,

            ):

                role = "assistant"


            else:

                continue


            messages.append(

                {

                    "role": role,

                    "content":
                        msg.content,

                }

            )


        st.session_state.message_history = (
            messages
        )


        st.rerun()


# ==========================================================
# Configuration
# ==========================================================

CONFIG = {

    "configurable": {

        "thread_id":

            st.session_state.thread_id

    }

}


# ==========================================================
# Display Existing Messages
# ==========================================================

for message in (
    st.session_state
    .message_history
):

    with st.chat_message(

        message["role"]

    ):


        # --------------------------------------------------
        # Display saved tool usage
        # --------------------------------------------------

        if (

            message["role"]
            == "assistant"

            and message.get(
                "tools"
            )

        ):


            with st.status(

                "✅ Tools used",

                expanded=True,

                state="complete",

            ):


                for tool in (

                    message["tools"]

                ):


                    st.write(

                        "🔧 "

                        f"`{tool['name']}`"

                    )


                    if tool.get(

                        "args"

                    ):


                        st.write(

                            "Arguments: "

                            f"`{tool['args']}`"

                        )


        # --------------------------------------------------
        # Display message
        # --------------------------------------------------

        st.markdown(

            message["content"]

        )


# ==========================================================
# User Input
# ==========================================================

user_input = st.chat_input(
    "Ask anything..."
)


if user_input:


    # ======================================================
    # Save User Message
    # ======================================================

    st.session_state.message_history.append(

        {

            "role": "user",

            "content":
                user_input,

        }

    )


    # ======================================================
    # Display User Message
    # ======================================================

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_input
        )


    # ======================================================
    # AI Response
    # ======================================================

    with st.chat_message(
        "assistant"
    ):


        # --------------------------------------------------
        # Tool Status Box
        # --------------------------------------------------

        with st.status(

            "🤖 Thinking...",

            expanded=True,

        ) as status:


            async def get_response():

                full_response = ""

                used_tools = []


                async with get_chatbot() as chatbot:


                    # ======================================
                    # Stream LangGraph Response
                    # ======================================

                    async for (

                        chunk,

                        metadata,

                    ) in chatbot.astream(

                        {

                            "messages": [

                                HumanMessage(

                                    content=user_input

                                )

                            ]

                        },

                        config=CONFIG,

                        stream_mode="messages",

                    ):


                        # ==================================
                        # Detect Tool Calls
                        # ==================================

                        if (

                            isinstance(

                                chunk,

                                AIMessage,

                            )

                            and chunk.tool_calls

                        ):


                            for tool_call in (

                                chunk.tool_calls

                            ):


                                tool_name = (

                                    tool_call.get(

                                        "name",

                                        "Unknown Tool",

                                    )

                                )


                                tool_arguments = (

                                    tool_call.get(

                                        "args",

                                        {},

                                    )

                                )


                                # ----------------------------------
                                # Save tool permanently
                                # ----------------------------------

                                used_tools.append(

                                    {

                                        "name":
                                            tool_name,

                                        "args":
                                            tool_arguments,

                                    }

                                )


                                # ----------------------------------
                                # Show tool immediately
                                # ----------------------------------

                                status.write(

                                    "🔧 Using tool: "

                                    f"`{tool_name}`"

                                )


                                if tool_arguments:


                                    status.write(

                                        "Arguments: "

                                        f"`{tool_arguments}`"

                                    )


                        # ==================================
                        # Collect AI Text
                        # ==================================

                        if (

                            isinstance(

                                chunk,

                                AIMessage,

                            )

                            and chunk.content

                        ):


                            full_response += (

                                chunk.content

                            )


                    # ======================================
                    # Get Conversation Title
                    # ======================================

                    state = (

                        await chatbot.aget_state(

                            config=CONFIG

                        )

                    )


                    title = (

                        state.values.get(

                            "conversation_name"

                        )

                    )


                    if title:


                        await save_conversation_name(

                            st.session_state
                            .thread_id,

                            title,

                        )


                return (

                    full_response,

                    used_tools,

                )


            # ==================================================
            # Run Async Function
            # ==================================================

            (

                ai_message,

                used_tools,

            ) = asyncio.run(

                get_response()

            )


            # ==================================================
            # Update Status
            # ==================================================

            if used_tools:


                status.update(

                    label=(

                        "✅ Tool execution completed"

                    ),

                    state="complete",

                    expanded=True,

                )


            else:


                status.update(

                    label=(

                        "✅ Response completed"

                    ),

                    state="complete",

                    expanded=True,

                )


        # ==================================================
        # Display Final AI Response
        # ==================================================

        st.markdown(

            ai_message

        )


    # ======================================================
    # Save AI Message + Tool History
    # ======================================================

    st.session_state.message_history.append(

        {

            "role": "assistant",

            "content":
                ai_message,

            "tools":
                used_tools,

        }

    )


    # ======================================================
    # Refresh App
    # ======================================================

    st.rerun()