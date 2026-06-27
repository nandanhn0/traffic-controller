import argparse

from .simulation import format_history, run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-based traffic controller simulation")
    parser.add_argument("--steps", type=int, default=12, help="Number of simulation ticks")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    history = run_simulation(steps=args.steps, seed=args.seed)
    print(format_history(history))


if __name__ == "__main__":
    main()
