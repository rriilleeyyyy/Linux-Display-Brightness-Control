from gui import MainWindow
from PyQt6.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication([])  # Create the QApplication instance first
    window = MainWindow()    # Then create the window
    window.show()
    app.exec()