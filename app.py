from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set page config as the first Streamlit command
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)  # Proper way to configure the API key

# Function to get Gemini response
def get_gemini_response(input_text, image_data, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')  # Ensure this is the correct model type

    # Pass the input_text, image_data (PIL Image), and prompt directly to the API
    response = model.generate_content([input_text, image_data, prompt])
    return response.text

# Upload image section
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image_data = None  # Initialize image_data as None
if uploaded_file is not None:
    image_data = Image.open(uploaded_file)
    st.image(image_data, caption="Uploaded Image", use_column_width=True)

# Button to submit
submit = st.button("Tell me about the document")

# Input prompt for the Gemini API
input_prompt = """You are an expert in understanding invoices.
We will upload an image as an invoice and you will have to answer any questions based on the uploaded invoice image."""

# App header
st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

# Description with custom styling
text = ("Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
        "from diverse multilingual documents, transcending language barriers with "
        "precision and efficiency for enhanced productivity and decision-making.")
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# Process image and get response when submit is clicked
if submit and image_data is not None:
    response = get_gemini_response(input_prompt, image_data, input_prompt)  # Pass the PIL Image directly
    st.subheader("The response is:")
    st.write(response)
