from __future__ import annotations

from collections.abc import Mapping, Sequence
from threading import RLock

from .controller import TrafficController


class TrafficControllerBackend:
    """Stateful backend service for API-driven traffic simulation."""

    def __init__(
        self,
        lanes: Sequence[str] = ("north", "south", "east", "west"),
        throughput_per_tick: int = 2,
    ) -> None:
        self._lanes = tuple(lanes)
        self._throughput_per_tick = throughput_per_tick
        self._lock = RLock()
        self._controller = TrafficController(
            lanes=self._lanes, throughput_per_tick=self._throughput_per_tick
        )
        self._last_decision: dict | None = None

    def get_state(self) -> dict:
        with self._lock:
            return {
                "tick": self._controller.tick,
                "current_green_lane": self._controller.current_green_lane,
                "queues": {
                    name: lane.queue_length
                    for name, lane in self._controller.lanes.items()
                },
                "congestion": self._controller.congestion_report(),
                "last_decision": self._last_decision,
            }

    def step(self, payload: Mapping | None) -> dict:
        payload = payload or {}
        incoming = self._normalize_incoming_traffic(payload.get("incoming_traffic", {}))
        emergency_lanes = self._normalize_emergency_lanes(payload.get("emergency_lanes", []))
        with self._lock:
            decision = self._controller.step(
                incoming_traffic=incoming,
                emergency_lanes=emergency_lanes,
            )
            self._last_decision = decision
            return decision

    def reset(self) -> dict:
        with self._lock:
            self._controller = TrafficController(
                lanes=self._lanes,
                throughput_per_tick=self._throughput_per_tick,
            )
            self._last_decision = None
            return self.get_state()

    def _normalize_incoming_traffic(self, incoming: Mapping) -> dict[str, int]:
        values: dict[str, int] = {}
        for lane in self._lanes:
            raw = incoming.get(lane, 0)
            try:
                value = int(raw)
            except (TypeError, ValueError):
                value = 0
            values[lane] = max(0, value)
        return values

    def _normalize_emergency_lanes(self, lanes: Sequence) -> set[str]:
        valid = set(self._lanes)
        return {str(lane) for lane in lanes if str(lane) in valid}
