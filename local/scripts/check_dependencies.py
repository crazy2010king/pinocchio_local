#!/usr/bin/env python3
"""
Dependency check script for Pinocchio examples collection.
Checks if all required system and Python dependencies are installed.
"""

import os
import sys
import json
import subprocess
import importlib
from typing import List, Dict, Tuple

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/examples_config.json")

def load_config() -> Dict:
    """Load the example configuration file"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def check_system_dependency(dep: str) -> Tuple[bool, str]:
    """Check if a system dependency is installed using pkg-config"""
    try:
        result = subprocess.run(
            ["pkg-config", "--exists", dep],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = subprocess.run(
                ["pkg-config", "--modversion", dep],
                capture_output=True,
                text=True
            ).stdout.strip()
            return True, version
        return False, "Not found"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_python_dependency(dep: str) -> Tuple[bool, str]:
    """Check if a Python dependency is installed"""
    try:
        module = importlib.import_module(dep)
        version = getattr(module, "__version__", "Unknown")
        return True, version
    except ImportError:
        return False, "Not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_all_dependencies(config: Dict) -> Tuple[set, set]:
    """Get all unique dependencies from the config"""
    system_deps = set()
    python_deps = set()

    # Common system dependencies
    system_deps.update(["pinocchio", "eigen3", "hpp-fcl", "urdfdom"])

    # Common Python dependencies
    python_deps.update(["pinocchio", "numpy", "scipy", "matplotlib"])

    for example in config["examples"]:
        for dep in example.get("dependencies", []):
            # Check if it's a system or Python dependency
            if dep in ["eigen3", "hpp-fcl", "urdfdom", "pinocchio"]:
                system_deps.add(dep)
            else:
                python_deps.add(dep)

    return system_deps, python_deps

def main():
    print("=" * 60)
    print("Pinocchio Examples Dependency Checker")
    print("=" * 60)

    try:
        config = load_config()
    except Exception as e:
        print(f"❌ Failed to load config: {str(e)}")
        sys.exit(1)

    system_deps, python_deps = get_all_dependencies(config)

    print("\n📋 System Dependencies:")
    print("-" * 40)
    system_ok = True
    for dep in sorted(system_deps):
        installed, version = check_system_dependency(dep)
        status = "✅" if installed else "❌"
        print(f"{status} {dep:<20} Version: {version}")
        if not installed:
            system_ok = False

    print("\n🐍 Python Dependencies:")
    print("-" * 40)
    python_ok = True
    for dep in sorted(python_deps):
        installed, version = check_python_dependency(dep)
        status = "✅" if installed else "❌"
        print(f"{status} {dep:<20} Version: {version}")
        if not installed:
            python_ok = False

    print("\n" + "=" * 60)
    print("Summary:")
    print("-" * 60)

    all_ok = system_ok and python_ok

    if all_ok:
        print("✅ All dependencies are installed! You can run the examples.")
    else:
        print("❌ Some dependencies are missing. Please install them before running examples.")
        print("\n💡 Installation commands:")
        print("sudo apt install libeigen3-dev libhpp-fcl-dev liburdfdom-dev")
        print("pip install pin numpy scipy matplotlib")

    print("=" * 60)
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
