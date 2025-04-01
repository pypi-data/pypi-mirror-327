# -*- coding: utf-8 -*-

import argparse
import time
import sys
from typing import final

import serial  # type: ignore
import pyftdi.serialext  # type: ignore
from pyftdi.ftdi import Ftdi  # type: ignore
from pyftdi.usbtools import UsbDeviceDescriptor, UsbTools, UsbToolsError  # type: ignore

from jn51xx_flasher.jn51xx_flasher import Flasher  # type: ignore

__all__ = ["Tweliter"]


@final
class Tweliter:
    __ftdi: Ftdi
    __url: str
    __device: UsbDeviceDescriptor
    __debugging: bool

    def __init__(
        self,
        url: str | None = None,
        debugging: bool = False,
    ):
        UsbTools.flush_cache()  # for reconnecting

        self.__ftdi = Ftdi()
        self.__debugging = debugging

        # Set __url and __device
        if url is not None:
            # URL was specified
            self.__url = url
            try:
                self.__device = self.__ftdi.get_identifiers(url)[0]
            except UsbToolsError:
                self.close()
                raise IOError(f"There's no device matches URL {url}")
        else:
            # Set dynamically
            if not sys.stdin.isatty():
                self.close()
                raise EnvironmentError("There's no console. Specify URL.")

            # Get available devices
            devices = self.__ftdi.list_devices()

            if len(devices) <= 0:
                # No devices
                self.__ftdi.close()
                raise IOError("There's no devices.")
            elif len(devices) == 1:
                # One device
                self.__url = "ftdi:///1"
                self.__device = devices[0][0]
            else:
                # Two or more devices -> Ask for the user
                print("Detected multiple devices: ")
                for index, device in enumerate(devices):
                    devinfo = device[0]
                    sn = getattr(devinfo, "sn")
                    description = getattr(devinfo, "description")
                    print(f"[{index}] {description} ({sn})")
                while True:
                    try:
                        selected_index = int(input("Select device number to use: "))
                        if selected_index < 0 or selected_index >= len(devices):
                            raise ValueError("Invalid number")
                        break
                    except ValueError as e:
                        print(e)
                self.__device = devices[selected_index][0]
                self.__url = f'ftdi://::{getattr(self.__device, "sn")}/1'

        if self.__debugging:
            print(f"[Debug] Set URL {self.__url}")
            print(f"[Debug] Set Device {self.__device}")

        serial_no = getattr(self.__device, "sn")
        description = getattr(self.__device, "description")
        print(f"Using {description} ({serial_no})")

        self.__ftdi.open_from_url(self.__url)

        if not self.__ftdi.has_cbus:
            # CBUS gpio are not initialized; Invalid device
            self.close()
            raise IOError("Device is invalid. Cannot use CBUS pins.")

    def __del__(self) -> None:
        self.close()

    def reopen(self) -> None:
        self.close()
        self.__ftdi.open_from_url(self.__url)
        if not self.__ftdi.has_cbus:
            # CBUS gpio are not initialized; Invalid device
            self.close()
            raise IOError("Device is invalid. Cannot use CBUS pins.")

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and close the connection."""
        self.close()

    def close(self) -> None:
        self.__ftdi.close()

    @property
    def url(self) -> str:
        return self.__url

    @property
    def ftdi(self) -> str:
        return self.__ftdi

    def enter_program_mode(self):
        self.__ftdi.set_cbus_direction(0b00001100, 0b00001100)
        self.__ftdi.set_cbus_gpio(0b00000100)  # Set PRG Low, RST High
        time.sleep(0.1)
        self.__ftdi.set_cbus_gpio(0b00000000)  # Set PRG Low, RST Low
        time.sleep(0.5)
        self.__ftdi.set_cbus_gpio(0b00000100)  # Set PRG Low, RST High

    def reset_device(self, set_low=False):
        if not set_low:
            self.__ftdi.set_cbus_direction(0b00000100, 0b00000100)
            self.__ftdi.set_cbus_gpio(0b00000000)  # Set RST Low
            time.sleep(0.5)
            self.__ftdi.set_cbus_gpio(0b00000100)  # Set RST High
        else:
            self.__ftdi.set_cbus_direction(0b00000110, 0b00000110)
            self.__ftdi.set_cbus_gpio(0b00000100)  # Set RST High, SET Low
            time.sleep(0.1)
            self.__ftdi.set_cbus_gpio(0b00000000)  # Set RST Low, SET Low
            time.sleep(0.5)
            self.__ftdi.set_cbus_gpio(0b00000100)  # Set RST High, SET Low

    def enter_interactive_mode(self):
        self.reset_device(True)

    def get_serial_instance(self, **options):
        default_options = {
            "baudrate": 38400,
            "bytesize": serial.EIGHTBITS,
            "parity": serial.PARITY_NONE,
            "stopbits": serial.STOPBITS_ONE,
            "timeout": 2,
        }
        final_options = default_options | options
        return pyftdi.serialext.serial_for_url(self.__url, **final_options)

    @staticmethod
    def write_firmware(ser: serial.Serial, file: str):
        ser.baudrate = 38400
        ser.flush()
        ser.flushInput()
        time.sleep(0.5)
        flasher = Flasher(ser, "none")
        flasher.run("write", file)
        ser.baudrate = 115200


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Write TWELITE BLUE/RED firmware")
    parser.add_argument(
        "--url", type=str, default=None, help="Device URL starting with ftdi://"
    )
    parser.add_argument(
        "--startmsg",
        type=str,
        default="!INF MONO WIRELESS",
        help="Prefix for startup message to check",
    )
    parser.add_argument("file", help="Firmware file to write")
    args = parser.parse_args()

    try:
        with Tweliter(args.url) as liter:
            # Get serial interface
            ser = liter.get_serial_instance()

            # Write
            liter.enter_program_mode()
            liter.write_firmware(ser, args.file)

            # Reset
            liter.reset_device()

            # Show startup message
            ser.read_until(args.startmsg.encode("utf-8"))
            line = ser.readline()
            print(line.decode("utf-8").strip())
    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()
