from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class StockQuoteRequest(BaseSchema):
    symbol: str

class StockQuoteResponse(BaseSchema):
    symbol: str
    price: float
    previous_close: float
    change: float
    changes_percentage: float
    volume: int
    avg_volume: float
    day_low: float
    day_high: float
    year_low: float
    year_high: float
    market_cap: float
    pe: float
    shares_outstanding: int
    timestamp: datetime

class StockQuoteBatchRequest(BaseSchema):
    symbols: List[str]

class StockQuoteBatchResponse(BaseSchema):
    quotes: List[StockQuoteResponse]