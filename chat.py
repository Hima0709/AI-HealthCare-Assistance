import os
import json
import streamlit as st
from groq import Groq

# ✅ Streamlit App Setup
st.set_page_config(page_title="AI DOCOUS", page_icon="🩺", layout="centered")
st.title("🩺 AI DOCOUS")

# ✅ Load API Key from config.json
try:
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(f"{working_dir}/config.json")
    with open(config_path) as f:
        config_data = json.load(f)
    GROQ_API_KEY = config_data["GROQ_API_KEY"]
    os.environ["GROQ_API_KEY"] = ("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")
except Exception as e:
    st.error("❌ Error loading API key from config.json")
    st.stop()

# ✅ Initialize Groq client
client = Groq()

# ✅ Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Show previous chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✅ Medical query checker
def is_medical_query(text):
    medical_keywords = [
        "fever", "cold", "hii", "Hello", "Hii", "Hlo", "headache","thank uh","thank you", "vomit", "nausea", "pain", "cough", "flu",
        "diabetes", "cancer", "bp", "blood", "pressure", "infection","hands", "fracture","name","liver","brain","eyes","nose",
        "injury", "stomach", "lungs", "heart", "symptom", "rash", "itch", "dizziness", "swelling", "burn", "fatigue", "anxiety", "doctor", "tablet", "medicine","fruits"
    ]
    text = text.lower()
    return any(keyword in text for keyword in medical_keywords)

# ✅ Get user input
user_input = st.chat_input("Lets discuss about ur health...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # ✅ Check if it's a medical query
    if is_medical_query(user_input):
        messages = [
            {"role": "system", "content": (
                "You are a Healthcare Assistance. Help the user based on their health symptoms. "
                "Always mention that this is a medical advice and if the condition is severe then recommend seeing a doctor."
            )},
            *st.session_state.chat_history
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        answer = response.choices[0].message.content
    else:
        answer = (
            "🤖 Sorry!, I'm here to assist with health and medical-related questions only. "
            "Please feel free to ask a query related to your symptoms, medications, or health conditions you may experiencing."
            "For the best assistance, kindly avoid non-medical queries."
            "Your well-being is our priority!"
            "Thank you"        
        )

    # Show assistant response
    st.chat_message("assistant").markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})