# CARLA Robust Autonomy Stack

**Self-Healing Autonomous Driving with Learned Risk Monitoring and RL Red-Teaming**

A complete autonomous driving stack for CARLA that includes:
- 🚗 Full autonomy pipeline: CV world model → tracking → prediction → planning → control
- 🛡️ ML-based failure risk estimator that triggers safe degradation modes
- 🎯 RL adversary for automated scenario generation and edge case discovery
- 📊 Reproducible evaluation suite with robustness analysis

## Features

- **Self-healing autonomy**: Automatically switches to cautious mode or minimal-risk condition when failure risk is high
- **Learned risk monitoring**: Supervised ML model predicts imminent failures based on stack health signals
- **RL red-teaming**: Adversarial agent discovers hard scenarios (cut-ins, weather, sensor dropouts)
- **Full reproducibility**: YAML-based scenarios with seeds for deterministic replay
- **Modular design**: Clean separation of perception, planning, control, and safety layers

## Quick Start

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- macOS/Linux (tested on M4 Mac)

### Installation

```bash
# Clone the repository
git clone https://github.com/SanjayS598/Carla-Robust-Autonomy-Stack.git
cd Carla-Robust-Autonomy-Stack

# Install Python dependencies
pip install -r requirements.txt

# Install CARLA Python API (match your CARLA version)
pip install carla==0.9.15
```

### Running CARLA Server

```bash
# Start CARLA in Docker
docker compose -f docker/compose.yml up
```

### Running a Scenario

```bash
# Run a scenario (coming in Phase 1+)
python -m carla_robust_autonomy_stack.cli run --scenario scenarios/examples/cut_in.yaml
```

## Project Structure

```
carla_robust_autonomy_stack/
├── adapters/          # CARLA client adapter
├── sensors/           # Sensor management
├── cv/                # Computer vision (freespace, lanes)
├── tracking/          # Multi-object tracking
├── prediction/        # Trajectory prediction
├── planning/          # Behavior FSM & trajectory planning
├── control/           # Lateral & longitudinal control
├── safety/            # Risk model & safety supervisor
├── scenarios/         # Scenario definitions
├── evaluation/        # Metrics & reporting
└── utils/             # Geometry, time, replay utilities
```

## Development Roadmap

- [x] Phase 0: Scaffolding & config schemas
- [ ] Phase 1: Docker CARLA + client adapter
- [ ] Phase 2: CV world model (segmentation → freespace + lanes)
- [ ] Phase 3: Tracking & prediction with uncertainty
- [ ] Phase 4: Planning & control
- [ ] Phase 5: ML risk model & safety supervisor
- [ ] Phase 6: RL adversary
- [ ] Phase 7: Evaluation & reporting

## CLI Commands

```bash
# Run a single scenario
carla-robust-autonomy-stack run --scenario path/to/scenario.yaml

# Run benchmark suite
carla-robust-autonomy-stack benchmark --suite path/to/suite.yaml

# Train risk prediction model
carla-robust-autonomy-stack train-risk --data runs/*/features.parquet

# Train RL adversary
carla-robust-autonomy-stack train-adversary --config adversary_config.yaml

# Replay a previous run
carla-robust-autonomy-stack replay --run-id <run_id>
```

## License

MIT License - see [LICENSE](LICENSE) for details
Reproducible CARLA autonomy full-stack with a CV world model, a learned failure-risk supervisor for safe degradation, and an automated scenario generator for edge-case discovery with benchmark reports and replays.
