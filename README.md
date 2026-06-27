# AI-Based Traffic Controller (Python)

Starter project for an AI-inspired traffic signal controller that combines:

- traffic light simulation
- AI-based signal timing optimization (heuristic decision layer)
- congestion monitoring
- emergency vehicle prioritization

## Project Structure

```
traffic-controller/
├── pyproject.toml
├── traffic_controller/
│   ├── __init__.py
│   ├── cli.py
│   ├── controller.py
│   ├── models.py
│   ├── optimizer.py
│   └── simulation.py
└── tests/
    └── test_controller.py
```

## Requirements

- Python 3.10+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run Simulation

```bash
traffic-controller --steps 10 --seed 42
```

Or:

```bash
python -m traffic_controller.cli --steps 10 --seed 42
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## How It Works

1. Incoming traffic updates lane queues each tick.
2. The optimizer selects the next green lane:
   - emergency lanes are always prioritized
   - otherwise the lane with highest queue is selected
3. Green duration is adaptively set from queue pressure.
4. Queue discharge is simulated using throughput-per-tick.
5. Congestion levels (`LOW`, `MEDIUM`, `HIGH`) are reported per lane.

This is intentionally lightweight and designed as a clean starter foundation for future expansion (ML models, live feeds, multi-intersection coordination, etc.).