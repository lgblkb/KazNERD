from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).with_name('.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='_',
    )

    project_folder: Path = Field(alias='project_dir')
    storage_folder: Path = Field(alias='storage_dir')

    @field_validator('project_folder', 'storage_folder')
    def check_folder(cls, v):
        assert v.exists()
        return v


settings = Settings()

# np.set_printoptions(threshold=np.inf, linewidth=np.inf)
