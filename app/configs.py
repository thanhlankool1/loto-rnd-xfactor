# -*- coding: utf-8 -*-
from typing import Optional, List, Union, Tuple
from pydantic import BaseSettings, AnyHttpUrl
import os

DEV = os.environ.get('DEV')
ENV_NAME = os.environ.get('ENV_NAME')

print('DEV', DEV, 'ENV_NAME', ENV_NAME)


class AppEnvConfig(BaseSettings):
    APP_BASE_DIR: Optional[str] = os.getcwd()
    APP_PROJECT_NAME: str = "FastApi-App"
    APP_SECRET_KEY: str = 'LoTo'
    APP_DEBUG: bool = True
    APP_USE_PROXY: bool = False
    APP_PROXY_SERVER: str = ""
    APP_NO_PROXY: str = '127.0.0.1,localhost'
    APP_USE_TZ: bool = False
    APP_TIMEZONE: str = 'UTC'
    APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_DOCS_URL: Optional[str] = '/docs'

    # -----------------web server-----------------
    SERVER_NAME: str = ''
    SERVER_HOST: AnyHttpUrl = 'http://localhost'

    GUNICORN_HOST: str = '0.0.0.0'
    GUNICORN_PORT: str = '9999'
    WEB_CONCURRENCY: str = '4'

    IP_VM: Optional[str] = None
    # -----------------end-----------------

    # -----------------middleware-----------------
    APP_MIDDLEWARE_ENABLE_BruteForceDefenderMiddleware: bool = False
    APP_MIDDLEWARE_ENABLE_IpProtectionMiddleware: bool = False
    APP_MIDDLEWARE_ENABLE_TrustedHostMiddleware: bool = False
    APP_MIDDLEWARE_ENABLE_CORSMiddleware: bool = True
    APP_MIDDLEWARE_ENABLE_SessionMiddleware: bool = False

    APP_MIDDLEWARE_TRUSTED_HOST: List[str] = ['localhost', '127.0.0.1']
    APP_MIDDLEWARE_LOCAL_IPS: List[str] = ["127.0.0.1", "localhost"]
    APP_MIDDLEWARE_ADMIN_IPS: List[str] = []

    APP_MIDDLEWARE_CORS_ALLOW_ORIGINS: List[str] = []
    APP_MIDDLEWARE_CORS_ALLOW_METHODS: List[str] = []
    APP_MIDDLEWARE_CORS_ALLOW_HEADERES: List[str] = []
    
    
    WS_SERVER_ENABLE_DEBUGGING: bool = False
    # ``'*'`` to allow all origins, or to ``[]`` to disable CORS handling, tested
    WS_SERVER_CORS_ORIGINS: Union[str, List] = "*"
    WS_SERVER_MOUNT_LOCATION: str = "/ws"
    WS_SERVER_SOCKETIO_PATH: str = "socket.io"
    WS_SERVER_KEEP_ALIVE: int = 120
    WS_SERVER_MAX_FILE_SIZE: int = 90 * (10**6)  # bytes  -> 10 Mb
    WS_SERVER_PING_TIMEOUT: int = 20  # s        -> 30 s
    WS_SERVER_PING_INTERVAL: int = 50  # s        -> 30 s
    
    # -----------------end-----------------


    APP_DB_SQLITE_PATH: str = 'sqlite://db.sqlite3'
    # -----------------end-----------------

    class Config:
        case_sensitive = True
        validate_assignment = True


env_file = None
if ENV_NAME:
    if ENV_NAME.endswith('.env'):
        file_path = os.path.join(os.getcwd(), 'env', ENV_NAME)
        if os.path.isfile(file_path):
            env_file = file_path
    else:
        file_path = os.path.join(os.getcwd(), 'env', f'{ENV_NAME}.env')
        if os.path.isfile(file_path):
            env_file = file_path


def notify_environment(from_env: str):
    print(2*'\n' + 50 * '-' + '\n')
    print('you select environment: ', from_env)
    print('\n' + 50 * '-' + 2 * '\n')


if DEV and env_file:
    notify_environment(env_file)
    settings = AppEnvConfig(_env_file=env_file)
else:
    if '.env' in os.listdir(os.getcwd()):
        notify_environment('.env')
        settings = AppEnvConfig(_env_file='.env')
    else:
        notify_environment('OS Environement')
        settings = AppEnvConfig()



settings.APP_NO_PROXY = settings.APP_NO_PROXY

print(settings.APP_NO_PROXY)


if __name__ == "__main__":
    pass
