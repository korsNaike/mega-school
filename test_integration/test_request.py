from typing import Any

import pytest
from httpx import AsyncClient

@pytest.mark.anyio
@pytest.mark.parametrize(
    "query, answer",
    [
        (
                {
                    "query": "В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород",
                    "id": 1
                },
            2
        ),
        (
                {
                    "query": "В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015",
                    "id": 2
                },
            2
        ),
        (
                {
                    "query": "В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities",
                    "id": 3
                },
            3
        )
    ]
)
async def test_request(client: AsyncClient, query: dict[str, Any], answer: int) -> None:
    response = await client.post(
        url="api/request", json=query
    )

    data = response.json()

    assert response.status_code == 200
    assert data["answer"] == answer
    assert data["id"] == query["id"]
    assert "sources" in data
    assert "reasoning" in data
