import os
import json
import pandas as pd
import streamlit as st
from groq import Groq

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Finance Chat",
    page_icon="🦙",
    layout="centered"
)

# Get the current working directory and load the config file
working_dir = os.path.dirname(os.path.abspath(__file__))

# Try to load configuration data
try:
    config_data = json.load(open(f"{working_dir}/config.json"))
except FileNotFoundError:
    st.error("Config file not found.")
    config_data = {}
except json.JSONDecodeError:
    st.error("Error reading the config file.")
    config_data = {}

# Get the Groq API key from the config
GROQ_API_KEY = config_data.get("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")

# Initialize the Groq client
client = Groq()
# Initialize the chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🦙 Finance ChatBot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask about finance...")

if user_prompt:
    # Display user's message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare the messages for the model with a finance-related system prompt
    messages = [
        {"role": "system", "content":"You are a knowledgeable and empathetic finance assistant. Based on the user's financial inquiries, your task is to provide insights, ask follow-up questions to gather more context (such as the user's financial goals, risk tolerance, investment horizon, etc.), and offer general guidance in line with good financial practices. Provide responses that are clear, informative, and suggest next steps, such as speaking to a financial advisor or considering specific investment strategies."},
        *st.session_state.chat_history
    ]

    # Call the Groq API to get the response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content
    except Exception as e:
        st.error(f"Error communicating with the API: {e}")
        assistant_response = "Sorry, I couldn't get a response at the moment."

    # Append the assistant's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
