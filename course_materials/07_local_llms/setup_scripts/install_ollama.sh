#!/bin/bash

# Ollama Installation Script
# Cross-platform installation script for Ollama
# Supports Linux, macOS, and Windows (via WSL)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Ollama on Linux
install_ollama_linux() {
    print_status "Installing Ollama on Linux..."
    
    # Check if curl is available
    if ! command_exists curl; then
        print_error "curl is required but not installed. Please install curl first."
        exit 1
    fi
    
    # Download and install Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Start Ollama service if systemd is available
    if command_exists systemctl; then
        print_status "Starting Ollama service..."
        sudo systemctl enable ollama
        sudo systemctl start ollama
        print_success "Ollama service started and enabled"
    else
        print_warning "systemd not found. You may need to start Ollama manually with 'ollama serve'"
    fi
}

# Function to install Ollama on macOS
install_ollama_macos() {
    print_status "Installing Ollama on macOS..."
    
    # Check if Homebrew is available
    if command_exists brew; then
        print_status "Installing Ollama via Homebrew..."
        brew install ollama
    else
        print_status "Homebrew not found. Installing via official installer..."
        
        # Check if curl is available
        if ! command_exists curl; then
            print_error "curl is required but not installed. Please install curl first."
            exit 1
        fi
        
        # Download and install Ollama
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    # Start Ollama service
    print_status "Starting Ollama service..."
    brew services start ollama 2>/dev/null || {
        print_warning "Could not start via brew services. Starting manually..."
        ollama serve &
    }
}

# Function to install Ollama on Windows (WSL)
install_ollama_windows() {
    print_status "Installing Ollama on Windows (WSL)..."
    
    # Check if we're in WSL
    if ! grep -q Microsoft /proc/version 2>/dev/null; then
        print_error "This script should be run in Windows Subsystem for Linux (WSL)"
        print_error "Please install WSL first: https://docs.microsoft.com/en-us/windows/wsl/install"
        exit 1
    fi
    
    # Install like Linux
    install_ollama_linux
}

# Function to verify installation
verify_installation() {
    print_status "Verifying Ollama installation..."
    
    # Wait a moment for service to start
    sleep 3
    
    # Check if ollama command is available
    if ! command_exists ollama; then
        print_error "Ollama command not found in PATH"
        return 1
    fi
    
    # Check if Ollama service is running
    if ollama list >/dev/null 2>&1; then
        print_success "Ollama is installed and running correctly"
        
        # Show version
        local version=$(ollama --version 2>/dev/null || echo "unknown")
        print_status "Ollama version: $version"
        
        return 0
    else
        print_warning "Ollama is installed but may not be running"
        print_status "Try running 'ollama serve' in a separate terminal"
        return 1
    fi
}

# Function to download a test model
download_test_model() {
    print_status "Would you like to download a small test model? (llama3.2:1b - ~1.3GB)"
    read -p "Download test model? [y/N]: " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Downloading llama3.2:1b model..."
        if ollama pull llama3.2:1b; then
            print_success "Test model downloaded successfully"
            print_status "You can test it with: ollama run llama3.2:1b"
        else
            print_warning "Failed to download test model. You can try again later with: ollama pull llama3.2:1b"
        fi
    fi
}

# Main installation function
main() {
    print_status "Ollama Cross-Platform Installation Script"
    print_status "========================================="
    
    # Detect operating system
    local os=$(detect_os)
    print_status "Detected OS: $os"
    
    # Check if Ollama is already installed
    if command_exists ollama; then
        print_warning "Ollama is already installed"
        local version=$(ollama --version 2>/dev/null || echo "unknown")
        print_status "Current version: $version"
        
        read -p "Do you want to continue anyway? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Installation cancelled"
            exit 0
        fi
    fi
    
    # Install based on OS
    case $os in
        "linux")
            install_ollama_linux
            ;;
        "macos")
            install_ollama_macos
            ;;
        "windows")
            install_ollama_windows
            ;;
        *)
            print_error "Unsupported operating system: $OSTYPE"
            print_error "Please visit https://ollama.ai for manual installation instructions"
            exit 1
            ;;
    esac
    
    # Verify installation
    if verify_installation; then
        print_success "Ollama installation completed successfully!"
        
        # Offer to download test model
        download_test_model
        
        print_status ""
        print_status "Next steps:"
        print_status "1. Try: ollama run llama3.2:1b"
        print_status "2. List models: ollama list"
        print_status "3. Pull more models: ollama pull <model-name>"
        print_status "4. Visit https://ollama.ai/library for available models"
    else
        print_error "Installation may have issues. Check the troubleshooting guide."
        exit 1
    fi
}

# Run main function
main "$@"