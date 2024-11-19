from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QPushButton
from PyQt6.QtCore import Qt

from Linux.setup import device1, device2
from changeBrightness import update_screen1_brightness, update_screen2_brightness


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instance variable for brightness
        self.currentValue1 = 100
        self.currentValue2 = 100

        self.setWindowTitle("Brightness")
        self.setGeometry(100, 100, 500, 500)

        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Layout for Slider + Labels
        sliders_layout = QHBoxLayout()
        sliders_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around the sliders
        sliders_layout.setSpacing(20)  # Space between sliders

        # 1st Slider
        slider1_layout = QVBoxLayout()
        slider1_label = QLabel("Brightness (Device 1: " + device1 + ")")
        slider1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider1_layout.addWidget(slider1_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.brightnessSlider1 = QSlider(Qt.Orientation.Vertical)
        self.brightnessSlider1.setMinimum(10)
        self.brightnessSlider1.setMaximum(100)
        self.brightnessSlider1.setValue(100)
        self.brightnessSlider1.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightnessSlider1.setTickInterval(10)
        slider1_layout.addWidget(self.brightnessSlider1, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Create a vertical layout for the second slider
        slider2_layout = QVBoxLayout()
        slider2_label = QLabel("Brightness (Device 2: " + device2 + ")")
        slider2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider2_layout.addWidget(slider2_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.brightnessSlider2 = QSlider(Qt.Orientation.Vertical)
        self.brightnessSlider2.setMinimum(10)
        self.brightnessSlider2.setMaximum(100)
        self.brightnessSlider2.setValue(100)
        self.brightnessSlider2.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.brightnessSlider2.setTickInterval(10)
        slider2_layout.addWidget(self.brightnessSlider2, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Add the slider layout to the horizontal sliders layout
        sliders_layout.addLayout(slider1_layout)
        sliders_layout.addLayout(slider2_layout)


        # Add the sliders layout to the main layout
        main_layout.addLayout(sliders_layout)

        # Label to show slider value
        self.labelValue1 = QLabel("Slider Value: 100")
        self.labelValue1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.labelValue1)

        self.labelValue2 = QLabel("Slider Value: 100")
        self.labelValue2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.labelValue2)

        # Reset button
        resetButton = QPushButton("Reset Screens")
        resetButton.clicked.connect(self.reset_button_click)
        main_layout.addWidget(resetButton)

        # Connect slider's valueChanged signal
        self.brightnessSlider1.valueChanged.connect(self.update_slider1)
        self.brightnessSlider2.valueChanged.connect(self.update_slider2)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_slider1(self, prevValue1):
        self.labelValue1.setText(f"Slider Value: {prevValue1}")
        if self.currentValue1 != prevValue1:
            self.currentValue1 = prevValue1  # Update the instance variable
            print(f"Slider updated to: {prevValue1}")
            update_screen1_brightness(self.currentValue1)

    def update_slider2(self, prevValue2):
        self.labelValue2.setText(f"Slider Value: {prevValue2}")
        if self.currentValue2 != prevValue2:
            self.currentValue2 = prevValue2  # Update the instance variable
            print(f"Slider updated to: {prevValue2}")
            update_screen2_brightness(self.currentValue2)

    #def swap_display_order_click(self):


    def reset_button_click(self):
        self.brightnessSlider1.setValue(100)  # This will trigger update_slider1
        self.brightnessSlider2.setValue(100)  # This will trigger update_slider1
        print("Brightness reset to 100")
