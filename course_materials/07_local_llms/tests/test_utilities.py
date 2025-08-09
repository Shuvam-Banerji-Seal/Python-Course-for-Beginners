"""
Unit tests for utility functions and helper methods.

This module contains tests for various utility functions used across
the local LLMs module, including validation, formatting, and helper functions.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Import utility modules
from test_utilities import (
    validate_model_name,
    format_model_size,
    parse_model_info,
    sanitize_filename,
    check_system_requirements,
    estimate_memory_requirements,
    format_duration,
    validate_generation_config
)

from validate_utilities import (
    validate_ollama_response,
    validate_transformers_config,
    check_model_compatibility,
    validate_prompt_template,
    sanitize_model_output
)


class TestUtilityFunctions:
    """Test cases for general utility functions."""
    
    def test_validate_model_name_valid(self):
        """Test model name validation with valid names."""
        valid_names = [
            "llama2:7b",
            "codellama:13b-instruct",
            "mistral:latest",
            "custom-model:v1.0",
            "organization/model-name:tag"
        ]
        
        for name in valid_names:
            assert validate_model_name(name) is True
    
    def test_validate_model_name_invalid(self):
        """Test model name validation with invalid names."""
        invalid_names = [
            "",
            "   ",
            "model with spaces",
            "model@invalid",
            "model#tag",
            "model:tag:extra",
            "model:",
            ":tag"
        ]
        
        for name in invalid_names:
            assert validate_model_name(name) is False
    
    def test_format_model_size_bytes(self):
        """Test model size formatting from bytes."""
        test_cases = [
            (1024, "1.0 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB"),
            (1099511627776, "1.0 TB"),
            (1536, "1.5 KB"),
            (3825819519, "3.6 GB"),
            (0, "0 B"),
            (512, "512 B")
        ]
        
        for size_bytes, expected in test_cases:
            assert format_model_size(size_bytes) == expected
    
    def test_parse_model_info_valid(self):
        """Test parsing valid model information."""
        model_data = {
            "name": "llama2:7b",
            "size": 3825819519,
            "digest": "sha256:abc123",
            "modified_at": "2024-01-01T00:00:00Z",
            "details": {
                "parameter_size": "7B",
                "quantization": "Q4_0"
            }
        }
        
        parsed = parse_model_info(model_data)
        
        assert parsed["name"] == "llama2:7b"
        assert parsed["size_formatted"] == "3.6 GB"
        assert parsed["parameter_size"] == "7B"
        assert parsed["quantization"] == "Q4_0"
        assert "modified_at" in parsed
    
    def test_parse_model_info_minimal(self):
        """Test parsing minimal model information."""
        model_data = {
            "name": "simple:model",
            "size": 1024,
            "digest": "sha256:def456",
            "modified_at": "2024-01-01T00:00:00Z"
        }
        
        parsed = parse_model_info(model_data)
        
        assert parsed["name"] == "simple:model"
        assert parsed["size_formatted"] == "1.0 KB"
        assert parsed["parameter_size"] == "Unknown"
        assert parsed["quantization"] == "Unknown"
    
    def test_sanitize_filename_valid(self):
        """Test filename sanitization with valid names."""
        test_cases = [
            ("model_name", "model_name"),
            ("model-name", "model-name"),
            ("model.name", "model.name"),
            ("model123", "model123")
        ]
        
        for input_name, expected in test_cases:
            assert sanitize_filename(input_name) == expected
    
    def test_sanitize_filename_invalid_chars(self):
        """Test filename sanitization with invalid characters."""
        test_cases = [
            ("model/name", "model_name"),
            ("model\\name", "model_name"),
            ("model:name", "model_name"),
            ("model*name", "model_name"),
            ("model?name", "model_name"),
            ("model\"name", "model_name"),
            ("model<name>", "model_name_"),
            ("model|name", "model_name")
        ]
        
        for input_name, expected in test_cases:
            assert sanitize_filename(input_name) == expected
    
    def test_sanitize_filename_empty(self):
        """Test filename sanitization with empty or whitespace names."""
        test_cases = [
            ("", "unnamed"),
            ("   ", "unnamed"),
            ("\t\n", "unnamed")
        ]
        
        for input_name, expected in test_cases:
            assert sanitize_filename(input_name) == expected
    
    @patch('psutil.virtual_memory')
    @patch('torch.cuda.is_available')
    @patch('torch.cuda.get_device_properties')
    def test_check_system_requirements_sufficient(self, mock_get_props, mock_cuda_available, mock_virtual_memory):
        """Test system requirements check with sufficient resources."""
        # Mock system memory (16GB)
        mock_vm = Mock()
        mock_vm.total = 16 * 1024**3
        mock_vm.available = 12 * 1024**3
        mock_virtual_memory.return_value = mock_vm
        
        # Mock CUDA availability and GPU memory
        mock_cuda_available.return_value = True
        mock_props = Mock()
        mock_props.total_memory = 8 * 1024**3  # 8GB GPU
        mock_get_props.return_value = mock_props
        
        requirements = check_system_requirements()
        
        assert requirements["sufficient_memory"] is True
        assert requirements["gpu_available"] is True
        assert requirements["total_memory_gb"] == 16
        assert requirements["available_memory_gb"] == 12
        assert requirements["gpu_memory_gb"] == 8
    
    @patch('psutil.virtual_memory')
    @patch('torch.cuda.is_available')
    def test_check_system_requirements_insufficient(self, mock_cuda_available, mock_virtual_memory):
        """Test system requirements check with insufficient resources."""
        # Mock system memory (4GB)
        mock_vm = Mock()
        mock_vm.total = 4 * 1024**3
        mock_vm.available = 1 * 1024**3
        mock_virtual_memory.return_value = mock_vm
        
        # No CUDA
        mock_cuda_available.return_value = False
        
        requirements = check_system_requirements()
        
        assert requirements["sufficient_memory"] is False
        assert requirements["gpu_available"] is False
        assert requirements["total_memory_gb"] == 4
        assert requirements["available_memory_gb"] == 1
        assert requirements["gpu_memory_gb"] == 0
    
    def test_estimate_memory_requirements_7b_model(self):
        """Test memory estimation for 7B parameter model."""
        estimates = estimate_memory_requirements("7B")
        
        assert estimates["parameters"] == "7B"
        assert estimates["fp16_memory_gb"] >= 13  # ~14GB for 7B model in fp16
        assert estimates["fp32_memory_gb"] >= 26  # ~28GB for 7B model in fp32
        assert estimates["int8_memory_gb"] >= 6   # ~7GB for 7B model in int8
        assert estimates["int4_memory_gb"] >= 3   # ~4GB for 7B model in int4
    
    def test_estimate_memory_requirements_13b_model(self):
        """Test memory estimation for 13B parameter model."""
        estimates = estimate_memory_requirements("13B")
        
        assert estimates["parameters"] == "13B"
        assert estimates["fp16_memory_gb"] >= 24  # ~26GB for 13B model in fp16
        assert estimates["fp32_memory_gb"] >= 48  # ~52GB for 13B model in fp32
        assert estimates["int8_memory_gb"] >= 12  # ~13GB for 13B model in int8
        assert estimates["int4_memory_gb"] >= 6   # ~7GB for 13B model in int4
    
    def test_estimate_memory_requirements_unknown(self):
        """Test memory estimation for unknown model size."""
        estimates = estimate_memory_requirements("Unknown")
        
        assert estimates["parameters"] == "Unknown"
        assert estimates["fp16_memory_gb"] == 0
        assert estimates["fp32_memory_gb"] == 0
        assert estimates["int8_memory_gb"] == 0
        assert estimates["int4_memory_gb"] == 0
    
    def test_format_duration_seconds(self):
        """Test duration formatting for various time periods."""
        test_cases = [
            (0.5, "0.50s"),
            (1.0, "1.00s"),
            (59.9, "59.90s"),
            (60.0, "1m 0s"),
            (61.5, "1m 1s"),
            (3600.0, "1h 0m 0s"),
            (3661.5, "1h 1m 1s"),
            (90061.5, "1d 1h 1m 1s")
        ]
        
        for duration, expected in test_cases:
            assert format_duration(duration) == expected
    
    def test_validate_generation_config_valid(self):
        """Test validation of valid generation configurations."""
        valid_configs = [
            {"temperature": 0.7, "top_p": 0.9, "max_length": 100},
            {"temperature": 0.0, "top_p": 1.0, "max_length": 1},
            {"temperature": 2.0, "top_p": 0.1, "max_length": 2048},
            {"do_sample": False, "max_length": 50},
            {"num_return_sequences": 3, "max_length": 100}
        ]
        
        for config in valid_configs:
            errors = validate_generation_config(config)
            assert len(errors) == 0
    
    def test_validate_generation_config_invalid(self):
        """Test validation of invalid generation configurations."""
        invalid_configs = [
            {"temperature": -0.1},  # Negative temperature
            {"temperature": 3.0},   # Temperature too high
            {"top_p": -0.1},        # Negative top_p
            {"top_p": 1.1},         # top_p > 1
            {"max_length": 0},      # Zero max_length
            {"max_length": -1},     # Negative max_length
            {"num_return_sequences": 0},  # Zero sequences
            {"top_k": -1}           # Negative top_k
        ]
        
        for config in invalid_configs:
            errors = validate_generation_config(config)
            assert len(errors) > 0


class TestValidationUtilities:
    """Test cases for validation utility functions."""
    
    def test_validate_ollama_response_valid(self):
        """Test validation of valid Ollama responses."""
        valid_responses = [
            {"response": "Hello, how can I help you?"},
            {"response": "Here's the answer to your question.", "done": True},
            {"response": "", "done": False},
            {"model": "llama2:7b", "response": "Response text"}
        ]
        
        for response in valid_responses:
            assert validate_ollama_response(response) is True
    
    def test_validate_ollama_response_invalid(self):
        """Test validation of invalid Ollama responses."""
        invalid_responses = [
            {},  # Empty response
            {"error": "Model not found"},  # Error response
            {"status": "loading"},  # Status without response
            None,  # None response
            "string response"  # String instead of dict
        ]
        
        for response in invalid_responses:
            assert validate_ollama_response(response) is False
    
    def test_validate_transformers_config_valid(self):
        """Test validation of valid Transformers configurations."""
        valid_configs = [
            {
                "model_name": "microsoft/DialoGPT-small",
                "device": "auto",
                "torch_dtype": "auto"
            },
            {
                "model_name": "gpt2",
                "device": "cpu",
                "torch_dtype": "float32",
                "trust_remote_code": False
            },
            {
                "model_name": "custom/model",
                "device": "cuda:0",
                "torch_dtype": "float16",
                "quantization_config": {"load_in_8bit": True}
            }
        ]
        
        for config in valid_configs:
            errors = validate_transformers_config(config)
            assert len(errors) == 0
    
    def test_validate_transformers_config_invalid(self):
        """Test validation of invalid Transformers configurations."""
        invalid_configs = [
            {},  # Missing model_name
            {"model_name": ""},  # Empty model_name
            {"model_name": "test", "device": "invalid_device"},  # Invalid device
            {"model_name": "test", "torch_dtype": "invalid_dtype"},  # Invalid dtype
            {"model_name": "test", "trust_remote_code": "yes"}  # Wrong type for boolean
        ]
        
        for config in invalid_configs:
            errors = validate_transformers_config(config)
            assert len(errors) > 0
    
    def test_check_model_compatibility_compatible(self):
        """Test model compatibility check for compatible models."""
        compatible_cases = [
            ("llama2:7b", {"total_memory_gb": 16, "gpu_available": True}),
            ("codellama:13b", {"total_memory_gb": 32, "gpu_available": True}),
            ("mistral:7b", {"total_memory_gb": 8, "gpu_available": False}),  # CPU only
        ]
        
        for model_name, system_info in compatible_cases:
            compatibility = check_model_compatibility(model_name, system_info)
            assert compatibility["compatible"] is True
            assert len(compatibility["warnings"]) == 0 or "performance" in compatibility["warnings"][0].lower()
    
    def test_check_model_compatibility_incompatible(self):
        """Test model compatibility check for incompatible models."""
        incompatible_cases = [
            ("llama2:70b", {"total_memory_gb": 8, "gpu_available": False}),  # Too large
            ("codellama:34b", {"total_memory_gb": 16, "gpu_available": True}),  # Insufficient memory
        ]
        
        for model_name, system_info in incompatible_cases:
            compatibility = check_model_compatibility(model_name, system_info)
            assert compatibility["compatible"] is False
            assert len(compatibility["errors"]) > 0
    
    def test_validate_prompt_template_valid(self):
        """Test validation of valid prompt templates."""
        valid_template = {
            "name": "test_template",
            "category": "assistant",
            "system_prompt": "You are a helpful assistant.",
            "user_template": "Help me with {task}.",
            "description": "A test template"
        }
        
        errors = validate_prompt_template(valid_template)
        assert len(errors) == 0
    
    def test_validate_prompt_template_invalid(self):
        """Test validation of invalid prompt templates."""
        invalid_templates = [
            {},  # Empty template
            {"name": ""},  # Empty name
            {"name": "test"},  # Missing required fields
            {"name": "test", "category": "invalid", "system_prompt": "", "user_template": ""},  # Invalid category
            {"name": "test", "category": "assistant", "system_prompt": "", "user_template": ""}  # Empty prompts
        ]
        
        for template in invalid_templates:
            errors = validate_prompt_template(template)
            assert len(errors) > 0
    
    def test_sanitize_model_output_clean(self):
        """Test sanitization of clean model output."""
        clean_outputs = [
            "This is a normal response.",
            "Here's some code:\n```python\nprint('hello')\n```",
            "Mathematical formula: E = mc²",
            "List:\n1. Item one\n2. Item two"
        ]
        
        for output in clean_outputs:
            sanitized = sanitize_model_output(output)
            assert sanitized == output  # Should be unchanged
    
    def test_sanitize_model_output_with_issues(self):
        """Test sanitization of model output with potential issues."""
        problematic_outputs = [
            "Response with \x00 null bytes",
            "Response with excessive\n\n\n\n\n\nnewlines",
            "Response with    excessive    spaces",
            "Response with control\x01characters\x02here"
        ]
        
        for output in problematic_outputs:
            sanitized = sanitize_model_output(output)
            assert "\x00" not in sanitized  # Null bytes removed
            assert "\x01" not in sanitized  # Control characters removed
            assert "\x02" not in sanitized
            # Should have normalized whitespace
            assert "    " not in sanitized or sanitized.count("\n\n\n") == 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])