# Hugging Face Transformers Setup Guide

This guide covers the installation and setup of Hugging Face Transformers for local LLM deployment.

## Prerequisites

- Python 3.8 or higher
- At least 8GB RAM (16GB+ recommended for larger models)
- Optional: CUDA-compatible GPU for acceleration

## Installation

### Basic Installation

```bash
# Install transformers with PyTorch
pip install transformers torch torchvision torchaudio

# For CPU-only installation
pip install transformers torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# For CUDA support (check your CUDA version)
pip install transformers torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Additional Dependencies

```bash
# For accelerated inference
pip install accelerate

# For quantization support
pip install bitsandbytes

# For tokenizer improvements
pip install tokenizers

# For audio models (optional)
pip install librosa soundfile

# For vision models (optional)
pip install pillow
```

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv transformers_env

# Activate environment
# On Linux/Mac:
source transformers_env/bin/activate
# On Windows:
transformers_env\Scripts\activate

# Install packages
pip install transformers torch accelerate bitsandbytes
```

## Verification

Test your installation with this simple script:

```python
from transformers import pipeline
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Test with a simple pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("I love using Transformers!")
print(f"Test result: {result}")
```

## Model Storage

By default, models are cached in:
- Linux/Mac: `~/.cache/huggingface/transformers/`
- Windows: `C:\Users\{username}\.cache\huggingface\transformers\`

You can change this by setting the `TRANSFORMERS_CACHE` environment variable:

```bash
export TRANSFORMERS_CACHE=/path/to/your/cache
```

## Common Issues and Solutions

### Out of Memory Errors

1. **Use smaller models**: Start with models like `distilbert-base-uncased`
2. **Enable gradient checkpointing**: Reduces memory at cost of speed
3. **Use quantization**: 8-bit or 4-bit quantization with bitsandbytes
4. **Reduce batch size**: Process fewer samples at once

### Slow Downloads

1. **Use Hugging Face Hub**: Models download automatically but can be large
2. **Resume interrupted downloads**: Transformers handles this automatically
3. **Use local models**: Download once and reuse

### CUDA Issues

1. **Check CUDA version**: `nvidia-smi` to see your CUDA version
2. **Install matching PyTorch**: Use the correct CUDA version for PyTorch
3. **Fallback to CPU**: Set `device="cpu"` if GPU issues persist

## Next Steps

- Try the basic inference examples in `local_inference.py`
- Learn about memory optimization in `memory_optimization.py`
- Compare performance with Ollama using `model_comparison.py`