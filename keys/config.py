from dataclasses import dataclass
from environs import Env


@dataclass
class FlaskConfig:
    secret_key: str

@dataclass
class DbConfig:
    host: str
    port: int
    password: str
    user: str
    database: str
    engine: str


@dataclass
class Config:
    db: DbConfig
    flask: FlaskConfig


def load_config():
    env = Env()
    env.read_env()

    return Config(
        db=DbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            engine=f"mysql+pymysql://{env.str('DB_USER')}:{env.str('DB_PASS')}@"
                   f"{env.str('DB_HOST')}/{env.str('DB_NAME')}?charset=utf8mb4"
        ),
        flask=FlaskConfig(
            secret_key=env.str('FLASK_SECRET_KEY')
        )
    )
