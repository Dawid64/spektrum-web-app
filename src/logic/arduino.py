from typing import Literal
import serial
from client.utils import get_logger

ARDUINO_COMMAND = Literal["read", "light", "camera", "bump"]


class MockArduinoController:
    def __init__(self, port: str, baudrate: int, timeout: float):
        self.logger = get_logger("Arduino-Mock")
        _ = (port, baudrate, timeout)
        self.logger.debug("Arduino mock initiated")

    def command(self, command: bytes | ARDUINO_COMMAND) -> None | str:
        self.logger.debug(f"Command: {command}")
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
