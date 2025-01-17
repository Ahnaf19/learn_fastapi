from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# * Database Connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# engine = create_engine('sqlite:///:memory', echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# * Create Models and Tables

# use tablePlus
# create a new connection for sqlite (using sqlite db here)
# give it a name (fastapi) and locate the blog.db file
# click test, if it works, click save
# double click on the fastapi connection to open it