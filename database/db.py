from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from security.config import settings

engine = create_engine(settings.DATABASE_URL)
LocalSession = sessionmaker(autocommit = False, autoflush = False, bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()