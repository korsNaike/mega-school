from logging import getLogger, Logger, StreamHandler
from types import TracebackType
from typing import Type

from colorlog import ColoredFormatter
from dependency_injector.wiring import inject, Provide


class ApplicationLogger:
    """
    Класс логгера приложения
    """

    __logger: Logger
    __handler: StreamHandler
    __level: str

    @inject
    def __init__(
            self,
            application_name: str = Provide['settings.provided.PROJECT_NAME'],
            level: str = Provide['settings.provided.LOG_LEVEL'],
    ):
        """
        :param application_name: - Название приложения
        :param level: - уровень логгирования
        """

        formatter = ColoredFormatter(
            f"%(log_color)s{application_name}%(reset)s - [%(name)s] - %(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red"
            }
        )

        self.__level = level

        self.__handler = StreamHandler()
        self.__handler.setLevel(self.__level)
        self.__handler.setFormatter(formatter)

    def activate(self, name: str, clear: bool = True):
        """
        Активация логгера

        :param clear: очистить ли остальные хендлеры
        :param name: название модуля
        :return:
        """
        self.__logger = getLogger(name)

        if clear:
            self.__logger.handlers.clear()

        self.__logger.setLevel(self.__level)
        self.__logger.addHandler(self.__handler)

    def debug(self, message: str):
        self.__logger.debug(message)

    def info(self, message: str):
        self.__logger.info(message)

    def warning(self, message: str):
        self.__logger.warning(message)

    def error(
            self,
            message: str,
            exc_info: None | bool | tuple[Type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | BaseException = None
    ):
        self.__logger.error(message, exc_info=exc_info)

    def critical(self, message: str):
        self.__logger.critical(message)
