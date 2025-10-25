import logging
from typing import Literal
import serial


ARDUINO_COMMAND = Literal["read", "light", "camera", "bump"]


class MockArduinoController:
    def __init__(self, port: str, baudrate: int, timeout: float):
        _ = (port, baudrate, timeout)
        print("Initiated")

    def command(self, command: bytes | ARDUINO_COMMAND) -> None | str:
        print(f"Running {command}")
        return f"result of {command}"


class ArduinoController:
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 10):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.command_map: dict[str, bytes] = {
            "read": b"R",
            "light": b"L",
            "camera": b"C",
            "bump": b"B",
        }

    def command(self, command: bytes | ARDUINO_COMMAND) -> None | str:
        """Simple command for arduino control

        Arduino interface:
            R - read from sensors
            L - turn the light switch
            C - camera
            B - bump
            P <time> - water for <time> seconds

        Args:
            command (bytes | ARDUINO_COMMAND): command to be passed to arduino
        """
        if isinstance(command, str):
            command = self.command_map[command]
        self.ser.reset_output_buffer()
        self.ser.write(command)
        self.ser.flush()
        if command in [b"R", b"B"]:
            self.ser.reset_input_buffer()
            response: bytes = self.ser.readline()
            return response.decode().strip()


class CustomFormatter(logging.Formatter):
    cyan = "\x1b[96m"
    grey = "\x1b[30;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: cyan + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    logger.propagate = False
    return logger
