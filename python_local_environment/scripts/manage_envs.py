#!/usr/bin/env python3
"""
Virtual Environment Management Script

This script provides utilities for managing Python virtual environments
across different platforms and tools.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional

class VirtualEnvManager:
    """Manages virtual environments using different tools."""
    
    def __init__(self):
        self.available_tools = self._check_available_tools()
    
    def _check_available_tools(self) -> dict:
        """Check which virtual environment tools are available."""
        tools = {}
        
        # Check for built-in venv
        try:
            subprocess.run([sys.executable, "-m", "venv", "--help"], 
                         capture_output=True, check=True)
            tools['venv'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['venv'] = False
        
        # Check for virtualenv
        try:
            subprocess.run(["virtualenv", "--version"], 
                         capture_output=True, check=True)
            tools['virtualenv'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['virtualenv'] = False
        
        # Check for uv
        try:
            subprocess.run(["uv", "--version"], 
                         capture_output=True, check=True)
            tools['uv'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['uv'] = False
        
        # Check for pyenv
        try:
            subprocess.run(["pyenv", "--version"], 
                         capture_output=True, check=True)
            tools['pyenv'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools['pyenv'] = False
        
        return tools
    
    def list_tools(self):
        """List available virtual environment tools."""
        print("Available Virtual Environment Tools:")
        print("=" * 40)
        
        for tool, available in self.available_tools.items():
            status = "✅ Available" if available else "❌ Not installed"
            print(f"{tool:12} {status}")
        
        if not any(self.available_tools.values()):
            print("\n⚠️  No virtual environment tools found!")
            print("Please install at least one: venv (built-in), virtualenv, or uv")
    
    def create_environment(self, name: str, tool: str = "auto", 
                         python_version: Optional[str] = None):
        """Create a virtual environment using the specified tool."""
        
        if tool == "auto":
            # Choose the best available tool
            if self.available_tools.get('uv'):
                tool = 'uv'
            elif self.available_tools.get('virtualenv'):
                tool = 'virtualenv'
            elif self.available_tools.get('venv'):
                tool = 'venv'
            else:
                print("❌ No virtual environment tools available!")
                return False
        
        if not self.available_tools.get(tool):
            print(f"❌ {tool} is not available!")
            return False
        
        print(f"🏗️  Creating virtual environment '{name}' using {tool}...")
        
        try:
            if tool == 'venv':
                cmd = [sys.executable, "-m", "venv", name]
                if python_version:
                    print("⚠️  venv doesn't support specifying Python version directly")
            
            elif tool == 'virtualenv':
                cmd = ["virtualenv", name]
                if python_version:
                    cmd.extend(["-p", f"python{python_version}"])
            
            elif tool == 'uv':
                cmd = ["uv", "venv", name]
                if python_version:
                    cmd.extend(["--python", python_version])
            
            subprocess.run(cmd, check=True)
            print(f"✅ Virtual environment '{name}' created successfully!")
            
            # Show activation instructions
            self._show_activation_instructions(name)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def _show_activation_instructions(self, name: str):
        """Show how to activate the virtual environment."""
        print(f"\n📋 To activate the virtual environment:")
        
        if os.name == 'nt':  # Windows
            print(f"   {name}\\Scripts\\activate")
        else:  # Unix-like
            print(f"   source {name}/bin/activate")
        
        print(f"\n📋 To deactivate:")
        print(f"   deactivate")
    
    def list_environments(self, directory: str = "."):
        """List virtual environments in the specified directory."""
        path = Path(directory)
        envs = []
        
        # Common virtual environment directory names
        env_names = ['venv', 'env', '.venv', '.env']
        
        # Look for environments
        for item in path.iterdir():
            if item.is_dir():
                # Check if it's a virtual environment
                if item.name in env_names or self._is_virtual_env(item):
                    envs.append(item)
        
        if envs:
            print(f"Virtual environments in {directory}:")
            print("=" * 40)
            for env in envs:
                python_exe = self._get_python_executable(env)
                if python_exe and python_exe.exists():
                    version = self._get_python_version(python_exe)
                    print(f"📁 {env.name:15} Python {version}")
                else:
                    print(f"📁 {env.name:15} (inactive/broken)")
        else:
            print(f"No virtual environments found in {directory}")
    
    def _is_virtual_env(self, path: Path) -> bool:
        """Check if a directory is a virtual environment."""
        # Check for common virtual environment indicators
        indicators = [
            path / "bin" / "activate",      # Unix
            path / "Scripts" / "activate",  # Windows
            path / "pyvenv.cfg"            # Both
        ]
        return any(indicator.exists() for indicator in indicators)
    
    def _get_python_executable(self, env_path: Path) -> Optional[Path]:
        """Get the Python executable path for a virtual environment."""
        candidates = [
            env_path / "bin" / "python",        # Unix
            env_path / "Scripts" / "python.exe" # Windows
        ]
        
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None
    
    def _get_python_version(self, python_exe: Path) -> str:
        """Get Python version from executable."""
        try:
            result = subprocess.run([str(python_exe), "--version"], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip().split()[1]
        except (subprocess.CalledProcessError, IndexError):
            return "unknown"
    
    def install_requirements(self, env_name: str, requirements_file: str):
        """Install requirements in a virtual environment."""
        env_path = Path(env_name)
        python_exe = self._get_python_executable(env_path)
        
        if not python_exe:
            print(f"❌ Virtual environment '{env_name}' not found or inactive")
            return False
        
        if not Path(requirements_file).exists():
            print(f"❌ Requirements file '{requirements_file}' not found")
            return False
        
        print(f"📦 Installing requirements from {requirements_file}...")
        
        try:
            subprocess.run([str(python_exe), "-m", "pip", "install", 
                          "-r", requirements_file], check=True)
            print("✅ Requirements installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            return False

def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description="Virtual Environment Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List tools command
    subparsers.add_parser('list-tools', help='List available virtual environment tools')
    
    # Create environment command
    create_parser = subparsers.add_parser('create', help='Create a virtual environment')
    create_parser.add_argument('name', help='Environment name')
    create_parser.add_argument('--tool', choices=['auto', 'venv', 'virtualenv', 'uv'], 
                              default='auto', help='Tool to use')
    create_parser.add_argument('--python', help='Python version (e.g., 3.9, 3.11)')
    
    # List environments command
    list_parser = subparsers.add_parser('list', help='List virtual environments')
    list_parser.add_argument('--directory', '-d', default='.', 
                           help='Directory to search (default: current)')
    
    # Install requirements command
    install_parser = subparsers.add_parser('install', help='Install requirements')
    install_parser.add_argument('env_name', help='Environment name')
    install_parser.add_argument('requirements_file', help='Requirements file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = VirtualEnvManager()
    
    if args.command == 'list-tools':
        manager.list_tools()
    
    elif args.command == 'create':
        manager.create_environment(args.name, args.tool, args.python)
    
    elif args.command == 'list':
        manager.list_environments(args.directory)
    
    elif args.command == 'install':
        manager.install_requirements(args.env_name, args.requirements_file)

if __name__ == "__main__":
    main()