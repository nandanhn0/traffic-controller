from collections.abc import Mapping, Sequence

from .models import CongestionLevel, LaneState
from .optimizer import SignalTimingOptimizer


class TrafficController:
    """All-in-one traffic controller with simulation and optimization logic."""

    def __init__(
        self,
        lanes: Sequence[str] = ("north", "south", "east", "west"),
        throughput_per_tick: int = 2,
    ) -> None:
        if not lanes:
            raise ValueError("At least one lane is required.")
        self.lanes = {name: LaneState(name=name) for name in lanes}
        self.throughput_per_tick = throughput_per_tick
        self.optimizer = SignalTimingOptimizer()
        self.current_green_lane = lanes[0]
        self.tick = 0

    def step(
        self,
        incoming_traffic: Mapping[str, int],
        emergency_lanes: set[str] | None = None,
    ) -> dict:
        emergency_lanes = emergency_lanes or set()

        for name, lane in self.lanes.items():
            lane.queue_length += max(0, incoming_traffic.get(name, 0))
            lane.has_emergency = name in emergency_lanes

        green_lane, duration, strategy = self.optimizer.choose_green_lane(
            self.lanes.values()
        )
        self.current_green_lane = green_lane

        discharged = duration * self.throughput_per_tick
        lane_state = self.lanes[green_lane]
        lane_state.queue_length = max(0, lane_state.queue_length - discharged)

        congestion = self._congestion_report()
        self.tick += 1
        return {
            "tick": self.tick,
            "green_lane": green_lane,
            "green_duration": duration,
            "strategy": strategy,
            "congestion": [item.__dict__ for item in congestion],
            "queues": {name: lane.queue_length for name, lane in self.lanes.items()},
        }

    def _congestion_report(self) -> list[CongestionLevel]:
        reports: list[CongestionLevel] = []
        for lane in self.lanes.values():
            if lane.queue_length >= 20:
                level = "HIGH"
            elif lane.queue_length >= 10:
                level = "MEDIUM"
            else:
                level = "LOW"
            reports.append(
                CongestionLevel(lane=lane.name, level=level, queue_length=lane.queue_length)
            )
        return reports

    def congestion_report(self) -> list[dict]:
        return [item.__dict__ for item in self._congestion_report()]
