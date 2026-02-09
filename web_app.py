import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
# 1. Setup & Security
load_dotenv()
# Handles both local (.env) and cloud (st.secrets)
api_key = os.getenv("GEMINI_API_KEY") or (st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else None)

if not api_key:
    st.error("API Key not found. Please check your Secrets or .env file.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Page Config
st.set_page_config(page_title="Ainwin Developer Suite", layout="wide", page_icon="🚀")

# 3. Sidebar Navigation
st.sidebar.title("🛠️ AI Suite")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("Select a Tool:", ["Code Assistant", "Vision Explainer", "Resume Matcher", "Voice Assistant"])

# --- MODE 1: CODE ASSISTANT (Your Original Logic) ---
if app_mode == "Code Assistant":
    st.header("💻 AI Code Assistant")
    st.write("Chat with the AI or refactor your code.")

    user_prompt = st.text_area("Enter your code or question:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ Get Help / Chat"):
            with st.spinner("Thinking..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_prompt)
                st.markdown("### AI Response:")
                st.write(response.text)
    
    with col2:
        if st.button("🛠️ Refactor Code"):
            with st.spinner("Refactoring..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Refactor and optimize this code for better performance and readability: {user_prompt}")
                st.markdown("### Refactored Code:")
                st.code(response.text, language='python')

# --- MODE 2: VISION EXPLAINER (The New Power) ---
elif app_mode == "Vision Explainer":
    st.header("📸 AI Vision Explainer")
    st.write("Upload a screenshot of an error, a UI design, or a logic flow.")
    
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    vision_prompt = st.text_input("What should the AI do?", value="Explain this image in detail and find any errors.")

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Uploaded Image", use_container_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner("Processing image..."):
                model = genai.GenerativeModel('gemini-2.5-flash')
                # Passing both text and image as a list
                response = model.generate_content([vision_prompt, image])
                st.markdown("### AI Analysis:")
                st.write(response.text)

# --- MODE 3: RESUME MATCHER (The Future Slot) ---
elif app_mode == "Resume Matcher":
    st.header("📄 Resume & Job Matcher")
    st.write("Upload your resume and paste a job description to see how you match up.")

    # File uploader for the PDF
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type="pdf")
    # Text area for the Job Description
    job_description = st.text_area("Paste the Job Description here:", height=250)

    if uploaded_resume and job_description:
        if st.button("Analyze Match"):
            with st.spinner("Reading resume and comparing..."):
                try:
                    # 1. Extract text from PDF
                    import pypdf
                    reader = pypdf.PdfReader(uploaded_resume)
                    resume_text = ""
                    for page in reader.pages:
                        resume_text += page.extract_text()

                    # 2. Build the "Expert Recruiter" Prompt
                    match_prompt = f"""
                    You are a Senior Technical Recruiter. Compare the following Resume text with the Job Description.
                    
                    RESUME TEXT:
                    {resume_text}
                    
                    JOB DESCRIPTION:
                    {job_description}
                    
                    Please provide:
                    1. A 'Match Percentage' (0-100%).
                    2. A list of 'Missing Keywords' (important skills in the JD not found in the resume).
                    3. Three specific 'Actionable Tips' to improve this resume for this specific job.
                    """

                    # 3. Get response from Gemini
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(match_prompt)
                    
                    st.divider()
                    st.subheader("Match Results")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
# --- MODE 4: VOICE MODE  ---
elif app_mode == "Voice Assistant":
    st.header("🎙️ AI Voice Assistant")
    st.write("Record your voice and get an AI response!")

    from gtts import gTTS
    import io

    # 1. Audio Input from User
    audio_value = st.audio_input("Say something to the AI:")

    if audio_value:
        if st.button("Process Voice"):
            with st.spinner("Thinking..."):
                # Note: For full speech-to-text, you'd usually use OpenAI Whisper 
                # or Google Cloud Speech. For now, let's process the input logic!
                
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # For this demo, we'll simulate the interaction
                # In a real app, you'd send the audio file to Gemini's multimodal endpoint
                response = model.generate_content("The user just spoke to you. Greet them and ask how you can help with their code.")
                
                st.markdown(f"### AI Response: \n {response.text}")

                # 2. Convert Text back to Speech
                tts = gTTS(text=response.text, lang='en')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                
                st.audio(audio_fp, format='audio/mp3')                   
st.sidebar.markdown("---")
with st.sidebar.expander("👨‍💻 About the Developer"):
    st.write("""
    **Name:** Ainwin
    **Focus:** AI Integrations & Full-Stack Python
    **GitHub:** [https://github.com/Ainwin]
    **LinkedIn:** [https://www.linkedin.com/in/ainwin-antony-b8a232305?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app]
    """)