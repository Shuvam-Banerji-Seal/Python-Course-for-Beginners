"""
OllamaManager utility class for managing Ollama interactions.

This module provides a comprehensive interface for interacting with Ollama,
including model management, response generation, and error handling.
"""

import json
import time
import logging
from typing import List, Dict, Optional, Any, Generator
from dataclasses import dataclass
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class ModelInfo:
    """Information about an Ollama model."""
    name: str
    size: int
    digest: str
    modified_at: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    num_predict: int = -1
    repeat_penalty: float = 1.1
    seed: Optional[int] = None
    stop: Optional[List[str]] = None


class OllamaError(Exception):
    """Base exception for Ollama-related errors."""
    pass


class OllamaConnectionError(OllamaError):
    """Raised when connection to Ollama server fails."""
    pass


class OllamaModelError(OllamaError):
    """Raised when model-related operations fail."""
    pass


class OllamaManager:
    """
    A utility class for managing Ollama interactions.
    
    This class provides methods for model management, response generation,
    and includes robust error handling and retry mechanisms.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        """
        Initialize the OllamaManager.
        
        Args:
            base_url: The base URL for the Ollama server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = self._create_session()
        self.logger = logging.getLogger(__name__)
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def is_server_running(self) -> bool:
        """
        Check if the Ollama server is running.
        
        Returns:
            True if server is accessible, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def list_models(self) -> List[ModelInfo]:
        """
        List all available models.
        
        Returns:
            List of ModelInfo objects
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaError: If API request fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            models = []
            
            for model_data in data.get('models', []):
                model_info = ModelInfo(
                    name=model_data['name'],
                    size=model_data['size'],
                    digest=model_data['digest'],
                    modified_at=model_data['modified_at'],
                    details=model_data.get('details')
                )
                models.append(model_info)
                
            return models
            
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaError(f"Failed to list models: {e}") from e
    
    def pull_model(self, model_name: str, progress_callback: Optional[callable] = None) -> bool:
        """
        Download a model from Ollama registry.
        
        Args:
            model_name: Name of the model to download
            progress_callback: Optional callback function for progress updates
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaModelError: If model pull fails
        """
        try:
            payload = {"name": model_name}
            
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=None,  # Model downloads can take a long time
                stream=True
            )
            response.raise_for_status()
            
            # Process streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        if progress_callback:
                            progress_callback(data)
                            
                        # Check for completion
                        if data.get('status') == 'success':
                            self.logger.info(f"Successfully pulled model: {model_name}")
                            return True
                            
                        # Check for errors
                        if 'error' in data:
                            raise OllamaModelError(f"Model pull failed: {data['error']}")
                            
                    except json.JSONDecodeError:
                        continue
                        
            return True
            
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaModelError(f"Failed to pull model {model_name}: {e}") from e
    
    def delete_model(self, model_name: str) -> bool:
        """
        Delete a model from local storage.
        
        Args:
            model_name: Name of the model to delete
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaModelError: If model deletion fails
        """
        try:
            payload = {"name": model_name}
            
            response = self.session.delete(
                f"{self.base_url}/api/delete",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            self.logger.info(f"Successfully deleted model: {model_name}")
            return True
            
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaModelError(f"Failed to delete model {model_name}: {e}") from e
    
    def generate_response(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        stream: bool = False
    ) -> str:
        """
        Generate response using specified model.
        
        Args:
            model: Name of the model to use
            prompt: User prompt
            system: Optional system prompt
            config: Generation configuration
            stream: Whether to stream the response
            
        Returns:
            Generated response text
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaModelError: If generation fails
        """
        if config is None:
            config = GenerationConfig()
            
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": config.temperature,
                "top_p": config.top_p,
                "top_k": config.top_k,
                "num_predict": config.num_predict,
                "repeat_penalty": config.repeat_penalty,
            }
        }
        
        if system:
            payload["system"] = system
            
        if config.seed is not None:
            payload["options"]["seed"] = config.seed
            
        if config.stop:
            payload["options"]["stop"] = config.stop
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=None if stream else self.timeout,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_streaming_response(response)
            else:
                data = response.json()
                return data.get('response', '')
                
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaModelError(f"Failed to generate response: {e}") from e
    
    def generate_streaming(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> Generator[str, None, None]:
        """
        Generate streaming response using specified model.
        
        Args:
            model: Name of the model to use
            prompt: User prompt
            system: Optional system prompt
            config: Generation configuration
            
        Yields:
            Response chunks as they arrive
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaModelError: If generation fails
        """
        if config is None:
            config = GenerationConfig()
            
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": config.temperature,
                "top_p": config.top_p,
                "top_k": config.top_k,
                "num_predict": config.num_predict,
                "repeat_penalty": config.repeat_penalty,
            }
        }
        
        if system:
            payload["system"] = system
            
        if config.seed is not None:
            payload["options"]["seed"] = config.seed
            
        if config.stop:
            payload["options"]["stop"] = config.stop
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=None,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        if 'error' in data:
                            raise OllamaModelError(f"Generation failed: {data['error']}")
                            
                        if 'response' in data:
                            yield data['response']
                            
                        if data.get('done', False):
                            break
                            
                    except json.JSONDecodeError:
                        continue
                        
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaModelError(f"Failed to generate streaming response: {e}") from e
    
    def _handle_streaming_response(self, response: requests.Response) -> str:
        """Handle streaming response and return complete text."""
        complete_response = ""
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    
                    if 'error' in data:
                        raise OllamaModelError(f"Generation failed: {data['error']}")
                        
                    if 'response' in data:
                        complete_response += data['response']
                        
                    if data.get('done', False):
                        break
                        
                except json.JSONDecodeError:
                    continue
                    
        return complete_response
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information dictionary or None if not found
            
        Raises:
            OllamaConnectionError: If unable to connect to server
            OllamaError: If API request fails
        """
        try:
            payload = {"name": model_name}
            
            response = self.session.post(
                f"{self.base_url}/api/show",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                return None
                
            response.raise_for_status()
            return response.json()
            
        except requests.ConnectionError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server at {self.base_url}") from e
        except requests.RequestException as e:
            raise OllamaError(f"Failed to get model info for {model_name}: {e}") from e
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check.
        
        Returns:
            Dictionary with health check results
        """
        health_info = {
            "server_running": False,
            "models_available": 0,
            "connection_time_ms": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            
            # Check server connectivity
            if self.is_server_running():
                health_info["server_running"] = True
                health_info["connection_time_ms"] = int((time.time() - start_time) * 1000)
                
                # Check available models
                models = self.list_models()
                health_info["models_available"] = len(models)
            else:
                health_info["error"] = "Server not responding"
                
        except Exception as e:
            health_info["error"] = str(e)
            
        return health_info


# Example usage and testing functions
def example_usage():
    """Example usage of OllamaManager."""
    # Initialize manager
    manager = OllamaManager()
    
    # Check if server is running
    if not manager.is_server_running():
        print("Ollama server is not running. Please start it first.")
        return
    
    # List available models
    try:
        models = manager.list_models()
        print(f"Available models: {[model.name for model in models]}")
        
        if models:
            # Generate a response with the first available model
            model_name = models[0].name
            response = manager.generate_response(
                model=model_name,
                prompt="What is Python?",
                system="You are a helpful programming assistant."
            )
            print(f"Response: {response}")
            
    except OllamaError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_usage()