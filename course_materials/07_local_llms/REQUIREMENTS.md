# Requirements and Installation Guide

This document explains the different requirement files and how to install dependencies for the Local LLMs module.

## 📋 Requirements Files Overview

### `requirements.txt` - Base Requirements
Contains the core dependencies needed for all module functionality:
- Ollama Python client
- Hugging Face Transformers (CPU version)
- Jupyter notebook environment
- Basic data processing libraries
- Testing and validation tools

**Use this for**: Standard course usage, basic experimentation

### `requirements-gpu.txt` - GPU Support
Extends base requirements with GPU acceleration:
- CUDA-enabled PyTorch
- GPU monitoring tools
- Accelerated inference libraries
- Quantization support

**Use this for**: Users with NVIDIA GPUs who want faster inference

### `requirements-dev.txt` - Development Tools
Extends base requirements with development utilities:
- Advanced code formatting and linting
- Documentation generation tools
- Performance profiling
- Experiment tracking
- Enhanced Jupyter extensions

**Use this for**: Instructors, contributors, or advanced users

## 🚀 Installation Instructions

### Option 1: Basic Installation (Recommended for Students)

```bash
# Navigate to the local LLMs directory
cd course_materials/07_local_llms/

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install base requirements
pip install -r requirements.txt
```

### Option 2: GPU-Accelerated Installation

```bash
# First, check your CUDA version
nvidia-smi

# Install base requirements
pip install -r requirements.txt

# Install GPU requirements (adjust CUDA version as needed)
pip install -r requirements-gpu.txt
```

**Note**: For GPU support, you may need to install the correct PyTorch version for your CUDA version. Visit [PyTorch Installation Guide](https://pytorch.org/get-started/locally/) for specific instructions.

### Option 3: Development Installation

```bash
# Install base requirements
pip install -r requirements.txt

# Install development tools
pip install -r requirements-dev.txt

# Set up pre-commit hooks (optional)
pre-commit install
```

### Option 4: Complete Installation (All Features)

```bash
# Install all requirements (use with caution - large download)
pip install -r requirements.txt
pip install -r requirements-gpu.txt
pip install -r requirements-dev.txt
```

## 🔧 Troubleshooting

### Common Issues

#### 1. PyTorch Installation Conflicts
If you encounter PyTorch version conflicts:
```bash
# Uninstall existing PyTorch
pip uninstall torch torchvision torchaudio

# Reinstall with specific index
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 2. Jupyter Widget Issues
If Jupyter widgets don't display properly:
```bash
# Enable widget extensions
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

#### 3. Memory Issues
If you encounter out-of-memory errors:
- Use CPU-only versions of models
- Reduce batch sizes in examples
- Close other applications
- Consider using quantized models

#### 4. Ollama Connection Issues
If Ollama client can't connect:
```bash
# Check if Ollama is running
ollama list

# Start Ollama server if needed
ollama serve
```

### Platform-Specific Notes

#### Windows
- Some packages (like `flash-attn`, `bitsandbytes`) may not be available
- Use Windows Subsystem for Linux (WSL) for better compatibility
- Ensure Visual Studio Build Tools are installed for compilation

#### macOS
- Apple Silicon (M1/M2) users should use MPS backend for acceleration
- Some CUDA-specific packages will be skipped automatically

#### Linux
- Most compatible platform for all features
- Ensure CUDA drivers are properly installed for GPU support

## 📊 Dependency Versions

All dependencies are pinned to compatible version ranges to ensure stability:
- **Major version constraints**: Prevent breaking changes
- **Minor version flexibility**: Allow bug fixes and security updates
- **Regular updates**: Dependencies are reviewed and updated periodically

## 🔄 Updating Dependencies

To update to the latest compatible versions:

```bash
# Update all packages to latest compatible versions
pip install --upgrade -r requirements.txt

# Or update specific packages
pip install --upgrade transformers ollama
```

## 💡 Minimal Installation

For users with limited resources or bandwidth:

```bash
# Install only essential packages
pip install ollama transformers torch jupyter ipywidgets matplotlib
```

This minimal setup provides basic functionality for most course activities.

## 🆘 Getting Help

If you encounter installation issues:

1. Check the [troubleshooting guide](setup_scripts/troubleshooting.md)
2. Run the [installation test script](setup_scripts/test_installation.py)
3. Consult the official documentation for specific packages
4. Ask for help during class sessions or office hours

---

*For questions about specific requirements or installation issues, please refer to the course documentation or ask during class sessions.*