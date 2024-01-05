import streamlit as st
from openai import OpenAI
import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import find_dotenv, load_dotenv
import time
from typing import Optional

from utils.chat_response import generate_chat_response
from utils.image_response import generate_image, generate_image_with_progress


load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Streamlit Page Configuration
st.set_page_config(
    page_title="Let's Talk - Urban Style",
    # layout="wide",
    initial_sidebar_state="expanded",
)


with st.sidebar:
    st.title('Tivim LLM Web App')
    st.markdown("---")
    st.header('Text Generator by:\nCHAT GPT 3.5 TURBO')
    st.markdown("---")
    st.header('Image Generator by:\nDALL-E-2')
    st.markdown("---")

st.subheader("AI Chatbot")

tab1, tab2 = st.tabs(['Text', 'Image'])

with tab1:
    st.chat_message('user').write("Who do you want to talk to?")
    text_system_prompt = st.text_input("Enter prompt for the person you want to talk to", '')

    st.chat_message('user').write("Enter prompt for text generator")
    text_user_prompt = st.text_input("Enter prompt for text generator", '')

    if len(text_system_prompt) > 1000 or len(text_user_prompt) > 1000:
        st.error("Por favor, reduza o comprimento do prompt para 1000 caracteres ou menos.")
    else:
        if st.button('Generate Response'):
            ai_response = generate_chat_response(client, text_system_prompt, text_user_prompt)
        
            st.chat_message('assistant').write("**AI Response:**")
            st.write(ai_response)

with tab2:
    st.chat_message('user').write("Enter prompt for image generation")
    image_prompt = st.text_input("Enter prompt for image generation", 'Type something')

    if len(image_prompt) > 1000:
        st.error("Por favor, reduza o comprimento do prompt para 1000 caracteres ou menos.")

    c1, c2, c3 = st.columns(3)
    with c1:
        size_config = st.selectbox("Image size", ("256x256", "512x512", "1024x1024"))

    with c2:
        quality_config = st.selectbox("Quality", ("standard", "hd"))

    with c3:
        style_config = st.selectbox("Style", ("natural", "vivid"))


    if st.button('Generate Image'):
        generate_image_with_progress(
            client, image_prompt
            , size_config=size_config
            , quality_config=quality_config
            , style_config=style_config
            )