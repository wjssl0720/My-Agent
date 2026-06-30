from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ecom-agent-platform-v3"
    env: str = "local"
    runtime_model_policy: str = "local_harness"
    default_model: str = "qwen-plus"
    trace_enabled: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
