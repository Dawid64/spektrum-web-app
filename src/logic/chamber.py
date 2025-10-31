from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import threading
import time
from typing import Any
from client.utils import get_logger
from logic import ChamberParameters, SESSION
from logic.database import Measurements
from .arduino import MockArduinoController


@dataclass
class Field:
    name: str
    fullname: str
    value: Any


class ChamberConfig:
    def __init__(
        self,
        name: str,
        water_interval: int = 10,
        water_quantity: int = 10,
        camera_frequency: int = 10,
        light_time: int = 10,
        sensor_delay: int = 10,
    ):
        self.lock = threading.RLock()
        self.name = name
        self.water_interval = water_interval
        self.water_quantity = water_quantity
        self.camera_frequency = camera_frequency
        self.light_time = light_time
        self.sensor_delay = sensor_delay

    def reader(self) -> list[Field]:
        return [
            Field("water_interval", "Water interval", self.water_interval),
            Field("water_quantity", "Water quantity", self.water_quantity),
            Field("camera_frequency", "Camera frequency", self.camera_frequency),
            Field("light_time", "Light time", self.light_time),
            Field("sensor_delay", "Sensor delay", self.sensor_delay),
        ]

    def set(
        self,
        water_interval: int | None = None,
        water_quantity: int | None = None,
        camera_frequency: int | None = None,
        light_time: int | None = None,
        sensor_delay: int | None = None,
    ) -> None:
        if water_interval is not None:
            self.water_interval = water_interval
        if water_quantity is not None:
            self.water_quantity = water_quantity
        if camera_frequency is not None:
            self.camera_frequency = camera_frequency
        if light_time is not None:
            self.light_time = light_time
        if sensor_delay is not None:
            self.sensor_delay = sensor_delay

    @classmethod
    def load(cls, name: str) -> "ChamberConfig":
        logger = get_logger(f"Config-{name}")
        with SESSION() as session:
            config: ChamberParameters | None = (
                session.query(ChamberParameters)
                .where(ChamberParameters.chamber_name == name)
                .order_by(ChamberParameters.date.desc())
                .first()
            )
        logger.debug(repr(config))
        if config is None:
            chamber_config = ChamberConfig(name)
            config = chamber_config.to_config_params()
            logger.debug("Config not found, submitting a new one")
            with SESSION() as session:
                session.add(config)
                session.commit()
            return cls.load(name)
        return cls.from_config_params(config)

    def save(self):
        logger = get_logger(f"Config-{self.name}")
        config = self.to_config_params()
        logger.debug(f"Saving configs\n{repr(config)}")
        with SESSION() as session:
            session.add(config)
            session.commit()

    @classmethod
    def from_config_params(cls, parameters: ChamberParameters) -> "ChamberConfig":
        return cls(
            name=parameters.chamber_name,
            water_interval=parameters.watering_interval,
            water_quantity=parameters.watering_interval,
            camera_frequency=parameters.camera_frequency,
            light_time=parameters.light_time,
            sensor_delay=parameters.sensor_delay,
        )

    def to_config_params(self) -> ChamberParameters:
        return ChamberParameters(
            chamber_name=self.name,
            date=datetime.now(timezone.utc),
            watering_interval=self.water_interval,
            watering_quantity=self.water_quantity,
            camera_frequency=self.camera_frequency,
            light_time=self.light_time,
            sensor_delay=self.sensor_delay,
        )

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()


class Chamber:
    def __init__(self, config: ChamberConfig):
        self.config: ChamberConfig = config
        self.logger = get_logger(self.config.name)
        self.arduino = MockArduinoController("COM9")

        self.watering_next_run = datetime.now(timezone.utc)
        self.light_next_run = datetime.now(timezone.utc)
        self.get_params_next_run = datetime.now(timezone.utc)

    def read_from_sensors(
        self, add_to_database: bool = False
    ) -> tuple[float, float, float]:
        temperature, humidity, light_intensity = self.arduino.measurement()
        if add_to_database:
            measurement = Measurements(
                datetime.now(timezone.utc),
                temperature,
                humidity,
                light_intensity,
            )
        return temperature, humidity, light_intensity

    def take_photo(self):
        self.logger.info("Taking photo")
        self.arduino.command("camera")

    def light_switch(self):
        self.logger.info(f"Changing light to {'on' if True else 'off'}")
        self.arduino.command("light")

    def water_plants(self):
        with self.config:
            water_quantity = self.config.water_quantity
            self.watering_next_run += timedelta(seconds=self.config.water_interval)
        watering_time: float = round(water_quantity / 30.55, 2)
        self.logger.info(f"Watering with quantity: {water_quantity} ml")
        self.arduino.command(f"P {watering_time}".encode("utf-8"))


class ChamberManager:
    def __init__(self, configs: dict[str, ChamberConfig]):
        self.chambers = {name: Chamber(config) for name, config in configs.items()}

    def scheduler_loop(self):
        while True:
            for chamber in self.chambers.values():
                current_time = datetime.now(timezone.utc)
                if current_time >= chamber.watering_next_run:
                    chamber.water_plants()
                if current_time >= chamber.light_next_run:
                    chamber.light_switch()
            time.sleep(0.5)
