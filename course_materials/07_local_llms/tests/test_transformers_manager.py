"""
Unit tests for TransformersManager utility class.

This module contains comprehensive tests for the TransformersManager class,
including model loading with quantization, memory optimization, and performance monitoring.
"""

import pytest
import torch
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import time

# Import the classes to test
import sys
sys.path.append(str(Path(__file__).parent.parent / "utils"))

from transformers_manager import (
    TransformersManager,
    TransformersError,
    TransformersModelError,
    TransformersMemoryError,
    ModelConfig,
    GenerationConfig,
    PerformanceMetrics,
    TRANSFORMERS_AVAILABLE,
    BITSANDBYTES_AVAILABLE
)


class TestModelConfig:
    """Test cases for ModelConfig dataclass."""
    
    def test_model_config_defaults(self):
        """Test ModelConfig with default values."""
        config = ModelConfig(model_name="test-model")
        
        assert config.model_name == "test-model"
        assert config.device == "auto"
        assert config.torch_dtype == "auto"
        assert config.quantization_config is None
        assert config.trust_remote_code is False
        assert config.use_cache is True
        assert config.low_cpu_mem_usage is True
        assert config.device_map is None
    
    def test_model_config_custom(self):
        """Test ModelConfig with custom values."""
        config = ModelConfig(
            model_name="custom-model",
            device="cuda",
            torch_dtype="float16",
            trust_remote_code=True,
            use_cache=False,
            low_cpu_mem_usage=False,
            device_map="auto"
        )
        
        assert config.model_name == "custom-model"
        assert config.device == "cuda"
        assert config.torch_dtype == "float16"
        assert config.trust_remote_code is True
        assert config.use_cache is False
        assert config.low_cpu_mem_usage is False
        assert config.device_map == "auto"


class TestGenerationConfig:
    """Test cases for GenerationConfig dataclass."""
    
    def test_generation_config_defaults(self):
        """Test GenerationConfig with default values."""
        config = GenerationConfig()
        
        assert config.max_length == 100
        assert config.max_new_tokens is None
        assert config.temperature == 0.7
        assert config.top_p == 0.9
        assert config.top_k == 50
        assert config.do_sample is True
        assert config.num_return_sequences == 1
        assert config.pad_token_id is None
        assert config.eos_token_id is None
        assert config.repetition_penalty == 1.1
        assert config.length_penalty == 1.0
        assert config.early_stopping is True
    
    def test_generation_config_custom(self):
        """Test GenerationConfig with custom values."""
        config = GenerationConfig(
            max_length=200,
            max_new_tokens=50,
            temperature=0.5,
            top_p=0.8,
            top_k=40,
            do_sample=False,
            num_return_sequences=2,
            pad_token_id=0,
            eos_token_id=2,
            repetition_penalty=1.2,
            length_penalty=0.8,
            early_stopping=False
        )
        
        assert config.max_length == 200
        assert config.max_new_tokens == 50
        assert config.temperature == 0.5
        assert config.top_p == 0.8
        assert config.top_k == 40
        assert config.do_sample is False
        assert config.num_return_sequences == 2
        assert config.pad_token_id == 0
        assert config.eos_token_id == 2
        assert config.repetition_penalty == 1.2
        assert config.length_penalty == 0.8
        assert config.early_stopping is False


class TestPerformanceMetrics:
    """Test cases for PerformanceMetrics dataclass."""
    
    def test_performance_metrics_creation(self):
        """Test PerformanceMetrics creation."""
        metrics = PerformanceMetrics(
            model_name="test-model",
            operation="load_model",
            duration_seconds=1.5,
            memory_before_mb=1000.0,
            memory_after_mb=2000.0,
            memory_peak_mb=2100.0,
            gpu_memory_used_mb=500.0,
            tokens_generated=50,
            tokens_per_second=33.33
        )
        
        assert metrics.model_name == "test-model"
        assert metrics.operation == "load_model"
        assert metrics.duration_seconds == 1.5
        assert metrics.memory_before_mb == 1000.0
        assert metrics.memory_after_mb == 2000.0
        assert metrics.memory_peak_mb == 2100.0
        assert metrics.gpu_memory_used_mb == 500.0
        assert metrics.tokens_generated == 50
        assert metrics.tokens_per_second == 33.33
        assert isinstance(metrics.timestamp, float)


@pytest.mark.skipif(not TRANSFORMERS_AVAILABLE, reason="Transformers not available")
class TestTransformersManager:
    """Test cases for TransformersManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('transformers_manager.psutil'):
            self.manager = TransformersManager()
    
    def test_initialization_without_transformers(self):
        """Test initialization when transformers is not available."""
        with patch('transformers_manager.TRANSFORMERS_AVAILABLE', False):
            with pytest.raises(TransformersError) as exc_info:
                TransformersManager()
            
            assert "Transformers library not available" in str(exc_info.value)
    
    @patch('transformers_manager.psutil')
    def test_initialization_with_cache_dir(self, mock_psutil):
        """Test initialization with custom cache directory."""
        cache_dir = "/tmp/test_cache"
        manager = TransformersManager(cache_dir=cache_dir)
        
        assert manager.cache_dir == Path(cache_dir)
    
    @patch('torch.cuda.is_available')
    @patch('torch.cuda.device_count')
    @patch('torch.cuda.get_device_properties')
    def test_get_device_info_with_cuda(self, mock_get_props, mock_device_count, mock_cuda_available):
        """Test device info detection with CUDA available."""
        mock_cuda_available.return_value = True
        mock_device_count.return_value = 2
        
        # Mock device properties
        mock_props = Mock()
        mock_props.name = "NVIDIA RTX 4090"
        mock_props.total_memory = 24 * 1024**3  # 24GB
        mock_props.major = 8
        mock_props.minor = 9
        mock_get_props.return_value = mock_props
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        device_info = manager.device_info
        assert device_info["cpu_available"] is True
        assert device_info["cuda_available"] is True
        assert device_info["cuda_device_count"] == 2
        assert len(device_info["cuda_devices"]) == 2
        assert device_info["cuda_devices"][0]["name"] == "NVIDIA RTX 4090"
        assert device_info["cuda_devices"][0]["memory_gb"] == 24.0
    
    @patch('torch.cuda.is_available')
    def test_get_device_info_without_cuda(self, mock_cuda_available):
        """Test device info detection without CUDA."""
        mock_cuda_available.return_value = False
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        device_info = manager.device_info
        assert device_info["cpu_available"] is True
        assert device_info["cuda_available"] is False
        assert device_info["cuda_device_count"] == 0
        assert device_info["cuda_devices"] == []
    
    @patch('transformers_manager.psutil.virtual_memory')
    @patch('torch.cuda.is_available')
    @patch('torch.cuda.memory_allocated')
    def test_get_memory_usage(self, mock_memory_allocated, mock_cuda_available, mock_virtual_memory):
        """Test memory usage detection."""
        # Mock CPU memory
        mock_vm = Mock()
        mock_vm.used = 8 * 1024**3  # 8GB
        mock_vm.percent = 75.0
        mock_virtual_memory.return_value = mock_vm
        
        # Mock GPU memory
        mock_cuda_available.return_value = True
        mock_memory_allocated.return_value = 2 * 1024**3  # 2GB
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        memory_usage = manager._get_memory_usage()
        
        assert memory_usage["cpu_memory_mb"] == 8 * 1024  # 8GB in MB
        assert memory_usage["cpu_memory_percent"] == 75.0
        assert memory_usage["gpu_memory_mb"] == 2 * 1024  # 2GB in MB
    
    @patch('transformers_manager.BITSANDBYTES_AVAILABLE', True)
    @patch('transformers_manager.BitsAndBytesConfig')
    def test_create_quantization_config_4bit(self, mock_bnb_config):
        """Test 4-bit quantization config creation."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        config = manager.create_quantization_config(
            load_in_4bit=True,
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        mock_bnb_config.assert_called_once_with(
            load_in_4bit=True,
            load_in_8bit=False,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
    
    @patch('transformers_manager.BITSANDBYTES_AVAILABLE', True)
    @patch('transformers_manager.BitsAndBytesConfig')
    def test_create_quantization_config_8bit(self, mock_bnb_config):
        """Test 8-bit quantization config creation."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        config = manager.create_quantization_config(load_in_8bit=True)
        
        mock_bnb_config.assert_called_once_with(
            load_in_4bit=False,
            load_in_8bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
    
    def test_create_quantization_config_both_bits_error(self):
        """Test error when both 4-bit and 8-bit are requested."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        with pytest.raises(TransformersError) as exc_info:
            manager.create_quantization_config(load_in_4bit=True, load_in_8bit=True)
        
        assert "Cannot use both 4-bit and 8-bit quantization" in str(exc_info.value)
    
    @patch('transformers_manager.BITSANDBYTES_AVAILABLE', False)
    def test_create_quantization_config_no_bitsandbytes(self):
        """Test quantization config when bitsandbytes is not available."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        config = manager.create_quantization_config(load_in_4bit=True)
        
        assert config is None
    
    def test_resolve_device_auto_cuda(self):
        """Test device resolution with CUDA available."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        manager.device_info = {
            "cuda_available": True,
            "mps_available": False
        }
        
        device = manager._resolve_device("auto")
        assert device == "cuda"
    
    def test_resolve_device_auto_mps(self):
        """Test device resolution with MPS available."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        manager.device_info = {
            "cuda_available": False,
            "mps_available": True
        }
        
        device = manager._resolve_device("auto")
        assert device == "mps"
    
    def test_resolve_device_auto_cpu(self):
        """Test device resolution fallback to CPU."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        manager.device_info = {
            "cuda_available": False,
            "mps_available": False
        }
        
        device = manager._resolve_device("auto")
        assert device == "cpu"
    
    def test_resolve_device_explicit(self):
        """Test explicit device specification."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        device = manager._resolve_device("cuda:1")
        assert device == "cuda:1"
    
    @patch('torch.cuda.is_available')
    def test_resolve_dtype_auto_cuda(self, mock_cuda_available):
        """Test dtype resolution with CUDA available."""
        mock_cuda_available.return_value = True
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        dtype = manager._resolve_dtype("auto")
        assert dtype == torch.float16
    
    @patch('torch.cuda.is_available')
    def test_resolve_dtype_auto_cpu(self, mock_cuda_available):
        """Test dtype resolution without CUDA."""
        mock_cuda_available.return_value = False
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        dtype = manager._resolve_dtype("auto")
        assert dtype == torch.float32
    
    def test_resolve_dtype_explicit(self):
        """Test explicit dtype specification."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        dtype = manager._resolve_dtype("bfloat16")
        assert dtype == torch.bfloat16
    
    @patch('transformers_manager.AutoTokenizer.from_pretrained')
    @patch('transformers_manager.AutoModelForCausalLM.from_pretrained')
    @patch('time.time')
    def test_load_model_success(self, mock_time, mock_model_from_pretrained, mock_tokenizer_from_pretrained):
        """Test successful model loading."""
        # Mock time for performance metrics
        mock_time.side_effect = [0, 1.5]  # Start and end times
        
        # Mock tokenizer
        mock_tokenizer = Mock()
        mock_tokenizer.pad_token = None
        mock_tokenizer.eos_token = "<eos>"
        mock_tokenizer_from_pretrained.return_value = mock_tokenizer
        
        # Mock model
        mock_model = Mock()
        mock_model_from_pretrained.return_value = mock_model
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Mock memory usage
        manager._get_memory_usage = Mock(side_effect=[
            {"cpu_memory_mb": 1000.0, "gpu_memory_mb": 0.0},  # Before
            {"cpu_memory_mb": 2000.0, "gpu_memory_mb": 500.0}  # After
        ])
        
        model_id = manager.load_model("test-model")
        
        assert model_id in manager.loaded_models
        assert manager.loaded_models[model_id]["model"] == mock_model
        assert manager.loaded_models[model_id]["tokenizer"] == mock_tokenizer
        assert mock_tokenizer.pad_token == "<eos>"  # Should be set to eos_token
        
        # Check performance metrics
        assert len(manager.performance_history) == 1
        metrics = manager.performance_history[0]
        assert metrics.model_name == "test-model"
        assert metrics.operation == "load_model"
        assert metrics.duration_seconds == 1.5
    
    @patch('transformers_manager.AutoTokenizer.from_pretrained')
    @patch('transformers_manager.AutoModelForCausalLM.from_pretrained')
    def test_load_model_already_loaded(self, mock_model_from_pretrained, mock_tokenizer_from_pretrained):
        """Test loading a model that's already loaded."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Mock existing model
        config = ModelConfig(model_name="test-model")
        model_id = f"test-model_{id(config)}"
        manager.loaded_models[model_id] = {"model": Mock(), "tokenizer": Mock()}
        
        result_id = manager.load_model("test-model", config)
        
        assert result_id == model_id
        # Should not call from_pretrained again
        mock_model_from_pretrained.assert_not_called()
        mock_tokenizer_from_pretrained.assert_not_called()
    
    @patch('transformers_manager.AutoTokenizer.from_pretrained')
    @patch('transformers_manager.AutoModelForCausalLM.from_pretrained')
    def test_load_model_out_of_memory(self, mock_model_from_pretrained, mock_tokenizer_from_pretrained):
        """Test model loading with GPU out of memory error."""
        mock_tokenizer_from_pretrained.return_value = Mock()
        mock_model_from_pretrained.side_effect = torch.cuda.OutOfMemoryError("CUDA out of memory")
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        with pytest.raises(TransformersMemoryError) as exc_info:
            manager.load_model("large-model")
        
        assert "GPU out of memory" in str(exc_info.value)
    
    @patch('transformers_manager.AutoTokenizer.from_pretrained')
    def test_load_model_general_error(self, mock_tokenizer_from_pretrained):
        """Test model loading with general error."""
        mock_tokenizer_from_pretrained.side_effect = Exception("Model not found")
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        with pytest.raises(TransformersModelError) as exc_info:
            manager.load_model("nonexistent-model")
        
        assert "Failed to load model" in str(exc_info.value)
    
    def test_generate_text_model_not_loaded(self):
        """Test text generation with model not loaded."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        with pytest.raises(TransformersModelError) as exc_info:
            manager.generate_text("nonexistent-model", "Hello")
        
        assert "Model nonexistent-model not loaded" in str(exc_info.value)
    
    @patch('torch.no_grad')
    @patch('time.time')
    def test_generate_text_success(self, mock_time, mock_no_grad):
        """Test successful text generation."""
        mock_time.side_effect = [0, 1.0]  # Start and end times
        
        # Mock model and tokenizer
        mock_tokenizer = Mock()
        mock_tokenizer.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}
        mock_tokenizer.pad_token_id = 0
        mock_tokenizer.eos_token_id = 2
        mock_tokenizer.decode.return_value = "Hello How are you?"
        
        mock_model = Mock()
        mock_model.generate.return_value = torch.tensor([[1, 2, 3, 4, 5, 6]])
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Set up loaded model
        model_id = "test-model"
        manager.loaded_models[model_id] = {
            "model": mock_model,
            "tokenizer": mock_tokenizer,
            "config": ModelConfig(model_name="test-model"),
            "device": "cpu"
        }
        
        # Mock memory usage
        manager._get_memory_usage = Mock(side_effect=[
            {"cpu_memory_mb": 1000.0, "gpu_memory_mb": 0.0},  # Before
            {"cpu_memory_mb": 1100.0, "gpu_memory_mb": 0.0}   # After
        ])
        
        response = manager.generate_text(model_id, "Hello", GenerationConfig(max_length=50))
        
        assert response == " How are you?"  # Should remove input prompt
        
        # Check performance metrics
        assert len(manager.performance_history) == 1
        metrics = manager.performance_history[0]
        assert metrics.operation == "generate_text"
        assert metrics.tokens_generated == 3  # 6 output - 3 input tokens
    
    @patch('torch.no_grad')
    def test_generate_text_out_of_memory(self, mock_no_grad):
        """Test text generation with GPU out of memory."""
        mock_tokenizer = Mock()
        mock_tokenizer.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}
        
        mock_model = Mock()
        mock_model.generate.side_effect = torch.cuda.OutOfMemoryError("CUDA out of memory")
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        model_id = "test-model"
        manager.loaded_models[model_id] = {
            "model": mock_model,
            "tokenizer": mock_tokenizer,
            "config": ModelConfig(model_name="test-model"),
            "device": "cuda"
        }
        
        with pytest.raises(TransformersMemoryError) as exc_info:
            manager.generate_text(model_id, "Hello")
        
        assert "GPU out of memory during generation" in str(exc_info.value)
    
    @patch('gc.collect')
    @patch('torch.cuda.is_available')
    @patch('torch.cuda.empty_cache')
    def test_unload_model_success(self, mock_empty_cache, mock_cuda_available, mock_gc_collect):
        """Test successful model unloading."""
        mock_cuda_available.return_value = True
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Set up loaded model
        model_id = "test-model"
        manager.loaded_models[model_id] = {
            "model": Mock(),
            "tokenizer": Mock()
        }
        
        result = manager.unload_model(model_id)
        
        assert result is True
        assert model_id not in manager.loaded_models
        mock_gc_collect.assert_called_once()
        mock_empty_cache.assert_called_once()
    
    def test_unload_model_not_found(self):
        """Test unloading non-existent model."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        result = manager.unload_model("nonexistent-model")
        
        assert result is False
    
    def test_get_model_info_success(self):
        """Test getting model info for loaded model."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Set up loaded model
        model_id = "test-model"
        config = ModelConfig(model_name="test-model")
        manager.loaded_models[model_id] = {
            "config": config,
            "device": "cpu",
            "load_time": 1.5,
            "quantization_config": None
        }
        
        manager._get_memory_usage = Mock(return_value={"cpu_memory_mb": 1000.0})
        
        info = manager.get_model_info(model_id)
        
        assert info is not None
        assert info["model_name"] == "test-model"
        assert info["device"] == "cpu"
        assert info["load_time"] == 1.5
        assert info["quantization_enabled"] is False
    
    def test_get_model_info_not_found(self):
        """Test getting model info for non-existent model."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        info = manager.get_model_info("nonexistent-model")
        
        assert info is None
    
    def test_list_loaded_models(self):
        """Test listing loaded models."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Set up loaded models
        manager.loaded_models = {
            "model1": {},
            "model2": {},
            "model3": {}
        }
        
        models = manager.list_loaded_models()
        
        assert set(models) == {"model1", "model2", "model3"}
    
    def test_get_performance_metrics_all(self):
        """Test getting all performance metrics."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Add some metrics
        metrics1 = PerformanceMetrics("model1", "load", 1.0, 100, 200, 200)
        metrics2 = PerformanceMetrics("model2", "generate", 0.5, 200, 250, 250)
        manager.performance_history = [metrics1, metrics2]
        
        all_metrics = manager.get_performance_metrics()
        
        assert len(all_metrics) == 2
        assert all_metrics[0] == metrics1
        assert all_metrics[1] == metrics2
    
    def test_get_performance_metrics_filtered(self):
        """Test getting performance metrics filtered by model name."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Add some metrics
        metrics1 = PerformanceMetrics("model1", "load", 1.0, 100, 200, 200)
        metrics2 = PerformanceMetrics("model2", "generate", 0.5, 200, 250, 250)
        metrics3 = PerformanceMetrics("model1", "generate", 0.3, 200, 220, 220)
        manager.performance_history = [metrics1, metrics2, metrics3]
        
        model1_metrics = manager.get_performance_metrics("model1")
        
        assert len(model1_metrics) == 2
        assert model1_metrics[0] == metrics1
        assert model1_metrics[1] == metrics3
    
    @patch('gc.collect')
    @patch('torch.cuda.is_available')
    @patch('torch.cuda.empty_cache')
    def test_optimize_memory(self, mock_empty_cache, mock_cuda_available, mock_gc_collect):
        """Test memory optimization."""
        mock_cuda_available.return_value = True
        
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Mock memory usage before and after
        manager._get_memory_usage = Mock(side_effect=[
            {"cpu_memory_mb": 2000.0, "gpu_memory_mb": 1000.0},  # Before
            {"cpu_memory_mb": 1500.0, "gpu_memory_mb": 500.0}    # After
        ])
        
        results = manager.optimize_memory()
        
        assert results["memory_freed_mb"] == 500.0  # 2000 - 1500
        assert results["gpu_memory_freed_mb"] == 500.0  # 1000 - 500
        mock_gc_collect.assert_called_once()
        mock_empty_cache.assert_called_once()
    
    def test_benchmark_model_success(self):
        """Test successful model benchmarking."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        # Set up loaded model
        model_id = "test-model"
        manager.loaded_models[model_id] = {"model": Mock(), "tokenizer": Mock()}
        
        # Mock generate_text method
        manager.generate_text = Mock(side_effect=[
            "Response 1",
            "Response 2"
        ])
        
        # Mock performance metrics
        metrics1 = PerformanceMetrics("test-model", "generate", 0.5, 100, 120, 120, 0, 10, 20.0)
        metrics2 = PerformanceMetrics("test-model", "generate", 0.3, 120, 130, 130, 0, 8, 26.7)
        manager.performance_history = [metrics1, metrics2]
        
        # Mock memory usage
        manager._get_memory_usage = Mock(side_effect=[
            {"cpu_memory_mb": 1000.0},
            {"cpu_memory_mb": 1100.0}
        ])
        
        test_prompts = ["Hello", "How are you?"]
        
        with patch('time.time', side_effect=[0, 0.8]):  # Total benchmark time
            results = manager.benchmark_model(model_id, test_prompts)
        
        assert results["model_id"] == model_id
        assert results["num_prompts"] == 2
        assert results["total_time"] == 0.8
        assert results["average_time"] == 0.4
        assert results["total_tokens"] == 18  # 10 + 8
        assert results["average_tokens_per_second"] == 22.5  # 18 / 0.8
        assert len(results["individual_results"]) == 2
        assert len(results["memory_usage"]) == 2
    
    def test_benchmark_model_not_loaded(self):
        """Test benchmarking non-existent model."""
        with patch('transformers_manager.psutil'):
            manager = TransformersManager()
        
        with pytest.raises(TransformersModelError) as exc_info:
            manager.benchmark_model("nonexistent-model", ["test"])
        
        assert "Model nonexistent-model not loaded" in str(exc_info.value)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])