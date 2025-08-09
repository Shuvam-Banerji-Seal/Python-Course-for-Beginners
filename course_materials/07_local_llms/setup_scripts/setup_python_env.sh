#!/bin/bash

# Python Environment Setup Script
# Sets up Python virtual environment with all required dependencies for local LLMs

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_NAME="local_llms_env"
PYTHON_MIN_VERSION="3.8"
REQUIREMENTS_FILE="requirements.txt"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare version numbers
version_compare() {
    if [[ $1 == $2 ]]; then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [[ -z ${ver2[i]} ]]; then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2
        fi
    done
    return 0
}

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    
    if ! command_exists "$python_cmd"; then
        return 1
    fi
    
    local python_version=$($python_cmd --version 2>&1 | cut -d' ' -f2)
    version_compare "$python_version" "$PYTHON_MIN_VERSION"
    local result=$?
    
    if [[ $result -eq 2 ]]; then
        return 1
    fi
    
    echo "$python_version"
    return 0
}

# Function to find suitable Python interpreter
find_python() {
    local python_commands=("python3" "python" "python3.11" "python3.10" "python3.9" "python3.8")
    
    for cmd in "${python_commands[@]}"; do
        if python_version=$(check_python_version "$cmd"); then
            echo "$cmd"
            return 0
        fi
    done
    
    return 1
}

# Function to create requirements.txt if it doesn't exist
create_requirements_file() {
    if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
        print_status "Creating requirements.txt file..."
        cat > "$REQUIREMENTS_FILE" << 'EOF'
# Core dependencies for local LLMs
ollama>=0.1.0
requests>=2.31.0
numpy>=1.24.0
torch>=2.0.0
transformers>=4.30.0
tokenizers>=0.13.0
accelerate>=0.20.0
bitsandbytes>=0.41.0

# Optional GPU support (uncomment if you have CUDA)
# torch-audio>=2.0.0
# torchaudio>=2.0.0

# Jupyter and interactive tools
jupyter>=1.0.0
ipywidgets>=8.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0

# Development and testing
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0

# Additional utilities
tqdm>=4.65.0
python-dotenv>=1.0.0
pyyaml>=6.0
rich>=13.0.0
typer>=0.9.0

# Optional: For advanced model formats
safetensors>=0.3.0
huggingface-hub>=0.16.0
datasets>=2.14.0

# Optional: For quantization
optimum>=1.12.0
auto-gptq>=0.4.0
EOF
        print_success "Created requirements.txt with essential dependencies"
    else
        print_status "Using existing requirements.txt file"
    fi
}

# Function to detect GPU support
detect_gpu_support() {
    print_status "Detecting GPU support..."
    
    # Check for NVIDIA GPU
    if command_exists nvidia-smi; then
        local gpu_info=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -1)
        if [[ -n "$gpu_info" ]]; then
            print_success "NVIDIA GPU detected: $gpu_info"
            return 0
        fi
    fi
    
    # Check for AMD GPU (basic detection)
    if lspci 2>/dev/null | grep -i amd | grep -i vga >/dev/null; then
        print_warning "AMD GPU detected (limited support for some libraries)"
        return 1
    fi
    
    # Check for Apple Silicon
    if [[ "$(uname)" == "Darwin" ]] && [[ "$(uname -m)" == "arm64" ]]; then
        print_success "Apple Silicon detected (Metal Performance Shaders support available)"
        return 0
    fi
    
    print_warning "No GPU detected or GPU support unavailable"
    return 1
}

# Function to install PyTorch with appropriate backend
install_pytorch() {
    print_status "Installing PyTorch with appropriate backend..."
    
    if detect_gpu_support; then
        if command_exists nvidia-smi; then
            print_status "Installing PyTorch with CUDA support..."
            $PYTHON_CMD -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        elif [[ "$(uname)" == "Darwin" ]] && [[ "$(uname -m)" == "arm64" ]]; then
            print_status "Installing PyTorch for Apple Silicon..."
            $PYTHON_CMD -m pip install torch torchvision torchaudio
        else
            print_status "Installing PyTorch CPU version..."
            $PYTHON_CMD -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        fi
    else
        print_status "Installing PyTorch CPU version..."
        $PYTHON_CMD -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    fi
}

# Function to create virtual environment
create_virtual_environment() {
    print_status "Creating virtual environment: $VENV_NAME"
    
    # Remove existing environment if it exists
    if [[ -d "$VENV_NAME" ]]; then
        print_warning "Virtual environment $VENV_NAME already exists"
        read -p "Do you want to remove it and create a new one? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_NAME"
            print_status "Removed existing virtual environment"
        else
            print_status "Using existing virtual environment"
            return 0
        fi
    fi
    
    # Create new virtual environment
    $PYTHON_CMD -m venv "$VENV_NAME"
    print_success "Virtual environment created successfully"
}

# Function to activate virtual environment
activate_virtual_environment() {
    print_status "Activating virtual environment..."
    
    # Check if activation script exists
    if [[ -f "$VENV_NAME/bin/activate" ]]; then
        source "$VENV_NAME/bin/activate"
        PYTHON_CMD="python"
    elif [[ -f "$VENV_NAME/Scripts/activate" ]]; then
        source "$VENV_NAME/Scripts/activate"
        PYTHON_CMD="python"
    else
        print_error "Could not find virtual environment activation script"
        return 1
    fi
    
    print_success "Virtual environment activated"
}

# Function to upgrade pip
upgrade_pip() {
    print_status "Upgrading pip..."
    $PYTHON_CMD -m pip install --upgrade pip setuptools wheel
    print_success "pip upgraded successfully"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies from requirements.txt..."
    
    # Install PyTorch first (special handling for GPU support)
    install_pytorch
    
    # Install other dependencies, excluding PyTorch to avoid conflicts
    $PYTHON_CMD -m pip install -r "$REQUIREMENTS_FILE" --no-deps || {
        print_warning "Some packages failed to install without dependencies. Trying with dependencies..."
        $PYTHON_CMD -m pip install -r "$REQUIREMENTS_FILE"
    }
    
    print_success "Dependencies installed successfully"
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Test core imports
    local test_script=$(cat << 'EOF'
import sys
print(f"Python version: {sys.version}")

try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU count: {torch.cuda.device_count()}")
except ImportError as e:
    print(f"PyTorch import error: {e}")

try:
    import transformers
    print(f"Transformers version: {transformers.__version__}")
except ImportError as e:
    print(f"Transformers import error: {e}")

try:
    import ollama
    print("Ollama Python client available")
except ImportError as e:
    print(f"Ollama import error: {e}")

try:
    import jupyter
    print("Jupyter available")
except ImportError as e:
    print(f"Jupyter import error: {e}")

print("Verification complete!")
EOF
)
    
    echo "$test_script" | $PYTHON_CMD
    
    if [[ $? -eq 0 ]]; then
        print_success "Installation verification completed"
        return 0
    else
        print_error "Installation verification failed"
        return 1
    fi
}

# Function to create activation helper script
create_activation_script() {
    print_status "Creating activation helper script..."
    
    cat > "activate_local_llms.sh" << EOF
#!/bin/bash
# Helper script to activate the local LLMs environment

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\${BLUE}Activating local LLMs environment...\${NC}"

# Activate virtual environment
if [[ -f "$VENV_NAME/bin/activate" ]]; then
    source "$VENV_NAME/bin/activate"
elif [[ -f "$VENV_NAME/Scripts/activate" ]]; then
    source "$VENV_NAME/Scripts/activate"
else
    echo "Error: Could not find virtual environment"
    exit 1
fi

echo -e "\${GREEN}Environment activated!\${NC}"
echo "You can now run:"
echo "  - jupyter notebook (for interactive notebooks)"
echo "  - python (to run Python scripts)"
echo "  - ollama (if Ollama is installed)"
echo ""
echo "To deactivate, run: deactivate"
EOF
    
    chmod +x "activate_local_llms.sh"
    print_success "Created activation script: activate_local_llms.sh"
}

# Main setup function
main() {
    print_status "Python Environment Setup for Local LLMs"
    print_status "========================================"
    
    # Find suitable Python interpreter
    if PYTHON_CMD=$(find_python); then
        local python_version=$(check_python_version "$PYTHON_CMD")
        print_success "Found suitable Python: $PYTHON_CMD (version $python_version)"
    else
        print_error "No suitable Python interpreter found (minimum version: $PYTHON_MIN_VERSION)"
        print_error "Please install Python $PYTHON_MIN_VERSION or higher"
        exit 1
    fi
    
    # Create requirements file if needed
    create_requirements_file
    
    # Create virtual environment
    create_virtual_environment
    
    # Activate virtual environment
    activate_virtual_environment
    
    # Upgrade pip
    upgrade_pip
    
    # Install dependencies
    install_dependencies
    
    # Verify installation
    if verify_installation; then
        print_success "Python environment setup completed successfully!"
        
        # Create activation helper
        create_activation_script
        
        print_status ""
        print_status "Next steps:"
        print_status "1. Activate environment: source activate_local_llms.sh"
        print_status "2. Start Jupyter: jupyter notebook"
        print_status "3. Test installation: python -c 'import torch, transformers; print(\"Success!\")'"
        print_status "4. Install Ollama if not already done: ./install_ollama.sh"
    else
        print_error "Setup completed with some issues. Check the output above."
        exit 1
    fi
}

# Run main function
main "$@"