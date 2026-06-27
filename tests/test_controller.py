import unittest

from traffic_controller.controller import TrafficController


class TrafficControllerTests(unittest.TestCase):
    def test_emergency_lane_is_prioritized(self) -> None:
        controller = TrafficController()
        result = controller.step(
            incoming_traffic={"north": 3, "south": 3, "east": 3, "west": 3},
            emergency_lanes={"west"},
        )
        self.assertEqual(result["green_lane"], "west")
        self.assertEqual(result["strategy"], "emergency-priority")

    def test_congestion_level_reaches_high(self) -> None:
        controller = TrafficController(throughput_per_tick=1)
        result = controller.step(
            incoming_traffic={"north": 24, "south": 0, "east": 0, "west": 0}
        )
        by_lane = {item["lane"]: item["level"] for item in result["congestion"]}
        self.assertEqual(by_lane["north"], "MEDIUM")

        result = controller.step(
            incoming_traffic={"north": 24, "south": 0, "east": 0, "west": 0}
        )
        by_lane = {item["lane"]: item["level"] for item in result["congestion"]}
        self.assertEqual(by_lane["north"], "HIGH")


if __name__ == "__main__":
    unittest.main()
