"""Global Settings Configuration.

Loads all configuration from environment variables (.env file).
"""

from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


# Load .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Settings(BaseSettings):
    """Global application settings"""

    # --- LLM Configuration ---
    llm_model: str = Field(default="mistral-large-latest", env="LLM_MODEL")
    mistral_api_key: Optional[str] = Field(default=None, env="MISTRAL_API_KEY")
    qwen_api_key: Optional[str] = Field(default=None, env="QWEN_API_KEY")

    # --- Execution Parameters ---
    batch_size: int = Field(default=4, env="BATCH_SIZE")
    retry_profile: str = Field(
        default="micro-batch-recovery", env="RETRY_PROFILE")
    max_retries: int = Field(default=5, env="MAX_RETRIES")
    api_timeout: int = Field(default=60, env="API_TIMEOUT")

    # --- GraphDB Configuration ---
    graphdb_endpoint: Optional[str] = Field(
        default=None, env="GRAPHDB_ENDPOINT")
    graphdb_repository: str = Field(
        default="default", env="GRAPHDB_REPOSITORY")
    graphdb_username: Optional[str] = Field(
        default=None, env="GRAPHDB_USERNAME")
    graphdb_password: Optional[str] = Field(
        default=None, env="GRAPHDB_PASSWORD")

    # --- Data Paths ---
    data_input_dir: Path = Field(default="data/input", env="DATA_INPUT_DIR")
    data_processed_dir: Path = Field(
        default="data/processed", env="DATA_PROCESSED_DIR")
    data_golden_sets_dir: Path = Field(
        default="data/golden_sets", env="DATA_GOLDEN_SETS_DIR"
    )
    data_cache_dir: Path = Field(default="data/cache", env="DATA_CACHE_DIR")

    # --- Logging ---
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Path = Field(default="logs/semantic_rag.log", env="LOG_FILE")

    # --- Feature Flags ---
    enable_multilingual: bool = Field(default=True, env="ENABLE_MULTILINGUAL")
    enable_aas_projection: bool = Field(
        default=False, env="ENABLE_AAS_PROJECTION")
    enable_graphdb_publication: bool = Field(
        default=False, env="ENABLE_GRAPHDB_PUBLICATION")

    # --- Advanced ---
    verbose: bool = Field(default=False, env="VERBOSE")
    temp_dir: Path = Field(default=".tmp", env="TEMP_DIR")

    # --- Project-Specific ---
    reference_project: str = Field(
        default="broaching-cnc-8070", env="REFERENCE_PROJECT")
    default_manual_id: str = Field(default="", env="DEFAULT_MANUAL_ID")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_graphdb_enabled(self) -> bool:
        """Check if GraphDB is properly configured"""
        return bool(
            self.enable_graphdb_publication
            and self.graphdb_endpoint
            and self.graphdb_username
        )

    @property
    def has_api_key(self) -> bool:
        """Check if API key is configured"""
        if self.llm_model == "mistral-large-latest":
            return bool(self.mistral_api_key)
        elif "qwen" in self.llm_model.lower():
            return bool(self.qwen_api_key)
        return False

    def get_api_key(self) -> str:
        """Get the appropriate API key"""
        if self.llm_model == "mistral-large-latest":
            if not self.mistral_api_key:
                raise ValueError("MISTRAL_API_KEY not set in .env")
            return self.mistral_api_key
        elif "qwen" in self.llm_model.lower():
            if not self.qwen_api_key:
                raise ValueError("QWEN_API_KEY not set in .env")
            return self.qwen_api_key
        raise ValueError(f"Unknown LLM model: {self.llm_model}")


# Global settings instance
settings = Settings()

# Create required directories
for directory in [settings.data_processed_dir, settings.data_golden_sets_dir, settings.data_cache_dir]:
    directory.mkdir(parents=True, exist_ok=True)

settings.log_file.parent.mkdir(parents=True, exist_ok=True)
