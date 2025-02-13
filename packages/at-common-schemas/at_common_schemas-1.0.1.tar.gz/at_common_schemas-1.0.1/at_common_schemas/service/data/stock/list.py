from typing import List
from at_common_schemas.service.data.base import BaseSchema

class StockListRequest(BaseSchema):
    exchanges: List[str]

class StockListResponse(BaseSchema):
    symbols: List[str]