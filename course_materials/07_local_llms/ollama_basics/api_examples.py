#!/usr/bin/env python3
"""
Ollama API Examples

This script demonstrates various ways to interact with Ollama using both
the REST API and Python client library approaches.

Requirements:
- Ollama installed and running (see installation_guide.md)
- requests library: pip install requests
- ollama library: pip install ollama
"""

import json
import requests
import time
from typing import Dict, List, Optional, Generator
import sys

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2:7b"


class OllamaAPIClient:
    """Simple Ollama API client using requests library."""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip('/')
        
    def is_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_version(self) -> Dict:
        """Get Ollama version information."""
        response = requests.get(f"{self.base_url}/api/version")
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> List[Dict]:
        """List all available models."""
        response = requests.get(f"{self.base_url}/api/tags")
        response.raise_for_status()
        return response.json().get('models', [])
    
    def pull_model(self, model_name: str) -> Generator[Dict, None, None]:
        """Pull a model from the registry with progress updates."""
        data = {"name": model_name}
        response = requests.post(
            f"{self.base_url}/api/pull",
            json=data,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                yield json.loads(line.decode('utf-8'))
    
    def generate_response(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """Generate a response using the specified model."""
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        if system:
            data["system"] = system
        
        response = requests.post(f"{self.base_url}/api/generate", json=data)
        response.raise_for_status()
        
        if stream:
            return response  # Return response object for streaming
        else:
            return response.json()
    
    def chat(
        self,
        model: str,
        messages: List[Dict],
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """Chat with the model using conversation format."""
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        response = requests.post(f"{self.base_url}/api/chat", json=data)
        response.raise_for_status()
        
        if stream:
            return response  # Return response object for streaming
        else:
            return response.json()


def example_basic_usage():
    """Demonstrate basic Ollama API usage."""
    print("=== Basic Ollama API Usage ===")
    
    client = OllamaAPIClient()
    
    # Check if Ollama is running
    if not client.is_running():
        print("❌ Ollama is not running. Please start Ollama first.")
        print("Run: ollama serve")
        return
    
    print("✅ Ollama is running")
    
    # Get version info
    try:
        version_info = client.get_version()
        print(f"📋 Ollama version: {version_info.get('version', 'unknown')}")
    except Exception as e:
        print(f"❌ Error getting version: {e}")
        return
    
    # List available models
    try:
        models = client.list_models()
        print(f"📦 Available models: {len(models)}")
        for model in models[:3]:  # Show first 3 models
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"  - {name} ({size:.1f}GB)")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return
    
    # Check if default model is available
    model_names = [m.get('name', '') for m in models]
    if DEFAULT_MODEL not in model_names:
        print(f"⚠️  Default model '{DEFAULT_MODEL}' not found.")
        print("Available models:", [m.get('name') for m in models[:3]])
        if models:
            DEFAULT_MODEL = models[0].get('name')
            print(f"Using '{DEFAULT_MODEL}' instead.")
        else:
            print("No models available. Please pull a model first:")
            print("ollama pull llama2:7b")
            return
    
    # Generate a simple response
    try:
        print(f"\n🤖 Generating response with {DEFAULT_MODEL}...")
        response = client.generate_response(
            model=DEFAULT_MODEL,
            prompt="Hello! Can you tell me a short joke?",
            stream=False
        )
        
        print("Response:")
        print(response.get('response', 'No response received'))
        print(f"⏱️  Generation time: {response.get('total_duration', 0) / 1e9:.2f}s")
        
    except Exception as e:
        print(f"❌ Error generating response: {e}")


def example_streaming_response():
    """Demonstrate streaming response generation."""
    print("\n=== Streaming Response Example ===")
    
    client = OllamaAPIClient()
    
    if not client.is_running():
        print("❌ Ollama is not running.")
        return
    
    try:
        print("🤖 Generating streaming response...")
        response = client.generate_response(
            model=DEFAULT_MODEL,
            prompt="Write a short story about a robot learning to paint.",
            stream=True
        )
        
        print("Response (streaming):")
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if 'response' in data:
                    chunk = data['response']
                    print(chunk, end='', flush=True)
                    full_response += chunk
                
                if data.get('done', False):
                    print(f"\n\n⏱️  Total time: {data.get('total_duration', 0) / 1e9:.2f}s")
                    break
                    
    except Exception as e:
        print(f"❌ Error with streaming: {e}")


def example_chat_conversation():
    """Demonstrate chat-style conversation."""
    print("\n=== Chat Conversation Example ===")
    
    client = OllamaAPIClient()
    
    if not client.is_running():
        print("❌ Ollama is not running.")
        return
    
    # Conversation history
    messages = [
        {"role": "system", "content": "You are a helpful programming tutor."},
        {"role": "user", "content": "What is Python?"}
    ]
    
    try:
        print("🤖 Starting chat conversation...")
        response = client.chat(
            model=DEFAULT_MODEL,
            messages=messages
        )
        
        assistant_message = response.get('message', {}).get('content', '')
        print("Assistant:", assistant_message)
        
        # Continue conversation
        messages.append({"role": "assistant", "content": assistant_message})
        messages.append({"role": "user", "content": "Can you give me a simple Python example?"})
        
        print("\n🤖 Continuing conversation...")
        response = client.chat(
            model=DEFAULT_MODEL,
            messages=messages
        )
        
        print("Assistant:", response.get('message', {}).get('content', ''))
        
    except Exception as e:
        print(f"❌ Error in chat: {e}")


def example_system_prompts():
    """Demonstrate different system prompts."""
    print("\n=== System Prompts Example ===")
    
    client = OllamaAPIClient()
    
    if not client.is_running():
        print("❌ Ollama is not running.")
        return
    
    system_prompts = {
        "helpful_assistant": "You are a helpful, harmless, and honest assistant.",
        "creative_writer": "You are a creative writer who loves crafting imaginative stories.",
        "code_reviewer": "You are an expert code reviewer who provides constructive feedback.",
        "teacher": "You are a patient teacher who explains concepts clearly and simply."
    }
    
    user_prompt = "Explain what machine learning is."
    
    for role, system_prompt in system_prompts.items():
        print(f"\n🎭 Role: {role.replace('_', ' ').title()}")
        print(f"System: {system_prompt}")
        
        try:
            response = client.generate_response(
                model=DEFAULT_MODEL,
                prompt=user_prompt,
                system=system_prompt
            )
            
            print("Response:", response.get('response', '')[:200] + "...")
            
        except Exception as e:
            print(f"❌ Error: {e}")


def example_model_parameters():
    """Demonstrate different model parameters."""
    print("\n=== Model Parameters Example ===")
    
    client = OllamaAPIClient()
    
    if not client.is_running():
        print("❌ Ollama is not running.")
        return
    
    prompt = "Complete this sentence: The future of AI is"
    
    parameters = [
        {"temperature": 0.1, "description": "Very focused/deterministic"},
        {"temperature": 0.7, "description": "Balanced creativity"},
        {"temperature": 1.2, "description": "Very creative/random"},
    ]
    
    for params in parameters:
        temp = params["temperature"]
        desc = params["description"]
        
        print(f"\n🌡️  Temperature: {temp} ({desc})")
        
        try:
            response = client.generate_response(
                model=DEFAULT_MODEL,
                prompt=prompt,
                temperature=temp,
                max_tokens=50
            )
            
            print("Response:", response.get('response', ''))
            
        except Exception as e:
            print(f"❌ Error: {e}")


def example_using_ollama_library():
    """Demonstrate using the official ollama Python library."""
    print("\n=== Using Official Ollama Library ===")
    
    try:
        import ollama
        
        # List models
        models = ollama.list()
        print(f"📦 Models available: {len(models.get('models', []))}")
        
        # Generate response
        response = ollama.generate(
            model=DEFAULT_MODEL,
            prompt="What are the benefits of using local LLMs?"
        )
        
        print("Response using ollama library:")
        print(response.get('response', ''))
        
        # Chat example
        messages = [
            {"role": "user", "content": "Why is Python popular for AI?"}
        ]
        
        chat_response = ollama.chat(
            model=DEFAULT_MODEL,
            messages=messages
        )
        
        print("\nChat response:")
        print(chat_response.get('message', {}).get('content', ''))
        
    except ImportError:
        print("⚠️  ollama library not installed. Install with: pip install ollama")
    except Exception as e:
        print(f"❌ Error using ollama library: {e}")


def example_error_handling():
    """Demonstrate proper error handling."""
    print("\n=== Error Handling Examples ===")
    
    client = OllamaAPIClient()
    
    # Test with non-existent model
    print("🧪 Testing with non-existent model...")
    try:
        response = client.generate_response(
            model="nonexistent-model",
            prompt="Hello"
        )
    except requests.exceptions.HTTPError as e:
        print(f"✅ Caught HTTP error as expected: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test with invalid URL
    print("\n🧪 Testing with invalid URL...")
    invalid_client = OllamaAPIClient("http://localhost:99999")
    try:
        response = invalid_client.generate_response(
            model=DEFAULT_MODEL,
            prompt="Hello"
        )
    except requests.exceptions.ConnectionError as e:
        print("✅ Caught connection error as expected")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def interactive_chat():
    """Interactive chat session with Ollama."""
    print("\n=== Interactive Chat Session ===")
    print("Type 'quit' to exit, 'clear' to clear history")
    
    client = OllamaAPIClient()
    
    if not client.is_running():
        print("❌ Ollama is not running.")
        return
    
    messages = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                messages = []
                print("🧹 Chat history cleared")
                continue
            elif not user_input:
                continue
            
            messages.append({"role": "user", "content": user_input})
            
            print("🤖 Assistant: ", end="", flush=True)
            
            response = client.chat(
                model=DEFAULT_MODEL,
                messages=messages,
                stream=True
            )
            
            assistant_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if 'message' in data and 'content' in data['message']:
                        chunk = data['message']['content']
                        print(chunk, end='', flush=True)
                        assistant_response += chunk
                    
                    if data.get('done', False):
                        print()  # New line after response
                        break
            
            messages.append({"role": "assistant", "content": assistant_response})
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """Run all examples."""
    print("🚀 Ollama API Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_streaming_response()
    example_chat_conversation()
    example_system_prompts()
    example_model_parameters()
    example_using_ollama_library()
    example_error_handling()
    
    # Ask if user wants interactive chat
    try:
        choice = input("\n🤔 Would you like to try interactive chat? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_chat()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()