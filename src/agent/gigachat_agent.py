import json
import uuid
from typing import Any

from dependency_injector.wiring import inject, Provide
from httpx import AsyncClient
from tenacity import retry, stop_after_attempt

from src.agent.base_agent import BaseAgent
from src.application_logger import ApplicationLogger
from src.dto.request import ResponseFromAgent


class GigaChatAgent(BaseAgent):

    _access_token: str

    @inject
    def __init__(
            self,
            auth_id: str = Provide['settings.provided.GIGACHAT_AUTH'],
            model: str = "GigaChat",
            logger: ApplicationLogger = Provide['logger_factory'],
            system_prompt: str = Provide["settings.provided.AGENT_SYSTEM_PROMPT"]
    ):
        """
        :param auth_id: Токен из личного кабинета
        :param model: Вид модели для генерации текста
        """
        self.auth_id = auth_id
        self.model = model
        self._system_prompt = system_prompt


        self._logger = logger
        self._logger.activate(self.__class__.__name__)

    async def find_answer(self, prompt: str) -> ResponseFromAgent:
        async with AsyncClient(verify=False) as client:
            await self.__get_access_token(client)
            prompt_data = await self.__gen_data_for_message(prompt)
            answer = await self.__ask_model(prompt_data, client)

            answer.replace("```json", '')
            answer.replace("```", '')
            self._logger.debug(f"JSON-message from AI-agent: {answer}")
            response_dict = json.loads(answer)

            return ResponseFromAgent(**response_dict)

    def get_sign(self):
        return "\n answered by GigaChat"

    @retry(reraise=True, stop=stop_after_attempt(3))
    async def __get_access_token(self, client: AsyncClient) -> str | None:
        """
        Получает токен доступа для API GigaChat.

        Returns:
            str|None: Токен доступа, если успешно, в противном случае возвращает None.
        """
        url_giga = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        data = "scope=GIGACHAT_API_PERS"
        auth_id = self.auth_id
        request_id = str(uuid.uuid4())

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Accept": "application/json",
            'RqUID': request_id,
            'Authorization': 'Basic ' + auth_id
        }

        try:
            response_giga = await client.post(url_giga, headers=headers, data=data)
            if response_giga.status_code != 200:
                raise Exception(f"Ошибка авторизации GigaChat: {response_giga.text}")

        except Exception as e:
            self._logger.error("Ошибка при авторизации GigaChatApi", exc_info=e)
            raise e

        self._access_token = response_giga.json().get('access_token')
        return self._access_token

    async def __gen_data_for_message(self, content: str) -> dict[str, Any]:
        """
        Генерирует данные для запроса к API GigaChat

        Args:
            content (str): Текст запроса

        Returns:
            dict: Словарь, содержащий данные для запроса к API GigaChat.
        """
        # Разделение строки content на фрагменты длиной до 4000 символов
        content_splitted = [content[i:i + 1000] for i in range(0, len(content), 1000)]
        content_splitted = content_splitted[:2]

        # Создание списка сообщений
        messages = [self.__get_role_prompt()]
        for part in content_splitted:
            messages.append({
                "role": "user",
                "content": part
            })

        return {
            "model": self.model,
            "messages": messages,
            "n": 1,
            "stream": False,
            "update_interval": 0
        }

    def __get_role_prompt(self) -> dict:
        """
        Возвращает словарь с ролью и содержанием
        Returns:
            dict: Словарь с ролью и содержанием.
        """
        return {
            "role": "system",
            "content": self._system_prompt
        }

    @retry(reraise=True, stop=stop_after_attempt(3))
    async def __ask_model(self, data: dict, client: AsyncClient):
        """
        Отправляет запрос к API GigaChat и получает ответ.

        Args:
            data (dict): Данные, которые нужно передать в запросе.
            client (AsyncClient): Клиент отправки запросов

        Returns:
            str: Содержимое ответа, если код состояния ответа 200
        """
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._access_token}'
        }
        self._logger.debug(f"Sended: {data}")
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            self._logger.error(f"Ошибка запроса к GigaChatAPI ({response.text})")
            raise Exception(response.text)
