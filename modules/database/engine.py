# --- Import the required libraries / modules:
from sqlalchemy.orm import declarative_base, sessionmaker

import os
import sqlalchemy as sa


# --- Set the base location for where the database will be stored:
DB_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


# --- Create the database engine:
engine = sa.create_engine(f"sqlite:///{DB_FOLDER_PATH}/database.db")


# --- Setup a session to the database:
Session = sessionmaker(bind = engine)


# --- Create a base class:
Base = declarative_base()

def create_engine() -> None:
    Base.metadata.create_all(engine)