import json

from dependency_injector.wiring import inject, Provide
from openai import OpenAI
from tenacity import retry, stop_after_attempt

from src.agent.base_agent import BaseAgent
from src.application_logger import ApplicationLogger
from src.dto.request import ResponseFromAgent


class OpenAIAgent(BaseAgent):

    @inject
    def __init__(
            self,
            logger: ApplicationLogger = Provide['logger_factory'],
            client: OpenAI = Provide["openai_client"],
            system_prompt: str = Provide["settings.provided.AGENT_SYSTEM_PROMPT"],
            model: str = Provide["settings.provided.OPENAI_MODEL"],
    ):
        self._logger = logger
        self._logger.activate(self.__class__.__name__)
        self.__client = client
        self.__system_prompt = system_prompt
        self.__model = model


    @retry(reraise=True, stop=stop_after_attempt(3))
    async def find_answer(self, prompt: str) -> ResponseFromAgent:
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content": self.__system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        self._logger.debug(f"Answer from gpt: {response}")

        response_json = response.choices[0].message.content
        response_json = response_json.replace("```json", '')
        response_json = response_json.replace("```", '')
        self._logger.debug(f"JSON-message from gpt: {response_json}")
        response_dict = json.loads(response_json)

        return ResponseFromAgent(**response_dict)

    def get_sign(self):
        return "\n" + self.__model
