from datetime import datetime
from typing import List
from at_common_schemas.service.data.base import BaseSchema
from .constants import CalendarEarningsPublishTime

class CalendarEarningsItem(BaseSchema):
    symbol: str
    publish_time: CalendarEarningsPublishTime
    eps_actual: float
    eps_estimate: float
    revenue_actual: float
    revenue_estimate: float
    fiscal_date_ending: datetime

class CalendarEarnings(BaseSchema):
    date: datetime
    earnings: List[CalendarEarningsItem]

class CalendarEarningsRequest(BaseSchema):
    from_date: datetime
    to_date: datetime

class CalendarEarningsResponse(BaseSchema):
    calendar: List[CalendarEarnings]