import subprocess
from setup import device1, device2

def update_screen1_brightness(brightness):
    convertValue1 = brightness * 0.01  # Convert to a decimal percentage
    print(f"Setting brightness on dev1 to: {convertValue1}")
    subprocess.run(["xrandr", "--output", device1, "--brightness", str(convertValue1)], capture_output=True, text=True)



def update_screen2_brightness(brightness):
    convertValue2 = brightness * 0.01  # Convert to a decimal percentage
    print(f"Setting brightness on dev2 to: {convertValue2}")
    subprocess.run(["xrandr", "--output", device2, "--brightness", str(convertValue2)], capture_output=True, text=True)
