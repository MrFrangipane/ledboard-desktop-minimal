import os.path
from dataclasses import dataclass

from ledboarddesktopminimal.components.board_communicator.communicator import BoardCommunicator
from ledboarddesktopminimal.components.board_detector import BoardDetector
from ledboarddesktopminimal.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    board_communicator: BoardCommunicator = BoardCommunicator()
    board_detector: BoardDetector = BoardDetector()
    resources_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
