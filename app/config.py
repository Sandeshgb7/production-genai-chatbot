from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "chatbot"
    env: str = "dev"

    postgres_url: str | None = None
    redis_url: str | None = None

    openai_api_key: str | None = None
    langchain_api_key: str | None = None
    langchain_tracing_v2: bool = False

    class Config:
        env_file = ".env"


# 👇 THIS LINE IS MISSING IN YOUR CODE
settings = Settings()