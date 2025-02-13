from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class NewsMarket(BaseSchema):
    published_date: datetime
    headline: str
    image: str
    source: str
    summary: str
    url: str

class NewsMarketLatestRequest(BaseSchema):
    limit: int

class NewsMarketLatestResponse(BaseSchema):
    news: List[NewsMarket]