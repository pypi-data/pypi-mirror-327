from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class StockProfileRequest(BaseSchema):
    symbol: str

class StockProfileResponse(BaseSchema):
    symbol: str
    exchange: str
    name: str
    description: str
    currency: str
    country: str
    address: str
    sector: str
    industry: str
    ceo: str
    ipo_date: datetime

class StockProfileBatchRequest(BaseSchema):
    symbols: List[str]

class StockProfileBatchResponse(BaseSchema):
    profiles: List[StockProfileResponse]