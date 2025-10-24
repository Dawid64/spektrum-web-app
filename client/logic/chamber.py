from datetime import datetime, timedelta, timezone
import threading
import time
from typing import Any
from .utils import MockArduinoController, get_logger


class Database:
    def __init__(self):
        pass

    def add_photo(self, photo):
        pass


class ChamberConfig:
    def __init__(self, name: str):
        self.lock = threading.RLock()
        self.name = name
        self.watering: dict[str, Any] = {
            "next_run_at": datetime.now(timezone.utc),
            "interval": 180,
            "quantity": 10,
        }
        self.camera_frequency = 8
        self.light_time = 6
        self.sensor_delay = 15

    def load(self):
        # TODO: Loading
        print("Loading")

    def save(self):
        # TODO: Saving
        print("Saving")


class Chamber:
    def __init__(self, config: ChamberConfig):
        self.config: ChamberConfig = config
        self.logger = get_logger(self.config.name)

        # self.logger: logging.Logger = LoggerAdapter(self.config.name, logger)
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
            self.config.save()
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
