from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "chatbot"
    env: str = "dev"  # dev | prod | test
    debug: bool = False

    # security
    secret_key: str = "change-this-in-prod"

    # database
    postgres_url: str | None = None
    redis_url: str | None = None

    # llm
    openai_api_key: str | None = None
    llm_model: str = "llama-3.1-70b-versatile"

    # observability
    langchain_api_key: str | None = None
    langchain_tracing_v2: bool = False


settings = Settings()