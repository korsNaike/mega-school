from pydantic_settings import BaseSettings, SettingsConfigDict

class ServerSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8080

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra='ignore'
    )

    server: ServerSettings = ServerSettings()

    PROJECT_NAME: str
    PROJECT_VERSION: str = "0.0.1"
    LOG_LEVEL: str = "DEBUG"

    DEBUG_MODE: bool = True

    API_V1_STR: str = "/api"

    OPENAI_KEY: str
    OPENAI_URL: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    AGENT_SYSTEM_PROMPT: str = "Ты знаешь всё о российском университете ИТМО, твоя задача - помогать искать информацию по данному университету и выдавать верные ответы на тест."

    GIGACHAT_AUTH: str = "<TOKEN>"



settings = Settings()
