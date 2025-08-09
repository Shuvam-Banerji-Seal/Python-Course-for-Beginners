#!/usr/bin/env python3
"""
Ollama Model Management Script

This script provides comprehensive model management functionality for Ollama,
including downloading, listing, removing, and organizing models.

Requirements:
- Ollama installed and running
- requests library: pip install requests
"""

import json
import requests
import time
import os
import sys
from typing import Dict, List, Optional, Generator
from datetime import datetime
import argparse


class OllamaModelManager:
    """Comprehensive model management for Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        
    def is_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_models(self) -> List[Dict]:
        """List all locally available models with detailed information."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Get detailed information about a specific model."""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error getting model info for {model_name}: {e}")
            return None
    
    def pull_model(self, model_name: str, show_progress: bool = True) -> bool:
        """Download a model with progress tracking."""
        print(f"📥 Pulling model: {model_name}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True
            )
            response.raise_for_status()
            
            total_size = 0
            downloaded = 0
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    
                    if show_progress:
                        status = data.get('status', '')
                        
                        if 'pulling' in status.lower():
                            if 'total' in data and 'completed' in data:
                                total_size = data['total']
                                downloaded = data['completed']
                                progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                                
                                # Format sizes
                                total_mb = total_size / (1024 * 1024)
                                downloaded_mb = downloaded / (1024 * 1024)
                                
                                print(f"\r📊 Progress: {progress:.1f}% "
                                      f"({downloaded_mb:.1f}MB / {total_mb:.1f}MB)", 
                                      end='', flush=True)
                        else:
                            print(f"\r📋 {status}", end='', flush=True)
                    
                    if data.get('status') == 'success':
                        print(f"\n✅ Successfully pulled {model_name}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"\n❌ Error pulling model {model_name}: {e}")
            return False
    
    def remove_model(self, model_name: str) -> bool:
        """Remove a model from local storage."""
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name}
            )
            response.raise_for_status()
            print(f"✅ Successfully removed {model_name}")
            return True
        except Exception as e:
            print(f"❌ Error removing model {model_name}: {e}")
            return False
    
    def copy_model(self, source: str, destination: str) -> bool:
        """Copy a model to a new name."""
        try:
            response = requests.post(
                f"{self.base_url}/api/copy",
                json={"source": source, "destination": destination}
            )
            response.raise_for_status()
            print(f"✅ Successfully copied {source} to {destination}")
            return True
        except Exception as e:
            print(f"❌ Error copying model: {e}")
            return False
    
    def create_model(self, name: str, modelfile_content: str) -> bool:
        """Create a custom model from a Modelfile."""
        try:
            response = requests.post(
                f"{self.base_url}/api/create",
                json={"name": name, "modelfile": modelfile_content},
                stream=True
            )
            response.raise_for_status()
            
            print(f"🔨 Creating model: {name}")
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    status = data.get('status', '')
                    if status:
                        print(f"📋 {status}")
                    
                    if data.get('status') == 'success':
                        print(f"✅ Successfully created {name}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error creating model {name}: {e}")
            return False
    
    def get_running_models(self) -> List[Dict]:
        """Get list of currently running models."""
        try:
            response = requests.get(f"{self.base_url}/api/ps")
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            print(f"❌ Error getting running models: {e}")
            return []


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}PB"


def format_duration(nanoseconds: int) -> str:
    """Format duration from nanoseconds to human readable format."""
    seconds = nanoseconds / 1e9
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def display_models_table(models: List[Dict]):
    """Display models in a formatted table."""
    if not models:
        print("📭 No models found")
        return
    
    print(f"\n📦 Found {len(models)} model(s):")
    print("-" * 80)
    print(f"{'Name':<25} {'Size':<10} {'Modified':<20} {'Family':<15}")
    print("-" * 80)
    
    for model in models:
        name = model.get('name', 'unknown')
        size = format_size(model.get('size', 0))
        
        # Format modified time
        modified_at = model.get('modified_at', '')
        if modified_at:
            try:
                dt = datetime.fromisoformat(modified_at.replace('Z', '+00:00'))
                modified = dt.strftime('%Y-%m-%d %H:%M')
            except:
                modified = modified_at[:16]
        else:
            modified = 'unknown'
        
        # Get model family from details
        details = model.get('details', {})
        family = details.get('family', 'unknown')
        
        print(f"{name:<25} {size:<10} {modified:<20} {family:<15}")


def display_model_details(model_info: Dict):
    """Display detailed information about a model."""
    print(f"\n🔍 Model Details:")
    print("-" * 50)
    
    # Basic info
    print(f"Name: {model_info.get('name', 'unknown')}")
    print(f"Size: {format_size(model_info.get('size', 0))}")
    
    # Model details
    details = model_info.get('details', {})
    if details:
        print(f"Family: {details.get('family', 'unknown')}")
        print(f"Format: {details.get('format', 'unknown')}")
        print(f"Parameter Size: {details.get('parameter_size', 'unknown')}")
        print(f"Quantization Level: {details.get('quantization_level', 'unknown')}")
    
    # Template info
    template = model_info.get('template', '')
    if template:
        print(f"Template: {template[:100]}{'...' if len(template) > 100 else ''}")
    
    # Parameters
    parameters = model_info.get('parameters', {})
    if parameters:
        print("\nParameters:")
        for key, value in parameters.items():
            print(f"  {key}: {value}")
    
    # Modelfile
    modelfile = model_info.get('modelfile', '')
    if modelfile:
        print(f"\nModelfile:\n{modelfile}")


def display_running_models(running_models: List[Dict]):
    """Display currently running models."""
    if not running_models:
        print("💤 No models currently running")
        return
    
    print(f"\n🏃 Running Models ({len(running_models)}):")
    print("-" * 60)
    print(f"{'Name':<25} {'Size':<10} {'Until':<25}")
    print("-" * 60)
    
    for model in running_models:
        name = model.get('name', 'unknown')
        size = format_size(model.get('size', 0))
        expires_at = model.get('expires_at', '')
        
        if expires_at:
            try:
                dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                until = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                until = expires_at
        else:
            until = 'unknown'
        
        print(f"{name:<25} {size:<10} {until:<25}")


def recommend_models():
    """Recommend popular models for different use cases."""
    recommendations = {
        "Beginner-friendly (Small)": [
            {"name": "llama2:7b", "size": "3.8GB", "description": "Good general-purpose model"},
            {"name": "mistral:7b", "size": "4.1GB", "description": "Fast and efficient"},
            {"name": "phi:2.7b", "size": "1.7GB", "description": "Very small, good for testing"},
        ],
        "Code-focused": [
            {"name": "codellama:7b", "size": "3.8GB", "description": "Code generation and analysis"},
            {"name": "codellama:13b", "size": "7.3GB", "description": "Better code understanding"},
            {"name": "deepseek-coder:6.7b", "size": "3.8GB", "description": "Specialized for coding"},
        ],
        "High Performance (Large)": [
            {"name": "llama2:13b", "size": "7.3GB", "description": "Better reasoning"},
            {"name": "llama2:70b", "size": "39GB", "description": "Best quality (requires lots of RAM)"},
            {"name": "mixtral:8x7b", "size": "26GB", "description": "Mixture of experts model"},
        ],
        "Specialized": [
            {"name": "llava:7b", "size": "4.7GB", "description": "Vision + language model"},
            {"name": "neural-chat:7b", "size": "4.1GB", "description": "Optimized for conversations"},
            {"name": "orca-mini:3b", "size": "1.9GB", "description": "Small but capable"},
        ]
    }
    
    print("\n🎯 Model Recommendations:")
    print("=" * 60)
    
    for category, models in recommendations.items():
        print(f"\n📂 {category}:")
        for model in models:
            print(f"  • {model['name']:<20} ({model['size']:<6}) - {model['description']}")
    
    print(f"\n💡 Tips:")
    print("  • Start with 7B models for good balance of performance and resource usage")
    print("  • Use quantized models (Q4_0, Q8_0) for faster inference")
    print("  • Check available RAM before downloading large models")
    print("  • Specialized models work better for specific tasks")


def interactive_model_manager():
    """Interactive model management interface."""
    manager = OllamaModelManager()
    
    if not manager.is_running():
        print("❌ Ollama is not running. Please start Ollama first.")
        return
    
    while True:
        print("\n" + "=" * 50)
        print("🛠️  Ollama Model Manager")
        print("=" * 50)
        print("1. List models")
        print("2. Pull model")
        print("3. Remove model")
        print("4. Model details")
        print("5. Running models")
        print("6. Copy model")
        print("7. Model recommendations")
        print("8. Create custom model")
        print("9. Exit")
        
        try:
            choice = input("\nSelect option (1-9): ").strip()
            
            if choice == '1':
                models = manager.list_models()
                display_models_table(models)
                
            elif choice == '2':
                model_name = input("Enter model name to pull: ").strip()
                if model_name:
                    manager.pull_model(model_name)
                
            elif choice == '3':
                models = manager.list_models()
                if models:
                    display_models_table(models)
                    model_name = input("\nEnter model name to remove: ").strip()
                    if model_name:
                        confirm = input(f"Are you sure you want to remove {model_name}? (y/N): ")
                        if confirm.lower() in ['y', 'yes']:
                            manager.remove_model(model_name)
                else:
                    print("No models available to remove")
                
            elif choice == '4':
                models = manager.list_models()
                if models:
                    display_models_table(models)
                    model_name = input("\nEnter model name for details: ").strip()
                    if model_name:
                        info = manager.get_model_info(model_name)
                        if info:
                            display_model_details(info)
                else:
                    print("No models available")
                
            elif choice == '5':
                running = manager.get_running_models()
                display_running_models(running)
                
            elif choice == '6':
                models = manager.list_models()
                if models:
                    display_models_table(models)
                    source = input("\nEnter source model name: ").strip()
                    destination = input("Enter destination model name: ").strip()
                    if source and destination:
                        manager.copy_model(source, destination)
                else:
                    print("No models available to copy")
                
            elif choice == '7':
                recommend_models()
                
            elif choice == '8':
                name = input("Enter new model name: ").strip()
                print("Enter Modelfile content (press Ctrl+D when done):")
                try:
                    modelfile_lines = []
                    while True:
                        line = input()
                        modelfile_lines.append(line)
                except EOFError:
                    modelfile_content = '\n'.join(modelfile_lines)
                    if name and modelfile_content.strip():
                        manager.create_model(name, modelfile_content)
                
            elif choice == '9':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please select 1-9.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Ollama Model Management Tool")
    parser.add_argument('--list', action='store_true', help='List all models')
    parser.add_argument('--pull', type=str, help='Pull a model')
    parser.add_argument('--remove', type=str, help='Remove a model')
    parser.add_argument('--info', type=str, help='Show model information')
    parser.add_argument('--running', action='store_true', help='Show running models')
    parser.add_argument('--recommend', action='store_true', help='Show model recommendations')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    
    args = parser.parse_args()
    
    manager = OllamaModelManager()
    
    if not manager.is_running():
        print("❌ Ollama is not running. Please start Ollama first.")
        print("Run: ollama serve")
        return
    
    if args.list:
        models = manager.list_models()
        display_models_table(models)
        
    elif args.pull:
        manager.pull_model(args.pull)
        
    elif args.remove:
        confirm = input(f"Are you sure you want to remove {args.remove}? (y/N): ")
        if confirm.lower() in ['y', 'yes']:
            manager.remove_model(args.remove)
        
    elif args.info:
        info = manager.get_model_info(args.info)
        if info:
            display_model_details(info)
            
    elif args.running:
        running = manager.get_running_models()
        display_running_models(running)
        
    elif args.recommend:
        recommend_models()
        
    elif args.interactive or len(sys.argv) == 1:
        interactive_model_manager()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()