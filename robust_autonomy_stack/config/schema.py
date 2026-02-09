# Pydantic configuration schemas for the autonomy stack
# These define the structure for all config files (YAML scenarios, stack params, etc.)

from typing import Optional, List, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import yaml


class SimulatorConfig(BaseModel):
    # MetaDrive simulator configuration
    
    use_render: bool = Field(default=False, description="Enable rendering window")
    map_name: str = Field(default="X", description="Map type (X, O, C, S, R, T)")
    manual_control: bool = Field(default=False, description="Enable manual keyboard control")
    num_scenarios: int = Field(default=1, description="Number of scenarios to generate")
    start_seed: int = Field(default=0, description="Random seed for environment")


class SensorConfig(BaseModel):
    # Camera sensor mounting and settings
    
    width: int = Field(default=800, description="Image width in pixels")
    height: int = Field(default=600, description="Image height in pixels")
    fov: float = Field(default=90.0, description="Field of view in degrees")
    fps: int = Field(default=20, description="Frames per second")
    mount_x: float = Field(default=1.5, description="X offset from vehicle center (forward)")
    mount_y: float = Field(default=0.0, description="Y offset from vehicle center (lateral)")
    mount_z: float = Field(default=2.4, description="Z offset from vehicle center (up)")
    pitch: float = Field(default=-15.0, description="Camera pitch in degrees")


class ScenarioConfig(BaseModel):
    # Defines a test scenario: map, traffic, scripted events, noise
    
    name: str = Field(description="Scenario name")
    map_type: str = Field(default="X", description="Map type (X, O, C, S, R, T)")
    traffic_density: float = Field(default=0.1, ge=0.0, le=1.0, description="Traffic density")
    
    # Ego spawn (optional - MetaDrive will use map defaults if not specified)
    ego_spawn_lane: Optional[int] = Field(default=None, description="Starting lane index")
    
    # Traffic configuration
    num_agents: int = Field(default=10, description="Number of traffic agents")
    agent_policy: str = Field(default="IDM", description="Agent driving policy (IDM, Manual)")
    
    # Scripted events (optional)
    scripted_events: List[Dict[str, Any]] = Field(default_factory=list, description="Scripted scenario events")
    
    # Perturbations
    frame_drop_prob: float = Field(default=0.0, ge=0.0, le=1.0, description="Frame drop probability")
    position_noise_std: float = Field(default=0.0, ge=0.0, description="Position noise std dev (meters)")
    
    # Reproducibility
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    
    @classmethod
    def from_yaml(cls, path: Path) -> "ScenarioConfig":
        # Load and validate scenario from YAML file
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)


class StackConfig(BaseModel):
    # Core autonomy stack parameters: planning weights, thresholds, control gains
    
    # Planning weights
    collision_weight: float = Field(default=100.0, description="Collision cost weight")
    progress_weight: float = Field(default=1.0, description="Progress reward weight")
    comfort_weight: float = Field(default=0.5, description="Comfort cost weight")
    legality_weight: float = Field(default=10.0, description="Legality violation cost weight")
    
    # Speed limits
    max_speed_mps: float = Field(default=13.89, description="Max speed (m/s) ~50 km/h")
    target_speed_mps: float = Field(default=11.11, description="Target cruise speed (m/s) ~40 km/h")
    
    # Safety thresholds
    min_following_distance: float = Field(default=10.0, description="Min following distance (m)")
    time_headway: float = Field(default=2.0, description="Desired time headway (s)")
    
    # Risk supervisor thresholds
    risk_threshold_cautious: float = Field(default=0.3, description="Risk threshold for cautious mode")
    risk_threshold_mrc: float = Field(default=0.7, description="Risk threshold for minimal risk condition")
    risk_horizon_s: float = Field(default=3.0, description="Risk prediction horizon (seconds)")
    
    # Control parameters
    pure_pursuit_lookahead: float = Field(default=5.0, description="Pure pursuit lookahead distance (m)")
    pid_kp: float = Field(default=1.0, description="PID proportional gain")
    pid_ki: float = Field(default=0.1, description="PID integral gain")
    pid_kd: float = Field(default=0.05, description="PID derivative gain")


class OutputConfig(BaseModel):
    # Output and logging settings
    
    log_dir: Path = Field(default=Path("runs"), description="Base directory for run outputs")
    save_video: bool = Field(default=True, description="Save video recordings")
    save_debug_plots: bool = Field(default=True, description="Save debug visualization plots")
    log_frequency_hz: float = Field(default=10.0, description="Logging frequency")
    
    @field_validator('log_dir')
    @classmethod
    def create_log_dir(cls, v: Path) -> Path:
        # Auto-create log directory if it doesn't exist
        v.mkdir(parents=True, exist_ok=True)
        return v
