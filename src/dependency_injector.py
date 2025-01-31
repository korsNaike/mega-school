from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory, List
from faker.proxy import Faker
from openai import OpenAI

from src.agent.gigachat_agent import GigaChatAgent
from src.agent.openai_agent import OpenAIAgent
from src.application_logger import ApplicationLogger
from src.config import Settings
from src.fast_api_app import FastAPIApp
from src.routers.itmo_router import ItmoRouter
from src.search_engine.google_search_engine import GoogleSearchEngine
from src.service.itmo_service import ItmoService
from src.uvicorn_server import UvicornServer


class DependencyInjector(DeclarativeContainer):

    settings = Singleton(Settings)

    logger_factory = Factory(ApplicationLogger)

    openai_client = Singleton(OpenAI, api_key=settings.provided.OPENAI_KEY, base_url=settings.provided.OPENAI_URL)

    faker_singleton = Singleton(Faker)

    search_engine_singleton = Singleton(GoogleSearchEngine)

    agent_singleton = Singleton(OpenAIAgent)

    itmo_service_factory = Factory(ItmoService)

    fastapi_app_singleton = Singleton(
        FastAPIApp,
        routers=List(
            Singleton(ItmoRouter)
        )
    )

    uvicorn_server_singleton = Singleton(UvicornServer)
