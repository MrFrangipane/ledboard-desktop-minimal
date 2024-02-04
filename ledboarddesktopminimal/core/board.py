

class Board:
    """
    This class represents a LED Board and its configuration
    """
    def __init__(self):
        self.name: str = None

        self.firmware_revision: int = None
        self.hardware_id: str = None
        self.hardware_revision: int = None
        self.ip_address: str = None
        self.port_name: str = None

        self.pixel_per_universe: int = None
        self.universe_a: int = None
        self.universe_b: int = None
        self.universe_c: int = None
