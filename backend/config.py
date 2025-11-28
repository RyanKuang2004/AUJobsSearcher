from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class ModelSettings(BaseSettings):
    """LLM model configuration for various components"""
    agent_model: str = "gpt-5-nano"
    agent_temperature: float = 0.0
    job_analyzer_model: str = "gpt-5-nano"
    job_analyzer_temperature: float = 1.0


class ScraperSettings(BaseSettings):
    """Job scraper configuration"""
    search_keywords: List[str] = [
        "Machine Learning",
        "Data Scientist",
        "Software Engineer",
        "AI Engineer"
    ]
    max_pages: int = 3
    days_from_posted: int = 2
    initial_days_from_posted: int = 31


class JobProcessorSettings(BaseSettings):
    """Job analysis processor configuration"""
    batch_size: int = 10
    max_retries: int = 3
    retry_delay_seconds: int = 5


class Settings(BaseSettings):
    """Main application settings"""
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    models: ModelSettings = ModelSettings()
    scraper: ScraperSettings = ScraperSettings()
    processor: JobProcessorSettings = JobProcessorSettings()


# Global settings instance
settings = Settings()
