from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://root:password@postgres:5432/parkinson_db"
SQLALCHEMY_DATABASE_URL = "postgresql://root:password@localhost:5432/parkinson_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
def get_db():
  db = SessionLocal()
  try: 
    yield db
  except Exception as e:
    print(e)
  finally:
    db.close()