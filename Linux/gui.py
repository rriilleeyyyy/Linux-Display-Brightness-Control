from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QPushButton, QComboBox
from PyQt6.QtCore import Qt
import os
import json
from Linux.setup import connected_devices
from changeBrightness import update_screen_brightness


configFile = "config.conf"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instance variables
        self.currentValue1 = 100
        self.currentValue2 = 100
        self.usrDevice1 = None
        self.usrDevice2 = None

        self.setWindowTitle("Brightness")
        self.setGeometry(100, 100, 500, 500)

        # Create central widget and layout
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

        # 1st Slider
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

    def usr_device_1_changed(self, device):
        self.usrDevice1 = device if device != "Select Device 1" else None
        self.sliderLabel1.setText(f"Brightness (Device 1: {self.usrDevice1})")
        device1 = self.usrDevice1  # Update device1 in setup.py
        print(device1)
        self.save_config()

    def usr_device_2_changed(self, device):
        self.usrDevice2 = device if device != "Select Device 2" else None
        self.sliderLabel2.setText(f"Brightness (Device 2: {self.usrDevice2})")
        device2 = self.usrDevice2  # Update device2 in setup.py
        print(device2)
        self.save_config()

    def update_slider1(self, prevValue1):
        self.sliderLabel1.setText(f"Slider Value: {prevValue1}")
        if self.currentValue1 != prevValue1:
            self.currentValue1 = prevValue1  # Update the instance variable
            print(f"Slider updated to: {prevValue1}")
            if self.usrDevice1: # To make sure its not none!
                update_screen_brightness(self.usrDevice1, self.currentValue1)

    def update_slider2(self, prevValue2):
        self.sliderLabel2.setText(f"Slider Value: {prevValue2}")
        if self.currentValue2 != prevValue2:
            self.currentValue2 = prevValue2  # Update the instance variable
            print(f"Slider updated to: {prevValue2}")
            if self.usrDevice2: # To make sure its not none!
                update_screen_brightness(self.usrDevice2, self.currentValue2)

    def reset_button_click(self):
        self.brightnessSlider1.setValue(100)
        self.brightnessSlider2.setValue(100)
        print("Brightness reset to 100")

    def save_config(self):
        config = {
            "device1": self.usrDevice1,
            "device2": self.usrDevice2  # Fixed typo: device2, not device1
        }
        with open(configFile, "w") as file:
            json.dump(config, file)

    def load_config(self):
        if os.path.exists(configFile):
            with open(configFile, "r") as file:
                config = json.load(file)
                self.usrDevice1 = config.get("device1")
                self.usrDevice2 = config.get("device2")

                if self.usrDevice1 in connected_devices:
                    self.usrDevice1_dropdown.setCurrentText(self.usrDevice1)
                    self.sliderLabel1.setText(f"Brightness (Device 1: {self.usrDevice1})")
                    global device1
                    device1 = self.usrDevice1

                if self.usrDevice2 in connected_devices:
                    self.usrDevice2_dropdown.setCurrentText(self.usrDevice2)
                    self.sliderLabel2.setText(f"Brightness (Device 2: {self.usrDevice2})")
                    global device2
                    device2 = self.usrDevice2

