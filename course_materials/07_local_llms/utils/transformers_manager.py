"""
TransformersManager utility class for managing Hugging Face Transformers.

This module provides a comprehensive interface for working with Hugging Face
Transformers, including model loading with quantization, memory optimization,
and performance monitoring.
"""

import gc
import time
import logging
import psutil
import torch
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import warnings

# Suppress some common warnings
warnings.filterwarnings("ignore", category=UserWarning)

try:
    from transformers import (
        AutoTokenizer, 
        AutoModelForCausalLM,
        BitsAndBytesConfig,
        pipeline,
        TextGenerationPipeline
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import bitsandbytes as bnb
    BITSANDBYTES_AVAILABLE = True
except ImportError:
    BITSANDBYTES_AVAILABLE = False


@dataclass
class ModelConfig:
    """Configuration for model loading and generation."""
    model_name: str
    device: str = "auto"
    torch_dtype: str = "auto"
    quantization_config: Optional[Dict[str, Any]] = None
    trust_remote_code: bool = False
    use_cache: bool = True
    low_cpu_mem_usage: bool = True
    device_map: Optional[Union[str, Dict]] = None


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    max_length: int = 100
    max_new_tokens: Optional[int] = None
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    num_return_sequences: int = 1
    pad_token_id: Optional[int] = None
    eos_token_id: Optional[int] = None
    repetition_penalty: float = 1.1
    length_penalty: float = 1.0
    early_stopping: bool = True


@dataclass
class PerformanceMetrics:
    """Performance metrics for model operations."""
    model_name: str
    operation: str
    duration_seconds: float
    memory_before_mb: float
    memory_after_mb: float
    memory_peak_mb: float
    gpu_memory_used_mb: float = 0.0
    tokens_generated: int = 0
    tokens_per_second: float = 0.0
    timestamp: float = field(default_factory=time.time)


class TransformersError(Exception):
    """Base exception for Transformers-related errors."""
    pass


class TransformersModelError(TransformersError):
    """Raised when model operations fail."""
    pass


class TransformersMemoryError(TransformersError):
    """Raised when memory-related operations fail."""
    pass


class TransformersManager:
    """
    A utility class for managing Hugging Face Transformers models.
    
    This class provides methods for model loading with quantization options,
    memory optimization, performance monitoring, and text generation.
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the TransformersManager.
        
        Args:
            cache_dir: Directory for caching models
        """
        if not TRANSFORMERS_AVAILABLE:
            raise TransformersError(
                "Transformers library not available. Install with: pip install transformers"
            )
        
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.logger = logging.getLogger(__name__)
        self.loaded_models: Dict[str, Dict[str, Any]] = {}
        self.performance_history: List[PerformanceMetrics] = []
        
        # Check available devices
        self.device_info = self._get_device_info()
        self.logger.info(f"Available devices: {self.device_info}")
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get information about available devices."""
        info = {
            "cpu_available": True,
            "cuda_available": torch.cuda.is_available(),
            "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False,
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "cuda_devices": []
        }
        
        if info["cuda_available"]:
            for i in range(info["cuda_device_count"]):
                device_props = torch.cuda.get_device_properties(i)
                info["cuda_devices"].append({
                    "id": i,
                    "name": device_props.name,
                    "memory_gb": device_props.total_memory / (1024**3),
                    "compute_capability": f"{device_props.major}.{device_props.minor}"
                })
        
        return info
    
    def _get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage."""
        memory_info = {
            "cpu_memory_mb": psutil.virtual_memory().used / (1024**2),
            "cpu_memory_percent": psutil.virtual_memory().percent,
            "gpu_memory_mb": 0.0
        }
        
        if torch.cuda.is_available():
            memory_info["gpu_memory_mb"] = torch.cuda.memory_allocated() / (1024**2)
            
        return memory_info
    
    def create_quantization_config(
        self,
        load_in_4bit: bool = False,
        load_in_8bit: bool = False,
        bnb_4bit_compute_dtype: str = "float16",
        bnb_4bit_use_double_quant: bool = True,
        bnb_4bit_quant_type: str = "nf4"
    ) -> Optional[BitsAndBytesConfig]:
        """
        Create quantization configuration for memory optimization.
        
        Args:
            load_in_4bit: Whether to load model in 4-bit precision
            load_in_8bit: Whether to load model in 8-bit precision
            bnb_4bit_compute_dtype: Compute dtype for 4-bit quantization
            bnb_4bit_use_double_quant: Whether to use double quantization
            bnb_4bit_quant_type: Quantization type for 4-bit
            
        Returns:
            BitsAndBytesConfig object or None
        """
        if not (load_in_4bit or load_in_8bit):
            return None
            
        if not BITSANDBYTES_AVAILABLE:
            self.logger.warning("bitsandbytes not available. Quantization disabled.")
            return None
        
        if load_in_4bit and load_in_8bit:
            raise TransformersError("Cannot use both 4-bit and 8-bit quantization")
        
        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32
        }
        
        compute_dtype = dtype_map.get(bnb_4bit_compute_dtype, torch.float16)
        
        return BitsAndBytesConfig(
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=bnb_4bit_use_double_quant,
            bnb_4bit_quant_type=bnb_4bit_quant_type
        )
    
    def load_model(
        self,
        model_name: str,
        config: Optional[ModelConfig] = None,
        quantization: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Load a model with optional quantization.
        
        Args:
            model_name: Name or path of the model
            config: Model configuration
            quantization: Quantization settings
            
        Returns:
            Model identifier for future operations
            
        Raises:
            TransformersModelError: If model loading fails
            TransformersMemoryError: If insufficient memory
        """
        if config is None:
            config = ModelConfig(model_name=model_name)
        
        model_id = f"{model_name}_{id(config)}"
        
        if model_id in self.loaded_models:
            self.logger.info(f"Model {model_name} already loaded")
            return model_id
        
        start_time = time.time()
        memory_before = self._get_memory_usage()
        
        try:
            # Create quantization config if specified
            quant_config = None
            if quantization:
                quant_config = self.create_quantization_config(**quantization)
            
            # Load tokenizer
            self.logger.info(f"Loading tokenizer for {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=config.trust_remote_code
            )
            
            # Set pad token if not present
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Determine device and dtype
            device = self._resolve_device(config.device)
            torch_dtype = self._resolve_dtype(config.torch_dtype)
            
            # Load model
            self.logger.info(f"Loading model {model_name} on {device}")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                torch_dtype=torch_dtype,
                device_map=config.device_map or device,
                quantization_config=quant_config,
                trust_remote_code=config.trust_remote_code,
                use_cache=config.use_cache,
                low_cpu_mem_usage=config.low_cpu_mem_usage
            )
            
            # Store model information
            self.loaded_models[model_id] = {
                "model": model,
                "tokenizer": tokenizer,
                "config": config,
                "device": device,
                "quantization_config": quant_config,
                "load_time": time.time() - start_time
            }
            
            # Record performance metrics
            memory_after = self._get_memory_usage()
            metrics = PerformanceMetrics(
                model_name=model_name,
                operation="load_model",
                duration_seconds=time.time() - start_time,
                memory_before_mb=memory_before["cpu_memory_mb"],
                memory_after_mb=memory_after["cpu_memory_mb"],
                memory_peak_mb=memory_after["cpu_memory_mb"],
                gpu_memory_used_mb=memory_after["gpu_memory_mb"]
            )
            self.performance_history.append(metrics)
            
            self.logger.info(f"Successfully loaded {model_name} in {metrics.duration_seconds:.2f}s")
            return model_id
            
        except torch.cuda.OutOfMemoryError as e:
            raise TransformersMemoryError(f"GPU out of memory loading {model_name}: {e}") from e
        except Exception as e:
            raise TransformersModelError(f"Failed to load model {model_name}: {e}") from e
    
    def _resolve_device(self, device: str) -> str:
        """Resolve device string to actual device."""
        if device == "auto":
            if self.device_info["cuda_available"]:
                return "cuda"
            elif self.device_info["mps_available"]:
                return "mps"
            else:
                return "cpu"
        return device
    
    def _resolve_dtype(self, dtype: str) -> torch.dtype:
        """Resolve dtype string to torch dtype."""
        if dtype == "auto":
            if torch.cuda.is_available():
                return torch.float16
            else:
                return torch.float32
        
        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
            "int8": torch.int8
        }
        
        return dtype_map.get(dtype, torch.float32)
    
    def generate_text(
        self,
        model_id: str,
        prompt: str,
        generation_config: Optional[GenerationConfig] = None
    ) -> str:
        """
        Generate text using a loaded model.
        
        Args:
            model_id: Identifier of the loaded model
            prompt: Input prompt
            generation_config: Generation configuration
            
        Returns:
            Generated text
            
        Raises:
            TransformersModelError: If generation fails
        """
        if model_id not in self.loaded_models:
            raise TransformersModelError(f"Model {model_id} not loaded")
        
        if generation_config is None:
            generation_config = GenerationConfig()
        
        model_info = self.loaded_models[model_id]
        model = model_info["model"]
        tokenizer = model_info["tokenizer"]
        
        start_time = time.time()
        memory_before = self._get_memory_usage()
        
        try:
            # Tokenize input
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
            
            # Move to device
            device = model_info["device"]
            if device != "cpu":
                inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Set generation parameters
            gen_kwargs = {
                "max_length": generation_config.max_length,
                "temperature": generation_config.temperature,
                "top_p": generation_config.top_p,
                "top_k": generation_config.top_k,
                "do_sample": generation_config.do_sample,
                "num_return_sequences": generation_config.num_return_sequences,
                "repetition_penalty": generation_config.repetition_penalty,
                "length_penalty": generation_config.length_penalty,
                "early_stopping": generation_config.early_stopping,
                "pad_token_id": generation_config.pad_token_id or tokenizer.pad_token_id,
                "eos_token_id": generation_config.eos_token_id or tokenizer.eos_token_id
            }
            
            if generation_config.max_new_tokens is not None:
                gen_kwargs["max_new_tokens"] = generation_config.max_new_tokens
                del gen_kwargs["max_length"]
            
            # Generate
            with torch.no_grad():
                outputs = model.generate(**inputs, **gen_kwargs)
            
            # Decode output
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove input prompt from output
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Record performance metrics
            duration = time.time() - start_time
            memory_after = self._get_memory_usage()
            tokens_generated = len(outputs[0]) - len(inputs["input_ids"][0])
            
            metrics = PerformanceMetrics(
                model_name=model_info["config"].model_name,
                operation="generate_text",
                duration_seconds=duration,
                memory_before_mb=memory_before["cpu_memory_mb"],
                memory_after_mb=memory_after["cpu_memory_mb"],
                memory_peak_mb=memory_after["cpu_memory_mb"],
                gpu_memory_used_mb=memory_after["gpu_memory_mb"],
                tokens_generated=tokens_generated,
                tokens_per_second=tokens_generated / duration if duration > 0 else 0
            )
            self.performance_history.append(metrics)
            
            return generated_text
            
        except torch.cuda.OutOfMemoryError as e:
            raise TransformersMemoryError(f"GPU out of memory during generation: {e}") from e
        except Exception as e:
            raise TransformersModelError(f"Text generation failed: {e}") from e
    
    def unload_model(self, model_id: str) -> bool:
        """
        Unload a model to free memory.
        
        Args:
            model_id: Identifier of the model to unload
            
        Returns:
            True if successful
        """
        if model_id not in self.loaded_models:
            self.logger.warning(f"Model {model_id} not found")
            return False
        
        try:
            # Delete model and tokenizer
            del self.loaded_models[model_id]
            
            # Force garbage collection
            gc.collect()
            
            # Clear GPU cache if available
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.logger.info(f"Successfully unloaded model {model_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unloading model {model_id}: {e}")
            return False
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a loaded model.
        
        Args:
            model_id: Identifier of the model
            
        Returns:
            Model information dictionary or None
        """
        if model_id not in self.loaded_models:
            return None
        
        model_info = self.loaded_models[model_id].copy()
        
        # Remove actual model objects for serialization
        info = {
            "model_name": model_info["config"].model_name,
            "device": model_info["device"],
            "load_time": model_info["load_time"],
            "quantization_enabled": model_info["quantization_config"] is not None,
            "memory_usage": self._get_memory_usage()
        }
        
        return info
    
    def list_loaded_models(self) -> List[str]:
        """
        List all loaded model identifiers.
        
        Returns:
            List of model identifiers
        """
        return list(self.loaded_models.keys())
    
    def get_performance_metrics(self, model_name: Optional[str] = None) -> List[PerformanceMetrics]:
        """
        Get performance metrics history.
        
        Args:
            model_name: Filter by model name (optional)
            
        Returns:
            List of performance metrics
        """
        if model_name is None:
            return self.performance_history.copy()
        
        return [m for m in self.performance_history if m.model_name == model_name]
    
    def optimize_memory(self) -> Dict[str, Any]:
        """
        Perform memory optimization operations.
        
        Returns:
            Memory optimization results
        """
        memory_before = self._get_memory_usage()
        
        # Force garbage collection
        gc.collect()
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        memory_after = self._get_memory_usage()
        
        results = {
            "memory_freed_mb": memory_before["cpu_memory_mb"] - memory_after["cpu_memory_mb"],
            "gpu_memory_freed_mb": memory_before["gpu_memory_mb"] - memory_after["gpu_memory_mb"],
            "memory_before": memory_before,
            "memory_after": memory_after
        }
        
        self.logger.info(f"Memory optimization completed: {results}")
        return results
    
    def benchmark_model(
        self,
        model_id: str,
        test_prompts: List[str],
        generation_config: Optional[GenerationConfig] = None
    ) -> Dict[str, Any]:
        """
        Benchmark a model's performance.
        
        Args:
            model_id: Identifier of the model to benchmark
            test_prompts: List of test prompts
            generation_config: Generation configuration
            
        Returns:
            Benchmark results
        """
        if model_id not in self.loaded_models:
            raise TransformersModelError(f"Model {model_id} not loaded")
        
        results = {
            "model_id": model_id,
            "num_prompts": len(test_prompts),
            "total_time": 0.0,
            "average_time": 0.0,
            "total_tokens": 0,
            "average_tokens_per_second": 0.0,
            "memory_usage": [],
            "individual_results": []
        }
        
        start_time = time.time()
        
        for i, prompt in enumerate(test_prompts):
            prompt_start = time.time()
            
            try:
                response = self.generate_text(model_id, prompt, generation_config)
                prompt_duration = time.time() - prompt_start
                
                # Get latest performance metrics
                latest_metrics = self.performance_history[-1]
                
                results["individual_results"].append({
                    "prompt_index": i,
                    "prompt": prompt[:50] + "..." if len(prompt) > 50 else prompt,
                    "response_length": len(response),
                    "duration": prompt_duration,
                    "tokens_generated": latest_metrics.tokens_generated,
                    "tokens_per_second": latest_metrics.tokens_per_second
                })
                
                results["total_tokens"] += latest_metrics.tokens_generated
                results["memory_usage"].append(self._get_memory_usage())
                
            except Exception as e:
                self.logger.error(f"Benchmark failed for prompt {i}: {e}")
                results["individual_results"].append({
                    "prompt_index": i,
                    "error": str(e)
                })
        
        results["total_time"] = time.time() - start_time
        results["average_time"] = results["total_time"] / len(test_prompts)
        results["average_tokens_per_second"] = (
            results["total_tokens"] / results["total_time"] 
            if results["total_time"] > 0 else 0
        )
        
        return results


# Example usage and testing functions
def example_usage():
    """Example usage of TransformersManager."""
    # Initialize manager
    manager = TransformersManager()
    
    try:
        # Load a small model for testing
        model_name = "microsoft/DialoGPT-small"
        
        # Create model config with quantization for memory efficiency
        config = ModelConfig(
            model_name=model_name,
            device="auto"
        )
        
        quantization = {
            "load_in_8bit": True
        } if manager.device_info["cuda_available"] else None
        
        # Load model
        model_id = manager.load_model(model_name, config, quantization)
        print(f"Loaded model: {model_id}")
        
        # Generate text
        response = manager.generate_text(
            model_id,
            "Hello, how are you?",
            GenerationConfig(max_new_tokens=50)
        )
        print(f"Response: {response}")
        
        # Get performance metrics
        metrics = manager.get_performance_metrics()
        if metrics:
            latest = metrics[-1]
            print(f"Generation took {latest.duration_seconds:.2f}s")
            print(f"Tokens per second: {latest.tokens_per_second:.2f}")
        
        # Cleanup
        manager.unload_model(model_id)
        
    except TransformersError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_usage()