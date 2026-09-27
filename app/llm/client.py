from http import client
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_llm(prompt:str):
    response = client.response.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response
