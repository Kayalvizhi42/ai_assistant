import os
from datetime import datetime
import streamlit as st
from src.invoke.chat_assistant import chat_with_files

st.set_page_config(page_title="Codebase Chat Assistant", layout="wide")
st.title("💬 Chat with Your Codebase")

# Session state for history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader("Upload your code files", accept_multiple_files=True)

st.subheader("💬 Start or continue your chat")
user_prompt = st.chat_input("Type your message here...")

if st.button("Ask") and user_prompt and uploaded_files:
    files_content = []
    for file in uploaded_files:
        content = file.read().decode("utf-8", errors="ignore")
        files_content.append(content)

    # Call your GPT logic
    answer = chat_with_files(user_prompt, files_content, st.session_state.chat_history)

    # Update history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Display chat history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 GPT"
        st.markdown(f"**{role}:** {msg['content']}")

    # Save Conversation button
    if st.button("💾 Save Conversation"):
        if not os.path.exists("saved_chats"):
            os.makedirs("saved_chats")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"saved_chats/chat_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            for msg in st.session_state.chat_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                f.write(f"{role}: {msg['content']}\n\n")

        st.success(f"Conversation saved as {filename}")