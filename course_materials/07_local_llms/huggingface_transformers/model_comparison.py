#!/usr/bin/env python3
"""
Model Comparison: Ollama vs Hugging Face Transformers

This script compares the performance, memory usage, and ease of use
between Ollama and Hugging Face Transformers for local LLM deployment.

Requirements: 2.2, 2.4
"""

import time
import psutil
import torch
import requests
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import warnings
warnings.filterwarnings("ignore")


@dataclass
class BenchmarkResult:
    """Data class for storing benchmark results"""
    approach: str
    model_name: str
    setup_time: float
    inference_time: float
    memory_usage_mb: float
    tokens_per_second: float
    response_quality: str
    ease_of_use: int  # 1-10 scale
    error_message: Optional[str] = None


class OllamaInterface:
    """Interface for interacting with Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available models"""
        if not self.available:
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except:
            pass
        return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model if not available"""
        if not self.available:
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=300  # 5 minutes timeout
            )
            return response.status_code == 200
        except:
            return False
    
    def generate(self, model: str, prompt: str, system: str = None) -> Tuple[str, float]:
        """Generate text and return response with timing"""
        if not self.available:
            raise Exception("Ollama not available")
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        if system:
            payload["system"] = system
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                inference_time = time.time() - start_time
                return data.get('response', ''), inference_time
            else:
                raise Exception(f"HTTP {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Generation failed: {e}")


class TransformersInterface:
    """Interface for Hugging Face Transformers"""
    
    def __init__(self):
        self.models = {}  # Cache loaded models
        self.tokenizers = {}  # Cache tokenizers
    
    def load_model(self, model_name: str, optimization: bool = True) -> float:
        """Load model and return setup time"""
        start_time = time.time()
        
        try:
            # Load tokenizer
            self.tokenizers[model_name] = AutoTokenizer.from_pretrained(model_name)
            
            # Load model with optimization
            if optimization and torch.cuda.is_available():
                self.models[model_name] = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                ).to("cuda")
            else:
                self.models[model_name] = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    low_cpu_mem_usage=True
                )
            
            # Set padding token
            if self.tokenizers[model_name].pad_token is None:
                self.tokenizers[model_name].pad_token = self.tokenizers[model_name].eos_token
            
            setup_time = time.time() - start_time
            return setup_time
            
        except Exception as e:
            raise Exception(f"Model loading failed: {e}")
    
    def generate(self, model_name: str, prompt: str, max_length: int = 100) -> Tuple[str, float]:
        """Generate text and return response with timing"""
        if model_name not in self.models:
            raise Exception(f"Model {model_name} not loaded")
        
        model = self.models[model_name]
        tokenizer = self.tokenizers[model_name]
        device = next(model.parameters()).device
        
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
        
        start_time = time.time()
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=max_length,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        inference_time = time.time() - start_time
        
        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return generated_text, inference_time


class ModelComparator:
    """Main class for comparing models across different approaches"""
    
    def __init__(self):
        self.ollama = OllamaInterface()
        self.transformers = TransformersInterface()
        self.results = []
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
    
    def benchmark_ollama(self, model_name: str, prompt: str) -> BenchmarkResult:
        """Benchmark Ollama approach"""
        print(f"Benchmarking Ollama with {model_name}...")
        
        if not self.ollama.available:
            return BenchmarkResult(
                approach="Ollama",
                model_name=model_name,
                setup_time=0,
                inference_time=0,
                memory_usage_mb=0,
                tokens_per_second=0,
                response_quality="N/A",
                ease_of_use=0,
                error_message="Ollama not available"
            )
        
        try:
            # Check if model is available
            available_models = self.ollama.list_models()
            if model_name not in available_models:
                print(f"Pulling model {model_name}...")
                setup_start = time.time()
                if not self.ollama.pull_model(model_name):
                    raise Exception("Failed to pull model")
                setup_time = time.time() - setup_start
            else:
                setup_time = 0
            
            # Measure memory before generation
            memory_before = self.get_memory_usage()
            
            # Generate response
            response, inference_time = self.ollama.generate(model_name, prompt)
            
            # Measure memory after generation
            memory_after = self.get_memory_usage()
            memory_usage = memory_after - memory_before
            
            # Calculate tokens per second (rough estimate)
            response_tokens = len(response.split())
            tokens_per_second = response_tokens / inference_time if inference_time > 0 else 0
            
            return BenchmarkResult(
                approach="Ollama",
                model_name=model_name,
                setup_time=setup_time,
                inference_time=inference_time,
                memory_usage_mb=memory_usage,
                tokens_per_second=tokens_per_second,
                response_quality=self._assess_quality(response),
                ease_of_use=9  # Ollama is very easy to use
            )
            
        except Exception as e:
            return BenchmarkResult(
                approach="Ollama",
                model_name=model_name,
                setup_time=0,
                inference_time=0,
                memory_usage_mb=0,
                tokens_per_second=0,
                response_quality="N/A",
                ease_of_use=0,
                error_message=str(e)
            )
    
    def benchmark_transformers(self, model_name: str, prompt: str) -> BenchmarkResult:
        """Benchmark Transformers approach"""
        print(f"Benchmarking Transformers with {model_name}...")
        
        try:
            # Measure memory before loading
            memory_before = self.get_memory_usage()
            
            # Load model
            setup_time = self.transformers.load_model(model_name)
            
            # Generate response
            response, inference_time = self.transformers.generate(model_name, prompt)
            
            # Measure memory after generation
            memory_after = self.get_memory_usage()
            memory_usage = memory_after - memory_before
            
            # Calculate tokens per second (rough estimate)
            response_tokens = len(response.split())
            tokens_per_second = response_tokens / inference_time if inference_time > 0 else 0
            
            return BenchmarkResult(
                approach="Transformers",
                model_name=model_name,
                setup_time=setup_time,
                inference_time=inference_time,
                memory_usage_mb=memory_usage,
                tokens_per_second=tokens_per_second,
                response_quality=self._assess_quality(response),
                ease_of_use=6  # More complex setup but flexible
            )
            
        except Exception as e:
            return BenchmarkResult(
                approach="Transformers",
                model_name=model_name,
                setup_time=0,
                inference_time=0,
                memory_usage_mb=0,
                tokens_per_second=0,
                response_quality="N/A",
                ease_of_use=0,
                error_message=str(e)
            )
    
    def _assess_quality(self, response: str) -> str:
        """Simple quality assessment of generated text"""
        if not response or len(response.strip()) < 10:
            return "Poor"
        elif len(response.strip()) < 50:
            return "Fair"
        elif response.count('.') >= 2 and len(response.strip()) > 100:
            return "Good"
        else:
            return "Fair"
    
    def run_comparison(self, test_cases: List[Dict]) -> List[BenchmarkResult]:
        """Run comparison across multiple test cases"""
        results = []
        
        for test_case in test_cases:
            model_name = test_case['model']
            prompt = test_case['prompt']
            
            print(f"\n--- Testing: {model_name} ---")
            print(f"Prompt: {prompt}")
            
            # Test Ollama
            ollama_result = self.benchmark_ollama(model_name, prompt)
            results.append(ollama_result)
            
            # Test Transformers (map Ollama model names to HF model names)
            hf_model = self._map_to_hf_model(model_name)
            if hf_model:
                transformers_result = self.benchmark_transformers(hf_model, prompt)
                results.append(transformers_result)
            
            # Clear memory between tests
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        return results
    
    def _map_to_hf_model(self, ollama_model: str) -> Optional[str]:
        """Map Ollama model names to Hugging Face model names"""
        mapping = {
            'llama2': 'meta-llama/Llama-2-7b-hf',
            'codellama': 'codellama/CodeLlama-7b-hf',
            'mistral': 'mistralai/Mistral-7B-v0.1',
            'phi': 'microsoft/phi-2',
            'tinyllama': 'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
            # For demo purposes, use smaller models
            'demo': 'gpt2',
            'small': 'distilgpt2'
        }
        return mapping.get(ollama_model)
    
    def print_results(self, results: List[BenchmarkResult]):
        """Print comparison results in a formatted table"""
        print("\n" + "=" * 100)
        print("MODEL COMPARISON RESULTS")
        print("=" * 100)
        
        # Group results by model
        model_groups = {}
        for result in results:
            base_model = result.model_name.split(':')[0]  # Remove version tags
            if base_model not in model_groups:
                model_groups[base_model] = []
            model_groups[base_model].append(result)
        
        for model, model_results in model_groups.items():
            print(f"\n--- {model.upper()} ---")
            
            # Print header
            print(f"{'Approach':<12} {'Setup(s)':<10} {'Inference(s)':<12} {'Memory(MB)':<12} {'Tokens/s':<10} {'Quality':<8} {'Ease':<6}")
            print("-" * 80)
            
            for result in model_results:
                if result.error_message:
                    print(f"{result.approach:<12} ERROR: {result.error_message}")
                else:
                    print(f"{result.approach:<12} {result.setup_time:<10.2f} {result.inference_time:<12.2f} "
                          f"{result.memory_usage_mb:<12.1f} {result.tokens_per_second:<10.1f} "
                          f"{result.response_quality:<8} {result.ease_of_use:<6}/10")
    
    def generate_summary(self, results: List[BenchmarkResult]) -> Dict[str, str]:
        """Generate a summary of the comparison"""
        successful_results = [r for r in results if r.error_message is None]
        
        if not successful_results:
            return {"summary": "No successful benchmarks to compare"}
        
        # Calculate averages by approach
        ollama_results = [r for r in successful_results if r.approach == "Ollama"]
        transformers_results = [r for r in successful_results if r.approach == "Transformers"]
        
        summary = {}
        
        if ollama_results:
            avg_ollama_inference = sum(r.inference_time for r in ollama_results) / len(ollama_results)
            avg_ollama_memory = sum(r.memory_usage_mb for r in ollama_results) / len(ollama_results)
            summary["ollama"] = f"Avg inference: {avg_ollama_inference:.2f}s, Avg memory: {avg_ollama_memory:.1f}MB"
        
        if transformers_results:
            avg_tf_inference = sum(r.inference_time for r in transformers_results) / len(transformers_results)
            avg_tf_memory = sum(r.memory_usage_mb for r in transformers_results) / len(transformers_results)
            summary["transformers"] = f"Avg inference: {avg_tf_inference:.2f}s, Avg memory: {avg_tf_memory:.1f}MB"
        
        # Overall recommendation
        if ollama_results and transformers_results:
            if avg_ollama_inference < avg_tf_inference:
                summary["speed_winner"] = "Ollama is faster for inference"
            else:
                summary["speed_winner"] = "Transformers is faster for inference"
            
            if avg_ollama_memory < avg_tf_memory:
                summary["memory_winner"] = "Ollama uses less memory"
            else:
                summary["memory_winner"] = "Transformers uses less memory"
        
        return summary


def create_hardware_considerations_doc():
    """Create documentation about hardware considerations"""
    content = """# Hardware Considerations for Local LLMs

## System Requirements

### Minimum Requirements
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space for models
- **CPU**: Modern multi-core processor
- **GPU**: Optional but recommended for larger models

### Recommended Configurations

#### Budget Setup (CPU Only)
- **RAM**: 16GB
- **CPU**: 8+ cores
- **Models**: Small models (1-3B parameters)
- **Approaches**: Ollama with quantized models, Transformers with optimization

#### Mid-Range Setup (GPU Accelerated)
- **RAM**: 16-32GB
- **GPU**: 8-12GB VRAM (RTX 3070/4060 Ti or better)
- **Models**: Medium models (7-13B parameters)
- **Approaches**: Both Ollama and Transformers work well

#### High-End Setup (Professional)
- **RAM**: 32GB+
- **GPU**: 16GB+ VRAM (RTX 4080/4090, A6000)
- **Models**: Large models (13-70B parameters)
- **Approaches**: Full flexibility with both approaches

## Performance Comparison

### Ollama Advantages
- **Ease of Use**: Simple installation and model management
- **Memory Efficiency**: Built-in quantization and optimization
- **Model Variety**: Easy access to many pre-optimized models
- **API Consistency**: Uniform interface across different models

### Transformers Advantages
- **Flexibility**: Full control over model loading and generation
- **Customization**: Extensive configuration options
- **Integration**: Better integration with ML pipelines
- **Research Features**: Access to latest research models

### When to Choose Ollama
- Quick prototyping and experimentation
- Production deployments with standard models
- Limited technical expertise with ML optimization
- Need for consistent API across models

### When to Choose Transformers
- Research and development work
- Custom model fine-tuning
- Integration with existing ML workflows
- Need for specific optimization techniques

## Memory Optimization Strategies

### For Limited RAM (8-16GB)
1. Use quantized models (4-bit or 8-bit)
2. Process one sample at a time
3. Clear memory caches frequently
4. Use CPU inference for very large models

### For GPU Acceleration
1. Use mixed precision (float16)
2. Enable gradient checkpointing if training
3. Use device mapping for multi-GPU setups
4. Monitor GPU memory usage

### For Production Deployments
1. Benchmark both approaches with your specific use case
2. Consider model serving frameworks
3. Implement proper error handling and fallbacks
4. Monitor resource usage in production

## Model Size Guidelines

| Model Size | RAM Needed | GPU VRAM | Use Cases |
|------------|------------|----------|-----------|
| 1-3B       | 4-8GB      | 2-4GB    | Simple tasks, chatbots |
| 7B         | 8-16GB     | 4-8GB    | General purpose, coding |
| 13B        | 16-32GB    | 8-16GB   | Complex reasoning |
| 30B+       | 32GB+      | 16GB+    | Professional applications |

## Troubleshooting Common Issues

### Out of Memory Errors
- Reduce model size or use quantization
- Decrease batch size
- Clear GPU cache between operations
- Use CPU fallback for large models

### Slow Performance
- Check if GPU acceleration is working
- Use appropriate model size for hardware
- Enable optimizations (quantization, mixed precision)
- Consider model-specific optimizations

### Installation Issues
- Verify CUDA version compatibility
- Use virtual environments
- Check system requirements
- Follow platform-specific installation guides
"""
    
    return content


def main():
    """Run the model comparison demonstration"""
    print("Model Comparison: Ollama vs Hugging Face Transformers")
    print("=" * 55)
    
    # Create hardware considerations documentation
    hardware_doc = create_hardware_considerations_doc()
    with open("course_materials/07_local_llms/huggingface_transformers/hardware_considerations.md", "w") as f:
        f.write(hardware_doc)
    print("Created hardware_considerations.md")
    
    # Initialize comparator
    comparator = ModelComparator()
    
    # Define test cases (using small models for demonstration)
    test_cases = [
        {
            'model': 'demo',  # Maps to gpt2 for transformers
            'prompt': 'The benefits of local language models include'
        },
        {
            'model': 'small',  # Maps to distilgpt2 for transformers
            'prompt': 'Artificial intelligence will help humanity by'
        }
    ]
    
    print(f"\nSystem Information:")
    print(f"- CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"- GPU: {torch.cuda.get_device_name()}")
        print(f"- GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"- RAM: {psutil.virtual_memory().total / 1e9:.1f} GB")
    print(f"- Ollama Available: {comparator.ollama.available}")
    
    if not comparator.ollama.available:
        print("\nNote: Ollama is not available. Only Transformers will be tested.")
        print("To test Ollama, install it from https://ollama.ai")
    
    # Run comparison
    try:
        results = comparator.run_comparison(test_cases)
        
        # Print results
        comparator.print_results(results)
        
        # Generate summary
        summary = comparator.generate_summary(results)
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        print("\n" + "=" * 50)
        print("RECOMMENDATIONS")
        print("=" * 50)
        print("For beginners: Start with Ollama for ease of use")
        print("For researchers: Use Transformers for flexibility")
        print("For production: Benchmark both with your specific models")
        print("For limited hardware: Use quantized models with either approach")
        
    except Exception as e:
        print(f"Comparison failed: {e}")
        print("\nMake sure you have the required dependencies:")
        print("pip install transformers torch accelerate psutil requests")


if __name__ == "__main__":
    main()