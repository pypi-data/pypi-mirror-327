from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema

class CalendarSplitsItem(BaseSchema):
    symbol: str
    numerator: int
    denominator: int

class CalendarSplits(BaseSchema):
    date: datetime
    splits: List[CalendarSplitsItem]

class CalendarSplitsRequest(BaseSchema):
    from_date: datetime
    to_date: datetime

class CalendarSplitsResponse(BaseSchema):
    calendar: List[CalendarSplits]