from typing import Iterable

from .models import LaneState


class SignalTimingOptimizer:
    """Simple AI-style heuristic optimizer for signal timing."""

    def __init__(self, base_green_ticks: int = 3, max_green_ticks: int = 8) -> None:
        self.base_green_ticks = base_green_ticks
        self.max_green_ticks = max_green_ticks

    def choose_green_lane(self, lanes: Iterable[LaneState]) -> tuple[str, int, str]:
        lane_list = list(lanes)
        emergency_lanes = [lane for lane in lane_list if lane.has_emergency]
        if emergency_lanes:
            selected = max(emergency_lanes, key=lambda lane: lane.queue_length)
            duration = self.max_green_ticks
            return selected.name, duration, "emergency-priority"

        selected = max(lane_list, key=lambda lane: lane.queue_length)
        duration = min(
            self.max_green_ticks,
            self.base_green_ticks + max(0, selected.queue_length // 3),
        )
        return selected.name, duration, "adaptive-queue-optimization"
