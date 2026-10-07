from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="postgresql://postgres:root@localhost:5432/fastapi"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)