# MetaDrive environment adapter - creates and manages MetaDrive simulator instance

import numpy as np
import os
from typing import Dict, Tuple, Optional, Any
from metadrive import MetaDriveEnv


def check_display_available() -> bool:
    # Check if a display is available for rendering
    # For SSH or headless sessions, return False
    if os.environ.get('SSH_CONNECTION') or os.environ.get('SSH_CLIENT'):
        return False
    if os.environ.get('DISPLAY'):
        return True
    # On macOS, WindowServer runs but we may not have GUI access
    # Check if we're in a proper terminal session with GUI
    if os.name == 'posix':
        try:
            import subprocess
            # Check if we have access to display (not just WindowServer running)
            result = subprocess.run(['ps', '-p', str(os.getppid()), '-o', 'comm='], 
                                  capture_output=True, text=True, timeout=1)
            parent = result.stdout.strip()
            # If parent is Terminal.app or similar GUI terminal, likely have display
            if 'Terminal' in parent or 'iTerm' in parent:
                return True
        except:
            pass
    return False


class MetaDriveAdapter:
    # Wraps MetaDrive environment and provides clean interface for autonomy stack
    
    def __init__(self, config):
        # Initialize MetaDrive environment with given configuration
        # config can be SimulatorConfig or dict
        
        if hasattr(config, 'model_dump'):
            # Pydantic model
            config_dict = config.model_dump()
        elif hasattr(config, 'dict'):
            # Older Pydantic
            config_dict = config.dict()
        else:
            # Already a dict
            config_dict = config
        
        # Check if rendering is requested but display is not available
        if config_dict.get("use_render", False) and not check_display_available():
            print("\nWarning: Rendering requested but no display detected.")
            print("Automatically disabling rendering (headless mode).")
            print("To suppress this warning, use --no-render flag.\n")
            config_dict["use_render"] = False
        
        # Map our config to MetaDrive config
        metadrive_config = {
            "use_render": config_dict.get("use_render", False),
            "manual_control": config_dict.get("manual_control", False),
            "map": config_dict.get("map_name", "X"),
            "start_seed": config_dict.get("start_seed", 0),
            "num_scenarios": config_dict.get("num_scenarios", 1),
            "traffic_density": config_dict.get("traffic_density", 0.1),
        }
        
        # Try to create environment with rendering, fall back to headless if it fails
        try:
            self.env = MetaDriveEnv(metadrive_config)
            self.current_obs = None
            self.current_info = None
        except Exception as e:
            if metadrive_config["use_render"] and "window" in str(e).lower():
                print(f"Warning: Could not open rendering window: {e}")
                print("Falling back to headless mode (no rendering)")
                metadrive_config["use_render"] = False
                self.env = MetaDriveEnv(metadrive_config)
                self.current_obs = None
                self.current_info = None
            else:
                raise
        
    def reset(self) -> Tuple[np.ndarray, Dict[str, Any]]:
        # Reset environment and return initial observation and info
        self.current_obs, self.current_info = self.env.reset()
        return self.current_obs, self.current_info
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        # Execute action and return (observation, reward, terminated, truncated, info)
        # action is [steering, throttle/brake] in range [-1, 1]
        obs, reward, terminated, truncated, info = self.env.step(action)
        self.current_obs = obs
        self.current_info = info
        return obs, reward, terminated, truncated, info
    
    def get_ego_state(self) -> Dict[str, Any]:
        # Extract ego vehicle state: position, velocity, heading, etc.
        
        if self.env.agent is None:
            return {}
        
        # In MetaDrive, agent IS the vehicle
        vehicle = self.env.agent
        
        # Get position
        pos = vehicle.position
        
        # Get velocity (m/s)
        velocity = vehicle.velocity
        speed = np.linalg.norm([velocity[0], velocity[1]])
        
        # Get heading (radians)
        heading = vehicle.heading_theta
        
        # Get steering angle
        steering = vehicle.steering
        
        state = {
            "position": {"x": float(pos[0]), "y": float(pos[1]), "z": float(pos[2] if len(pos) > 2 else 0.0)},
            "velocity": {"x": float(velocity[0]), "y": float(velocity[1])},
            "speed": float(speed),
            "heading": float(heading),
            "steering": float(steering),
            "lane_index": vehicle.lane_index,
            "on_lane": vehicle.on_lane,
        }
        
        return state
    
    def get_camera_image(self) -> Optional[np.ndarray]:
        # Get RGB camera image if available
        # MetaDrive uses sensor manager, check if camera is available
        
        if not hasattr(self.env, 'main_camera') or self.env.main_camera is None:
            return None
        
        # Try to get camera image
        try:
            # MetaDrive cameras return images through the perception module
            if hasattr(self.env.agent, 'image_sensors'):
                for sensor_name, sensor in self.env.agent.image_sensors.items():
                    if 'camera' in sensor_name.lower():
                        return sensor.perceive()
            return None
        except Exception:
            return None
    
    def get_observation_space(self):
        # Return environment observation space
        return self.env.observation_space
    
    def get_action_space(self):
        # Return environment action space
        return self.env.action_space
    
    def render(self):
        # Render the environment (if rendering is enabled)
        if self.env.config["use_render"]:
            self.env.render()
    
    def close(self):
        # Clean shutdown of environment
        if self.env is not None:
            self.env.close()
            self.env = None
    
    def __del__(self):
        # Ensure environment is closed on deletion
        self.close()
