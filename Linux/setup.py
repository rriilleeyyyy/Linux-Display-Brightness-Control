import subprocess
import re

device1 = ""
device2 = ""
device3 = ""

# Run xrandr capture output
xrandrCurrent = subprocess.run(["xrandr", "--current"], capture_output=True, text=True)

# Regular expression to find lines with any device (before "connected")
connected_devices = re.findall(r"^(.*\S+)\s+connected.*", xrandrCurrent.stdout, re.MULTILINE)

# Print all connected device names
print(connected_devices)

print("Current amount of connected devices: " + str(len(connected_devices)))

