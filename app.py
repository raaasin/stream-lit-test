import os
import pandas as pd
import streamlit as st
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse
from PIL import Image
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Function to load CSV file
@st.cache_data
def load_csv(file):
    df = pd.read_csv(file)
    return df

# Title and File Uploader
st.title("PandasAI Test Streamlit")
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = load_csv(file)
    st.write(df.head())  # Display uploaded DataFrame

    # Setting up PandasAI agent
    os.environ["PANDASAI_API_KEY"] = "$2a$10$foYM9PHFSnQrKNdPmla6aeq.4Os1z8tO0opn7A3mtX4E.XrClySgq"
    agent = Agent(
        [df],
        config={"verbose": True, 
                "response_parser": StreamlitResponse,
                "enable_cache": False,
                },
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    chat_container = st.empty()
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_container.text(f"You: {message['content']}")
        else:
            chat_container.text(f"Assistant: {message['content']}")

    # Chat Interface
    st.subheader("Chat Interface")
    user_input = st.text_input("You:", key="user_input")
    if st.button("Send"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Get response from the assistant
        response = agent.chat(user_input)

        if os.path.exists(response):  # Check if the response is a file path
            st.image(Image.open(response))  # Display the image
        else:
            # If not a file path, add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Clear the previous input
        user_input = ""
