from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QScrollArea

from pyside6helpers import layout

from ledboarddesktopminimal.core.configuration import Configuration
from ledboarddesktopminimal.components.boards_widget.board_widget import BoardWidget


class BoardsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.widgets = dict()

        self.layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(scroll)

        group = QGroupBox("Boards")
        group.setLayout(scroll_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(group)

        Configuration().board_detector.detectionStarted.connect(self._clear)
        Configuration().board_detector.boardDetected.connect(self._update_widgets)
        Configuration().board_detector.detectionFinished.connect(self._complete_detection)

    def _clear(self):
        layout.clear(self.layout)
        self.widgets = dict()

    def _update_widgets(self):
        for board in Configuration().board_detector.boards:
            if board.hardware_id not in self.widgets:
                new_board_widget = BoardWidget(board)
                self.widgets[board.hardware_id] = new_board_widget
                self.layout.addWidget(new_board_widget)

    def _complete_detection(self):
        self.layout.addWidget(QWidget())
        self.layout.setStretch(len(self.widgets), 100)
