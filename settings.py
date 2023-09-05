import sys
from pathlib import Path

import pandas as pd
from boltons.funcutils import partial
from loguru import logger
from pydantic import Field, field_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    username: str
    password: str
    host: str
    port: int
    name: str

    def get_url(self, namespace: str = 'postgresql+asyncpg'):
        return f'{namespace}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}'


class OSRM(BaseModel):
    host: str
    port: int

    @property
    def base_url(self):
        return f'http://{self.host}:{self.port}'

    @property
    def driving_url(self):
        return f'{self.base_url}/table/v1/driving'

    @property
    def car_url(self):
        return f'{self.base_url}/route/v1/car'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).with_name('.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='_',
    )

    project_folder: Path = Field(alias='project_dir')
    storage_folder: Path = Field(alias='storage_dir')

    osrm: OSRM

    @field_validator('project_folder', 'storage_folder')
    def check_folder(cls, v):
        assert v.exists()
        return v


settings = Settings()

pd.set_option('max_colwidth', 40)
# pd.set_option("display.max_rows", None)
pd.set_option('display.width', None)

# np.set_printoptions(threshold=np.inf, linewidth=np.inf)


no = 328
logger.remove()
logger.add(sys.stdout, colorize=True, format="{level.icon} <level>{message}</level>")
logger.level("CarManager", no=no, color="<cyan>", icon="🚛")
logger.level("CarManagerShifted", no=no, color="<cyan>", icon="🚛")
logger.level("StationManager", no=no, color="<yellow>", icon="🎁")
logger.level("Dispatcher", no=no, color="<fg #0eff00>", icon="🧠")
# noinspection SpellCheckingInspection
logger.level("Order", no=no, color="<fg #530154><bg #E8DAEF>", icon="🟣")
logger.level("OrderManager", no=no, color="<fg #d6e7d6><bg #00688b>", icon="🏵")
logger.level("OrderManagerHistoric", no=no, color="<fg #d6e7d6><bg #00688b>", icon="🏵")
logger.level("BatchManager", no=no, color="<fg #f7e9b5><bg #5a5a5a>", icon="💮")
logger.level("Station", no=no, color="<fg #b993a6>", icon="📦")
logger.level("Car", no=no, color="<fg #E25D00>", icon="🚘")
