"""Classes: abstract parent + three child classes (inheritance, polymorphism)."""
from abc import ABC, abstractmethod


class PacketError(Exception):
    """Raised when the size or urgency is wrong."""


class Packet(ABC):
    mode = ""

    def __init__(self, size, urgency):                  # constructor
        if size <= 0:
            raise PacketError("Size must be a positive number")
        if not 1 <= urgency <= 5:
            raise PacketError("Urgency must be between 1 and 5")
        self.size = size
        self.urgency = urgency

    @abstractmethod
    def priority(self):
        """Higher number = sent first."""

    @abstractmethod
    def min_link(self):
        """Minimum signal (%) needed to send."""

    def tx_time(self, link):                            # seconds to send at this signal
        return round(self.size * 8 / (1200 * link / 100), 1)


class Telemetry(Packet):
    mode = "TT&C"
    def priority(self): return 100 + self.urgency
    def min_link(self): return 10


class Image(Packet):
    mode = "SSTV"
    def priority(self): return 30 + self.urgency
    def min_link(self): return 50


class Voice(Packet):
    mode = "Voice"
    def priority(self): return 20 + self.urgency
    def min_link(self): return 40


MODES = {"TT&C": Telemetry, "SSTV": Image, "Voice": Voice}
