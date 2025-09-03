import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="HR Assistant Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- App Title ---
st.title("🤖 HR Resource Query Assistant")
st.caption("Ask me to find employees based on skills, experience, or project history!")

# --- Backend API URL ---
BACKEND_URL = "http://127.0.0.1:8000/chat"

# --- Session State Initialization ---
# This holds the chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you find the right employee for your project today?"}
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("e.g., 'Find Python developers with 3+ years experience'"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Get Assistant Response ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            # Prepare the data for the POST request
            payload = {"query": prompt}
            
            # Send request to the backend
            response = requests.post(BACKEND_URL, json=payload, timeout=120)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the JSON response
            result = response.json()
            assistant_response = result.get("response", "Sorry, I couldn't get a response.")
            
            # Display the assistant's response
            message_placeholder.markdown(assistant_response)

        except requests.exceptions.RequestException as e:
            error_message = f"Could not connect to the backend. Please make sure it's running. \n\n**Error:** {e}"
            message_placeholder.error(error_message)
            assistant_response = error_message
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            message_placeholder.error(error_message)
            assistant_response = error_message

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
