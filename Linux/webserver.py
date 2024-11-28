from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from changeBrightness import update_screen_brightness
from setup import connected_devices

app = Flask(__name__)
socketio = SocketIO(app)

current_brightness = {
    "device1": 100,
    "device2": 100
}

@app.route("/")
def index():
    return render_template("index.html", devices=connected_devices)

@app.route("/update_brightness", methods=["POST"])
def update_brightness():
    device = request.form.get("device")
    brightness = int(request.form.get("brightness"))

    # Update the brightness for the selected device
    update_screen_brightness(device, brightness)
    current_brightness[device] = brightness

    # Notify all clients about the brightness change
    socketio.emit("brightness_update", current_brightness)
    return jsonify(success=True)

@app.route("/get_brightness", methods=["GET"])
def get_brightness():
    return jsonify(current_brightness)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
