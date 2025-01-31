from dependency_injector.wiring import inject, Provide

from src.application_logger import ApplicationLogger


class BaseService:

    @inject
    def __init__(self, logger: ApplicationLogger = Provide['logger_factory']):
        self._logger = logger
        self._logger.activate(self.__class__.__name__)
