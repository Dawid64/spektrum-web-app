from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    sessionmaker,
    declarative_base,
    DeclarativeMeta,
)

Base: DeclarativeMeta = declarative_base()

DB = sa.create_engine("sqlite:///test.db")
SESSION = sessionmaker(DB)


class ConfigParameters(Base):
    __tablename__ = "config_parameters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    chamber_name: Mapped[str] = mapped_column(index=True)

    date: Mapped[datetime]
    watering_interval: Mapped[int]
    watering_quantity: Mapped[int]
    camera_frequency: Mapped[int]
    light_time: Mapped[int]
    sensor_delay: Mapped[int]

    def __repr__(self) -> str:
        return f"<{self.date} | {self.chamber_name} | water: (interval={self.watering_interval}, quantity={self.watering_quantity}), camera frequency={self.camera_frequency}, light time={self.light_time}, sensor delay={self.sensor_delay}>"


class Measurements(Base):
    __tablename__ = "measurements"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    chamber_name: Mapped[str] = mapped_column(index=True)

    date: Mapped[datetime]
    temperature: Mapped[float]
    humidity: Mapped[float]
    light_intensity: Mapped[float]

    def __repr__(self) -> str:
        return f"<{self.date} | {self.chamber_name} | temperature: {self.temperature}, humidity={self.humidity}, light intensity={self.light_intensity}>"


# class User(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
#     name: Mapped[str] = mapped_column(index=True)

#     password: Mapped[str]
#     role: Mapped[Literal["User", "Maintainer", "Admin"]]

#     def __repr__(self) -> str:
#         return f"<{self.name}: {self.role}>"


Base.metadata.create_all(DB)
