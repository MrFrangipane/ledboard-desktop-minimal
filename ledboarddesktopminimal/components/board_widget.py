from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLineEdit, QSpinBox, QLabel

from pyside6helpers import icons
from pyside6helpers.group import make_group
from pyside6helpers.error_reporting import error_reported

from ledboarddesktopminimal.core.board import Board
from ledboarddesktopminimal.core.configuration import Configuration
from ledboarddesktopminimal.components.board_communicator.structs import BoardSettings
from ledboarddesktopminimal.components.board_factory import board_factory


class BoardWidget(QWidget):
    def __init__(self, board: Board, parent=None):
        super().__init__(parent)

        self._board = board

        self.lineedit_name = QLineEdit()
        self.lineedit_name.setMaxLength(7)  # see board communicator structs
        self.lineedit_name.setFixedWidth(90)

        self.lineedit_ip = QLineEdit()
        self.lineedit_ip.setMaxLength(15)
        self.lineedit_ip.setFixedWidth(110)

        self.spin_universe_a = QSpinBox()
        self.spin_universe_a.setMinimum(0)
        self.spin_universe_a.setMaximum(256)

        self.spin_universe_b = QSpinBox()
        self.spin_universe_b.setMinimum(0)
        self.spin_universe_b.setMaximum(256)

        self.spin_universe_c = QSpinBox()
        self.spin_universe_c.setMinimum(0)
        self.spin_universe_c.setMaximum(256)

        self.spin_led_per_universe = QSpinBox()
        self.spin_led_per_universe.setMinimum(1)
        self.spin_led_per_universe.setMaximum(500)

        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.setToolTip("Update GUI from the board info")
        self.button_refresh.setIcon(icons.refresh())
        self.button_refresh.clicked.connect(self.refresh)

        self.button_apply = QPushButton("Apply")
        self.button_apply.setToolTip("Update board settings from GUI. No saving")
        self.button_apply.setIcon(icons.play_button())
        self.button_apply.clicked.connect(self.apply)

        self.button_save_and_reboot = QPushButton("Save & reboot")
        self.button_save_and_reboot.setToolTip("Update board settings from GUI. Save. Reboot.")
        self.button_save_and_reboot.setIcon(icons.diskette())
        self.button_save_and_reboot.clicked.connect(self.save_and_reboot)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(make_group("Name", [self.lineedit_name]))
        layout.addWidget(make_group("IP Address", [self.lineedit_ip]))
        layout.addWidget(make_group("Artnet Universes", orientation=Qt.Horizontal, widgets=[
            QLabel("A"), self.spin_universe_a,
            QLabel("B"), self.spin_universe_b,
            QLabel("C"), self.spin_universe_c,
        ]))
        layout.addWidget(make_group(
            title="LED count",
            widgets=[self.spin_led_per_universe],
            tooltip="LED count per universe"
        ))

        layout.addWidget(QWidget())
        layout.addWidget(make_group("Actions", orientation=Qt.Horizontal, widgets=[
            self.button_refresh,
            self.button_apply,
            self.button_save_and_reboot
        ]))
        layout.setStretch(layout.count() - 2, 100)

        self.update_widgets()

    def update_widgets(self):
        self.lineedit_name.setText(self._board.name)

        self.lineedit_ip.setText(self._board.ip_address)

        self.spin_universe_a.setValue(self._board.universe_a)
        self.spin_universe_b.setValue(self._board.universe_b)
        self.spin_universe_c.setValue(self._board.universe_c)
        self.spin_led_per_universe.setValue(self._board.pixel_per_universe)

        self.setToolTip(
            f"Board name: {self._board.name}\n"
            f"Port: {self._board.port_name}\n"
            f"Hardware ID: {self._board.hardware_id}\n"
            f"Hardware revision: {self._board.hardware_revision}\n"
            f"Firmware revision: {self._board.firmware_revision}"
        )

    @error_reported("Refresh Board")
    def refresh(self):
        Configuration().board_communicator.set_serial_port_name(self._board.port_name)
        settings = Configuration().board_communicator.get_configuration()
        self._board = board_factory(self._board.port_name, settings)
        self.update_widgets()

    @error_reported("Apply Settings")
    def apply(self):
        Configuration().board_communicator.set_serial_port_name(self._board.port_name)
        Configuration().board_communicator.configure(self._make_settings())

    @error_reported("Save and reboot")
    def save_and_reboot(self):
        Configuration().board_communicator.set_serial_port_name(self._board.port_name)
        Configuration().board_communicator.configure(self._make_settings(do_save_and_reboot=True))

    # FIXME should we construct a Board instead ? (and let the factory convert to BoardSettings)
    def _make_settings(self, do_save_and_reboot=False) -> BoardSettings:
        return BoardSettings(
            name=self.lineedit_name.text(),
            ip_address=bytes([int(i) for i in self.lineedit_ip.text().split('.')]),
            universe_a=self.spin_universe_a.value(),
            universe_b=self.spin_universe_b.value(),
            universe_c=self.spin_universe_c.value(),
            pixel_per_universe=self.spin_led_per_universe.value(),
            do_save_and_reboot=do_save_and_reboot
        )
