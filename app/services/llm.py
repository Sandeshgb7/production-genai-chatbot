from app.config import settings
from openai import AsyncOpenAI

# Groq uses OpenAI-compatible API
client = AsyncOpenAI(
    api_key=settings.openai_api_key,   # reuse same field OR rename later
    base_url="https://api.groq.com/openai/v1"
)


async def generate_response(messages):
    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",   # fast + free tier#llama3-8b-8192
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content