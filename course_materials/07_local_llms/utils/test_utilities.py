"""
Test utility functions for the local LLMs module.

This module provides utility functions for testing, validation, formatting,
and system requirement checking used across the local LLMs module.
"""

import re
import math
from typing import Dict, List, Any, Optional

# Optional imports with fallbacks
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def validate_model_name(name: str) -> bool:
    """
    Validate a model name format.
    
    Args:
        name: Model name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Basic pattern: allows alphanumeric, hyphens, underscores, slashes, colons
    # Format: [org/]model-name[:tag]
    pattern = r'^[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(:[a-zA-Z0-9._-]+)?$'
    
    return bool(re.match(pattern, name.strip()))


def format_model_size(size_bytes: int) -> str:
    """
    Format model size in bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def parse_model_info(model_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and enhance model information.
    
    Args:
        model_data: Raw model data from API
        
    Returns:
        Enhanced model information
    """
    parsed = {
        "name": model_data.get("name", "Unknown"),
        "size_bytes": model_data.get("size", 0),
        "size_formatted": format_model_size(model_data.get("size", 0)),
        "digest": model_data.get("digest", ""),
        "modified_at": model_data.get("modified_at", ""),
        "parameter_size": "Unknown",
        "quantization": "Unknown"
    }
    
    # Extract additional details if available
    details = model_data.get("details", {})
    if details:
        parsed["parameter_size"] = details.get("parameter_size", "Unknown")
        parsed["quantization"] = details.get("quantization", "Unknown")
    
    return parsed


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    if not filename or not filename.strip():
        return "unnamed"
    
    # Remove invalid characters for most filesystems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename.strip())
    
    # Remove control characters
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    
    # Ensure it's not empty after sanitization
    if not sanitized:
        return "unnamed"
    
    return sanitized


def check_system_requirements() -> Dict[str, Any]:
    """
    Check system requirements for running local LLMs.
    
    Returns:
        Dictionary with system information and requirements check
    """
    # Default values
    total_memory_gb = 0
    available_memory_gb = 0
    gpu_available = False
    gpu_memory_gb = 0
    
    # Get memory information if psutil is available
    if PSUTIL_AVAILABLE:
        try:
            memory = psutil.virtual_memory()
            total_memory_gb = memory.total / (1024**3)
            available_memory_gb = memory.available / (1024**3)
        except Exception:
            pass
    
    # Check GPU availability if torch is available
    if TORCH_AVAILABLE:
        try:
            gpu_available = torch.cuda.is_available()
            if gpu_available:
                gpu_props = torch.cuda.get_device_properties(0)
                gpu_memory_gb = gpu_props.total_memory / (1024**3)
        except Exception:
            gpu_available = False
    
    # Determine if system has sufficient resources
    # Minimum: 8GB RAM for small models, 16GB recommended
    sufficient_memory = total_memory_gb >= 8 if total_memory_gb > 0 else None
    
    return {
        "total_memory_gb": round(total_memory_gb, 1),
        "available_memory_gb": round(available_memory_gb, 1),
        "sufficient_memory": sufficient_memory,
        "gpu_available": gpu_available,
        "gpu_memory_gb": round(gpu_memory_gb, 1),
        "recommended_memory_gb": 16,
        "minimum_memory_gb": 8,
        "psutil_available": PSUTIL_AVAILABLE,
        "torch_available": TORCH_AVAILABLE
    }


def estimate_memory_requirements(parameter_size: str) -> Dict[str, Any]:
    """
    Estimate memory requirements for different model sizes and precisions.
    
    Args:
        parameter_size: Model parameter size (e.g., "7B", "13B", "70B")
        
    Returns:
        Dictionary with memory estimates for different precisions
    """
    # Parameter count mapping (approximate)
    param_counts = {
        "1B": 1e9,
        "3B": 3e9,
        "7B": 7e9,
        "13B": 13e9,
        "30B": 30e9,
        "65B": 65e9,
        "70B": 70e9,
        "175B": 175e9
    }
    
    param_count = param_counts.get(parameter_size, 0)
    
    if param_count == 0:
        return {
            "parameters": parameter_size,
            "fp32_memory_gb": 0,
            "fp16_memory_gb": 0,
            "int8_memory_gb": 0,
            "int4_memory_gb": 0
        }
    
    # Memory estimates (bytes per parameter + overhead)
    # These are rough estimates and can vary by model architecture
    fp32_memory = param_count * 4 * 1.2  # 4 bytes per param + 20% overhead
    fp16_memory = param_count * 2 * 1.2  # 2 bytes per param + 20% overhead
    int8_memory = param_count * 1 * 1.2  # 1 byte per param + 20% overhead
    int4_memory = param_count * 0.5 * 1.2  # 0.5 bytes per param + 20% overhead
    
    return {
        "parameters": parameter_size,
        "fp32_memory_gb": math.ceil(fp32_memory / (1024**3)),
        "fp16_memory_gb": math.ceil(fp16_memory / (1024**3)),
        "int8_memory_gb": math.ceil(int8_memory / (1024**3)),
        "int4_memory_gb": math.ceil(int4_memory / (1024**3))
    }


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"
    
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    if hours < 24:
        return f"{hours}h {remaining_minutes}m {remaining_seconds}s"
    
    days = int(hours // 24)
    remaining_hours = int(hours % 24)
    
    return f"{days}d {remaining_hours}h {remaining_minutes}m {remaining_seconds}s"


def validate_generation_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate generation configuration parameters.
    
    Args:
        config: Generation configuration dictionary
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate temperature
    if "temperature" in config:
        temp = config["temperature"]
        if not isinstance(temp, (int, float)) or temp < 0 or temp > 2.5:
            errors.append("Temperature must be between 0 and 2.5")
    
    # Validate top_p
    if "top_p" in config:
        top_p = config["top_p"]
        if not isinstance(top_p, (int, float)) or top_p < 0 or top_p > 1:
            errors.append("top_p must be between 0 and 1")
    
    # Validate top_k
    if "top_k" in config:
        top_k = config["top_k"]
        if not isinstance(top_k, int) or top_k < 0:
            errors.append("top_k must be a non-negative integer")
    
    # Validate max_length
    if "max_length" in config:
        max_length = config["max_length"]
        if not isinstance(max_length, int) or max_length <= 0:
            errors.append("max_length must be a positive integer")
    
    # Validate max_new_tokens
    if "max_new_tokens" in config:
        max_new_tokens = config["max_new_tokens"]
        if not isinstance(max_new_tokens, int) or max_new_tokens <= 0:
            errors.append("max_new_tokens must be a positive integer")
    
    # Validate num_return_sequences
    if "num_return_sequences" in config:
        num_seq = config["num_return_sequences"]
        if not isinstance(num_seq, int) or num_seq <= 0:
            errors.append("num_return_sequences must be a positive integer")
    
    # Validate repetition_penalty
    if "repetition_penalty" in config:
        rep_penalty = config["repetition_penalty"]
        if not isinstance(rep_penalty, (int, float)) or rep_penalty <= 0:
            errors.append("repetition_penalty must be positive")
    
    # Validate length_penalty
    if "length_penalty" in config:
        len_penalty = config["length_penalty"]
        if not isinstance(len_penalty, (int, float)):
            errors.append("length_penalty must be a number")
    
    # Validate boolean parameters
    boolean_params = ["do_sample", "early_stopping"]
    for param in boolean_params:
        if param in config and not isinstance(config[param], bool):
            errors.append(f"{param} must be a boolean")
    
    return errors


# Example usage and testing functions
def run_system_diagnostics() -> Dict[str, Any]:
    """
    Run comprehensive system diagnostics for local LLM usage.
    
    Returns:
        Dictionary with diagnostic results
    """
    diagnostics = {
        "system_requirements": check_system_requirements(),
        "model_estimates": {},
        "recommendations": []
    }
    
    # Get memory estimates for common model sizes
    common_sizes = ["7B", "13B", "30B", "70B"]
    for size in common_sizes:
        diagnostics["model_estimates"][size] = estimate_memory_requirements(size)
    
    # Generate recommendations
    sys_req = diagnostics["system_requirements"]
    
    if sys_req["sufficient_memory"] is False:
        diagnostics["recommendations"].append(
            f"Consider upgrading RAM. Current: {sys_req['total_memory_gb']}GB, "
            f"Recommended: {sys_req['recommended_memory_gb']}GB"
        )
    
    if not sys_req["gpu_available"]:
        diagnostics["recommendations"].append(
            "No GPU detected. Models will run on CPU, which may be slower."
        )
    elif sys_req["gpu_memory_gb"] < 8:
        diagnostics["recommendations"].append(
            f"GPU memory is limited ({sys_req['gpu_memory_gb']}GB). "
            "Consider using quantized models for better performance."
        )
    
    if sys_req["available_memory_gb"] < 4:
        diagnostics["recommendations"].append(
            "Low available memory. Close other applications before running large models."
        )
    
    return diagnostics


if __name__ == "__main__":
    # Run diagnostics when executed directly
    diagnostics = run_system_diagnostics()
    
    print("System Diagnostics for Local LLMs")
    print("=" * 40)
    
    sys_req = diagnostics["system_requirements"]
    print(f"Total Memory: {sys_req['total_memory_gb']}GB")
    print(f"Available Memory: {sys_req['available_memory_gb']}GB")
    print(f"GPU Available: {sys_req['gpu_available']}")
    if sys_req['gpu_available']:
        print(f"GPU Memory: {sys_req['gpu_memory_gb']}GB")
    
    print("\nModel Memory Estimates:")
    for size, estimates in diagnostics["model_estimates"].items():
        print(f"  {size} model:")
        print(f"    FP16: {estimates['fp16_memory_gb']}GB")
        print(f"    INT8: {estimates['int8_memory_gb']}GB")
        print(f"    INT4: {estimates['int4_memory_gb']}GB")
    
    if diagnostics["recommendations"]:
        print("\nRecommendations:")
        for rec in diagnostics["recommendations"]:
            print(f"  - {rec}")