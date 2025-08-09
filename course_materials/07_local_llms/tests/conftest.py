"""
Pytest configuration and fixtures for local LLMs tests.

This module provides common fixtures and configuration for all test modules.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add the utils directory to the Python path
utils_path = Path(__file__).parent.parent / "utils"
sys.path.insert(0, str(utils_path))


@pytest.fixture
def mock_transformers():
    """Mock transformers library components."""
    with patch('transformers_manager.TRANSFORMERS_AVAILABLE', True):
        with patch('transformers_manager.AutoTokenizer') as mock_tokenizer:
            with patch('transformers_manager.AutoModelForCausalLM') as mock_model:
                with patch('transformers_manager.BitsAndBytesConfig') as mock_bnb:
                    yield {
                        'tokenizer': mock_tokenizer,
                        'model': mock_model,
                        'bnb_config': mock_bnb
                    }


@pytest.fixture
def mock_torch():
    """Mock torch library components."""
    with patch('torch.cuda.is_available') as mock_cuda_available:
        with patch('torch.cuda.device_count') as mock_device_count:
            with patch('torch.cuda.get_device_properties') as mock_get_props:
                with patch('torch.cuda.memory_allocated') as mock_memory_allocated:
                    with patch('torch.cuda.empty_cache') as mock_empty_cache:
                        mock_cuda_available.return_value = False
                        mock_device_count.return_value = 0
                        mock_memory_allocated.return_value = 0
                        
                        yield {
                            'cuda_available': mock_cuda_available,
                            'device_count': mock_device_count,
                            'get_props': mock_get_props,
                            'memory_allocated': mock_memory_allocated,
                            'empty_cache': mock_empty_cache
                        }


@pytest.fixture
def mock_psutil():
    """Mock psutil library components."""
    with patch('transformers_manager.psutil') as mock_psutil_module:
        mock_vm = Mock()
        mock_vm.used = 1024 * 1024 * 1024  # 1GB
        mock_vm.percent = 50.0
        mock_psutil_module.virtual_memory.return_value = mock_vm
        
        yield mock_psutil_module


@pytest.fixture
def mock_requests():
    """Mock requests library components."""
    with patch('requests.Session') as mock_session_class:
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        yield mock_session


@pytest.fixture
def sample_model_info():
    """Sample model information for testing."""
    return {
        "name": "llama2:7b",
        "size": 3825819519,
        "digest": "sha256:abc123def456",
        "modified_at": "2024-01-01T00:00:00Z",
        "details": {
            "parameter_size": "7B",
            "quantization": "Q4_0"
        }
    }


@pytest.fixture
def sample_prompt_template():
    """Sample prompt template for testing."""
    from prompt_template import PromptTemplate, PromptCategory
    
    return PromptTemplate(
        name="test_template",
        category=PromptCategory.ASSISTANT,
        system_prompt="You are a {role} assistant with expertise in {domain}.",
        user_template="Please help me with {task}.",
        description="A test template for unit testing",
        parameters={"role": str, "domain": str, "task": str},
        example_inputs=[
            {"role": "helpful", "domain": "Python", "task": "debugging code"}
        ],
        expected_behavior="Provides helpful assistance in the specified domain",
        tags=["test", "assistant", "helpful"]
    )


@pytest.fixture
def temp_templates_dir(tmp_path):
    """Create a temporary directory with sample template files."""
    import json
    from prompt_template import PromptCategory
    
    # Create sample template files
    template1_data = {
        "name": "assistant_template",
        "category": "assistant",
        "system_prompt": "You are a helpful assistant.",
        "user_template": "Help me with {task}.",
        "description": "General assistant template",
        "tags": ["assistant", "general"]
    }
    
    template2_data = {
        "name": "creative_template",
        "category": "creative",
        "system_prompt": "You are a creative writer.",
        "user_template": "Write a {type} about {topic}.",
        "description": "Creative writing template",
        "tags": ["creative", "writing"]
    }
    
    # Write template files
    (tmp_path / "assistant_template.json").write_text(json.dumps(template1_data, indent=2))
    (tmp_path / "creative_template.json").write_text(json.dumps(template2_data, indent=2))
    
    # Create a non-JSON file (should be ignored)
    (tmp_path / "readme.txt").write_text("This is not a template file")
    
    return tmp_path


# Pytest markers for different test categories
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (may require external services)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "gpu: marks tests that require GPU"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark integration tests
        if "integration" in item.name.lower() or "real_server" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        
        # Mark slow tests
        if "benchmark" in item.name.lower() or "performance" in item.name.lower():
            item.add_marker(pytest.mark.slow)
        
        # Mark GPU tests
        if "gpu" in item.name.lower() or "cuda" in item.name.lower():
            item.add_marker(pytest.mark.gpu)


# Skip integration tests by default unless explicitly requested
def pytest_runtest_setup(item):
    """Setup function to handle test skipping."""
    if "integration" in item.keywords:
        if not item.config.getoption("--run-integration", default=False):
            pytest.skip("Integration tests skipped (use --run-integration to run)")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that require external services"
    )
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run slow tests"
    )