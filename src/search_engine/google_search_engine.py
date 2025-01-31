from googlesearch import search

from src.search_engine.base_search_engine import BaseSearchEngine


class GoogleSearchEngine(BaseSearchEngine):

    async def find_links(self, query: str, links_count: int = 3) -> list[str]:
        """
        Найти релевантные ссылки по запросу пользователя
        :param query: Текст запроса
        :param links_count: Количество ссылок
        :return:
        """
        query = self.__extract_before_choices(query)
        links = []
        for result in search(query, num_results=links_count):
            links.append(result)
        return links


    def __extract_before_choices(self, text: str) -> str:
        """
        Отделить вопрос от вариантов ответов
        :param text: Полный текст запроса пользователя
        :return: Только вопрос
        """
        return text.split("\n1.", 1)[0]
