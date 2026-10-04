from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str="postgresql+asyncpg://postgres:postgres@localhost:5432/ragtrust"
 api_key:str="change-me"; issuer:str="ragtrust-local"; passport_ttl_seconds:int=86400
 min_trust_score:float=.35; max_poison_score:float=.70
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
