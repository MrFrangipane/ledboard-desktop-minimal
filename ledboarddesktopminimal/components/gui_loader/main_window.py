import os.path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QStatusBar, QLabel

from ledboarddesktopminimal.core.configuration import Configuration


class MainWindow(QMainWindow):
    shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("LED Board Configuration")

        logo_filepath = os.path.join(Configuration().resources_path, "frangitron-logo.png")
        logo_pixmap = QPixmap(logo_filepath)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)

        status_bar = QStatusBar()
        status_bar.addPermanentWidget(logo_label)
        status_bar.showMessage("Ready.")
        self.setStatusBar(status_bar)

    def showEvent(self, event):
        self.shown.emit()
        event.accept()
