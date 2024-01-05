# image_functions.py

import requests
from PIL import Image
from io import BytesIO
from typing import Optional
import time
import streamlit as st


def generate_image(
    client, 
    prompt: str, 
    size: Optional[str] = "256x256", 
    quality: Optional[str] = 'standard', 
    style: Optional[str] = 'natural'
) -> Image:
    """
    Generates an image using OpenAI DALL-E-2 model.

    Parameters:
    - client: An instance of the OpenAI client.
    - prompt (str): The prompt for generating the image.
    - size (Optional[str]): The size of the image (default: "256x256").
    - quality (Optional[str]): The quality of the image (default: "standard").
    - style (Optional[str]): The style of the image (default: "natural").

    Returns:
    - Image: The generated image.
    """
    response = client.images.generate(
        prompt=prompt,
        n=1,
        style=style,
        size=size,
        quality=quality,
    )

    img_url = response.data[0].url
    img_response = requests.get(img_url)
    return Image.open(BytesIO(img_response.content))


# Função para gerar a imagem com barra de progresso
def generate_image_with_progress(client, image_prompt, size_config, quality_config, style_config):
    progress_bar = st.progress(0)  # Inicializar a barra de progresso

    generated_image = generate_image(client, image_prompt, size=size_config, quality=quality_config, style=style_config)

    for percent_complete in range(100):
        time.sleep(0.02)  # Simular atraso (remova isso na produção)
        progress_bar.progress(percent_complete + 1)

    st.image(generated_image, caption='Generated Image', use_column_width=True)
