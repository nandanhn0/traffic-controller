from dataclasses import dataclass


@dataclass
class LaneState:
    name: str
    queue_length: int = 0
    has_emergency: bool = False


@dataclass
class CongestionLevel:
    lane: str
    level: str
    queue_length: int
