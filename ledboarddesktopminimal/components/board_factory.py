from binascii import hexlify

from ledboarddesktopminimal.core.board import Board
from ledboarddesktopminimal.components.board_communicator.structs import BoardSettings


def board_factory(port_name, settings: BoardSettings) -> Board:
    new_board = Board()

    new_board.name = settings.name.strip(" \0")

    new_board.firmware_revision = settings.firmware_revision
    new_board.hardware_id = hexlify(settings.hardware_id, sep=" ")  # FIXME construct a proper string
    new_board.hardware_revision = settings.hardware_revision
    new_board.ip_address = ".".join(str(int(b)) for b in settings.ip_address)
    new_board.port_name = port_name

    new_board.pixel_per_universe = settings.pixel_per_universe
    new_board.universe_a = settings.universe_a
    new_board.universe_b = settings.universe_b
    new_board.universe_c = settings.universe_c

    return new_board
