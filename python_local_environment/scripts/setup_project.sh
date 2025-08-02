#!/bin/bash

# Python Project Setup Script
# Usage: ./setup_project.sh <project_name> [python_version]

set -e

PROJECT_NAME=${1:-"my_python_project"}
PYTHON_VERSION=${2:-"3.11"}

echo "🐍 Setting up Python project: $PROJECT_NAME"
echo "📦 Using Python version: $PYTHON_VERSION"

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Set Python version with pyenv (if available)
if command -v pyenv &> /dev/null; then
    echo "🔧 Setting Python version with pyenv..."
    pyenv local "$PYTHON_VERSION"
else
    echo "⚠️  pyenv not found, using system Python"
fi

# Create virtual environment
echo "🏗️  Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Create basic project structure
echo "📁 Creating project structure..."
mkdir -p src tests docs

# Create basic files
cat > README.md << EOF
# $PROJECT_NAME

A Python project created with the setup script.

## Setup

1. Create virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate     # Windows
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Development

Install development dependencies:
\`\`\`bash
pip install -r requirements-dev.txt
\`\`\`

Run tests:
\`\`\`bash
pytest
\`\`\`

## Usage

TODO: Add usage instructions
EOF

# Create .gitignore
cat > .gitignore << EOF
# Virtual environments
venv/
env/
ENV/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Documentation
docs/_build/
EOF

# Create requirements files
cat > requirements.txt << EOF
# Production dependencies
# Add your dependencies here
# Example:
# requests>=2.25.0
# click>=8.0.0
EOF

cat > requirements-dev.txt << EOF
-r requirements.txt

# Development dependencies
pytest>=6.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.900
pre-commit>=2.15.0
EOF

# Create basic Python files
cat > src/__init__.py << EOF
"""$PROJECT_NAME package."""

__version__ = "0.1.0"
EOF

cat > src/main.py << EOF
"""Main module for $PROJECT_NAME."""


def main():
    """Main function."""
    print("Hello from $PROJECT_NAME!")


if __name__ == "__main__":
    main()
EOF

cat > tests/__init__.py << EOF
"""Tests for $PROJECT_NAME."""
EOF

cat > tests/test_main.py << EOF
"""Tests for main module."""

from src.main import main


def test_main():
    """Test main function."""
    # This is a placeholder test
    assert main() is None
EOF

# Create pyproject.toml
cat > pyproject.toml << EOF
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
requires-python = ">=3.8"
dependencies = [
    # Add your dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "pytest-cov>=3.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
    "mypy>=0.900",
    "pre-commit>=2.15.0",
]

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=html --cov-report=term"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
EOF

# Initialize git repository
echo "📝 Initializing git repository..."
git init
git add .
git commit -m "Initial commit: Project setup"

echo "✅ Project setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. source venv/bin/activate"
echo "3. pip install -r requirements-dev.txt"
echo "4. Start coding in src/"
echo ""
echo "🧪 Run tests with: pytest"
echo "🎨 Format code with: black src/ tests/"
echo "🔍 Lint code with: flake8 src/ tests/"