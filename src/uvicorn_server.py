import uvicorn
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI

from src.fast_api_app import FastAPIApp


class UvicornServer:
    """
    Класс, отвечающий за конфигурацию uvicorn сервера

    A.Vorobyev <A.Vorobyev@winsolutions.ru>
    """

    __port: int
    __host: str
    __reload: bool
    __fastapi_app: FastAPI

    @inject
    def __init__(
            self,
            port: int = Provide["settings.provided.server.port"],
            host: str = Provide["settings.provided.server.host"],
            fastapi_app: FastAPIApp = Provide["fastapi_app_singleton"],
    ):
        """
        :param port: - порт приложения
        :param host: - хост приложения
        :param fastapi_app: - класс обёртка над фастапи
        """
        self.__port = port
        self.__host = host
        self.__fastapi_app = fastapi_app.get_instance()

    def run(self):
        """
        Запуск сервера
        """
        uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
        del uvicorn_log_config["loggers"]

        uvicorn.run(
            app=self.__fastapi_app,
            host=self.__host,
            port=self.__port,
            log_config=uvicorn_log_config,
        )
