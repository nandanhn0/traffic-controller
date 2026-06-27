# AI-Based Traffic Controller (Python Full Stack Starter)

This project now includes both:
- **Backend API** for simulation state and control
- **Frontend dashboard** to run ticks and visualize controller output

Core features:
- traffic light simulation
- AI-based signal timing optimization (heuristic adaptive policy)
- congestion monitoring
- emergency vehicle prioritization

## Project Structure

```text
traffic-controller/
├── pyproject.toml
├── traffic_controller/
│   ├── api.py                # Backend server (HTTP API + static frontend hosting)
│   ├── backend.py            # Backend state/service layer
│   ├── cli.py                # CLI simulation runner
│   ├── controller.py         # Core traffic control logic
│   ├── models.py
│   ├── optimizer.py
│   ├── simulation.py
│   └── web/
│       ├── index.html        # Frontend UI
│       ├── app.js            # Frontend logic
│       └── styles.css
└── tests/
    ├── test_backend.py
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

## How to Use This Project

### 1) Run Backend + Frontend Dashboard

```bash
traffic-controller-server --host 127.0.0.1 --port 8000
```

Then open:

`http://127.0.0.1:8000`

From the web UI you can:
- set incoming vehicles per lane
- optionally choose an emergency lane
- run one simulation tick
- reset the controller
- inspect JSON state output

### 2) Run CLI Simulation (Backend logic only)

```bash
traffic-controller --steps 10 --seed 42
```

Or:

```bash
python -m traffic_controller.cli --steps 10 --seed 42
```

### 3) API Endpoints

- `GET /api/state` → current tick, queues, congestion, latest decision
- `POST /api/step` → advances one tick
- `POST /api/reset` → resets state

Example payload for `/api/step`:

```json
{
  "incoming_traffic": { "north": 6, "south": 2, "east": 1, "west": 0 },
  "emergency_lanes": ["south"]
}
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Controller Workflow

1. Incoming traffic updates lane queues.
2. Emergency lane gets top priority when present.
3. Otherwise, the highest queue is selected for green light.
4. Green duration is adaptively chosen from queue pressure.
5. Vehicles are discharged based on throughput per tick.
6. Congestion levels are reported (`LOW`, `MEDIUM`, `HIGH`).

This foundation is ready for extension (real ML models, camera feeds, multiple intersections, and scheduling strategies).