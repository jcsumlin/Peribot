import os

from sqlalchemy import Column, String, Date, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 
class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    date = Column(Date(), nullable=False)
    server_id = Column(String, nullable=False)
    user_name = Column(String(32), nullable=False)
    user_id = Column(String, nullable=False)
    mod_name = Column(String(32), nullable=False)
    mod_id = Column(String, nullable=False)
    reason = Column(String, nullable=False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///warnings.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(bind=engine)
# moves database to correct folder for bot to function
if __name__ == '__main__':
    os.rename('./database.db', './cogs/database.db')
