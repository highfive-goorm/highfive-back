# alert/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# alert/app/database.py
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:admin123@alert-db:3306/alert")
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)