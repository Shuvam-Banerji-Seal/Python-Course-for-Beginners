# Troubleshooting Guide

This guide covers common issues and solutions when setting up the local LLMs environment.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Python Environment Problems](#python-environment-problems)
3. [Ollama Issues](#ollama-issues)
4. [PyTorch and GPU Problems](#pytorch-and-gpu-problems)
5. [Transformers Issues](#transformers-issues)
6. [Memory and Performance Issues](#memory-and-performance-issues)
7. [Platform-Specific Issues](#platform-specific-issues)

## Installation Issues

### Script Permission Denied

**Problem**: `bash: ./install_ollama.sh: Permission denied`

**Solution**:
```bash
chmod +x install_ollama.sh setup_python_env.sh test_installation.py
```

### Curl Not Found (Linux)

**Problem**: `curl: command not found`

**Solutions**:
- Ubuntu/Debian: `sudo apt update && sudo apt install curl`
- CentOS/RHEL: `sudo yum install curl` or `sudo dnf install curl`
- Arch Linux: `sudo pacman -S curl`

### Homebrew Not Found (macOS)

**Problem**: `brew: command not found`

**Solution**: Install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Python Environment Problems

### Python Version Too Old

**Problem**: `Python version 3.7 is below minimum required 3.8`

**Solutions**:
- **Ubuntu/Debian**: 
  ```bash
  sudo apt update
  sudo apt install python3.8 python3.8-venv python3.8-pip
  ```
- **macOS**: 
  ```bash
  brew install python@3.8
  ```
- **Windows**: Download from [python.org](https://python.org)

### Virtual Environment Creation Failed

**Problem**: `Error: could not create virtual environment`

**Solutions**:
1. Install venv module:
   ```bash
   sudo apt install python3-venv  # Ubuntu/Debian
   ```

2. Use alternative Python version:
   ```bash
   python3.8 -m venv local_llms_env
   ```

3. Clear existing environment:
   ```bash
   rm -rf local_llms_env
   ./setup_python_env.sh
   ```

### Pip Installation Failures

**Problem**: `ERROR: Could not install packages due to an EnvironmentError`

**Solutions**:
1. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Use user installation:
   ```bash
   pip install --user package_name
   ```

3. Clear pip cache:
   ```bash
   pip cache purge
   ```

## Ollama Issues

### Ollama Command Not Found

**Problem**: `ollama: command not found`

**Solutions**:
1. Check if Ollama is in PATH:
   ```bash
   which ollama
   echo $PATH
   ```

2. Add to PATH (if installed but not in PATH):
   ```bash
   export PATH=$PATH:/usr/local/bin
   echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
   ```

3. Reinstall Ollama:
   ```bash
   ./install_ollama.sh
   ```

### Ollama Server Not Running

**Problem**: `Error: could not connect to ollama server`

**Solutions**:
1. Start Ollama server:
   ```bash
   ollama serve
   ```

2. Check if port 11434 is in use:
   ```bash
   lsof -i :11434
   netstat -tulpn | grep 11434
   ```

3. Kill existing Ollama processes:
   ```bash
   pkill ollama
   ollama serve
   ```

### Model Download Failures

**Problem**: `Error downloading model`

**Solutions**:
1. Check internet connection
2. Try smaller model first:
   ```bash
   ollama pull llama3.2:1b
   ```
3. Check disk space:
   ```bash
   df -h
   ```
4. Clear Ollama cache:
   ```bash
   rm -rf ~/.ollama/models/*
   ```

### Permission Issues (Linux)

**Problem**: `Permission denied` when running Ollama

**Solutions**:
1. Add user to ollama group:
   ```bash
   sudo usermod -aG ollama $USER
   newgrp ollama
   ```

2. Fix ownership:
   ```bash
   sudo chown -R $USER:$USER ~/.ollama
   ```

## PyTorch and GPU Problems

### CUDA Not Detected

**Problem**: `torch.cuda.is_available()` returns `False`

**Solutions**:
1. Check NVIDIA driver:
   ```bash
   nvidia-smi
   ```

2. Install CUDA-compatible PyTorch:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. Verify CUDA installation:
   ```bash
   nvcc --version
   ```

### Out of Memory Errors

**Problem**: `CUDA out of memory` or `RuntimeError: out of memory`

**Solutions**:
1. Reduce batch size
2. Use CPU instead:
   ```python
   device = torch.device('cpu')
   ```
3. Clear GPU cache:
   ```python
   torch.cuda.empty_cache()
   ```
4. Use gradient checkpointing
5. Use smaller models

### Apple Silicon (M1/M2) Issues

**Problem**: PyTorch not using Metal Performance Shaders

**Solutions**:
1. Install MPS-compatible PyTorch:
   ```bash
   pip install torch torchvision torchaudio
   ```

2. Check MPS availability:
   ```python
   import torch
   print(torch.backends.mps.is_available())
   ```

3. Use MPS device:
   ```python
   device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
   ```

## Transformers Issues

### Model Loading Failures

**Problem**: `OSError: Can't load tokenizer` or model loading errors

**Solutions**:
1. Clear Hugging Face cache:
   ```bash
   rm -rf ~/.cache/huggingface/
   ```

2. Use offline mode:
   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("model_name", local_files_only=True)
   ```

3. Check internet connection and try again

### Slow Model Loading

**Problem**: Models take too long to load

**Solutions**:
1. Use smaller models for testing
2. Enable model caching
3. Use quantized models:
   ```python
   from transformers import AutoModelForCausalLM
   model = AutoModelForCausalLM.from_pretrained(
       "model_name",
       load_in_8bit=True,
       device_map="auto"
   )
   ```

### Token Limit Exceeded

**Problem**: `Token indices sequence length is longer than the specified maximum`

**Solutions**:
1. Truncate input:
   ```python
   inputs = tokenizer(text, truncation=True, max_length=512)
   ```

2. Use sliding window approach
3. Split long texts into chunks

## Memory and Performance Issues

### High Memory Usage

**Problem**: System runs out of RAM

**Solutions**:
1. Use smaller models
2. Enable model quantization
3. Use CPU offloading:
   ```python
   model = AutoModelForCausalLM.from_pretrained(
       "model_name",
       device_map="auto",
       offload_folder="offload"
   )
   ```
4. Increase swap space (Linux):
   ```bash
   sudo fallocate -l 8G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Slow Performance

**Problem**: Models run very slowly

**Solutions**:
1. Use GPU if available
2. Enable optimizations:
   ```python
   model = model.to(torch.float16)  # Use half precision
   ```
3. Use optimized libraries:
   ```bash
   pip install optimum[onnxruntime]
   ```
4. Reduce sequence length
5. Use batch processing

## Platform-Specific Issues

### Windows WSL Issues

**Problem**: Various issues in Windows Subsystem for Linux

**Solutions**:
1. Update WSL:
   ```bash
   wsl --update
   ```

2. Use WSL 2:
   ```bash
   wsl --set-version Ubuntu 2
   ```

3. Install Windows Terminal for better experience

4. Enable GPU support in WSL 2:
   - Install NVIDIA drivers on Windows
   - Install CUDA in WSL

### macOS Rosetta Issues

**Problem**: Performance issues on Apple Silicon

**Solutions**:
1. Use native ARM64 Python:
   ```bash
   arch -arm64 brew install python
   ```

2. Avoid Rosetta emulation:
   ```bash
   arch -arm64 python -m pip install package_name
   ```

### Linux Distribution Specific

#### Ubuntu/Debian
- Update package lists: `sudo apt update`
- Install build essentials: `sudo apt install build-essential`

#### CentOS/RHEL
- Enable EPEL: `sudo yum install epel-release`
- Install development tools: `sudo yum groupinstall "Development Tools"`

#### Arch Linux
- Update system: `sudo pacman -Syu`
- Install base-devel: `sudo pacman -S base-devel`

## Getting Help

### Diagnostic Information

When seeking help, provide:

1. **System Information**:
   ```bash
   uname -a
   python --version
   pip --version
   ```

2. **Error Messages**: Full error output, not just the last line

3. **Test Results**: Run the test script and share results:
   ```bash
   python test_installation.py
   ```

4. **Environment Details**:
   ```bash
   pip list
   ollama --version
   nvidia-smi  # if applicable
   ```

### Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **PyTorch Documentation**: https://pytorch.org/docs
- **Transformers Documentation**: https://huggingface.co/docs/transformers
- **Course Materials**: Check other modules in `course_materials/`

### Common Commands for Debugging

```bash
# Check Python environment
python -c "import sys; print(sys.executable, sys.version)"

# Test PyTorch
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# Test Transformers
python -c "import transformers; print(transformers.__version__)"

# Test Ollama
ollama list
ollama ps

# Check system resources
free -h  # Memory
df -h    # Disk space
top      # Running processes
```

### Emergency Reset

If everything is broken, start fresh:

```bash
# Remove virtual environment
rm -rf local_llms_env

# Clear Python cache
rm -rf ~/.cache/pip

# Clear Hugging Face cache
rm -rf ~/.cache/huggingface

# Reinstall everything
./setup_python_env.sh
./install_ollama.sh
python test_installation.py
```

Remember: Most issues are environment-related and can be solved by careful attention to error messages and systematic troubleshooting.