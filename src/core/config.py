from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = 'qna'
    API_V1_PREFIX: str = '/api/v1'
    DB_HOST: str = 'qna_db'
    DB_PORT: int = 5432
    DB_USER: str = 'qna_user'
    DB_PASSWORD: str = 'qna_password'
    DB_NAME: str = 'qna'
    SQLALCHEMY_ECHO: bool = False

    model_config = SettingsConfigDict(env_file = '.env', env_prefix = '', extra = 'ignore')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()