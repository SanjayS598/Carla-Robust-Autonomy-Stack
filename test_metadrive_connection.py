# Test script to verify MetaDrive installation and basic functionality
# Run this to check if MetaDrive is properly installed

import sys

try:
    from metadrive import MetaDriveEnv
    from metadrive.constants import HELP_MESSAGE
    print("SUCCESS: MetaDrive imported successfully")
    print(f"MetaDrive version: {MetaDriveEnv.VERSION if hasattr(MetaDriveEnv, 'VERSION') else 'unknown'}")
except ImportError as e:
    print(f"ERROR: Failed to import MetaDrive: {e}")
    print("\nInstall MetaDrive with: pip install metadrive-simulator")
    sys.exit(1)

def test_metadrive():
    print("\nCreating MetaDrive environment...")
    
    try:
        # Create a simple environment
        config = {
            "use_render": False,  # No rendering for this test
            "manual_control": False,
            "traffic_density": 0.1,
            "map": "X",  # Simple intersection map
            "start_seed": 0,
        }
        
        env = MetaDriveEnv(config)
        print("SUCCESS: MetaDrive environment created")
        
        # Reset environment
        obs, info = env.reset()
        print(f"Observation shape: {obs.shape if hasattr(obs, 'shape') else type(obs)}")
        print(f"Info keys: {list(info.keys()) if isinstance(info, dict) else 'N/A'}")
        
        # Take a few random steps
        print("\nTaking 5 random steps...")
        for i in range(5):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"Step {i+1}: reward={reward:.3f}, terminated={terminated}, truncated={truncated}")
            
            if terminated or truncated:
                print("Episode ended early")
                break
        
        env.close()
        print("\nSUCCESS: MetaDrive is working correctly!")
        print("\nYou can now proceed with Phase 1.2: Implementing the MetaDrive adapter")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to run MetaDrive: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_metadrive()
    sys.exit(0 if success else 1)
