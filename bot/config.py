from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Telegram
    bot_token: str = Field(alias="BOT_TOKEN")
    
    # LMS API
    lms_api_url: str = Field(alias="LMS_API_URL", default="http://localhost:42002")
    lms_api_key: str = Field(alias="LMS_API_KEY")
    
    # LLM API
    llm_api_key: str = Field(alias="LLM_API_KEY")
    llm_api_base_url: str = Field(alias="LLM_API_BASE_URL", default="http://localhost:42005/v1")
    llm_api_model: str = Field(alias="LLM_API_MODEL", default="qwen3-coder-plus")
    
    class Config:
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
