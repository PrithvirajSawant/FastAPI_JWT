from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Define the same engine for both
DATABASE_URL = "mysql+pymysql://root:Admin%40123@localhost/fast_api_check"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
