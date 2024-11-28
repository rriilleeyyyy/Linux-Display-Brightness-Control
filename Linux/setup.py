# setup.py

import subprocess
import re

device1 = ""
device2 = ""

xrandrCurrent = subprocess.run(["xrandr", "--current"], capture_output=True, text=True)

connected_devices = re.findall(r"^(.*\S+)\s+connected.*", xrandrCurrent.stdout, re.MULTILINE)

print(connected_devices)

print("Current amount of connected devices: " + str(len(connected_devices)))

