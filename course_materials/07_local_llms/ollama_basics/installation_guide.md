# Ollama Installation and Setup Guide

## Overview

Ollama is a tool that allows you to run large language models locally on your machine. This guide provides comprehensive installation instructions for different operating systems and troubleshooting for common issues.

## System Requirements

### Minimum Requirements
- **RAM**: 8GB (16GB recommended for larger models)
- **Storage**: 10GB free space (varies by model size)
- **CPU**: Modern multi-core processor
- **OS**: Linux, macOS, or Windows

### Recommended Requirements
- **RAM**: 16GB+ for 7B models, 32GB+ for 13B models
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional but recommended)
- **Storage**: SSD with 50GB+ free space
- **Network**: Stable internet connection for model downloads

## Installation Instructions

### Linux Installation

#### Method 1: Official Installation Script (Recommended)
```bash
# Download and run the official installation script
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Method 2: Manual Installation
```bash
# Download the binary
curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
chmod +x ollama

# Move to system path
sudo mv ollama /usr/local/bin/

# Create systemd service (optional)
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

# Create ollama user
sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### Ubuntu/Debian Package Installation
```bash
# Add Ollama repository
curl -fsSL https://ollama.ai/gpg | sudo gpg --dearmor -o /usr/share/keyrings/ollama-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/ollama-keyring.gpg] https://ollama.ai/apt stable main" | sudo tee /etc/apt/sources.list.d/ollama.list

# Update and install
sudo apt update
sudo apt install ollama
```

### macOS Installation

#### Method 1: Official Installer (Recommended)
1. Download the Ollama installer from [https://ollama.ai/download](https://ollama.ai/download)
2. Open the downloaded `.dmg` file
3. Drag Ollama to your Applications folder
4. Launch Ollama from Applications

#### Method 2: Homebrew
```bash
# Install using Homebrew
brew install ollama

# Start Ollama service
brew services start ollama
```

#### Method 3: Manual Installation
```bash
# Download and install
curl -L https://ollama.ai/download/ollama-darwin -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/
```

### Windows Installation

#### Method 1: Official Installer (Recommended)
1. Download the Ollama installer from [https://ollama.ai/download](https://ollama.ai/download)
2. Run the downloaded `.exe` file
3. Follow the installation wizard
4. Ollama will start automatically after installation

#### Method 2: Windows Subsystem for Linux (WSL)
```bash
# Install WSL2 first, then follow Linux instructions
wsl --install
# Restart and follow Linux installation steps
```

#### Method 3: Docker (Cross-platform)
```bash
# Pull and run Ollama in Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# For GPU support (NVIDIA)
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Post-Installation Setup

### 1. Verify Installation
```bash
# Check if Ollama is running
ollama --version

# Test the service
curl http://localhost:11434/api/version
```

### 2. Download Your First Model
```bash
# Download a small model for testing
ollama pull llama2:7b

# List available models
ollama list
```

### 3. Test Basic Functionality
```bash
# Run a simple chat
ollama run llama2:7b "Hello, how are you?"
```

### 4. Configure Environment Variables (Optional)
```bash
# Set custom model storage location
export OLLAMA_MODELS="/path/to/your/models"

# Set custom host and port
export OLLAMA_HOST="0.0.0.0:11434"

# Enable debug logging
export OLLAMA_DEBUG=1
```

## GPU Acceleration Setup

### NVIDIA GPU Support

#### Linux
```bash
# Install NVIDIA Container Toolkit (for Docker)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Verify GPU is available
nvidia-smi
```

#### Windows
- Ensure NVIDIA drivers are installed and up to date
- Ollama will automatically detect and use GPU if available

### AMD GPU Support
```bash
# AMD ROCm support (Linux only)
# Follow AMD ROCm installation guide for your distribution
# Ollama will automatically detect ROCm if properly installed
```

## Model Management

### Popular Models to Try
```bash
# Small models (good for testing)
ollama pull llama2:7b          # 3.8GB
ollama pull mistral:7b         # 4.1GB
ollama pull codellama:7b       # 3.8GB

# Medium models (better performance)
ollama pull llama2:13b         # 7.3GB
ollama pull mistral:7b-instruct # 4.1GB

# Large models (best performance, requires more resources)
ollama pull llama2:70b         # 39GB
ollama pull codellama:34b      # 19GB
```

### Model Storage Locations
- **Linux**: `~/.ollama/models`
- **macOS**: `~/.ollama/models`
- **Windows**: `%USERPROFILE%\.ollama\models`

## Configuration Files

### Ollama Configuration
Create `~/.ollama/config.json` for custom settings:
```json
{
  "models_path": "/custom/path/to/models",
  "host": "0.0.0.0",
  "port": 11434,
  "gpu_layers": -1,
  "num_ctx": 2048,
  "temperature": 0.7
}
```

### Systemd Service Configuration (Linux)
Edit `/etc/systemd/system/ollama.service` to customize:
```ini
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_MODELS=/opt/ollama/models"

[Install]
WantedBy=default.target
```

## Troubleshooting Common Issues

### Installation Issues

#### Issue: "Command not found: ollama"
**Solution:**
```bash
# Check if ollama is in PATH
which ollama

# If not found, add to PATH or reinstall
export PATH=$PATH:/usr/local/bin
# Or reinstall using the official script
```

#### Issue: Permission denied errors (Linux)
**Solution:**
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.ollama
sudo chmod -R 755 ~/.ollama

# Or run with proper user
sudo -u ollama ollama serve
```

#### Issue: Port 11434 already in use
**Solution:**
```bash
# Check what's using the port
sudo lsof -i :11434

# Kill the process or use a different port
export OLLAMA_HOST="0.0.0.0:11435"
ollama serve
```

### Model Download Issues

#### Issue: Download fails or is very slow
**Solutions:**
1. Check internet connection
2. Try a different mirror:
   ```bash
   export OLLAMA_REGISTRY="https://registry.ollama.ai"
   ```
3. Use resume capability:
   ```bash
   ollama pull llama2:7b --resume
   ```

#### Issue: "Not enough space" error
**Solutions:**
1. Check available disk space:
   ```bash
   df -h ~/.ollama
   ```
2. Clean up old models:
   ```bash
   ollama rm unused_model_name
   ```
3. Change models directory:
   ```bash
   export OLLAMA_MODELS="/path/to/larger/drive"
   ```

### Runtime Issues

#### Issue: High memory usage
**Solutions:**
1. Use smaller models:
   ```bash
   ollama pull llama2:7b-q4_0  # Quantized version
   ```
2. Limit context size:
   ```bash
   ollama run llama2:7b --ctx-size 1024
   ```
3. Monitor memory usage:
   ```bash
   htop  # or top on macOS
   ```

#### Issue: Slow inference speed
**Solutions:**
1. Enable GPU acceleration (if available)
2. Use quantized models
3. Increase system RAM
4. Close other applications

#### Issue: API connection refused
**Solutions:**
1. Check if service is running:
   ```bash
   ps aux | grep ollama
   ```
2. Restart the service:
   ```bash
   # Linux with systemd
   sudo systemctl restart ollama
   
   # Manual restart
   pkill ollama
   ollama serve &
   ```
3. Check firewall settings:
   ```bash
   # Linux
   sudo ufw allow 11434
   
   # macOS
   # Allow in System Preferences > Security & Privacy > Firewall
   ```

### GPU Issues

#### Issue: GPU not detected
**Solutions:**
1. Verify GPU drivers:
   ```bash
   nvidia-smi  # For NVIDIA
   rocm-smi    # For AMD
   ```
2. Check CUDA installation:
   ```bash
   nvcc --version
   ```
3. Restart Ollama after driver installation

#### Issue: Out of GPU memory
**Solutions:**
1. Use smaller models
2. Reduce batch size
3. Enable memory optimization:
   ```bash
   export OLLAMA_GPU_MEMORY_FRACTION=0.8
   ```

### Network Issues

#### Issue: Cannot access Ollama from other machines
**Solutions:**
1. Bind to all interfaces:
   ```bash
   export OLLAMA_HOST="0.0.0.0:11434"
   ollama serve
   ```
2. Configure firewall:
   ```bash
   # Linux
   sudo ufw allow from 192.168.1.0/24 to any port 11434
   ```
3. Check network connectivity:
   ```bash
   telnet your_server_ip 11434
   ```

## Performance Optimization

### Hardware Optimization
1. **Use SSD storage** for faster model loading
2. **Increase RAM** for better performance with larger models
3. **Use GPU acceleration** when available
4. **Close unnecessary applications** to free up resources

### Software Optimization
1. **Use quantized models** for faster inference
2. **Adjust context size** based on your needs
3. **Enable parallel processing** for multiple requests
4. **Monitor resource usage** and adjust accordingly

### Model Selection Guidelines
- **7B models**: Good balance of performance and resource usage
- **13B models**: Better quality, requires more resources
- **Quantized models**: Faster inference with slight quality trade-off
- **Specialized models**: Use task-specific models when available

## Getting Help

### Official Resources
- **Documentation**: [https://ollama.ai/docs](https://ollama.ai/docs)
- **GitHub**: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Discord**: [https://discord.gg/ollama](https://discord.gg/ollama)

### Community Resources
- **Reddit**: r/ollama
- **Stack Overflow**: Tag `ollama`
- **GitHub Issues**: For bug reports and feature requests

### Diagnostic Commands
```bash
# System information
ollama --version
uname -a
free -h
df -h

# Ollama status
curl http://localhost:11434/api/version
ollama list
ollama ps

# Log files (Linux)
journalctl -u ollama -f
tail -f ~/.ollama/logs/ollama.log
```

## Next Steps

After successful installation:
1. Explore the `ollama_features.py` script for feature demonstrations
2. Try the `api_examples.py` for API integration examples
3. Learn model management with `model_management.py`
4. Experiment with different models and configurations
5. Check out the interactive notebooks for hands-on learning

## Security Considerations

1. **Network Security**: Only expose Ollama to trusted networks
2. **Model Verification**: Verify model checksums when possible
3. **Resource Limits**: Set appropriate resource limits in production
4. **Access Control**: Implement authentication for public deployments
5. **Regular Updates**: Keep Ollama updated to the latest version