"""
Validation utilities for the local LLMs module.

This module provides validation functions for responses, configurations,
model compatibility, and output sanitization.
"""

import re
from typing import Dict, List, Any, Optional, Union


def validate_ollama_response(response: Any) -> bool:
    """
    Validate an Ollama API response.
    
    Args:
        response: Response from Ollama API
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(response, dict):
        return False
    
    # Check for error responses
    if "error" in response:
        return False
    
    # Valid response should have either 'response' field or be a status update
    if "response" in response:
        return True
    
    # Status updates during model pulling are also valid
    if "status" in response and response["status"] in ["downloading", "verifying", "success"]:
        return True
    
    return False


def validate_transformers_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate a Transformers model configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Required fields
    if "model_name" not in config or not config["model_name"]:
        errors.append("model_name is required and cannot be empty")
    
    # Validate device
    if "device" in config:
        device = config["device"]
        valid_devices = ["auto", "cpu", "cuda", "mps"]
        # Also allow specific CUDA devices like "cuda:0"
        if device not in valid_devices and not re.match(r"^cuda:\d+$", device):
            errors.append(f"Invalid device: {device}. Must be one of {valid_devices} or 'cuda:N'")
    
    # Validate torch_dtype
    if "torch_dtype" in config:
        dtype = config["torch_dtype"]
        valid_dtypes = ["auto", "float16", "bfloat16", "float32", "int8"]
        if dtype not in valid_dtypes:
            errors.append(f"Invalid torch_dtype: {dtype}. Must be one of {valid_dtypes}")
    
    # Validate boolean fields
    boolean_fields = ["trust_remote_code", "use_cache", "low_cpu_mem_usage"]
    for field in boolean_fields:
        if field in config and not isinstance(config[field], bool):
            errors.append(f"{field} must be a boolean")
    
    # Validate quantization_config if present
    if "quantization_config" in config and config["quantization_config"] is not None:
        quant_config = config["quantization_config"]
        if not isinstance(quant_config, dict):
            errors.append("quantization_config must be a dictionary")
        else:
            # Check for conflicting quantization settings
            if quant_config.get("load_in_4bit") and quant_config.get("load_in_8bit"):
                errors.append("Cannot use both 4-bit and 8-bit quantization")
    
    return errors


def check_model_compatibility(model_name: str, system_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if a model is compatible with the current system.
    
    Args:
        model_name: Name of the model to check
        system_info: System information dictionary
        
    Returns:
        Dictionary with compatibility information
    """
    compatibility = {
        "compatible": True,
        "errors": [],
        "warnings": [],
        "recommendations": []
    }
    
    # Extract model size from name (rough estimation)
    model_size = "Unknown"
    if ":7b" in model_name.lower() or "7b" in model_name.lower():
        model_size = "7B"
    elif ":13b" in model_name.lower() or "13b" in model_name.lower():
        model_size = "13B"
    elif ":30b" in model_name.lower() or "30b" in model_name.lower():
        model_size = "30B"
    elif ":70b" in model_name.lower() or "70b" in model_name.lower():
        model_size = "70B"
    
    # Memory requirements (rough estimates in GB)
    memory_requirements = {
        "7B": {"min": 8, "recommended": 16},
        "13B": {"min": 16, "recommended": 32},
        "30B": {"min": 32, "recommended": 64},
        "70B": {"min": 64, "recommended": 128}
    }
    
    total_memory = system_info.get("total_memory_gb", 0)
    gpu_available = system_info.get("gpu_available", False)
    
    if model_size in memory_requirements:
        req = memory_requirements[model_size]
        
        # Check minimum requirements
        if total_memory < req["min"]:
            compatibility["compatible"] = False
            compatibility["errors"].append(
                f"Insufficient memory for {model_size} model. "
                f"Required: {req['min']}GB, Available: {total_memory}GB"
            )
        elif total_memory < req["recommended"]:
            compatibility["warnings"].append(
                f"Memory below recommended for {model_size} model. "
                f"Recommended: {req['recommended']}GB, Available: {total_memory}GB. "
                f"Performance may be degraded."
            )
        
        # GPU recommendations
        if not gpu_available and model_size in ["30B", "70B"]:
            compatibility["warnings"].append(
                f"Large model ({model_size}) without GPU acceleration will be very slow."
            )
            compatibility["recommendations"].append(
                "Consider using a GPU or a smaller quantized model for better performance."
            )
        elif not gpu_available:
            compatibility["recommendations"].append(
                "Consider using quantized models (INT8/INT4) for better CPU performance."
            )
    
    return compatibility


def validate_prompt_template(template: Dict[str, Any]) -> List[str]:
    """
    Validate a prompt template structure.
    
    Args:
        template: Template dictionary to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Required fields
    required_fields = ["name", "category", "system_prompt", "user_template"]
    for field in required_fields:
        if field not in template:
            errors.append(f"Missing required field: {field}")
        elif not template[field] or (isinstance(template[field], str) and not template[field].strip()):
            errors.append(f"Field '{field}' cannot be empty")
    
    # Validate category
    if "category" in template:
        valid_categories = [
            "assistant", "creative", "technical", "educational", 
            "analysis", "conversation", "custom"
        ]
        if template["category"] not in valid_categories:
            errors.append(f"Invalid category: {template['category']}. Must be one of {valid_categories}")
    
    # Validate parameter consistency
    if "system_prompt" in template and "user_template" in template:
        system_params = set(re.findall(r'\{(\w+)\}', template["system_prompt"]))
        user_params = set(re.findall(r'\{(\w+)\}', template["user_template"]))
        all_params = system_params.union(user_params)
        
        # Check if parameters field matches template parameters
        if "parameters" in template and isinstance(template["parameters"], dict):
            declared_params = set(template["parameters"].keys())
            
            # Warn about undeclared parameters
            undeclared = all_params - declared_params
            if undeclared:
                errors.append(f"Template uses undeclared parameters: {', '.join(undeclared)}")
            
            # Warn about unused declared parameters
            unused = declared_params - all_params
            if unused:
                errors.append(f"Declared parameters not used in template: {', '.join(unused)}")
    
    # Validate example inputs if present
    if "example_inputs" in template and isinstance(template["example_inputs"], list):
        for i, example in enumerate(template["example_inputs"]):
            if not isinstance(example, dict):
                errors.append(f"Example input {i} must be a dictionary")
    
    # Validate tags if present
    if "tags" in template:
        if not isinstance(template["tags"], list):
            errors.append("Tags must be a list")
        elif not all(isinstance(tag, str) for tag in template["tags"]):
            errors.append("All tags must be strings")
    
    return errors


def sanitize_model_output(output: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize model output by removing problematic characters and formatting.
    
    Args:
        output: Raw model output
        max_length: Maximum length to truncate to (optional)
        
    Returns:
        Sanitized output
    """
    if not isinstance(output, str):
        return str(output)
    
    # Remove null bytes and other control characters (except newlines and tabs)
    sanitized = ''.join(
        char for char in output 
        if ord(char) >= 32 or char in '\n\r\t'
    )
    
    # Normalize excessive whitespace
    # Replace multiple consecutive newlines with at most 2
    sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
    
    # Replace multiple consecutive spaces with single space
    sanitized = re.sub(r' {2,}', ' ', sanitized)
    
    # Remove leading/trailing whitespace from each line while preserving structure
    lines = sanitized.split('\n')
    sanitized_lines = [line.rstrip() for line in lines]
    sanitized = '\n'.join(sanitized_lines)
    
    # Truncate if max_length is specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip() + "..."
    
    return sanitized


def validate_api_response_format(response: Dict[str, Any], expected_fields: List[str]) -> List[str]:
    """
    Validate that an API response contains expected fields.
    
    Args:
        response: API response dictionary
        expected_fields: List of expected field names
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not isinstance(response, dict):
        errors.append("Response must be a dictionary")
        return errors
    
    # Check for required fields
    for field in expected_fields:
        if field not in response:
            errors.append(f"Missing required field: {field}")
    
    # Check for error field
    if "error" in response:
        errors.append(f"API returned error: {response['error']}")
    
    return errors


def validate_model_parameters(parameters: Dict[str, Any]) -> List[str]:
    """
    Validate model generation parameters.
    
    Args:
        parameters: Dictionary of model parameters
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Temperature validation
    if "temperature" in parameters:
        temp = parameters["temperature"]
        if not isinstance(temp, (int, float)):
            errors.append("Temperature must be a number")
        elif temp < 0 or temp > 2.0:
            errors.append("Temperature must be between 0 and 2.0")
    
    # Top-p validation
    if "top_p" in parameters:
        top_p = parameters["top_p"]
        if not isinstance(top_p, (int, float)):
            errors.append("top_p must be a number")
        elif top_p < 0 or top_p > 1.0:
            errors.append("top_p must be between 0 and 1.0")
    
    # Top-k validation
    if "top_k" in parameters:
        top_k = parameters["top_k"]
        if not isinstance(top_k, int):
            errors.append("top_k must be an integer")
        elif top_k < 0:
            errors.append("top_k must be non-negative")
    
    # Repeat penalty validation
    if "repeat_penalty" in parameters:
        repeat_penalty = parameters["repeat_penalty"]
        if not isinstance(repeat_penalty, (int, float)):
            errors.append("repeat_penalty must be a number")
        elif repeat_penalty <= 0:
            errors.append("repeat_penalty must be positive")
    
    # Seed validation
    if "seed" in parameters:
        seed = parameters["seed"]
        if seed is not None and not isinstance(seed, int):
            errors.append("seed must be an integer or None")
    
    # Stop sequences validation
    if "stop" in parameters:
        stop = parameters["stop"]
        if stop is not None:
            if not isinstance(stop, list):
                errors.append("stop must be a list or None")
            elif not all(isinstance(s, str) for s in stop):
                errors.append("All stop sequences must be strings")
    
    return errors


def check_prompt_injection(prompt: str) -> Dict[str, Any]:
    """
    Check for potential prompt injection attempts.
    
    Args:
        prompt: User prompt to check
        
    Returns:
        Dictionary with injection check results
    """
    result = {
        "safe": True,
        "warnings": [],
        "risk_level": "low"
    }
    
    # Patterns that might indicate prompt injection
    suspicious_patterns = [
        r"ignore\s+previous\s+instructions",
        r"forget\s+everything\s+above",
        r"system\s*:\s*you\s+are",
        r"new\s+instructions\s*:",
        r"override\s+your\s+programming",
        r"act\s+as\s+if\s+you\s+are",
        r"pretend\s+to\s+be",
        r"roleplay\s+as",
        r"jailbreak",
        r"developer\s+mode"
    ]
    
    prompt_lower = prompt.lower()
    
    for pattern in suspicious_patterns:
        if re.search(pattern, prompt_lower):
            result["safe"] = False
            result["warnings"].append(f"Potential prompt injection detected: {pattern}")
            result["risk_level"] = "high"
    
    # Check for excessive repetition (potential DoS)
    words = prompt.split()
    if len(words) > 100:
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        max_count = max(word_counts.values())
        if max_count > len(words) * 0.3:  # More than 30% repetition
            result["warnings"].append("Excessive word repetition detected")
            result["risk_level"] = "medium"
    
    # Check for very long prompts (potential resource exhaustion)
    if len(prompt) > 10000:
        result["warnings"].append("Unusually long prompt detected")
        if result["risk_level"] == "low":
            result["risk_level"] = "medium"
    
    return result


def validate_file_path(file_path: str, allowed_extensions: Optional[List[str]] = None) -> List[str]:
    """
    Validate a file path for security and format.
    
    Args:
        file_path: File path to validate
        allowed_extensions: List of allowed file extensions (optional)
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not file_path or not file_path.strip():
        errors.append("File path cannot be empty")
        return errors
    
    # Check for path traversal attempts
    if ".." in file_path or file_path.startswith("/"):
        errors.append("Path traversal detected in file path")
    
    # Check for null bytes
    if "\x00" in file_path:
        errors.append("Null bytes not allowed in file path")
    
    # Validate extension if specified
    if allowed_extensions:
        file_ext = file_path.lower().split('.')[-1] if '.' in file_path else ""
        if file_ext not in [ext.lower().lstrip('.') for ext in allowed_extensions]:
            errors.append(f"File extension '{file_ext}' not allowed. Allowed: {allowed_extensions}")
    
    # Check for reserved names (Windows)
    reserved_names = ["CON", "PRN", "AUX", "NUL"] + [f"COM{i}" for i in range(1, 10)] + [f"LPT{i}" for i in range(1, 10)]
    filename = file_path.split('/')[-1].split('\\')[-1].split('.')[0].upper()
    if filename in reserved_names:
        errors.append(f"Reserved filename: {filename}")
    
    return errors


# Example usage and testing functions
def run_validation_tests() -> Dict[str, Any]:
    """
    Run validation tests on sample data.
    
    Returns:
        Dictionary with test results
    """
    results = {
        "ollama_response_tests": [],
        "transformers_config_tests": [],
        "prompt_template_tests": [],
        "output_sanitization_tests": []
    }
    
    # Test Ollama response validation
    test_responses = [
        {"response": "Hello world"},  # Valid
        {"error": "Model not found"},  # Invalid
        {"status": "downloading"},  # Valid
        "not a dict"  # Invalid
    ]
    
    for response in test_responses:
        is_valid = validate_ollama_response(response)
        results["ollama_response_tests"].append({
            "response": str(response)[:50],
            "valid": is_valid
        })
    
    # Test Transformers config validation
    test_configs = [
        {"model_name": "gpt2", "device": "auto"},  # Valid
        {"model_name": "", "device": "auto"},  # Invalid
        {"model_name": "gpt2", "device": "invalid"},  # Invalid
    ]
    
    for config in test_configs:
        errors = validate_transformers_config(config)
        results["transformers_config_tests"].append({
            "config": str(config)[:50],
            "errors": errors
        })
    
    return results


if __name__ == "__main__":
    # Run validation tests when executed directly
    test_results = run_validation_tests()
    
    print("Validation Utilities Test Results")
    print("=" * 40)
    
    for test_type, tests in test_results.items():
        print(f"\n{test_type.replace('_', ' ').title()}:")
        for test in tests:
            if "valid" in test:
                status = "✓" if test["valid"] else "✗"
                print(f"  {status} {test.get('response', test.get('config', 'Unknown'))}")
            elif "errors" in test:
                status = "✓" if not test["errors"] else "✗"
                print(f"  {status} {test.get('config', 'Unknown')}")
                if test["errors"]:
                    for error in test["errors"]:
                        print(f"    - {error}")