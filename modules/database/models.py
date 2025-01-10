# --- Import the required libraries / modules:
from datetime import datetime
from .engine import Base
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Reading(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key = True, unique = True)
    hostname: Mapped[str]
    temperature: Mapped[float]
    pressure: Mapped[float]
    humidity: Mapped[float]
    altitude: Mapped[float]
    created: Mapped[datetime] = mapped_column(DateTime(timezone = True), 
                                                       server_default = func.now())
    
    def __repr__(self) -> str:
        return f"<{self.__tablename__} (id: {self.id}, created: {self.created})>"