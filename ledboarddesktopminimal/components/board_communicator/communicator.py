import logging

from serial.tools.list_ports import comports as list_serial_ports
from pythonarduinoserial.communicator import SerialCommunicator

from ledboarddesktopminimal.components.board_communicator.structs import BoardSettings, all_structs


_logger = logging.getLogger(__name__)


class BoardCommunicator:
    def __init__(self):
        self.serial_communicator = SerialCommunicator(structs=all_structs)

    @staticmethod
    def available_serial_port_names():
        return [port.name for port in list_serial_ports()]

    def set_serial_port_name(self, name):
        self.serial_communicator.set_port_name(name)

    def configure(self, settings: BoardSettings):
        self.serial_communicator.send(settings)
        _logger.info(f"Configured board on {self.serial_communicator.serial_port_name}")

    def get_configuration(self) -> BoardSettings:
        _logger.info(f"Get board configuration from {self.serial_communicator.serial_port_name}")
        return self.serial_communicator.receive(BoardSettings)
