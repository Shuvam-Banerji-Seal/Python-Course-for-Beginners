#!/usr/bin/env python3
"""
Basic project example demonstrating virtual environment usage.
"""

import sys
import os
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def show_environment_info():
    """Display information about the current Python environment."""
    
    table = Table(title="Python Environment Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    # Python version and executable
    table.add_row("Python Version", sys.version.split()[0])
    table.add_row("Python Executable", sys.executable)
    
    # Virtual environment
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        table.add_row("Virtual Environment", venv_path)
    else:
        table.add_row("Virtual Environment", "Not activated")
    
    # Package locations (first few)
    table.add_row("Python Path (first 3)", "\n".join(sys.path[:3]))
    
    console.print(table)

def test_requests():
    """Test that requests library works."""
    try:
        response = requests.get("https://httpbin.org/json", timeout=5)
        if response.status_code == 200:
            console.print("✅ Requests library working correctly", style="green")
            return True
        else:
            console.print(f"❌ HTTP request failed: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Requests library error: {e}", style="red")
        return False

def main():
    """Main function."""
    console.print("🐍 Basic Python Project Example", style="bold blue")
    console.print()
    
    show_environment_info()
    console.print()
    
    console.print("Testing installed packages...", style="yellow")
    test_requests()
    
    console.print()
    console.print("✨ Project running successfully!", style="bold green")

if __name__ == "__main__":
    main()