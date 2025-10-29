import datetime
from pydantic import BaseModel


# Used when creating a new record (base schema)
class AnalysisRecordBase(BaseModel):
    filename: str
    average_brightness: float
    brightest_value: float
    darkest_value: float


# Used when reading data from the DB
class AnalysisRecord(AnalysisRecordBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
