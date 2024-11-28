# gui.py
import asyncio
import threading
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QPushButton, QComboBox
from PyQt6.QtCore import Qt, QTimer
import os
import json
from setup import connected_devices
from changeBrightness import update_screen_brightness
import requests
import time
import websockets

configFile = "config.conf"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.websocket_thread = threading.Thread(target=self.start_websocket_listener, daemon=True)
        self.websocket_thread.start()

        # Instance variables
        self.currentValue1 = 100
        self.currentValue2 = 100
        self.usrDevice1 = None
        self.usrDevice2 = None

        self.setWindowTitle("Brightness")
        self.setGeometry(100, 100, 500, 500)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Device dropdowns
        dropdown_layout = QHBoxLayout()
        self.usrDevice1_dropdown = QComboBox()

        if len(connected_devices) == 1:
            # Automatically set Device 1 if only one screen is connected
            self.usrDevice1 = connected_devices[0]
            self.usrDevice1_dropdown.addItem(self.usrDevice1)
            self.usrDevice1_dropdown.setEnabled(False)  # Disable dropdown since there's only one choice
        else:
            self.usrDevice1_dropdown.addItem("Select Device 1")
            self.usrDevice1_dropdown.addItems(connected_devices)

        self.usrDevice1_dropdown.currentTextChanged.connect(self.usr_device_1_changed)

        dropdown_layout.addWidget(QLabel("Device 1:"))
        dropdown_layout.addWidget(self.usrDevice1_dropdown)

        if len(connected_devices) > 1:  # Add second dropdown if multiple devices exist
            self.usrDevice2_dropdown = QComboBox()
            self.usrDevice2_dropdown.addItem("Select Device 2")
            self.usrDevice2_dropdown.addItems(connected_devices)
            self.usrDevice2_dropdown.currentTextChanged.connect(self.usr_device_2_changed)

            dropdown_layout.addWidget(QLabel("Device 2:"))
            dropdown_layout.addWidget(self.usrDevice2_dropdown)

        main_layout.addLayout(dropdown_layout)

        # Layout for sliders
        sliders_layout = QHBoxLayout()

        slider1_layout = QVBoxLayout()
        self.sliderLabel1 = QLabel(f"Brightness (Device 1: {self.usrDevice1 or 'None'})")
        self.sliderLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider1_layout.addWidget(self.sliderLabel1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.brightnessSlider1 = QSlider(Qt.Orientation.Vertical)
        self.brightnessSlider1.setMinimum(10)
        self.brightnessSlider1.setMaximum(100)
        self.brightnessSlider1.setValue(100)
        self.brightnessSlider1.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightnessSlider1.setTickInterval(10)
        self.brightnessSlider1.valueChanged.connect(self.update_slider1)
        slider1_layout.addWidget(self.brightnessSlider1, alignment=Qt.AlignmentFlag.AlignHCenter)

        sliders_layout.addLayout(slider1_layout)

        if len(connected_devices) > 1:  # Add second slider if multiple devices exist
            slider2_layout = QVBoxLayout()
            self.sliderLabel2 = QLabel(f"Brightness (Device 2: None)")
            self.sliderLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slider2_layout.addWidget(self.sliderLabel2, alignment=Qt.AlignmentFlag.AlignHCenter)

            self.brightnessSlider2 = QSlider(Qt.Orientation.Vertical)
            self.brightnessSlider2.setMinimum(10)
            self.brightnessSlider2.setMaximum(100)
            self.brightnessSlider2.setValue(100)
            self.brightnessSlider2.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.brightnessSlider2.setTickInterval(10)
            self.brightnessSlider2.valueChanged.connect(self.update_slider2)
            slider2_layout.addWidget(self.brightnessSlider2, alignment=Qt.AlignmentFlag.AlignHCenter)

            sliders_layout.addLayout(slider2_layout)

        main_layout.addLayout(sliders_layout)

        # Reset button
        resetButton = QPushButton("Reset Screens")
        resetButton.clicked.connect(self.reset_button_click)
        main_layout.addWidget(resetButton)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_config()

        # Timer to fetch brightness from web server
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_brightness_from_web)
        self.timer.start(1000)  # Update every second

    def usr_device_1_changed(self, new_device):
        self.usrDevice1 = new_device
        self.sliderLabel1.setText(f"Brightness (Device 1: {self.usrDevice1})")
        self.update_device_brightness(self.usrDevice1, self.currentValue1)

    def usr_device_2_changed(self, new_device):
        self.usrDevice2 = new_device
        self.sliderLabel2.setText(f"Brightness (Device 2: {self.usrDevice2})")
        self.update_device_brightness(self.usrDevice2, self.currentValue2)

    def update_slider1(self):
        self.currentValue1 = self.brightnessSlider1.value()
        self.update_device_brightness(self.usrDevice1, self.currentValue1)

        # Sync brightness to the server
        self.sync_brightness_to_server("device1", self.currentValue1)

    def update_slider2(self):
        self.currentValue2 = self.brightnessSlider2.value()
        self.update_device_brightness(self.usrDevice2, self.currentValue2)

        # Sync brightness to the server
        self.sync_brightness_to_server("device2", self.currentValue2)

    def update_device_brightness(self, device, value):
        if device:
            update_screen_brightness(device, value)

    def reset_button_click(self):
        self.brightnessSlider1.setValue(100)
        if self.usrDevice1:
            self.update_device_brightness(self.usrDevice1, 100)

        if self.usrDevice2:
            self.brightnessSlider2.setValue(100)
            self.update_device_brightness(self.usrDevice2, 100)

    def fetch_brightness_from_web(self):
        retries = 5
        for _ in range(retries):
            try:
                response = requests.get("http://localhost:5000/get_brightness")
                if response.status_code == 200:
                    data = response.json()
                    self.brightnessSlider1.setValue(data["device1"])
                    self.brightnessSlider2.setValue(data["device2"])
                    return
            except requests.exceptions.RequestException as e:
                print(f"Error fetching brightness from web: {e}")
            time.sleep(1)  # Retry after a brief delay

    def load_config(self):
        if os.path.exists(configFile):
            with open(configFile, "r") as f:
                config = json.load(f)
                if 'usrDevice1' in config:
                    self.usrDevice1 = config['usrDevice1']
                    self.usrDevice1_dropdown.setCurrentText(self.usrDevice1)
                if 'usrDevice2' in config:
                    self.usrDevice2 = config['usrDevice2']
                    self.usrDevice2_dropdown.setCurrentText(self.usrDevice2)

    async def websocket_listener(self):
        uri = "ws://localhost:5000/socket.io/"
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    # Update sliders based on data from the server
                    self.brightnessSlider1.setValue(data.get("device1", 100))
                    if self.usrDevice2:
                        self.brightnessSlider2.setValue(data.get("device2", 100))
                except Exception as e:
                    print(f"WebSocket error: {e}")
                    break

    def start_websocket_listener(self):
        asyncio.run(self.websocket_listener())

    def sync_brightness_to_server(self, device, value):
        try:
            requests.post("http://localhost:5000/update_brightness", data={"device": device, "brightness": value})
        except requests.exceptions.RequestException as e:
            print(f"Error syncing with server: {e}")
