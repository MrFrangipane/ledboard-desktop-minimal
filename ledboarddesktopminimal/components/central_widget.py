from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QGridLayout, QScrollArea, QPushButton

from pyside6helpers import layout
from pyside6helpers import icons
from pyside6helpers.hourglass import Hourglass
from pyside6helpers.error_reporting import error_reported

from ledboarddesktopminimal.core.configuration import Configuration
from ledboarddesktopminimal.components.board_widget import BoardWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.board_widgets = dict()
        self.board_widgets_layout = QVBoxLayout()

        self.button_detect_boards = QPushButton("Detect Boards...")
        self.button_detect_boards.setIcon(icons.refresh())
        self.button_detect_boards.clicked.connect(self._detect)

        #
        # Scroll Area
        scrolled_widget = QWidget()
        scrolled_widget.setLayout(self.board_widgets_layout)

        scroll = QScrollArea()
        scroll.setWidget(scrolled_widget)
        scroll.setWidgetResizable(True)

        scroll_layout = QGridLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(scroll)

        group = QGroupBox("Boards")
        group.setLayout(scroll_layout)

        main_layout = QGridLayout(self)
        main_layout.addWidget(self.button_detect_boards, 0, 1)
        main_layout.addWidget(group, 1, 0, 1, 2)
        main_layout.setColumnStretch(0, 100)

        Configuration().board_detector.detectionStarted.connect(self._clear)
        Configuration().board_detector.boardDetected.connect(self._update_widgets)
        Configuration().board_detector.detectionFinished.connect(self._complete_detection)

    @error_reported("Board detection")
    def _detect(self):
        with Hourglass():
            Configuration().board_detector.detect()

    def _clear(self):
        layout.clear(self.board_widgets_layout)
        self.board_widgets = dict()

    def _update_widgets(self):
        for board in Configuration().board_detector.boards:
            if board.hardware_id not in self.board_widgets:
                new_board_widget = BoardWidget(board)
                self.board_widgets[board.hardware_id] = new_board_widget
                self.board_widgets_layout.addWidget(new_board_widget)

    def _complete_detection(self):
        self.board_widgets_layout.addWidget(QWidget())
        self.board_widgets_layout.setStretch(len(self.board_widgets), 100)
