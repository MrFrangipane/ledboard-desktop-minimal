import logging

from PySide6.QtCore import QObject, Signal

from ledboarddesktopminimal.core.board import Board
from ledboarddesktopminimal.components.board_communicator.communicator import BoardCommunicator
from ledboarddesktopminimal.components.board_factory import board_factory

_logger = logging.getLogger(__name__)


class BoardDetector(QObject):
    detectionStarted = Signal()
    detectionFinished = Signal()
    boardDetected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._communicator = BoardCommunicator()
        self.boards: [Board] = list()

    def detect(self):
        self.boards = list()
        self.detectionStarted.emit()

        ports = BoardCommunicator.available_serial_port_names()
        if not ports:
            _logger.info(f"No serial ports, nothing to detect")
            self.detectionFinished.emit()
            return

        _logger.info(f"Detecting boards...")
        for port_name in ports:
            _logger.info(f"Port {port_name}")
            self._communicator.set_serial_port_name(port_name)
            settings = self._communicator.get_configuration()
            if settings is not None:
                self.boards.append(board_factory(port_name, settings))
                self.boardDetected.emit()
                _logger.info(f"Detected board '{settings.name}'")
            else:
                _logger.info(f"No board")

        self.detectionFinished.emit()
