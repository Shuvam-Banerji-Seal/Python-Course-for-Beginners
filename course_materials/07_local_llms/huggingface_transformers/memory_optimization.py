#!/usr/bin/env python3
"""
Hugging Face Transformers - Memory Optimization Techniques

This script demonstrates various techniques for optimizing memory usage
when working with large language models using Hugging Face Transformers.

Requirements: 2.2, 2.4
"""

import torch
import psutil
import gc
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    BitsAndBytesConfig, pipeline
)
from typing import Dict, Any, Optional
import warnings
warnings.filterwarnings("ignore")


class MemoryMonitor:
    """Utility class for monitoring memory usage"""
    
    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        """Get current memory usage information"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        info = {
            'ram_used_gb': memory_info.rss / (1024**3),
            'ram_available_gb': psutil.virtual_memory().available / (1024**3),
            'ram_percent': psutil.virtual_memory().percent
        }
        
        if torch.cuda.is_available():
            info['gpu_allocated_gb'] = torch.cuda.memory_allocated() / (1024**3)
            info['gpu_reserved_gb'] = torch.cuda.memory_reserved() / (1024**3)
            info['gpu_total_gb'] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        
        return info
    
    @staticmethod
    def print_memory_usage(label: str = ""):
        """Print current memory usage"""
        info = MemoryMonitor.get_memory_info()
        print(f"\n--- Memory Usage {label} ---")
        print(f"RAM Used: {info['ram_used_gb']:.2f} GB ({info['ram_percent']:.1f}%)")
        print(f"RAM Available: {info['ram_available_gb']:.2f} GB")
        
        if torch.cuda.is_available():
            print(f"GPU Allocated: {info['gpu_allocated_gb']:.2f} GB")
            print(f"GPU Reserved: {info['gpu_reserved_gb']:.2f} GB")
            print(f"GPU Total: {info['gpu_total_gb']:.2f} GB")
    
    @staticmethod
    def clear_memory():
        """Clear memory caches"""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


class OptimizedTransformersManager:
    """
    Enhanced TransformersManager with memory optimization techniques
    """
    
    def __init__(self, model_name: str, device: str = "auto"):
        self.model_name = model_name
        self.device = self._get_device(device)
        self.tokenizer = None
        self.model = None
        self.memory_monitor = MemoryMonitor()
        
    def _get_device(self, device: str) -> str:
        """Determine the best device to use"""
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def load_model_standard(self):
        """Load model with standard settings (baseline)"""
        print(f"Loading model {self.model_name} with standard settings...")
        self.memory_monitor.print_memory_usage("Before Loading")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.model.to(self.device)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.memory_monitor.print_memory_usage("After Standard Loading")
    
    def load_model_optimized(self, optimization_level: int = 1):
        """
        Load model with various optimization techniques
        
        Args:
            optimization_level: 1=basic, 2=aggressive, 3=maximum
        """
        print(f"Loading model {self.model_name} with optimization level {optimization_level}...")
        self.memory_monitor.print_memory_usage("Before Optimized Loading")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        if optimization_level >= 1:
            # Basic optimization: use float16 on GPU
            if self.device == "cuda":
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    low_cpu_mem_usage=True
                )
        
        if optimization_level >= 2 and self.device == "cuda":
            # Aggressive optimization: 8-bit quantization
            try:
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_threshold=6.0,
                    llm_int8_has_fp16_weight=False
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                    low_cpu_mem_usage=True
                )
            except Exception as e:
                print(f"8-bit quantization failed: {e}")
                print("Falling back to float16...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                )
        
        if optimization_level >= 3 and self.device == "cuda":
            # Maximum optimization: 4-bit quantization
            try:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                    low_cpu_mem_usage=True
                )
            except Exception as e:
                print(f"4-bit quantization failed: {e}")
                print("Falling back to 8-bit or float16...")
        
        # Move to device if not using device_map
        if not hasattr(self.model, 'hf_device_map'):
            self.model.to(self.device)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.memory_monitor.print_memory_usage("After Optimized Loading")
    
    def generate_with_memory_management(self, prompt: str, max_length: int = 100) -> str:
        """Generate text with memory management techniques"""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded")
        
        # Clear memory before generation
        self.memory_monitor.clear_memory()
        self.memory_monitor.print_memory_usage("Before Generation")
        
        # Tokenize with attention to memory
        inputs = self.tokenizer.encode(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512  # Limit input length
        ).to(self.device)
        
        # Generate with memory-efficient settings
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id,
                use_cache=True,  # Enable KV cache for efficiency
                num_return_sequences=1
            )
        
        # Decode and clean up
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clear intermediate tensors
        del inputs, outputs
        self.memory_monitor.clear_memory()
        self.memory_monitor.print_memory_usage("After Generation")
        
        return generated_text


def demo_memory_optimization_levels():
    """Demonstrate different levels of memory optimization"""
    print("=== Memory Optimization Levels Demo ===")
    
    model_name = "gpt2"  # Use a small model for demonstration
    prompt = "The advantages of memory optimization include"
    
    # Test different optimization levels
    for level in [0, 1, 2, 3]:
        print(f"\n--- Optimization Level {level} ---")
        
        try:
            manager = OptimizedTransformersManager(model_name)
            
            if level == 0:
                manager.load_model_standard()
            else:
                manager.load_model_optimized(optimization_level=level)
            
            # Generate text and measure performance
            import time
            start_time = time.time()
            result = manager.generate_with_memory_management(prompt, max_length=60)
            generation_time = time.time() - start_time
            
            print(f"Generated: {result}")
            print(f"Generation time: {generation_time:.2f} seconds")
            
            # Clean up
            del manager
            MemoryMonitor.clear_memory()
            
        except Exception as e:
            print(f"Level {level} failed: {e}")


def demo_batch_processing_optimization():
    """Demonstrate memory-efficient batch processing"""
    print("\n=== Batch Processing Optimization Demo ===")
    
    # Create a pipeline with memory optimization
    device = 0 if torch.cuda.is_available() else -1
    generator = pipeline(
        "text-generation",
        model="distilgpt2",
        device=device,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    
    prompts = [
        "Artificial intelligence is",
        "Machine learning helps",
        "Deep learning models",
        "Natural language processing",
        "Computer vision applications"
    ]
    
    print("Processing prompts individually (memory efficient):")
    MemoryMonitor.print_memory_usage("Before Individual Processing")
    
    results = []
    for i, prompt in enumerate(prompts):
        print(f"Processing prompt {i+1}/{len(prompts)}: {prompt}")
        
        result = generator(
            prompt,
            max_length=40,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )
        
        results.append(result[0]['generated_text'])
        
        # Clear cache after each generation
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    MemoryMonitor.print_memory_usage("After Individual Processing")
    
    # Display results
    for i, (prompt, result) in enumerate(zip(prompts, results)):
        print(f"{i+1}. {result}")


def demo_gradient_checkpointing():
    """Demonstrate gradient checkpointing for memory efficiency"""
    print("\n=== Gradient Checkpointing Demo ===")
    
    model_name = "distilgpt2"
    
    print("Loading model with gradient checkpointing...")
    MemoryMonitor.print_memory_usage("Before Loading")
    
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        # Enable gradient checkpointing
        model.gradient_checkpointing_enable()
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        MemoryMonitor.print_memory_usage("After Loading with Checkpointing")
        
        # Test generation
        prompt = "Gradient checkpointing allows"
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=50,
                do_sample=True,
                temperature=0.7
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated: {result}")
        
        MemoryMonitor.print_memory_usage("After Generation")
        
    except Exception as e:
        print(f"Gradient checkpointing demo failed: {e}")


def demo_memory_profiling():
    """Demonstrate memory profiling techniques"""
    print("\n=== Memory Profiling Demo ===")
    
    def profile_model_loading(model_name: str, optimization: bool = False):
        """Profile memory usage during model loading"""
        print(f"\nProfiling {model_name} (optimized: {optimization})")
        
        initial_memory = MemoryMonitor.get_memory_info()
        print(f"Initial RAM: {initial_memory['ram_used_gb']:.2f} GB")
        
        if optimization:
            manager = OptimizedTransformersManager(model_name)
            manager.load_model_optimized(optimization_level=2)
        else:
            manager = OptimizedTransformersManager(model_name)
            manager.load_model_standard()
        
        final_memory = MemoryMonitor.get_memory_info()
        memory_increase = final_memory['ram_used_gb'] - initial_memory['ram_used_gb']
        
        print(f"Final RAM: {final_memory['ram_used_gb']:.2f} GB")
        print(f"Memory increase: {memory_increase:.2f} GB")
        
        return memory_increase
    
    # Profile different models
    models = ["distilgpt2", "gpt2"]
    
    for model in models:
        try:
            standard_memory = profile_model_loading(model, optimization=False)
            MemoryMonitor.clear_memory()
            
            optimized_memory = profile_model_loading(model, optimization=True)
            MemoryMonitor.clear_memory()
            
            savings = standard_memory - optimized_memory
            print(f"Memory savings: {savings:.2f} GB ({savings/standard_memory*100:.1f}%)")
            
        except Exception as e:
            print(f"Profiling {model} failed: {e}")


def print_hardware_recommendations():
    """Print hardware recommendations based on current system"""
    print("\n=== Hardware Recommendations ===")
    
    memory_info = MemoryMonitor.get_memory_info()
    total_ram = psutil.virtual_memory().total / (1024**3)
    
    print(f"Current System:")
    print(f"- Total RAM: {total_ram:.1f} GB")
    print(f"- Available RAM: {memory_info['ram_available_gb']:.1f} GB")
    
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name()
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"- GPU: {gpu_name}")
        print(f"- GPU Memory: {gpu_memory:.1f} GB")
    else:
        print("- GPU: Not available")
    
    print(f"\nRecommendations:")
    
    if total_ram < 8:
        print("- Consider upgrading to at least 8GB RAM")
        print("- Use heavily quantized models (4-bit)")
        print("- Process one sample at a time")
    elif total_ram < 16:
        print("- Good for small to medium models")
        print("- Use 8-bit quantization for larger models")
        print("- Enable gradient checkpointing if training")
    else:
        print("- Sufficient RAM for most models")
        print("- Can run larger models with optimization")
    
    if not torch.cuda.is_available():
        print("- Consider GPU acceleration for better performance")
        print("- CPU inference is slower but still functional")
    elif torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        if gpu_memory < 6:
            print("- GPU memory is limited, use quantization")
        elif gpu_memory < 12:
            print("- Good GPU memory for most models")
        else:
            print("- Excellent GPU memory, can run large models")


def main():
    """Run all memory optimization demonstrations"""
    print("Hugging Face Transformers - Memory Optimization Examples")
    print("=" * 60)
    
    try:
        # Print system information
        print_hardware_recommendations()
        
        # Memory optimization levels demo
        demo_memory_optimization_levels()
        
        # Batch processing optimization
        demo_batch_processing_optimization()
        
        # Gradient checkpointing demo
        demo_gradient_checkpointing()
        
        # Memory profiling demo
        demo_memory_profiling()
        
        print("\n" + "=" * 60)
        print("Memory optimization demos completed!")
        print("\nKey takeaways:")
        print("- Use quantization to reduce memory usage")
        print("- Enable gradient checkpointing for training")
        print("- Process samples individually for large batches")
        print("- Monitor memory usage regularly")
        print("- Clear caches between operations")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install transformers torch accelerate bitsandbytes psutil")


if __name__ == "__main__":
    main()