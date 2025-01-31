from abc import ABC, abstractmethod

from src.dto.request import ResponseFromAgent


class BaseAgent(ABC):

    @abstractmethod
    async def find_answer(self, prompt: str) -> ResponseFromAgent:
        pass

    @abstractmethod
    def get_sign(self):
        pass
