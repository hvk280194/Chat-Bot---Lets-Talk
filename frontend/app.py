import streamlit as st
import requests
import time

st.set_page_config(page_title="Lets Talk", page_icon="🌌", layout="wide")

st.title("Lets Learn: Powered by FastAPI, HuggingFace, and Streamlit")

API_URL = "http://127.0.0.1:8000/chat/invoke"

# Chat session management
if "session_id" not in st.session_state:
    st.session_state.session_id = "session_" + str(int(time.time()))

# User input
user_input = st.chat_input("Type your message here...")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle new message
if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")

        try:
            resp = requests.post(
                API_URL,
                json={"session_id": st.session_state.session_id, "message": user_input},
                timeout=120
            )
            if resp.status_code == 200:
                output = resp.json().get("output", "No response")
            else:
                output = f"Error: {resp.status_code}"
        except Exception as e:
            output = f"⚠️ Error contacting backend: {e}"

        placeholder.markdown(output)
        st.session_state.chat_history.append(("assistant", output))
