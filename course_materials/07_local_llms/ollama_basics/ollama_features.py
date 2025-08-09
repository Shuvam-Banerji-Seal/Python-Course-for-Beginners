#!/usr/bin/env python3
"""
Ollama Features Demonstration

This script demonstrates various Ollama features and configurations including
different model parameters, prompt templates, and advanced usage patterns.

Requirements:
- Ollama installed and running
- requests library: pip install requests
"""

import json
import requests
import time
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime


class OllamaFeatureDemo:
    """Demonstrate various Ollama features and capabilities."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.default_model = "llama2:7b"
        
    def is_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available model names."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get('models', [])
            return [model.get('name', '') for model in models]
        except Exception:
            return []
    
    def generate_with_options(
        self,
        model: str,
        prompt: str,
        **options
    ) -> Dict[str, Any]:
        """Generate response with custom options."""
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def chat_with_options(
        self,
        model: str,
        messages: List[Dict],
        **options
    ) -> Dict[str, Any]:
        """Chat with custom options."""
        data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/chat", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def demo_temperature_effects():
    """Demonstrate how temperature affects response creativity."""
    print("🌡️  Temperature Effects Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]  # Use first available model
    prompt = "Write a creative opening line for a science fiction story."
    
    temperatures = [0.1, 0.5, 0.9, 1.3]
    
    print(f"Using model: {model}")
    print(f"Prompt: {prompt}\n")
    
    for temp in temperatures:
        print(f"🌡️  Temperature: {temp}")
        print("-" * 30)
        
        response = demo.generate_with_options(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_tokens=100
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')}")
            print(f"Tokens: {response.get('eval_count', 0)}")
            print(f"Time: {response.get('total_duration', 0) / 1e9:.2f}s")
        
        print()


def demo_context_length():
    """Demonstrate different context lengths."""
    print("📏 Context Length Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    
    # Create a long context
    long_context = """
    In a distant galaxy, there lived a wise old robot named Zephyr. Zephyr had been 
    exploring the cosmos for centuries, collecting stories from different worlds. 
    One day, Zephyr discovered a planet where music could heal any wound and where 
    the inhabitants communicated through colors instead of words. The planet was 
    called Chromia, and it was unlike anything Zephyr had ever seen before.
    
    The Chromians were peaceful beings who lived in harmony with their environment. 
    Their cities were built from crystalline structures that resonated with different 
    musical frequencies. Each building served as both shelter and instrument, creating 
    a symphony that could be heard across the entire planet.
    """
    
    context_sizes = [512, 1024, 2048]
    
    for ctx_size in context_sizes:
        print(f"📏 Context size: {ctx_size} tokens")
        print("-" * 30)
        
        response = demo.generate_with_options(
            model=model,
            prompt=f"{long_context}\n\nBased on this story, what do you think happens next?",
            num_ctx=ctx_size,
            max_tokens=150
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')[:200]}...")
            print(f"Context used: {response.get('prompt_eval_count', 0)} tokens")
        
        print()


def demo_top_k_top_p():
    """Demonstrate top-k and top-p sampling."""
    print("🎯 Top-K and Top-P Sampling Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    prompt = "The most interesting thing about artificial intelligence is"
    
    sampling_configs = [
        {"top_k": 10, "top_p": 0.9, "description": "Conservative (top_k=10, top_p=0.9)"},
        {"top_k": 40, "top_p": 0.95, "description": "Balanced (top_k=40, top_p=0.95)"},
        {"top_k": 100, "top_p": 1.0, "description": "Creative (top_k=100, top_p=1.0)"},
    ]
    
    print(f"Using model: {model}")
    print(f"Prompt: {prompt}\n")
    
    for config in sampling_configs:
        print(f"🎯 {config['description']}")
        print("-" * 40)
        
        response = demo.generate_with_options(
            model=model,
            prompt=prompt,
            top_k=config['top_k'],
            top_p=config['top_p'],
            temperature=0.7,
            max_tokens=100
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')}")
        
        print()


def demo_repeat_penalty():
    """Demonstrate repeat penalty effects."""
    print("🔄 Repeat Penalty Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    prompt = "List the benefits of exercise. The benefits of exercise include"
    
    penalties = [1.0, 1.1, 1.3]
    
    print(f"Using model: {model}")
    print(f"Prompt: {prompt}\n")
    
    for penalty in penalties:
        print(f"🔄 Repeat penalty: {penalty}")
        print("-" * 30)
        
        response = demo.generate_with_options(
            model=model,
            prompt=prompt,
            repeat_penalty=penalty,
            max_tokens=150
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')}")
        
        print()


def demo_system_prompts():
    """Demonstrate different system prompt configurations."""
    print("🎭 System Prompts Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    user_message = "Explain quantum computing"
    
    system_prompts = {
        "Teacher": "You are a patient teacher who explains complex topics in simple terms with examples.",
        "Scientist": "You are a research scientist who provides detailed, technical explanations.",
        "Storyteller": "You are a creative storyteller who explains concepts through engaging narratives.",
        "Comedian": "You are a comedian who explains things with humor and funny analogies."
    }
    
    print(f"Using model: {model}")
    print(f"User message: {user_message}\n")
    
    for role, system_prompt in system_prompts.items():
        print(f"🎭 Role: {role}")
        print(f"System: {system_prompt}")
        print("-" * 50)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = demo.chat_with_options(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            message = response.get('message', {})
            print(f"Response: {message.get('content', 'No response')}")
        
        print("\n" + "=" * 50 + "\n")


def demo_conversation_memory():
    """Demonstrate conversation memory and context."""
    print("🧠 Conversation Memory Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    
    # Build a conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant with a good memory."},
        {"role": "user", "content": "My name is Alice and I'm a software engineer."},
    ]
    
    print(f"Using model: {model}")
    print("Building conversation context...\n")
    
    # First exchange
    print("👤 User: My name is Alice and I'm a software engineer.")
    
    response = demo.chat_with_options(
        model=model,
        messages=messages,
        temperature=0.7
    )
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
        return
    
    assistant_msg = response.get('message', {}).get('content', '')
    print(f"🤖 Assistant: {assistant_msg}")
    
    messages.append({"role": "assistant", "content": assistant_msg})
    
    # Test memory
    follow_up_questions = [
        "What's my name?",
        "What do I do for work?",
        "Can you recommend a programming language for beginners?",
        "Remember what I told you about myself?"
    ]
    
    for question in follow_up_questions:
        print(f"\n👤 User: {question}")
        
        messages.append({"role": "user", "content": question})
        
        response = demo.chat_with_options(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
            continue
        
        assistant_msg = response.get('message', {}).get('content', '')
        print(f"🤖 Assistant: {assistant_msg}")
        
        messages.append({"role": "assistant", "content": assistant_msg})


def demo_model_comparison():
    """Compare different models on the same task."""
    print("⚖️  Model Comparison Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if len(models) < 2:
        print("❌ Need at least 2 models for comparison")
        print(f"Available models: {models}")
        return
    
    # Use first 3 models or all if less than 3
    test_models = models[:3]
    prompt = "Write a haiku about programming."
    
    print(f"Comparing models on task: {prompt}\n")
    
    for model in test_models:
        print(f"🤖 Model: {model}")
        print("-" * 30)
        
        start_time = time.time()
        
        response = demo.generate_with_options(
            model=model,
            prompt=prompt,
            temperature=0.7,
            max_tokens=100
        )
        
        end_time = time.time()
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')}")
            print(f"Tokens generated: {response.get('eval_count', 0)}")
            print(f"Time taken: {end_time - start_time:.2f}s")
            
            # Calculate tokens per second
            tokens = response.get('eval_count', 0)
            if tokens > 0 and end_time > start_time:
                tps = tokens / (end_time - start_time)
                print(f"Tokens/second: {tps:.1f}")
        
        print()


def demo_advanced_parameters():
    """Demonstrate advanced model parameters."""
    print("⚙️  Advanced Parameters Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    prompt = "Explain the concept of machine learning in simple terms."
    
    parameter_sets = [
        {
            "name": "Default",
            "params": {}
        },
        {
            "name": "Focused (Low temperature, high top_p)",
            "params": {
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 20
            }
        },
        {
            "name": "Creative (High temperature, diverse sampling)",
            "params": {
                "temperature": 1.0,
                "top_p": 0.9,
                "top_k": 100,
                "repeat_penalty": 1.1
            }
        },
        {
            "name": "Precise (Very low temperature)",
            "params": {
                "temperature": 0.1,
                "top_p": 0.8,
                "top_k": 10,
                "repeat_penalty": 1.05
            }
        }
    ]
    
    print(f"Using model: {model}")
    print(f"Prompt: {prompt}\n")
    
    for param_set in parameter_sets:
        print(f"⚙️  Configuration: {param_set['name']}")
        print(f"Parameters: {param_set['params']}")
        print("-" * 40)
        
        response = demo.generate_with_options(
            model=model,
            prompt=prompt,
            max_tokens=150,
            **param_set['params']
        )
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"Response: {response.get('response', 'No response')}")
            print(f"Generation time: {response.get('total_duration', 0) / 1e9:.2f}s")
        
        print("\n" + "=" * 50 + "\n")


def demo_streaming_vs_non_streaming():
    """Compare streaming vs non-streaming responses."""
    print("🌊 Streaming vs Non-Streaming Demo")
    print("=" * 50)
    
    demo = OllamaFeatureDemo()
    
    if not demo.is_running():
        print("❌ Ollama is not running")
        return
    
    models = demo.get_available_models()
    if not models:
        print("❌ No models available")
        return
    
    model = models[0]
    prompt = "Write a short story about a robot who learns to paint."
    
    print(f"Using model: {model}")
    print(f"Prompt: {prompt}\n")
    
    # Non-streaming
    print("📦 Non-streaming response:")
    print("-" * 30)
    
    start_time = time.time()
    response = demo.generate_with_options(
        model=model,
        prompt=prompt,
        max_tokens=200
    )
    end_time = time.time()
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        print(f"Response: {response.get('response', 'No response')}")
        print(f"Total time: {end_time - start_time:.2f}s")
        print(f"Time to first token: {end_time - start_time:.2f}s (all at once)")
    
    print("\n" + "=" * 50)
    
    # Streaming
    print("\n🌊 Streaming response:")
    print("-" * 30)
    
    try:
        data = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {"max_tokens": 200}
        }
        
        start_time = time.time()
        response = requests.post(f"{demo.base_url}/api/generate", json=data, stream=True)
        response.raise_for_status()
        
        first_token_time = None
        token_count = 0
        
        print("Response (streaming): ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                chunk_data = json.loads(line.decode('utf-8'))
                
                if 'response' in chunk_data:
                    chunk = chunk_data['response']
                    print(chunk, end='', flush=True)
                    
                    if first_token_time is None:
                        first_token_time = time.time()
                    
                    token_count += 1
                
                if chunk_data.get('done', False):
                    end_time = time.time()
                    print(f"\n\nTotal time: {end_time - start_time:.2f}s")
                    if first_token_time:
                        print(f"Time to first token: {first_token_time - start_time:.2f}s")
                        print(f"Streaming advantage: {(end_time - start_time) - (first_token_time - start_time):.2f}s")
                    break
                    
    except Exception as e:
        print(f"❌ Error with streaming: {e}")


def main():
    """Run all feature demonstrations."""
    print("🚀 Ollama Features Demonstration")
    print("=" * 60)
    
    demos = [
        ("Temperature Effects", demo_temperature_effects),
        ("Context Length", demo_context_length),
        ("Top-K and Top-P Sampling", demo_top_k_top_p),
        ("Repeat Penalty", demo_repeat_penalty),
        ("System Prompts", demo_system_prompts),
        ("Conversation Memory", demo_conversation_memory),
        ("Model Comparison", demo_model_comparison),
        ("Advanced Parameters", demo_advanced_parameters),
        ("Streaming vs Non-Streaming", demo_streaming_vs_non_streaming),
    ]
    
    print("Available demonstrations:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")
    
    print("\nOptions:")
    print("- Enter a number (1-9) to run a specific demo")
    print("- Enter 'all' to run all demos")
    print("- Enter 'quit' to exit")
    
    while True:
        try:
            choice = input("\nSelect demo: ").strip().lower()
            
            if choice == 'quit':
                print("👋 Goodbye!")
                break
            elif choice == 'all':
                for name, demo_func in demos:
                    print(f"\n{'='*60}")
                    print(f"Running: {name}")
                    print('='*60)
                    demo_func()
                    input("\nPress Enter to continue to next demo...")
                break
            elif choice.isdigit():
                demo_num = int(choice)
                if 1 <= demo_num <= len(demos):
                    name, demo_func = demos[demo_num - 1]
                    print(f"\n{'='*60}")
                    print(f"Running: {name}")
                    print('='*60)
                    demo_func()
                else:
                    print(f"❌ Invalid choice. Please enter 1-{len(demos)}")
            else:
                print("❌ Invalid input. Enter a number, 'all', or 'quit'")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()