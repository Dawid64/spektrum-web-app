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
    def __init__(self, port: str, baudrate: int, timeout: float):
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
