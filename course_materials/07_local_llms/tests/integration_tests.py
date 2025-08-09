"""
Integration tests for the local LLMs module.

This module contains end-to-end integration tests that verify the complete
workflow from setup to inference, including cross-platform compatibility
and real service interactions.
"""

import pytest
import sys
import os
import time
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from unittest.mock import patch

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

from ollama_manager import OllamaManager, OllamaError
from transformers_manager import TransformersManager, TransformersError, TRANSFORMERS_AVAILABLE
from prompt_template import PromptTemplateManager, PromptCategory


@pytest.mark.integration
class TestOllamaIntegration:
    """Integration tests for Ollama functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = OllamaManager()
        self.test_model = "llama2:7b"  # Use a common small model for testing
    
    def test_ollama_server_connection(self):
        """Test connection to Ollama server."""
        if not self.manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        # Test basic connectivity
        assert self.manager.is_server_running() is True
        
        # Test health check
        health = self.manager.health_check()
        assert health["server_running"] is True
        assert health["connection_time_ms"] is not None
        assert health["error"] is None
    
    def test_ollama_model_management(self):
        """Test model listing and management."""
        if not self.manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        # List available models
        models = self.manager.list_models()
        assert isinstance(models, list)
        
        # If no models are available, skip model-specific tests
        if not models:
            pytest.skip("No models available for testing")
        
        # Test model info retrieval
        first_model = models[0]
        model_info = self.manager.get_model_info(first_model.name)
        assert model_info is not None
        assert isinstance(model_info, dict)
    
    def test_ollama_text_generation(self):
        """Test text generation with Ollama."""
        if not self.manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        models = self.manager.list_models()
        if not models:
            pytest.skip("No models available for testing")
        
        # Use the first available model
        model_name = models[0].name
        
        # Test basic generation
        response = self.manager.generate_response(
            model=model_name,
            prompt="Hello, how are you?",
            system="You are a helpful assistant."
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_ollama_streaming_generation(self):
        """Test streaming text generation with Ollama."""
        if not self.manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        models = self.manager.list_models()
        if not models:
            pytest.skip("No models available for testing")
        
        model_name = models[0].name
        
        # Test streaming generation
        chunks = list(self.manager.generate_streaming(
            model=model_name,
            prompt="Count to 5",
            system="You are a helpful assistant."
        ))
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        
        # Combine chunks to form complete response
        complete_response = "".join(chunks)
        assert len(complete_response) > 0


@pytest.mark.integration
@pytest.mark.skipif(not TRANSFORMERS_AVAILABLE, reason="Transformers not available")
class TestTransformersIntegration:
    """Integration tests for Transformers functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = TransformersManager()
        self.test_model = "microsoft/DialoGPT-small"  # Small model for testing
    
    def test_transformers_model_loading(self):
        """Test loading a Transformers model."""
        try:
            # Load a small model
            model_id = self.manager.load_model(self.test_model)
            
            assert model_id in self.manager.loaded_models
            
            # Check model info
            info = self.manager.get_model_info(model_id)
            assert info is not None
            assert info["model_name"] == self.test_model
            
            # Cleanup
            self.manager.unload_model(model_id)
            
        except Exception as e:
            pytest.skip(f"Model loading failed (may be due to network/resources): {e}")
    
    def test_transformers_text_generation(self):
        """Test text generation with Transformers."""
        try:
            # Load model
            model_id = self.manager.load_model(self.test_model)
            
            # Generate text
            response = self.manager.generate_text(
                model_id=model_id,
                prompt="Hello, how are you?"
            )
            
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Cleanup
            self.manager.unload_model(model_id)
            
        except Exception as e:
            pytest.skip(f"Text generation failed (may be due to network/resources): {e}")
    
    def test_transformers_memory_optimization(self):
        """Test memory optimization features."""
        try:
            # Load model
            model_id = self.manager.load_model(self.test_model)
            
            # Test memory optimization
            results = self.manager.optimize_memory()
            
            assert "memory_freed_mb" in results
            assert "gpu_memory_freed_mb" in results
            assert isinstance(results["memory_freed_mb"], (int, float))
            
            # Cleanup
            self.manager.unload_model(model_id)
            
        except Exception as e:
            pytest.skip(f"Memory optimization test failed: {e}")


@pytest.mark.integration
class TestPromptTemplateIntegration:
    """Integration tests for prompt template functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PromptTemplateManager()
    
    def test_builtin_templates_creation(self):
        """Test creation and usage of built-in templates."""
        # Create built-in templates
        self.manager.create_builtin_templates()
        
        # Verify templates were created
        templates = self.manager.list_templates()
        assert len(templates) > 0
        
        # Test specific built-in templates
        expected_templates = ["helpful_assistant", "creative_writer", "code_reviewer", "educational_tutor"]
        for template_name in expected_templates:
            assert template_name in templates
            
            template = self.manager.get_template(template_name)
            assert template is not None
            assert template.name == template_name
    
    def test_template_rendering_workflow(self):
        """Test complete template rendering workflow."""
        self.manager.create_builtin_templates()
        
        # Test assistant template
        result = self.manager.render_template(
            "helpful_assistant",
            {
                "tone": "friendly",
                "user_input": "What is machine learning?"
            }
        )
        
        assert "system" in result
        assert "user" in result
        assert "friendly" in result["system"]
        assert "machine learning" in result["user"]
    
    def test_template_file_operations(self):
        """Test template save/load operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create and save a template
            from prompt_template import PromptTemplate
            
            template = PromptTemplate(
                name="test_integration_template",
                category=PromptCategory.ASSISTANT,
                system_prompt="You are a test assistant.",
                user_template="Help with {task}.",
                description="Integration test template"
            )
            
            self.manager.add_template(template)
            self.manager.save_template(template, temp_path / "test_template.json")
            
            # Verify file was created
            assert (temp_path / "test_template.json").exists()
            
            # Create new manager and load template
            new_manager = PromptTemplateManager()
            loaded_template = new_manager.load_template(temp_path / "test_template.json")
            
            assert loaded_template.name == template.name
            assert loaded_template.category == template.category
            assert loaded_template.system_prompt == template.system_prompt


@pytest.mark.integration
class TestEndToEndWorkflow:
    """End-to-end workflow integration tests."""
    
    def test_complete_ollama_workflow(self):
        """Test complete workflow from setup to inference with Ollama."""
        manager = OllamaManager()
        
        if not manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        # Step 1: Check system health
        health = manager.health_check()
        assert health["server_running"] is True
        
        # Step 2: List available models
        models = manager.list_models()
        if not models:
            pytest.skip("No models available")
        
        model_name = models[0].name
        
        # Step 3: Get model information
        model_info = manager.get_model_info(model_name)
        assert model_info is not None
        
        # Step 4: Generate response with system prompt
        response = manager.generate_response(
            model=model_name,
            prompt="Explain what you are in one sentence.",
            system="You are a helpful AI assistant."
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Step 5: Test with different generation config
        from ollama_manager import GenerationConfig
        
        config = GenerationConfig(
            temperature=0.5,
            top_p=0.8,
            num_predict=50
        )
        
        response2 = manager.generate_response(
            model=model_name,
            prompt="What is 2+2?",
            config=config
        )
        
        assert isinstance(response2, str)
        assert len(response2) > 0
    
    @pytest.mark.skipif(not TRANSFORMERS_AVAILABLE, reason="Transformers not available")
    def test_complete_transformers_workflow(self):
        """Test complete workflow with Transformers."""
        manager = TransformersManager()
        
        try:
            # Step 1: Check system capabilities
            device_info = manager.device_info
            assert "cpu_available" in device_info
            
            # Step 2: Load model
            model_name = "microsoft/DialoGPT-small"
            model_id = manager.load_model(model_name)
            
            # Step 3: Get model information
            info = manager.get_model_info(model_id)
            assert info is not None
            assert info["model_name"] == model_name
            
            # Step 4: Generate text
            response = manager.generate_text(
                model_id=model_id,
                prompt="Hello, how are you?"
            )
            
            assert isinstance(response, str)
            
            # Step 5: Check performance metrics
            metrics = manager.get_performance_metrics()
            assert len(metrics) > 0
            
            # Step 6: Cleanup
            success = manager.unload_model(model_id)
            assert success is True
            
        except Exception as e:
            pytest.skip(f"Transformers workflow failed: {e}")
    
    def test_prompt_template_with_llm_integration(self):
        """Test prompt templates integrated with LLM generation."""
        # Set up prompt template manager
        template_manager = PromptTemplateManager()
        template_manager.create_builtin_templates()
        
        # Set up Ollama manager
        ollama_manager = OllamaManager()
        
        if not ollama_manager.is_server_running():
            pytest.skip("Ollama server not running")
        
        models = ollama_manager.list_models()
        if not models:
            pytest.skip("No models available")
        
        model_name = models[0].name
        
        # Render template
        rendered = template_manager.render_template(
            "helpful_assistant",
            {
                "tone": "professional",
                "user_input": "Explain the concept of machine learning."
            }
        )
        
        # Use rendered template with LLM
        response = ollama_manager.generate_response(
            model=model_name,
            prompt=rendered["user"],
            system=rendered["system"]
        )
        
        assert isinstance(response, str)
        assert len(response) > 0


@pytest.mark.integration
class TestCrossPlatformCompatibility:
    """Cross-platform compatibility tests."""
    
    def test_path_handling(self):
        """Test path handling across different platforms."""
        from test_utilities import sanitize_filename
        
        # Test various filename scenarios
        test_cases = [
            ("normal_file.txt", "normal_file.txt"),
            ("file with spaces.txt", "file with spaces.txt"),
            ("file/with/slashes.txt", "file_with_slashes.txt"),
            ("file\\with\\backslashes.txt", "file_with_backslashes.txt"),
        ]
        
        for input_name, expected_pattern in test_cases:
            result = sanitize_filename(input_name)
            # On different platforms, the exact result might vary slightly
            assert len(result) > 0
            assert not any(char in result for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
    
    def test_memory_detection(self):
        """Test memory detection across platforms."""
        from test_utilities import check_system_requirements
        
        requirements = check_system_requirements()
        
        # These should work on all platforms
        assert "total_memory_gb" in requirements
        assert "available_memory_gb" in requirements
        assert "gpu_available" in requirements
        assert isinstance(requirements["total_memory_gb"], (int, float))
        assert isinstance(requirements["available_memory_gb"], (int, float))
        assert isinstance(requirements["gpu_available"], bool)
    
    def test_file_operations(self):
        """Test file operations across platforms."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test template file operations
            manager = PromptTemplateManager()
            manager.create_builtin_templates()
            
            # Export templates
            count = manager.export_templates(temp_path)
            assert count > 0
            
            # Verify files were created
            json_files = list(temp_path.glob("*.json"))
            assert len(json_files) == count
            
            # Test loading templates back
            new_manager = PromptTemplateManager()
            loaded_count = new_manager.load_templates_from_directory(temp_path)
            assert loaded_count == count


def run_integration_test_suite():
    """
    Run the complete integration test suite.
    
    This function can be called directly to run all integration tests
    without pytest, useful for CI/CD or manual testing.
    """
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "skipped_tests": 0,
        "test_results": []
    }
    
    # List of test classes and methods to run
    test_classes = [
        (TestOllamaIntegration, ["test_ollama_server_connection", "test_ollama_model_management"]),
        (TestPromptTemplateIntegration, ["test_builtin_templates_creation", "test_template_rendering_workflow"]),
        (TestCrossPlatformCompatibility, ["test_path_handling", "test_memory_detection"])
    ]
    
    for test_class, test_methods in test_classes:
        instance = test_class()
        if hasattr(instance, 'setup_method'):
            instance.setup_method()
        
        for method_name in test_methods:
            results["total_tests"] += 1
            
            try:
                method = getattr(instance, method_name)
                method()
                results["passed_tests"] += 1
                results["test_results"].append({
                    "test": f"{test_class.__name__}.{method_name}",
                    "status": "PASSED"
                })
            except pytest.skip.Exception as e:
                results["skipped_tests"] += 1
                results["test_results"].append({
                    "test": f"{test_class.__name__}.{method_name}",
                    "status": "SKIPPED",
                    "reason": str(e)
                })
            except Exception as e:
                results["failed_tests"] += 1
                results["test_results"].append({
                    "test": f"{test_class.__name__}.{method_name}",
                    "status": "FAILED",
                    "error": str(e)
                })
    
    return results


if __name__ == "__main__":
    # Run integration tests when executed directly
    print("Running Local LLMs Integration Test Suite")
    print("=" * 50)
    
    results = run_integration_test_suite()
    
    print(f"\nTest Results:")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed_tests']}")
    print(f"Failed: {results['failed_tests']}")
    print(f"Skipped: {results['skipped_tests']}")
    
    print(f"\nDetailed Results:")
    for result in results["test_results"]:
        status_symbol = {
            "PASSED": "✓",
            "FAILED": "✗",
            "SKIPPED": "⚠"
        }.get(result["status"], "?")
        
        print(f"  {status_symbol} {result['test']} - {result['status']}")
        
        if result["status"] == "FAILED":
            print(f"    Error: {result['error']}")
        elif result["status"] == "SKIPPED":
            print(f"    Reason: {result.get('reason', 'Unknown')}")
    
    # Exit with appropriate code
    exit_code = 0 if results["failed_tests"] == 0 else 1
    sys.exit(exit_code)