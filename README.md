# Robust Autonomy Stack

**Self-Healing Autonomous Driving with Learned Risk Monitoring and RL Red-Teaming**

A complete autonomous driving stack built on MetaDrive that includes:
- Full autonomy pipeline: CV world model → tracking → prediction → planning → control
- ML-based failure risk estimator that triggers safe degradation modes
- RL adversary for automated scenario generation and edge case discovery
- Reproducible evaluation suite with robustness analysis
- Cross-platform: Works on Mac (ARM/Intel), Linux, and Windows

## Features

- **Self-healing autonomy**: Automatically switches to cautious mode or minimal-risk condition when failure risk is high
- **Learned risk monitoring**: Supervised ML model predicts imminent failures based on stack health signals
- **RL red-teaming**: Adversarial agent discovers hard scenarios (cut-ins, aggressive drivers, sensor failures)
- **Full reproducibility**: YAML-based scenarios with seeds for deterministic replay
- **Modular design**: Clean separation of perception, planning, control, and safety layers
- **Cross-platform**: Pure Python implementation works on any OS including Apple Silicon Macs

## Development Status

- Work in progress

## License

MIT License - see [LICENSE](LICENSE) for details
