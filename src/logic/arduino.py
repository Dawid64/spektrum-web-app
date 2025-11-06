import logging
from typing import Literal
import serial
import streamlit as st
from client.utils import get_logger

ARDUINO_COMMAND = Literal[
    "read",
    "light",
    "camera",
    "bump",
]


class BaseArduinoController:
    port: str
    logger: logging.Logger

    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 10): ...
    def bump(self) -> bool: ...
    def measurement(self) -> tuple[float, float, float]: ...
    def command(self, command: bytes | ARDUINO_COMMAND) -> str: ...


class MockArduinoController(BaseArduinoController):
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 10):
        self.port = port
        self.logger = get_logger("Arduino-Mock")
        _ = (port, baudrate, timeout)
        self.logger.debug("Arduino mock initiated")

    def bump(self) -> bool:
        response = "BUMP"
        self.logger.debug(f"Arduino bumped, {response = }")
        return response == "BUMP"

    def measurement(self) -> tuple[float, float, float]:
        response = "BUMP"
        self.logger.debug(f"Arduino bumped, {response = }")
        return 0, 0, 0

    def command(self, command: bytes | ARDUINO_COMMAND) -> str:
        self.logger.debug(f"Command: {command}")
        return f"result of {command}"


class ArduinoController(BaseArduinoController):
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 10):
        self.port = port
        self.logger = get_logger("Arduino-Controller")
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.command_map: dict[str, bytes] = {
            "read": b"R",
            "light": b"L",
            "camera": b"C",
            "bump": b"B",
        }

    def bump(self) -> bool:
        response = self.command("bump")
        self.logger.debug(f"Arduino bumped, {response = }")
        return response == "BUMP"

    def measurement(self) -> tuple[float, float, float]:
        response = self.command("read")
        temperature = float(response[:5])
        humidity = float(response[5:10])
        light_intensity = float(response[10:15])
        self.logger.debug(f"Arduino measurement, {response = }")
        return temperature, humidity, light_intensity

    def command(self, command: bytes | ARDUINO_COMMAND) -> str:
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
        return ""


def create_arduino_controller(port: str) -> BaseArduinoController:
    if port == "None":
        return MockArduinoController(port)
    try:
        return ArduinoController(port)
    except Exception:
        get_logger("Create arduino controller").error(
            f"Connecting to port: {port} has failed!"
        )
        st.error(f"Setting port: {port} failed")
        return MockArduinoController("None")
