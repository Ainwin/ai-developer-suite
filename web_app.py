import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

st.set_page_config(page_title="DevAssistant AI", layout="wide")

# This makes the app look sleek and dark
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #00FF00;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #00FF00;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

load_dotenv()

# Get the key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the key exists
if not API_KEY:
    st.error("API Key not found. Please check your .env file.")
    st.stop()
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"

# 2. SIDEBAR (The new controls we talked about)
with st.sidebar:
    st.title("🛠️ Dev Settings")
    # This creates the toggle button
    mode = st.radio("Choose AI Mode:", ["Just Comment", "Refactor & Comment"])
    st.write("---")
    st.info("Refactor mode cleans up messy code and makes it professional.")

# 3. MAIN INTERFACE (The website look)
st.title("🤖 AI Junior Dev Assistant")
st.write("Paste your code below to improve it instantly!")

user_code = st.text_area("Input Code:", height=200, placeholder="Paste your code here...")

# 4. THE BRAIN (The logic that talks to Google)
if st.button("Generate"):
    if user_code:
        # We decide WHAT to ask based on the Sidebar choice
        if mode == "Refactor & Comment":
            prompt = f"Refactor this code to be cleaner/shorter and add comments to every line:\n{user_code}"
        else:
            prompt = f"Keep the logic the same but add helpful comments to every line of this code:\n{user_code}"

        # The actual request to Google
        with st.spinner("Processing..."):
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                answer = result['candidates'][0]['content']['parts'][0]['text']
                
                
                st.subheader("Result:")
                st.code(answer, language='python')
            else:
                st.error("Google API Error. Check your key!")
    else:
        st.warning("Please paste some code first!")