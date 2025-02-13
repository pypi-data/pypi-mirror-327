from enum import Enum

class CalendarEarningsPublishTime(Enum):
    BEFORE_MARKET_OPEN = "BEFORE_MARKET_OPEN"
    AFTER_MARKET_CLOSE = "AFTER_MARKET_CLOSE"
    UNKNOWN = "UNKNOWN"