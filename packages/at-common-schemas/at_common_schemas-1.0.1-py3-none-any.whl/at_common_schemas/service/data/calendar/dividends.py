from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class CalendarDividendsItem(BaseSchema):
    symbol: str
    dividend: float
    adj_dividend: float
    record_date: datetime | None
    payment_date: datetime | None

class CalendarDividends(BaseSchema):
    date: datetime
    dividends: List[CalendarDividendsItem]

class CalendarDividendsRequest(BaseSchema):
    from_date: datetime
    to_date: datetime

class CalendarDividendsResponse(BaseSchema):
    calendar: List[CalendarDividends]