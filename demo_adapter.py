#!/usr/bin/env python3
# Demo script showing MetaDrive adapter usage
# Drives forward for 100 steps and prints ego state

import sys
import argparse
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from robust_autonomy_stack.adapters.metadrive_adapter import MetaDriveAdapter


def main():
    parser = argparse.ArgumentParser(description="Demo MetaDrive adapter")
    parser.add_argument("--no-render", action="store_true", help="Disable rendering window")
    args = parser.parse_args()
    
    # Create adapter with simple config
    config = {
        "use_render": not args.no_render,  # Render by default unless --no-render specified
        "manual_control": False,
        "map_name": "X",
        "start_seed": 42,
        "num_scenarios": 1,
        "traffic_density": 0.1,
    }
    
    render_status = "enabled" if not args.no_render else "disabled"
    print(f"Creating MetaDrive adapter (rendering {render_status})")
    adapter = MetaDriveAdapter(config)
    print(f"Action space: {adapter.get_action_space()}")
    print(f"Observation space shape: {adapter.get_observation_space().shape}\n")
    
    # Reset environment
    print("Resetting environment...")
    obs, info = adapter.reset()
    print(f"Initial observation shape: {obs.shape}")
    print(f"Initial info keys: {list(info.keys())}\n")
    
    # Get initial ego state
    ego_state = adapter.get_ego_state()
    print("Initial ego state:")
    print(f"  Position: x={ego_state['position']['x']:.2f}, y={ego_state['position']['y']:.2f}")
    print(f"  Speed: {ego_state['speed']:.2f} m/s")
    print(f"  Heading: {ego_state['heading']:.2f} rad\n")
    
    # Drive forward for 100 steps
    print("Driving forward for 100 steps\n")
    
    for step in range(100):
        # Simple forward action: no steering, constant throttle
        action = np.array([0.0, 0.5])  # [steering, throttle]
        
        # Step environment
        obs, reward, terminated, truncated, info = adapter.step(action)
        
        # Print progress every 10 steps
        if (step + 1) % 10 == 0:
            ego_state = adapter.get_ego_state()
            print(f"Step {step + 1:3d}: "
                  f"pos=({ego_state['position']['x']:6.2f}, {ego_state['position']['y']:6.2f}), "
                  f"speed={ego_state['speed']:5.2f} m/s, "
                  f"reward={reward:6.3f}, "
                  f"on_lane={ego_state['on_lane']}")
        
        # Check if episode ended
        if terminated or truncated:
            print(f"\nEpisode ended at step {step + 1}")
            print(f"  Terminated: {terminated}")
            print(f"  Truncated: {truncated}")
            if info.get('crash'):
                print(f"  Crash detected!")
            if info.get('arrive_dest'):
                print(f"  Reached destination!")
            break
    
    # Final state
    print("\nFinal ego state:")
    ego_state = adapter.get_ego_state()
    print(f"  Position: x={ego_state['position']['x']:.2f}, y={ego_state['position']['y']:.2f}")
    print(f"  Speed: {ego_state['speed']:.2f} m/s")
    print(f"  Heading: {ego_state['heading']:.2f} rad")
    
    # Clean up
    adapter.close()
    print("\nDemo Complete")


if __name__ == "__main__":
    main()
