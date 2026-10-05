from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data.db")
LocalSession = sessionmaker(autocommit = False, autoflush = False, bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
