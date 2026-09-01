import streamlit as st

from memory_manager import (
    store_message,
    get_relevant_memories,
    get_all_memories,
)

from recipe_agent import chat_with_gemini


USER_ID = "mehnaz_demo_user"


def should_store_memory(text: str) -> bool:
    lowered = text.lower()

    memory_phrases = [
        "i have ",
        "i'm allergic",
        "i am allergic",
        "allergic to",
        "i don't like ",
        "i do not like ",
        "i dislike ",
        "i love ",
        "i like ",
        "i prefer ",
        "i hate ",
        "i avoid ",
        "i can't eat ",
        "i cannot eat ",
        "i am vegetarian",
        "i'm vegetarian",
        "i am vegan",
        "i'm vegan",
        "i follow a ",
        "my diet is ",
    ]

    return any(phrase in lowered for phrase in memory_phrases)


st.set_page_config(
    page_title="AI Recipe Assistant",
    page_icon="🍳",
    layout="wide",
)


# ---------- SIDEBAR ----------

with st.sidebar:
    st.title("🍳 Recipe Assistant")

    st.write(
        "Your AI cooking assistant with "
        "personalized memory."
    )

    st.divider()

    st.subheader("🧠 My Preferences")

    if st.button("Refresh Profile", use_container_width=True):
        st.rerun()

    try:
        memories = get_all_memories(USER_ID)

        if memories:
            for memory in memories:
                st.write(f"• {memory}")
        else:
            st.caption("No preferences stored yet.")

    except Exception:
        st.caption("Memory profile unavailable.")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# ---------- MAIN PAGE ----------

st.title("🍳 AI Recipe Assistant")

st.caption(
    "Personalized recipes powered by Gemini, "
    "Mem0 and Qdrant."
)


# ---------- CHAT HISTORY ----------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------- USER INPUT ----------

user_input = st.chat_input(
    "Ask me anything about cooking or recipes..."
)


if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve relevant memories
    try:
        relevant_facts = get_relevant_memories(
            USER_ID,
            query=user_input,
        )
    except Exception:
        relevant_facts = []

    # Gemini response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = chat_with_gemini(
                    user_input,
                    relevant_facts,
                )

                st.markdown(response)

            except Exception as e:

                response = (
                    "Sorry, I couldn't process that request "
                    "right now. Please try again."
                )

                st.error(str(e))

    # Save assistant response to chat
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    # Store useful user information
    if should_store_memory(user_input):

        try:
            store_message(
                USER_ID,
                user_input,
            )
        except Exception:
            pass
