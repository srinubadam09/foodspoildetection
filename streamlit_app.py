import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import io

# Set Gemini API Key
GOOGLE_API_KEY = "AIzaSyD1XItbxOXLsvsK9RD-v_gLGwroSC2C43s"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to encode the image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Function to analyze food spoilage
def analyze_food(img_base64):
    prompt = """
    You are an expert in food quality assessment. Given an image of food, identify the food type and analyze visual cues such as color changes, mold growth, texture degradation, and other spoilage signs.

    **Task:**  
    1️⃣ **Identify** the food type (e.g., apple, bread, meat).  
    2️⃣ **Classify** its condition as:  
       - **Fresh** – Safe to eat.  
       - **Slightly Stale** – Can be consumed but with caution.  
       - **Spoiled** – Unsafe to eat, discard immediately.  
    3️⃣ **Explain** why the food is classified that way.

    **Considerations:**  
    - Presence of mold or fungal growth  
    - Discoloration (e.g., dark spots, unnatural hues)  
    - Texture abnormalities (e.g., excessive dryness, sliminess)  
    - Structural breakdown (e.g., rotting, excessive softness)  

    Provide a classification along with a short explanation.
    """

    image_data = {
        "mime_type": "image/jpeg",
        "data": img_base64
    }

    model = genai.GenerativeModel("gemini-1.5-flash")  
    response = model.generate_content([image_data, prompt])

    return response.text

# Streamlit UI
st.title("🍎🥦 AI-Powered Food Spoilage Detector")

# File Upload
uploaded_file = st.file_uploader("📷 Upload an image of food", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img_base64 = encode_image(image)

    if st.button("🔍 Analyze Food Condition"):
        with st.spinner("Analyzing... 🤖"):
            result = analyze_food(img_base64)

        st.subheader("🧐 Analysis Result:")
        st.write(result)

# Divider
st.markdown("---")

# --- Embedded Chatbot Section ---
st.subheader("🤖 AI Chatbot - Ask About Food Safety!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chatbot Response Function
def chatbot_response(query):
    chatbot_prompt = f"You are an AI expert in food safety. Answer user queries related to food spoilage, storage, and freshness.\n\nUser: {query}\nBot:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(chatbot_prompt)
    return response.text

# Chat Input
user_input = st.text_input("💬 Ask a question about food safety:")

if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

# Display chat history
chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")
