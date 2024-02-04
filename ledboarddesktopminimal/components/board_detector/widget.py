from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from pyside6helpers import icons
from pyside6helpers.error_reporting import error_reported
from pyside6helpers.hourglass import Hourglass

from ledboarddesktopminimal.core.configuration import Configuration


class BoardDetectionWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.icon = QLabel()
        self.message = QLabel()
        self.button = QPushButton("Detect boards...")
        self.button.setIcon(icons.refresh())
        self.button.clicked.connect(self.detect)

        layout = QHBoxLayout(self)
        layout.addWidget(self.icon)
        layout.addWidget(self.message)
        layout.addWidget(self.button)
        layout.setStretch(1, 100)

        Configuration().board_detector.detectionStarted.connect(self._begin_detection)
        Configuration().board_detector.detectionFinished.connect(self._reset_message)

        self._reset_message()

    @error_reported("Board detection")
    def detect(self):
        with Hourglass():
            Configuration().board_detector.detect()

    def _begin_detection(self):
        self.icon.setPixmap(icons.refresh().pixmap(16, 16))
        self.message.setText("Detecting boards...")

    def _reset_message(self):
        self.icon.setPixmap(icons.check().pixmap(16, 16))
        self.message.setText("Ready.")
