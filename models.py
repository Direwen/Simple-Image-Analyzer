import datetime
import sqlalchemy as sql
from database import Base


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    filename = sql.Column(sql.String, index=True)
    average_brightness = sql.Column(sql.Float)
    brightest_value = sql.Column(sql.Float)
    darkest_value = sql.Column(sql.Float)
    created_at = sql.Column(sql.DateTime, default=datetime.datetime.utcnow)
