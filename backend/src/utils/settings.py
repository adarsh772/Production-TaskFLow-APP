from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    EXP_TIME: int = 30  # access token lifetime, in minutes
    ALLOWED_ORIGINS: str = "*"  # comma-separated list of allowed CORS origins

    @property
    def cors_origins(self) -> list[str]:
        if self.ALLOWED_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
