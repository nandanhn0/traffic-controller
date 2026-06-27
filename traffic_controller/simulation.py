import random
from collections.abc import Iterable

from .controller import TrafficController


def run_simulation(steps: int = 12, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    controller = TrafficController()
    history: list[dict] = []

    for _ in range(steps):
        incoming = {
            "north": rng.randint(0, 6),
            "south": rng.randint(0, 6),
            "east": rng.randint(0, 6),
            "west": rng.randint(0, 6),
        }
        emergency_lanes: set[str] = set()
        if rng.random() < 0.2:
            emergency_lanes.add(rng.choice(tuple(incoming.keys())))
        history.append(
            controller.step(incoming_traffic=incoming, emergency_lanes=emergency_lanes)
        )
    return history


def format_history(history: Iterable[dict]) -> str:
    lines = []
    for item in history:
        lines.append(
            (
                f"tick={item['tick']}, green={item['green_lane']}, "
                f"duration={item['green_duration']}, strategy={item['strategy']}, "
                f"queues={item['queues']}"
            )
        )
    return "\n".join(lines)
