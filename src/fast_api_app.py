from contextlib import asynccontextmanager

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI

from src.application_logger import ApplicationLogger
from src.config import Settings
from src.routers.base_router import BaseRouter


class FastAPIApp:
    """
    Класс, отвечающий за FastApi
    """

    __app: FastAPI
    """Инстанс класса FastAPI application из fastapi"""

    __logger: ApplicationLogger

    @inject
    def __init__(
            self,
            routers: list[BaseRouter],
            logger: ApplicationLogger = Provide["logger_factory"],
            settings: Settings = Provide['settings'],
    ):
        self.__logger = logger

        self.__app = FastAPI(
            title=settings.PROJECT_NAME,
            description="Мегашкола",
            version=settings.PROJECT_VERSION,
            lifespan=self.lifespan,
            debug=settings.DEBUG_MODE
        )

        for router in routers:
            router.init_routes()
            self.__app.include_router(router.get_instance(), prefix=settings.API_V1_STR)



    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        Жизненный цикл приложения FastAPI
        """
        await self.handle_startup()
        yield
        await self.handle_shutdown()


    async def handle_startup(self):
        """
        Действия перед запуском FastAPI приложения
        """
        self.__logger.activate("uvicorn")

    async def handle_shutdown(self):
        """
        Действия после остановки FastAPI приложения
        """
        pass

    def get_instance(self) -> FastAPI:
        return self.__app
