from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class NewsStock(BaseSchema):
    symbol: str
    published_date: datetime
    headline: str
    image: str
    source: str
    summary: str
    url: str

class NewsStockLatestRequest(BaseSchema):
    symbol: str
    limit: int

class NewsStockLatestResponse(BaseSchema):
    news: List[NewsStock]