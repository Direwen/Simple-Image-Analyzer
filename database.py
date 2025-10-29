import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL)

SessionLocal = orm.sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative.declarative_base()
