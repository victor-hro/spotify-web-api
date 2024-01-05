# openai_functions.py

from openai import OpenAI
import requests
from typing import Optional
from PIL import Image
from io import BytesIO


def generate_chat_response(client, system_prompt: str, user_prompt: str) -> str:
    """
    Generates a chat response using OpenAI GPT-3.5 Turbo model.

    Parameters:
    - client (OpenAI): An instance of OpenAI client.
    - system_prompt (str): The prompt for the system role.
    - user_prompt (str): The prompt for the user role.

    Returns:
    - str: The generated chat response.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    msg = completion.choices[0].message.content
    return msg
