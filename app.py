import os
import pandas as pd
import streamlit as st
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse
from PIL import Image

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

    # Chat Interface
    st.subheader("Chat Interface")
    user_input = st.text_input("Enter your query:")
    if st.button("Send"):
        response = agent.chat(user_input)
        if os.path.exists(response):  # Check if the response is a file path
            st.image(Image.open(response))  # Display the image
        else:
            st.write(response)  # If not a file path, print the response as text
