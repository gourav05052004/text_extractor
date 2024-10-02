from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="MultiLanguage Handwritten Text Extractor")

st.header("MultiLanguage Handwritten Text Extractor")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Extract the text from the image")

# Define input prompt
input_prompt = """You are an AI assistant trained on a large dataset of images, including handwritten texts. Your task is to extract and read the text from any image provided.
The image may contain human handwriting or printed text. If you are unable to understand a word or sentence completely, attempt to predict and autocomplete the text based on the context. 
Ensure that the output is as accurate and readable as possible. If the handwriting is unclear or ambiguous, make reasonable assumptions and provide your best guess for the missing or incomplete parts. Please display the extracted or predicted text."""

# If submit is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("The Text is")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")
