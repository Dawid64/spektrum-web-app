from datetime import datetime, timedelta, timezone
import threading
import time
from typing import Any, Literal
from client.utils import get_logger
from logic import ConfigParameters, SESSION
from .utils import MockArduinoController


class ChamberConfig:
    def __init__(
        self,
        name: str,
        watering: dict[Literal["interval", "quantity", "next_run_at"], Any],
        camera_frequency: int,
        light_time: int,
        sensor_delay: int,
    ):
        self.lock = threading.RLock()
        self.name = name
        self.watering = watering
        self.camera_frequency = camera_frequency
        self.light_time = light_time
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
        return cls(
            name=name,
            watering={
                "interval": config.watering_interval,
                "quantity": config.watering_quantity,
                "next_run_at": datetime.now(timezone.utc),
            },
            camera_frequency=config.camera_frequency,
            light_time=config.light_time,
            sensor_delay=config.sensor_delay,
        )

    def save(self):
        logger = get_logger(f"Config-{self.name}")
        config = ConfigParameters(
            chamber_name=self.name,
            date=datetime.now(timezone.utc),
            watering_interval=self.watering["interval"],
            watering_quantity=self.watering["quantity"],
            camera_frequency=self.camera_frequency,
            light_time=self.light_time,
            sensor_delay=self.sensor_delay,
        )
        logger.debug(f"Saving configs\n{repr(config)}")
        with SESSION() as session:
            session.add(config)
            session.commit()


class Chamber:
    def __init__(self, config: ChamberConfig):
        self.config: ChamberConfig = config
        self.logger = get_logger(self.config.name)
        self.arduino = MockArduinoController("COM9", 9600, timeout=3.0)

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
            water_quantity = self.config.watering["quantity"]
            self.config.watering["next_run_at"] += timedelta(
                seconds=self.config.watering["interval"]
            )
            # self.config.save()
        # Function to calculate the water time
        watering_time: float = round(water_quantity / 30.55, 2)
        self.logger.info(f"Watering with quantity: {water_quantity} ml")
        self.arduino.command(f"P {watering_time}".encode("utf-8"))


class ChamberManager:
    def __init__(self, chambers: dict[str, Chamber]):
        self.chambers = chambers

    def scheduler_loop(self):
        while True:
            for chamber in self.chambers.values():
                with chamber.config.lock:
                    due: bool = (
                        datetime.now(timezone.utc)
                        >= chamber.config.watering["next_run_at"]
                    )
                if due:
                    chamber.water_plants()
            time.sleep(0.5)
