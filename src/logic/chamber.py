from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import threading
import time
from typing import Any
from client.utils import get_logger
from logic import ConfigParameters, SESSION
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
        water_interval: int,
        water_quantity: int,
        camera_frequency: int,
        light_time: int,
        sensor_delay: int,
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
            Field("camera_frequency", "camera_frequency", self.camera_frequency),
            Field("light_time", "light_time", self.light_time),
            Field("sensor_delay", "sensor_delay", self.sensor_delay),
        ]

    def setter(
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
            config: ConfigParameters | None = (
                session.query(ConfigParameters)
                .where(ConfigParameters.chamber_name == name)
                .order_by(ConfigParameters.date.desc())
                .first()
            )
        logger.debug(repr(config))
        if config is None:
            config = ConfigParameters(
                chamber_name=name,
                date=datetime.now(timezone.utc),
                watering_interval=100,
                watering_quantity=100,
                camera_frequency=10,
                light_time=10,
                sensor_delay=10,
            )
            logger.debug("Config not found, submitting a new one")
            with SESSION() as session:
                session.add(config)
                session.commit()
            return cls.load(name)
        return cls.from_config_params(config)

    def save(self):
        logger = get_logger(f"Config-{self.name}")
        config = ConfigParameters(
            chamber_name=self.name,
            date=datetime.now(timezone.utc),
            watering_interval=self.water_interval,
            watering_quantity=self.water_quantity,
            camera_frequency=self.camera_frequency,
            light_time=self.light_time,
            sensor_delay=self.sensor_delay,
        )
        logger.debug(f"Saving configs\n{repr(config)}")
        with SESSION() as session:
            session.add(config)
            session.commit()

    @classmethod
    def from_config_params(cls, parameters: ConfigParameters) -> "ChamberConfig":
        return cls(
            name=parameters.chamber_name,
            water_interval=parameters.watering_interval,
            water_quantity=parameters.watering_interval,
            camera_frequency=parameters.camera_frequency,
            light_time=parameters.light_time,
            sensor_delay=parameters.sensor_delay,
        )


class Chamber:
    def __init__(self, config: ChamberConfig):
        self.config: ChamberConfig = config
        self.logger = get_logger(self.config.name)
        self.arduino = MockArduinoController("COM9", 9600, timeout=3.0)
        self.watering_next_run = datetime.now(timezone.utc)

    def get_data(self):
        pass

    def read_from_sensors(self, table) -> str:
        response = self.arduino.command("read")
        if not isinstance(response, str):
            raise ValueError
        return response

    def take_photo(self):
        self.logger.info("Taking photo")
        self.arduino.command("camera")

    def light_switch(self):
        self.logger.info(f"Changing light to {'on' if True else 'off'}")
        self.arduino.command("light")

    def water_plants(self):
        with self.config.lock:
            water_quantity = self.config.water_quantity
            self.watering_next_run += timedelta(seconds=self.config.water_interval)
        watering_time: float = round(water_quantity / 30.55, 2)
        self.logger.info(f"Watering with quantity: {water_quantity} ml")
        self.arduino.command(f"P {watering_time}".encode("utf-8"))


class ChamberManager:
    def __init__(self, chambers: dict[str, Chamber]):
        self.chambers = chambers

    def scheduler_loop(self):
        while True:
            for chamber in self.chambers.values():
                if datetime.now(timezone.utc) >= chamber.watering_next_run:
                    chamber.water_plants()
            time.sleep(0.5)
