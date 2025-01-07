import subprocess

def update_screen_brightness(device, brightness):
    convertValue = brightness * 0.01  # Convert to a decimal percentage
    print(f"Setting brightness on {device} to: {convertValue}")
    subprocess.run(["xrandr", "--output", device, "--brightness", str(convertValue)], capture_output=True, text=True)
