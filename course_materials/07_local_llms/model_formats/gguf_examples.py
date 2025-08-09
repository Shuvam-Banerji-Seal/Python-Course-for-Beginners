#!/usr/bin/env python3
"""
GGUF Format Usage Examples

This script demonstrates practical usage of GGUF format models including:
- Loading and inspecting GGUF models
- Working with quantized models
- Memory-efficient inference
- Model metadata extraction

Requirements:
    pip install llama-cpp-python numpy

Note: This script assumes you have GGUF models available locally.
You can download them from Hugging Face Hub or convert existing models.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from llama_cpp import Llama, LlamaGrammar
    import numpy as np
except ImportError:
    print("Required packages not installed. Run:")
    print("pip install llama-cpp-python numpy")
    sys.exit(1)


class GGUFModelManager:
    """
    A utility class for managing GGUF models with llama-cpp-python.
    Provides methods for loading, inspecting, and using GGUF models efficiently.
    """
    
    def __init__(self, model_path: str, **kwargs):
        """
        Initialize the GGUF model manager.
        
        Args:
            model_path: Path to the GGUF model file
            **kwargs: Additional arguments for Llama initialization
        """
        self.model_path = Path(model_path)
        self.model = None
        self.model_info = {}
        self.default_params = {
            'n_ctx': 2048,          # Context window size
            'n_batch': 512,         # Batch size for processing
            'n_threads': None,      # Number of threads (auto-detect)
            'n_gpu_layers': 0,      # Number of layers to offload to GPU
            'verbose': False,       # Reduce output verbosity
            'use_mmap': True,       # Use memory mapping for efficiency
            'use_mlock': False,     # Lock memory pages
        }
        self.default_params.update(kwargs)
    
    def load_model(self) -> bool:
        """
        Load the GGUF model with error handling and performance monitoring.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if not self.model_path.exists():
            print(f"Error: Model file not found: {self.model_path}")
            return False
        
        print(f"Loading GGUF model: {self.model_path.name}")
        print(f"File size: {self.model_path.stat().st_size / (1024**3):.2f} GB")
        
        start_time = time.time()
        
        try:
            self.model = Llama(
                model_path=str(self.model_path),
                **self.default_params
            )
            
            load_time = time.time() - start_time
            print(f"Model loaded successfully in {load_time:.2f} seconds")
            
            # Extract model information
            self._extract_model_info()
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def _extract_model_info(self):
        """Extract and store model metadata information."""
        if not self.model:
            return
        
        # Basic model information
        self.model_info = {
            'file_path': str(self.model_path),
            'file_size_gb': self.model_path.stat().st_size / (1024**3),
            'context_size': self.default_params['n_ctx'],
            'batch_size': self.default_params['n_batch'],
            'gpu_layers': self.default_params['n_gpu_layers'],
        }
        
        # Try to get additional metadata if available
        try:
            # Note: llama-cpp-python doesn't expose all GGUF metadata directly
            # This is a placeholder for when such functionality becomes available
            self.model_info['loaded_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
    
    def generate_text(self, 
                     prompt: str, 
                     max_tokens: int = 100,
                     temperature: float = 0.7,
                     top_p: float = 0.9,
                     top_k: int = 40,
                     repeat_penalty: float = 1.1,
                     stop: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate text using the loaded GGUF model.
        
        Args:
            prompt: Input text prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            repeat_penalty: Repetition penalty
            stop: List of stop sequences
            
        Returns:
            Dict containing generated text and metadata
        """
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        start_time = time.time()
        
        # Generate text
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repeat_penalty=repeat_penalty,
            stop=stop or [],
            echo=False  # Don't include prompt in output
        )
        
        generation_time = time.time() - start_time
        
        # Calculate performance metrics
        generated_text = output['choices'][0]['text']
        token_count = len(self.model.tokenize(generated_text.encode('utf-8')))
        tokens_per_second = token_count / generation_time if generation_time > 0 else 0
        
        return {
            'generated_text': generated_text,
            'prompt': prompt,
            'token_count': token_count,
            'generation_time': generation_time,
            'tokens_per_second': tokens_per_second,
            'parameters': {
                'max_tokens': max_tokens,
                'temperature': temperature,
                'top_p': top_p,
                'top_k': top_k,
                'repeat_penalty': repeat_penalty
            }
        }
    
    def benchmark_performance(self, test_prompts: List[str]) -> Dict[str, Any]:
        """
        Benchmark model performance with multiple test prompts.
        
        Args:
            test_prompts: List of prompts to test
            
        Returns:
            Dict containing benchmark results
        """
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        results = []
        total_time = 0
        total_tokens = 0
        
        print(f"Running benchmark with {len(test_prompts)} prompts...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"Processing prompt {i}/{len(test_prompts)}")
            
            result = self.generate_text(
                prompt=prompt,
                max_tokens=50,  # Shorter for benchmarking
                temperature=0.7
            )
            
            results.append(result)
            total_time += result['generation_time']
            total_tokens += result['token_count']
        
        avg_time = total_time / len(test_prompts)
        avg_tokens_per_second = total_tokens / total_time if total_time > 0 else 0
        
        return {
            'individual_results': results,
            'summary': {
                'total_prompts': len(test_prompts),
                'total_time': total_time,
                'total_tokens': total_tokens,
                'average_time_per_prompt': avg_time,
                'average_tokens_per_second': avg_tokens_per_second,
                'model_info': self.model_info
            }
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information."""
        return self.model_info.copy()
    
    def cleanup(self):
        """Clean up model resources."""
        if self.model:
            del self.model
            self.model = None
            print("Model resources cleaned up")


def demonstrate_gguf_loading():
    """Demonstrate basic GGUF model loading and inspection."""
    print("=== GGUF Model Loading Demo ===")
    
    # Example model paths (adjust these to your actual model locations)
    example_models = [
        "models/llama-2-7b-chat.Q4_0.gguf",
        "models/codellama-7b.Q5_0.gguf",
        "models/mistral-7b-instruct.Q8_0.gguf"
    ]
    
    # Find the first available model
    model_path = None
    for path in example_models:
        if Path(path).exists():
            model_path = path
            break
    
    if not model_path:
        print("No GGUF models found. Please download a model first.")
        print("Example: Download from Hugging Face Hub:")
        print("  huggingface-cli download microsoft/DialoGPT-medium --local-dir models/")
        return
    
    # Initialize model manager
    manager = GGUFModelManager(
        model_path=model_path,
        n_ctx=1024,      # Smaller context for demo
        n_gpu_layers=0,  # CPU only for compatibility
        verbose=False
    )
    
    # Load model
    if manager.load_model():
        # Display model information
        info = manager.get_model_info()
        print("\nModel Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Test generation
        test_prompt = "The future of artificial intelligence is"
        print(f"\nGenerating text for prompt: '{test_prompt}'")
        
        result = manager.generate_text(
            prompt=test_prompt,
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"\nGenerated text: {result['generated_text']}")
        print(f"Performance: {result['tokens_per_second']:.2f} tokens/second")
        
        # Cleanup
        manager.cleanup()


def demonstrate_quantization_comparison():
    """Compare different quantization levels if multiple models are available."""
    print("\n=== Quantization Comparison Demo ===")
    
    # Look for models with different quantization levels
    model_patterns = {
        'Q2_K': 'models/*Q2_K*.gguf',
        'Q4_0': 'models/*Q4_0*.gguf', 
        'Q5_0': 'models/*Q5_0*.gguf',
        'Q8_0': 'models/*Q8_0*.gguf'
    }
    
    available_models = {}
    for quant_type, pattern in model_patterns.items():
        import glob
        matches = glob.glob(pattern)
        if matches:
            available_models[quant_type] = matches[0]
    
    if len(available_models) < 2:
        print("Need at least 2 different quantization levels for comparison")
        print("Available models:", list(available_models.keys()))
        return
    
    test_prompt = "Explain quantum computing in simple terms:"
    results = {}
    
    for quant_type, model_path in available_models.items():
        print(f"\nTesting {quant_type} quantization...")
        
        manager = GGUFModelManager(
            model_path=model_path,
            n_ctx=512,
            verbose=False
        )
        
        if manager.load_model():
            result = manager.generate_text(
                prompt=test_prompt,
                max_tokens=100,
                temperature=0.7
            )
            
            results[quant_type] = {
                'file_size_gb': manager.get_model_info()['file_size_gb'],
                'tokens_per_second': result['tokens_per_second'],
                'generation_time': result['generation_time'],
                'generated_text': result['generated_text'][:100] + "..."
            }
            
            manager.cleanup()
    
    # Display comparison
    print("\n=== Quantization Comparison Results ===")
    print(f"{'Quantization':<12} {'Size (GB)':<10} {'Speed (t/s)':<12} {'Time (s)':<10}")
    print("-" * 50)
    
    for quant_type, data in results.items():
        print(f"{quant_type:<12} {data['file_size_gb']:<10.2f} "
              f"{data['tokens_per_second']:<12.2f} {data['generation_time']:<10.2f}")


def demonstrate_memory_efficient_usage():
    """Demonstrate memory-efficient GGUF usage patterns."""
    print("\n=== Memory-Efficient Usage Demo ===")
    
    # Find any available GGUF model
    import glob
    models = glob.glob("models/*.gguf")
    
    if not models:
        print("No GGUF models found for memory efficiency demo")
        return
    
    model_path = models[0]
    print(f"Using model: {Path(model_path).name}")
    
    # Memory-efficient configuration
    manager = GGUFModelManager(
        model_path=model_path,
        n_ctx=512,           # Smaller context window
        n_batch=128,         # Smaller batch size
        use_mmap=True,       # Enable memory mapping
        use_mlock=False,     # Don't lock memory pages
        n_gpu_layers=0,      # CPU only for predictable memory usage
        verbose=False
    )
    
    if not manager.load_model():
        return
    
    # Demonstrate batch processing with memory monitoring
    prompts = [
        "Write a haiku about programming:",
        "Explain recursion briefly:",
        "What is machine learning?",
        "Describe the scientific method:",
        "How do computers work?"
    ]
    
    print("Processing multiple prompts efficiently...")
    
    # Process prompts one by one to minimize memory usage
    for i, prompt in enumerate(prompts, 1):
        print(f"\nPrompt {i}: {prompt}")
        
        result = manager.generate_text(
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"Response: {result['generated_text'].strip()}")
        print(f"Speed: {result['tokens_per_second']:.2f} tokens/second")
    
    manager.cleanup()


def demonstrate_advanced_features():
    """Demonstrate advanced GGUF features like grammar-guided generation."""
    print("\n=== Advanced GGUF Features Demo ===")
    
    import glob
    models = glob.glob("models/*.gguf")
    
    if not models:
        print("No GGUF models found for advanced features demo")
        return
    
    model_path = models[0]
    
    # Load model with advanced configuration
    manager = GGUFModelManager(
        model_path=model_path,
        n_ctx=1024,
        verbose=False
    )
    
    if not manager.load_model():
        return
    
    # Demonstrate constrained generation with stop sequences
    print("1. Constrained generation with stop sequences:")
    
    result = manager.generate_text(
        prompt="List three benefits of renewable energy:\n1.",
        max_tokens=150,
        temperature=0.3,
        stop=["\n4.", "\n\n", "4."]  # Stop at fourth item or double newline
    )
    
    print(f"Generated list:\n1.{result['generated_text']}")
    
    # Demonstrate different temperature settings
    print("\n2. Temperature comparison:")
    
    base_prompt = "The most important invention in human history was"
    temperatures = [0.1, 0.5, 0.9]
    
    for temp in temperatures:
        result = manager.generate_text(
            prompt=base_prompt,
            max_tokens=30,
            temperature=temp
        )
        print(f"Temperature {temp}: {result['generated_text'].strip()}")
    
    manager.cleanup()


def main():
    """Main function demonstrating various GGUF usage patterns."""
    print("GGUF Format Usage Examples")
    print("=" * 50)
    
    # Check if models directory exists
    models_dir = Path("models")
    if not models_dir.exists():
        print("Creating models directory...")
        models_dir.mkdir(exist_ok=True)
        print("\nTo run these examples, download GGUF models to the 'models' directory.")
        print("Example commands:")
        print("  # Download from Hugging Face Hub")
        print("  huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF llama-2-7b-chat.Q4_0.gguf --local-dir models/")
        print("  # Or use wget/curl")
        print("  wget -P models/ https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf")
        return
    
    try:
        # Run demonstrations
        demonstrate_gguf_loading()
        demonstrate_quantization_comparison()
        demonstrate_memory_efficient_usage()
        demonstrate_advanced_features()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("GGUF examples completed!")
    print("\nKey takeaways:")
    print("- GGUF models offer excellent memory efficiency through quantization")
    print("- Memory mapping enables fast loading of large models")
    print("- Different quantization levels provide size/quality trade-offs")
    print("- Proper configuration is crucial for optimal performance")


if __name__ == "__main__":
    main()