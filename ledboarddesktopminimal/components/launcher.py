import logging

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QApplication, QDockWidget

# from pyside6helpers.css.editor import CSSEditor
from pyside6helpers import css
from pyside6helpers.logger import dock_logger_to_main_window

from ledboarddesktopminimal.components.central_widget import CentralWidget
from ledboarddesktopminimal.components.main_window import MainWindow


_logger = logging.getLogger(__name__)


class Launcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._application = QApplication()
        css.load_onto(self._application)

        self._main_window = MainWindow()

        #
        # Logger
        dock_logger_to_main_window(self._main_window)

        #
        # Boards
        self._central_widget = CentralWidget()
        self._main_window.setCentralWidget(self._central_widget)

        self._main_window.resize(950, 600)

        logging.basicConfig(level=logging.INFO)

        # self.css_editor = CSSEditor("Frangitron")

    def exec(self) -> int:
        self._main_window.show()
        return self._application.exec()
