# --- Import the required libraries / modules:
from modules.database.engine import Session
from modules.database.models import Reading

import os


def add_reading(readings: dir):
    entry = Reading(hostname = os.uname()[1],
                    temperature = readings["temperature"],
                    humidity = readings["humidity"],
                    pressure = readings["pressure"],
                    altitude = readings["altitude"])
    
    # --- Write a reading to the DB:
    with Session() as session:
        session.add(entry)
        session.commit()
        

# def get_all_readings() -> None:
#     with Session() as session:
#         print(session.query(Reading).all())
        

# def get_last_ten_readings() -> None:
#     with Session() as session:
#         print(session.query(Reading).order_by(Reading.id.desc()).limit(10))