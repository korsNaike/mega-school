import httpx
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from faker.proxy import Faker
from tenacity import stop_after_attempt, retry

from src.agent.base_agent import BaseAgent
from src.dto.request import PredictionRequest, PredictionResponse
from src.search_engine.base_search_engine import BaseSearchEngine
from src.service.base_service import BaseService


class ItmoService(BaseService):

    @inject
    def __init__(
            self,
            search_engine: BaseSearchEngine = Provide['search_engine_singleton'],
            agent: BaseAgent = Provide['agent_singleton'],
            faker: Faker = Provide['faker_singleton'],
            **kwargs
    ):
        super().__init__(**kwargs)
        self.__search_engine = search_engine
        self.__agent = agent
        self.__faker = faker

    async def answer_for_query(self, dto: PredictionRequest) -> PredictionResponse:
        query_text = dto.query
        splitted = query_text.split('\n1.', 1)
        if len(splitted) == 2:
            question, answers = splitted
        else:
            question, answers = (query_text, '')
        self._logger.debug(f'Query: {query_text}, Question: {question}, Answers: {answers}')

        links = await self.__search_engine.find_links(question, links_count=1)
        self._logger.debug(f'Links: {links}')

        web_context = await self.__get_web_context(links)

        prepared_prompt = await self.__prepare_prompt_text(question, answers, web_context)
        answer = await self.__agent.find_answer(prepared_prompt)
        self._logger.debug(f'Answer: {answer}')

        result = PredictionResponse(
            id=dto.id,
            answer=answer.answer,
            reasoning=answer.reasoning + self.__agent.get_sign(),
            sources=links
        )
        self._logger.debug(f'Result: {result}')
        return result

    async def __prepare_prompt_text(self, question: str, answers: str, context: str) -> str:
        return """
        Ответь на вопрос:{:s}\n .Выбери правильный вариант ответа:\n {:s} \n.
        Ответ предоставь СТРОГО в следующем формате:
        {{ "answer":номер ответа из вариантов ответа, "reasoning": Объяснение выбора,"sources": [массив сайтов, информация с которых использовалась]}}
        Если вариантов ответов не было предоставлено, напиши null в том поле.

        Информацию ищи среди данного текста, собранного с веб-страниц: {:s}

        """.format(question, answers, context)

    @retry(stop=stop_after_attempt(3))
    async def __fetch_page_content(self, url):
        headers = {"User-Agent": self.__faker.user_agent()}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(separator="\n", strip=True)

    async def __get_web_context(self, links: list[str]) -> str:
        content = ""
        for link in links:
            try:
                content += await self.__fetch_page_content(link) + '\n\n'
            except Exception as e:
                self._logger.error(f'Error fetching {link}: {e}')

        return content


