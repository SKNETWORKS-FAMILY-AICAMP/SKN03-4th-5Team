import streamlit as st
from openai import OpenAI
import time

@st.cache_resource 
def get_client():
    return OpenAI()

def response_from_llm(prompt, model_id: str = "gpt-4o-mini"):
    messages = []
    if len(prompt) == 0:
        messages.append(
            {
                "role": "assistant",
                "content": "You are a helpful assistant. You must answer in Korean."
            }
        )
    else:
        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

    streaming = get_client().chat.completions.create(
        model=model_id,
        messages=messages,
        stream=True
    )

    for chunk in streaming:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
            time.sleep(0.05)