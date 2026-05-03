from app.config import settings
from openai import AsyncOpenAI

client = None

def get_client():
    global client
    if client is None:
        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    return client

async def generate_response(messages):
    client = get_client()

    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )

    return response.choices[0].message.content

