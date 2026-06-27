import unittest

from traffic_controller.backend import TrafficControllerBackend


class TrafficControllerBackendTests(unittest.TestCase):
    def test_step_returns_decision_and_state_updates(self) -> None:
        backend = TrafficControllerBackend()
        decision = backend.step(
            {
                "incoming_traffic": {"north": 6, "south": 2, "east": 1, "west": 0},
                "emergency_lanes": ["south"],
            }
        )
        self.assertEqual(decision["green_lane"], "south")
        self.assertEqual(decision["strategy"], "emergency-priority")
        state = backend.get_state()
        self.assertEqual(state["tick"], 1)
        self.assertIsNotNone(state["last_decision"])

    def test_reset_clears_tick_and_last_decision(self) -> None:
        backend = TrafficControllerBackend()
        backend.step({"incoming_traffic": {"north": 10}})
        state = backend.reset()
        self.assertEqual(state["tick"], 0)
        self.assertIsNone(state["last_decision"])
        self.assertEqual(state["queues"]["north"], 0)


if __name__ == "__main__":
    unittest.main()
