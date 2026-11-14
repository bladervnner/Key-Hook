import os
from dotenv import load_dotenv
# Establishes connection with postgres database
# No longer hardcoded

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()
db_url = os.environ["DATABASE_URL"]

engine = create_engine(
    db_url,
    pool_size=5,
    pool_recycle=3600,
    echo=True
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)