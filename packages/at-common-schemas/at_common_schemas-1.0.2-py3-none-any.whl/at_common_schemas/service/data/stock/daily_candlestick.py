from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class StockDailyCandlestick(BaseSchema):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockDailyCandlestickRequest(BaseSchema):
    symbol: str
    date_from: datetime
    date_to: datetime

class StockDailyCandlestickResponse(BaseSchema):
    candlesticks: List[StockDailyCandlestick]