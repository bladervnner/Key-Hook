#establishes connection with postgres database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db_url = "postgresql+psycopg2://postgres:<password>@localhost:5432/postgres"
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
