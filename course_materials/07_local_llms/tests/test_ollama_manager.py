"""
Unit tests for OllamaManager utility class.

This module contains comprehensive tests for the OllamaManager class,
including model management, response generation, and error handling.
"""

import json
import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import ConnectionError, RequestException, Timeout
import time

# Import the classes to test
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

from ollama_manager import (
    OllamaManager,
    OllamaError,
    OllamaConnectionError,
    OllamaModelError,
    ModelInfo,
    GenerationConfig
)


class TestModelInfo:
    """Test cases for ModelInfo dataclass."""
    
    def test_model_info_creation(self):
        """Test ModelInfo creation with required fields."""
        model_info = ModelInfo(
            name="llama2:7b",
            size=3825819519,
            digest="sha256:abc123",
            modified_at="2024-01-01T00:00:00Z"
        )
        
        assert model_info.name == "llama2:7b"
        assert model_info.size == 3825819519
        assert model_info.digest == "sha256:abc123"
        assert model_info.modified_at == "2024-01-01T00:00:00Z"
        assert model_info.details is None
    
    def test_model_info_with_details(self):
        """Test ModelInfo creation with optional details."""
        details = {"parameter_size": "7B", "quantization": "Q4_0"}
        model_info = ModelInfo(
            name="llama2:7b",
            size=3825819519,
            digest="sha256:abc123",
            modified_at="2024-01-01T00:00:00Z",
            details=details
        )
        
        assert model_info.details == details


class TestGenerationConfig:
    """Test cases for GenerationConfig dataclass."""
    
    def test_default_generation_config(self):
        """Test GenerationConfig with default values."""
        config = GenerationConfig()
        
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.top_k == 40
        assert config.num_predict == -1
        assert config.repeat_penalty == 1.1
        assert config.seed is None
        assert config.stop is None
    
    def test_custom_generation_config(self):
        """Test GenerationConfig with custom values."""
        config = GenerationConfig(
            temperature=0.5,
            top_p=0.8,
            top_k=30,
            num_predict=100,
            repeat_penalty=1.2,
            seed=42,
            stop=[".", "!"]
        )
        
        assert config.temperature == 0.5
        assert config.top_p == 0.8
        assert config.top_k == 30
        assert config.num_predict == 100
        assert config.repeat_penalty == 1.2
        assert config.seed == 42
        assert config.stop == [".", "!"]


class TestOllamaManager:
    """Test cases for OllamaManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = OllamaManager(base_url="http://localhost:11434", timeout=30)
    
    def test_initialization_default(self):
        """Test OllamaManager initialization with defaults."""
        manager = OllamaManager()
        
        assert manager.base_url == "http://localhost:11434"
        assert manager.timeout == 30
        assert manager.session is not None
    
    def test_initialization_custom(self):
        """Test OllamaManager initialization with custom values."""
        manager = OllamaManager(base_url="http://custom:8080", timeout=60)
        
        assert manager.base_url == "http://custom:8080"
        assert manager.timeout == 60
    
    def test_base_url_trailing_slash_removal(self):
        """Test that trailing slashes are removed from base_url."""
        manager = OllamaManager(base_url="http://localhost:11434/")
        assert manager.base_url == "http://localhost:11434"
    
    @patch('requests.Session.get')
    def test_is_server_running_success(self, mock_get):
        """Test is_server_running when server is accessible."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.manager.is_server_running()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=5)
    
    @patch('requests.Session.get')
    def test_is_server_running_failure(self, mock_get):
        """Test is_server_running when server is not accessible."""
        mock_get.side_effect = ConnectionError("Connection failed")
        
        result = self.manager.is_server_running()
        
        assert result is False
    
    @patch('requests.Session.get')
    def test_is_server_running_non_200_status(self, mock_get):
        """Test is_server_running with non-200 status code."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        result = self.manager.is_server_running()
        
        assert result is False
    
    @patch('requests.Session.get')
    def test_list_models_success(self, mock_get):
        """Test successful model listing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {
                    "name": "llama2:7b",
                    "size": 3825819519,
                    "digest": "sha256:abc123",
                    "modified_at": "2024-01-01T00:00:00Z",
                    "details": {"parameter_size": "7B"}
                },
                {
                    "name": "codellama:13b",
                    "size": 7365960935,
                    "digest": "sha256:def456",
                    "modified_at": "2024-01-02T00:00:00Z"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        models = self.manager.list_models()
        
        assert len(models) == 2
        assert models[0].name == "llama2:7b"
        assert models[0].size == 3825819519
        assert models[0].details == {"parameter_size": "7B"}
        assert models[1].name == "codellama:13b"
        assert models[1].details is None
    
    @patch('requests.Session.get')
    def test_list_models_empty(self, mock_get):
        """Test model listing with no models."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": []}
        mock_get.return_value = mock_response
        
        models = self.manager.list_models()
        
        assert len(models) == 0
    
    @patch('requests.Session.get')
    def test_list_models_connection_error(self, mock_get):
        """Test list_models with connection error."""
        mock_get.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(OllamaConnectionError) as exc_info:
            self.manager.list_models()
        
        assert "Cannot connect to Ollama server" in str(exc_info.value)
    
    @patch('requests.Session.get')
    def test_list_models_request_error(self, mock_get):
        """Test list_models with general request error."""
        mock_get.side_effect = RequestException("Request failed")
        
        with pytest.raises(OllamaError) as exc_info:
            self.manager.list_models()
        
        assert "Failed to list models" in str(exc_info.value)
    
    @patch('requests.Session.post')
    def test_pull_model_success(self, mock_post):
        """Test successful model pulling."""
        # Mock streaming response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"status": "downloading", "completed": 1024, "total": 2048}',
            b'{"status": "success"}'
        ]
        mock_post.return_value = mock_response
        
        result = self.manager.pull_model("llama2:7b")
        
        assert result is True
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["json"] == {"name": "llama2:7b"}
        assert call_args[1]["stream"] is True
    
    @patch('requests.Session.post')
    def test_pull_model_with_progress_callback(self, mock_post):
        """Test model pulling with progress callback."""
        progress_data = []
        
        def progress_callback(data):
            progress_data.append(data)
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"status": "downloading", "completed": 1024, "total": 2048}',
            b'{"status": "success"}'
        ]
        mock_post.return_value = mock_response
        
        result = self.manager.pull_model("llama2:7b", progress_callback)
        
        assert result is True
        assert len(progress_data) == 2
        assert progress_data[0]["status"] == "downloading"
        assert progress_data[1]["status"] == "success"
    
    @patch('requests.Session.post')
    def test_pull_model_error_in_stream(self, mock_post):
        """Test model pulling with error in stream."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"error": "Model not found"}'
        ]
        mock_post.return_value = mock_response
        
        with pytest.raises(OllamaModelError) as exc_info:
            self.manager.pull_model("nonexistent:model")
        
        assert "Model pull failed" in str(exc_info.value)
    
    @patch('requests.Session.post')
    def test_pull_model_connection_error(self, mock_post):
        """Test pull_model with connection error."""
        mock_post.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(OllamaConnectionError):
            self.manager.pull_model("llama2:7b")
    
    @patch('requests.Session.delete')
    def test_delete_model_success(self, mock_delete):
        """Test successful model deletion."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response
        
        result = self.manager.delete_model("llama2:7b")
        
        assert result is True
        mock_delete.assert_called_once()
        call_args = mock_delete.call_args
        assert call_args[1]["json"] == {"name": "llama2:7b"}
    
    @patch('requests.Session.delete')
    def test_delete_model_connection_error(self, mock_delete):
        """Test delete_model with connection error."""
        mock_delete.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(OllamaConnectionError):
            self.manager.delete_model("llama2:7b")
    
    @patch('requests.Session.post')
    def test_generate_response_success(self, mock_post):
        """Test successful response generation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Hello! How can I help you?"}
        mock_post.return_value = mock_response
        
        response = self.manager.generate_response(
            model="llama2:7b",
            prompt="Hello",
            system="You are a helpful assistant"
        )
        
        assert response == "Hello! How can I help you?"
        mock_post.assert_called_once()
        
        # Check the payload
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["model"] == "llama2:7b"
        assert payload["prompt"] == "Hello"
        assert payload["system"] == "You are a helpful assistant"
        assert payload["stream"] is False
    
    @patch('requests.Session.post')
    def test_generate_response_with_config(self, mock_post):
        """Test response generation with custom config."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Custom response"}
        mock_post.return_value = mock_response
        
        config = GenerationConfig(
            temperature=0.5,
            top_p=0.8,
            seed=42,
            stop=[".", "!"]
        )
        
        response = self.manager.generate_response(
            model="llama2:7b",
            prompt="Test",
            config=config
        )
        
        assert response == "Custom response"
        
        # Check the payload includes config options
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        assert payload["options"]["temperature"] == 0.5
        assert payload["options"]["top_p"] == 0.8
        assert payload["options"]["seed"] == 42
        assert payload["options"]["stop"] == [".", "!"]
    
    @patch('requests.Session.post')
    def test_generate_response_streaming(self, mock_post):
        """Test streaming response generation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello"}',
            b'{"response": " there!"}',
            b'{"done": true}'
        ]
        mock_post.return_value = mock_response
        
        response = self.manager.generate_response(
            model="llama2:7b",
            prompt="Hello",
            stream=True
        )
        
        assert response == "Hello there!"
    
    @patch('requests.Session.post')
    def test_generate_response_connection_error(self, mock_post):
        """Test generate_response with connection error."""
        mock_post.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(OllamaConnectionError):
            self.manager.generate_response("llama2:7b", "Hello")
    
    @patch('requests.Session.post')
    def test_generate_streaming_success(self, mock_post):
        """Test successful streaming generation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello"}',
            b'{"response": " there!"}',
            b'{"response": " How"}',
            b'{"response": " are you?"}',
            b'{"done": true}'
        ]
        mock_post.return_value = mock_response
        
        chunks = list(self.manager.generate_streaming("llama2:7b", "Hello"))
        
        assert chunks == ["Hello", " there!", " How", " are you?"]
    
    @patch('requests.Session.post')
    def test_generate_streaming_error_in_stream(self, mock_post):
        """Test streaming generation with error in stream."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"error": "Generation failed"}'
        ]
        mock_post.return_value = mock_response
        
        with pytest.raises(OllamaModelError) as exc_info:
            list(self.manager.generate_streaming("llama2:7b", "Hello"))
        
        assert "Generation failed" in str(exc_info.value)
    
    @patch('requests.Session.post')
    def test_get_model_info_success(self, mock_post):
        """Test successful model info retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "modelfile": "FROM llama2:7b",
            "parameters": {"temperature": 0.7},
            "template": "{{ .System }}\n{{ .Prompt }}"
        }
        mock_post.return_value = mock_response
        
        info = self.manager.get_model_info("llama2:7b")
        
        assert info is not None
        assert info["modelfile"] == "FROM llama2:7b"
        assert info["parameters"]["temperature"] == 0.7
    
    @patch('requests.Session.post')
    def test_get_model_info_not_found(self, mock_post):
        """Test model info retrieval for non-existent model."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response
        
        info = self.manager.get_model_info("nonexistent:model")
        
        assert info is None
    
    @patch('requests.Session.post')
    def test_get_model_info_connection_error(self, mock_post):
        """Test get_model_info with connection error."""
        mock_post.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(OllamaConnectionError):
            self.manager.get_model_info("llama2:7b")
    
    @patch.object(OllamaManager, 'is_server_running')
    @patch.object(OllamaManager, 'list_models')
    def test_health_check_success(self, mock_list_models, mock_is_running):
        """Test successful health check."""
        mock_is_running.return_value = True
        mock_list_models.return_value = [
            ModelInfo("llama2:7b", 123, "abc", "2024-01-01"),
            ModelInfo("codellama:13b", 456, "def", "2024-01-02")
        ]
        
        with patch('time.time', side_effect=[0, 0.1]):  # Mock timing
            health = self.manager.health_check()
        
        assert health["server_running"] is True
        assert health["models_available"] == 2
        assert health["connection_time_ms"] == 100
        assert health["error"] is None
    
    @patch.object(OllamaManager, 'is_server_running')
    def test_health_check_server_not_running(self, mock_is_running):
        """Test health check when server is not running."""
        mock_is_running.return_value = False
        
        health = self.manager.health_check()
        
        assert health["server_running"] is False
        assert health["models_available"] == 0
        assert health["error"] == "Server not responding"
    
    @patch.object(OllamaManager, 'is_server_running')
    def test_health_check_exception(self, mock_is_running):
        """Test health check with exception."""
        mock_is_running.side_effect = Exception("Unexpected error")
        
        health = self.manager.health_check()
        
        assert health["server_running"] is False
        assert health["error"] == "Unexpected error"


class TestOllamaManagerIntegration:
    """Integration tests for OllamaManager (require actual Ollama server)."""
    
    @pytest.mark.integration
    def test_real_server_connection(self):
        """Test connection to real Ollama server (if available)."""
        manager = OllamaManager()
        
        # This test only runs if server is actually running
        if manager.is_server_running():
            models = manager.list_models()
            assert isinstance(models, list)
            
            health = manager.health_check()
            assert health["server_running"] is True
        else:
            pytest.skip("Ollama server not running")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])