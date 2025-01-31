from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseRouter(ABC):

    def __init__(self):
        self._router = APIRouter()

    @abstractmethod
    def init_routes(self):
        pass

    def get_instance(self):
        return self._router
