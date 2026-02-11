from pydantic import BaseModel, field_validator
from datetime import time


class AvailabilityCreate(BaseModel):
    user_id: str
    day: int  # 1-7
    start: time
    end: time

    @field_validator("day")
    @classmethod
    def validate_day(cls, v):
        if v < 1 or v > 7:
            raise ValueError("day must be between 1 and 7")
        return v

    @field_validator("end")
    @classmethod
    def validate_time_order(cls, v, info):
        start = info.data.get("start")
        if start and v <= start:
            raise ValueError("end must be after start")
        return v
