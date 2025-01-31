from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.dto.request import PredictionRequest
from src.routers.base_router import BaseRouter
from src.service.itmo_service import ItmoService

@inject
async def request(
                data: PredictionRequest,
                service: ItmoService = Depends(Provide['itmo_service_factory'])
):
    return await service.answer_for_query(data)

class ItmoRouter(BaseRouter):

    def init_routes(self):

        self._router.post('/request')(request)




