import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.dependency_injector import DependencyInjector

ClientManagerType = AsyncGenerator[AsyncClient, None]

@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture(scope="session")
async def container():
    dependency_injector = DependencyInjector()

    dependency_injector.wire(
        packages=['src'],
    )
    yield dependency_injector

@pytest.fixture(scope="session")
async def app(container) -> FastAPI:
    """
    Фикстура FastAPI приложения
    :return:
    """
    app = container.fastapi_app_singleton()
    yield app.get_instance()



@asynccontextmanager
async def client_manager(app: FastAPI, base_url: str ="http://test", **kw) -> ClientManagerType:
    """
    Клиентный менеджер приложения, контролирует жизненный цикл приложения
    """
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c


@pytest.fixture(scope="session")
async def client(app) -> ClientManagerType:
    """
    Фикстура клиента приложения для отправки запросов
    """
    async with client_manager(app) as c:
        yield c

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
