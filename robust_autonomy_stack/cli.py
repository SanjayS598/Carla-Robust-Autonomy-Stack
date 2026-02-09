# Command-line interface for Robust Autonomy Stack

import argparse
import sys
from pathlib import Path


def run_scenario(args):
    # Execute a single scenario from YAML config
    import numpy as np
    from pathlib import Path
    from robust_autonomy_stack.adapters.metadrive_adapter import MetaDriveAdapter
    from robust_autonomy_stack.config.schema import ScenarioConfig
    
    print(f"Loading scenario: {args.scenario}")
    
    # Load scenario config
    scenario_path = Path(args.scenario)
    if scenario_path.suffix in ['.yaml', '.yml']:
        scenario = ScenarioConfig.from_yaml(scenario_path)
    else:
        print(f"Error: Scenario file must be YAML (.yaml or .yml)")
        sys.exit(1)
    
    # Create adapter
    adapter_config = {
        "use_render": not args.no_render,  # Render by default unless --no-render specified
        "manual_control": False,
        "map_name": scenario.map_type,
        "start_seed": scenario.seed if scenario.seed is not None else 0,
        "num_scenarios": 1,
        "traffic_density": scenario.traffic_density,
    }
    
    print(f"Creating environment with map '{scenario.map_type}'...")
    adapter = MetaDriveAdapter(adapter_config)
    
    # Reset
    obs, info = adapter.reset()
    print(f"Environment ready. Observation shape: {obs.shape}")
    
    # Run simple forward controller for now
    print("\nRunning scenario...")
    for step in range(100):
        action = np.array([0.0, 0.5])  # Drive forward
        obs, reward, terminated, truncated, info = adapter.step(action)
        
        if (step + 1) % 20 == 0:
            ego = adapter.get_ego_state()
            print(f"Step {step+1}: pos=({ego['position']['x']:.1f}, {ego['position']['y']:.1f}), "
                  f"speed={ego['speed']:.1f} m/s, reward={reward:.3f}")
        
        if terminated or truncated:
            print(f"\nEpisode ended at step {step + 1}")
            break
    
    adapter.close()
    print(f"\nScenario complete. Output saved to: {args.output}")
    # TODO: Save metrics and replay data


def run_benchmark(args):
    # Run full benchmark suite with multiple scenarios
    print(f"Running benchmark suite: {args.suite}")
    # TODO: Implement benchmark suite
    pass


def train_risk_model(args):
    # Train the ML model that predicts failure risk
    print(f"Training risk model with data: {args.data}")
    # TODO: Implement risk model training
    pass


def train_adversary(args):
    # Train the RL agent that generates adversarial scenarios
    print(f"Training adversary with config: {args.config}")
    # TODO: Implement adversary training
    pass


def replay_run(args):
    # Replay a previous run using saved seed and config
    print(f"Replaying run: {args.run_id}")
    # TODO: Implement replay
    pass


def main():
    # Main entry point - parse commands and dispatch to handlers
    parser = argparse.ArgumentParser(
        prog="robust-autonomy-stack",
        description="Robust Autonomy Stack - Self-healing autonomy with RL red-teaming"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run scenario command
    run_parser = subparsers.add_parser("run", help="Run a single scenario")
    run_parser.add_argument("--scenario", required=True, help="Path to scenario YAML file")
    run_parser.add_argument("--output", default="runs", help="Output directory for results")
    run_parser.add_argument("--no-render", action="store_true", help="Disable rendering window")
    run_parser.set_defaults(func=run_scenario)
    
    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run benchmark suite")
    bench_parser.add_argument("--suite", required=True, help="Path to benchmark suite config")
    bench_parser.add_argument("--output", default="runs/benchmarks", help="Output directory")
    bench_parser.set_defaults(func=run_benchmark)
    
    # Train risk model command
    train_risk_parser = subparsers.add_parser("train-risk", help="Train failure risk model")
    train_risk_parser.add_argument("--data", required=True, help="Path to feature data (parquet/csv)")
    train_risk_parser.add_argument("--output", default="models/risk", help="Model output directory")
    train_risk_parser.set_defaults(func=train_risk_model)
    
    # Train adversary command
    train_adv_parser = subparsers.add_parser("train-adversary", help="Train RL adversary")
    train_adv_parser.add_argument("--config", required=True, help="Path to adversary config")
    train_adv_parser.add_argument("--output", default="models/adversary", help="Model output directory")
    train_adv_parser.set_defaults(func=train_adversary)
    
    # Replay command
    replay_parser = subparsers.add_parser("replay", help="Replay a previous run")
    replay_parser.add_argument("--run-id", required=True, help="Run ID to replay")
    replay_parser.set_defaults(func=replay_run)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
