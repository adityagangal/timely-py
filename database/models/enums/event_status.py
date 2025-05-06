from enum import Enum

class EventStatusEnum(str, Enum):
    cancelled = "cancelled"
    rescheduled = "rescheduled"
    active = "active"  # Optional: to indicate a normal/unchanged state