from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .confg import settings
'''
import psycopg2
import time
from psycopg2.extras import RealDictCursor #used for column names
'''

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
#used for interaction with postgre without sqlalchemy orm
#Only keeping for documentation.
#if even one of the fields break the rest of code works we want to avoid so using while loop 
while True:
    try:
        conn = psycopg2.connect(host ='localhost', database = 'fastapi', user = 'postgres', password = 'postgres2022', cursor_factory = RealDictCursor)
        #cursor_factory just gets the column name
        cursor = conn.cursor()
        #print("Database Connection Established")
        break
    except Exception as Error:
        print("Connection to Database failed")
        print("Error : ", Error)
        time.sleep(5) #after every 5 seconds
'''