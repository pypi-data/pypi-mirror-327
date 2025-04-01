<a href="https://mono-wireless.com/jp/index.html">
    <img src="https://mono-wireless.com/common/images/logo/logo.svg" alt="mono wireless logo" title="MONO WIRELESS" align="right" height="35" />
</a>

# tweliter

A Python module for writing TWELITE BLUE/RED firmware. (beta)

[![MW-OSSLA](https://img.shields.io/badge/License-MW--OSSLA-e4007f)](LICENSE)

## Overview

Write firmware over TWELITE R series via USB.

This module is executable in standalone and importable for your scripts.

## Installation

The module is available in [PyPI](https://pypi.org/project/tweliter/).

Use `pip`

```
pip install tweliter
```

or `poetry`

```
poetry add tweliter
```

### Linux

Sometimes you need to set permission with `udev`.

1. Create `/etc/udev/rules.d/99-ftdi.rules`

```sh
# TWELITE R / MONOSTICK (FT232R / 0403:6001)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"

# TWELITE R2 / R3 (FT230X / 0403:6015)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", MODE="0666"
```

2. Reload udev rules

```sh
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

### Command line

```shell
$ tweliter dir/SomeApp_BLUE.bin
```

### In script

```python
from pathlib import Path
from tweliter import Tweliter

file = Path('dir/SomeApp_BLUE.bin')

try:
    with Tweliter(url="ftdi://:ft-x:/1") as liter:
        # Get serial interface for communication
        ser = liter.get_serial_instance()

        # Reset and enter program mode
        liter.enter_program_mode()

        # Write firmware
        liter.write_firmware(ser, file)

        # Reset device to check startup message
        liter.reset_device()

        # Show startup message
        ser.read_until(b"!INF MONO WIRELESS") # wait for prefix
        line = ser.readline()
        print(line.decode("utf-8").strip())
except IOError as e:
    print(e)
```

## LICENSE

MW-OSSLA
