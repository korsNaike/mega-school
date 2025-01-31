from abc import ABC, abstractmethod


class BaseSearchEngine(ABC):

    @abstractmethod
    async def find_links(self, query: str, links_count: int = 3) -> list[str]:
        """
        Найти релевантные ссылки по запросу пользователя
        :param query: Текст запроса
        :param links_count: Количество ссылок
        :return:
        """
        pass
