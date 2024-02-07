import os.path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel

from ledboarddesktopminimal.core.components import Components


class MainWindow(QMainWindow):
    shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("LED Board Configuration")

        icon_filepath = os.path.join(Components().resources_path, "led.png")
        self.setWindowIcon(QIcon(icon_filepath))

        logo_filepath = os.path.join(Components().resources_path, "frangitron-logo.png")
        logo_pixmap = QPixmap(logo_filepath)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        self.statusBar().addPermanentWidget(logo_label)


    def showEvent(self, event):
        self.shown.emit()
        event.accept()
