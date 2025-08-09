#!/bin/bash

# 🚀 Quick Start Script for Local LLMs Course! 🚀
# This script helps you get everything set up quickly and easily!

echo "🌟 Welcome to the Local LLMs Quick Start Setup! 🌟"
echo "=================================================="

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "course_materials/07_local_llms" ]; then
    print_error "Please run this script from the course root directory!"
    exit 1
fi

print_step "Step 1: Checking system requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not found!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is required but not found!"
    exit 1
fi

print_step "Step 2: Installing Python dependencies..."

# Install required packages
pip3 install -r course_materials/07_local_llms/requirements.txt

if [ $? -eq 0 ]; then
    print_status "Python packages installed successfully!"
else
    print_error "Failed to install Python packages"
    exit 1
fi

print_step "Step 3: Checking for Ollama..."

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    print_status "Ollama is installed!"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_status "Ollama is running!"
        
        # List available models
        echo ""
        print_info "Available models:"
        ollama list
        
    else
        print_warning "Ollama is installed but not running"
        print_info "Starting Ollama..."
        
        # Try to start Ollama in background
        ollama serve &
        OLLAMA_PID=$!
        
        # Wait a moment for it to start
        sleep 3
        
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            print_status "Ollama started successfully!"
        else
            print_error "Failed to start Ollama automatically"
            print_info "Please start Ollama manually: ollama serve"
        fi
    fi
    
else
    print_warning "Ollama is not installed!"
    echo ""
    print_info "To install Ollama:"
    echo "1. Visit: https://ollama.ai"
    echo "2. Download for your operating system"
    echo "3. Install and run: ollama serve"
    echo "4. Download a model: ollama pull llama2:7b-chat"
    echo ""
fi

print_step "Step 4: Setting up Jupyter environment..."

# Install Jupyter if not present
if ! command -v jupyter &> /dev/null; then
    print_info "Installing Jupyter..."
    pip3 install jupyter ipywidgets
fi

# Enable widgets extension
jupyter nbextension enable --py widgetsnbextension --sys-prefix 2>/dev/null

print_step "Step 5: Creating quick access scripts..."

# Create a quick start script for notebooks
cat > course_materials/07_local_llms/start_notebooks.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Jupyter Notebooks for Local LLMs Course!"
echo "📂 Opening notebooks directory..."
cd course_materials/07_local_llms/notebooks
jupyter notebook
EOF

chmod +x course_materials/07_local_llms/start_notebooks.sh

# Create a quick test script
cat > course_materials/07_local_llms/test_setup.py << 'EOF'
#!/usr/bin/env python3
"""
🧪 Quick setup test script
"""
import sys
import requests

def test_setup():
    print("🧪 Testing Local LLMs Setup...")
    print("=" * 40)
    
    # Test Python packages
    try:
        import ipywidgets
        import matplotlib
        import pandas
        import numpy
        print("✅ Python packages: OK")
    except ImportError as e:
        print(f"❌ Python packages: Missing {e}")
        return False
    
    # Test Ollama connection
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connection: OK ({len(models)} models)")
            if models:
                print("📚 Available models:")
                for model in models:
                    print(f"   - {model['name']}")
            else:
                print("⚠️  No models downloaded yet")
                print("💡 Try: ollama pull llama2:7b-chat")
        else:
            print("❌ Ollama connection: Failed")
            return False
    except Exception as e:
        print(f"❌ Ollama connection: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    
    print("\n🎉 Setup test completed!")
    return True

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
EOF

chmod +x course_materials/07_local_llms/test_setup.py

print_step "Step 6: Final setup verification..."

# Run the test script
python3 course_materials/07_local_llms/test_setup.py

echo ""
print_status "🎉 Quick Start Setup Complete!"
echo ""
print_info "Next steps:"
echo "1. 📚 Start with: course_materials/07_local_llms/notebooks/00_welcome_to_local_llms.ipynb"
echo "2. 🚀 Launch notebooks: ./course_materials/07_local_llms/start_notebooks.sh"
echo "3. 🎭 Try character prompts: python3 course_materials/07_local_llms/system_prompts/anime_character_prompts.py"
echo ""
print_info "If you need to download a model:"
echo "   ollama pull llama2:7b-chat"
echo ""
print_status "Happy learning! 🌟"