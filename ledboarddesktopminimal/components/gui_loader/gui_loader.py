import logging

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QApplication, QDockWidget

# from pyside6helpers.css.editor import CSSEditor
from pyside6helpers import css
from pyside6helpers.hourglass import Hourglass
from pyside6helpers.error_reporting import error_reported

from ledboarddesktopminimal.components.boards_widget.boards_widget import BoardsWidget
from ledboarddesktopminimal.components.board_detector.widget import BoardDetectionWidget
from ledboarddesktopminimal.components.gui_loader.main_window import MainWindow
from ledboarddesktopminimal.components.logger.widget import LoggerWidget
from ledboarddesktopminimal.core.configuration import Configuration


_logger = logging.getLogger(__name__)


class GUILoader(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._application = QApplication()
        css.load_onto(self._application)

        self._main_window = MainWindow()

        #
        # Logger
        self._logger_widget = LoggerWidget()
        logger_dock_widget = QDockWidget()
        logger_dock_widget.setWindowTitle("Logger")
        logger_dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        logger_dock_widget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        logger_dock_widget.setWidget(self._logger_widget)
        self._main_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, logger_dock_widget)

        #
        # Board detection
        self._board_detection_widget = BoardDetectionWidget()
        board_detection_dock_widget = QDockWidget()
        board_detection_dock_widget.setWindowTitle("Board Detector")
        board_detection_dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        board_detection_dock_widget.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        board_detection_dock_widget.setWidget(self._board_detection_widget)
        self._main_window.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, board_detection_dock_widget)

        #
        # Boards
        self._boards_widget = BoardsWidget()
        self._main_window.setCentralWidget(self._boards_widget)

        self._main_window.resize(950, 600)

        logging.basicConfig(level=logging.INFO)

        # self.css_editor = CSSEditor("Frangitron")

    def exec(self) -> int:
        self._main_window.show()
        return self._application.exec()
