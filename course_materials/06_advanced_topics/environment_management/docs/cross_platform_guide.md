# Cross-Platform Python Environment Guide

This guide covers Python environment management across Arch Linux, Ubuntu, and Windows.

## Platform-Specific Commands

### Virtual Environment Creation

#### Arch Linux
```bash
# Using system package manager
sudo pacman -S python python-pip python-virtualenv

# Create environment
python -m venv myproject
# or
virtualenv myproject

# Activate
source myproject/bin/activate

# Install uv (modern alternative)
sudo pacman -S uv
# or
pip install uv
uv venv myproject
```

#### Ubuntu/Debian
```bash
# Install Python and tools
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-virtualenv

# Create environment
python3 -m venv myproject
# or
virtualenv myproject

# Activate
source myproject/bin/activate

# Install uv
pip install uv
# or using curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
```powershell
# Using Python installer from python.org
# pip is included by default

# Create environment
python -m venv myproject
# or
virtualenv myproject

# Activate
myproject\Scripts\activate

# Install uv
pip install uv
# or using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Python Version Management

#### Arch Linux (pyenv)
```bash
# Install pyenv
yay -S pyenv
# or manual
curl https://pyenv.run | bash

# Add to ~/.bashrc or ~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Install Python versions
pyenv install 3.11.7
pyenv install 3.12.1
pyenv global 3.11.7
```

#### Ubuntu (pyenv)
```bash
# Install dependencies
sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev

# Install pyenv
curl https://pyenv.run | bash

# Add to shell configuration
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Install Python versions
pyenv install 3.11.7
pyenv global 3.11.7
```

#### Windows (pyenv-win)
```powershell
# Install pyenv-win
git clone https://github.com/pyenv-win/pyenv-win.git $env:USERPROFILE\.pyenv

# Add to PATH (PowerShell profile)
$env:PYENV = "$env:USERPROFILE\.pyenv\pyenv-win\"
$env:PYENV_ROOT = "$env:USERPROFILE\.pyenv\pyenv-win\"
$env:PYENV_HOME = "$env:USERPROFILE\.pyenv\pyenv-win\"
$env:PATH = "$env:PYENV\bin;$env:PYENV\shims;$env:PATH"

# Or use Chocolatey
choco install pyenv-win

# Install Python versions
pyenv install 3.11.7
pyenv global 3.11.7
```

## Shell Configuration

### Bash (.bashrc)
```bash
# Python environment tools
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# uv
export PATH="$HOME/.local/bin:$PATH"

# Aliases for convenience
alias py="python"
alias venv-create="python -m venv"
alias venv-activate="source ./venv/bin/activate"
```

### Zsh (.zshrc)
```zsh
# Python environment tools
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# uv
export PATH="$HOME/.local/bin:$PATH"

# Oh My Zsh plugins (if using)
plugins=(git python pip virtualenv)
```

### Fish (config.fish)
```fish
# Python environment tools
set -gx PYENV_ROOT $HOME/.pyenv
set -gx PATH $PYENV_ROOT/bin $PATH
pyenv init - | source

# uv
set -gx PATH $HOME/.local/bin $PATH

# Abbreviations
abbr py python
abbr venv-create python -m venv
abbr venv-activate source ./venv/bin/activate
```

### PowerShell (Profile)
```powershell
# Python environment tools
$env:PYENV = "$env:USERPROFILE\.pyenv\pyenv-win\"
$env:PYENV_ROOT = "$env:USERPROFILE\.pyenv\pyenv-win\"
$env:PATH = "$env:PYENV\bin;$env:PYENV\shims;$env:PATH"

# uv
$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"

# Aliases
Set-Alias py python
function venv-create { python -m venv $args }
function venv-activate { & ".\venv\Scripts\activate" }
```

## Common Workflows

### Project Setup (Cross-platform)
```bash
# 1. Create project directory
mkdir myproject
cd myproject

# 2. Set Python version (if using pyenv)
pyenv local 3.11.7

# 3. Create virtual environment
python -m venv venv

# 4. Activate environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install dependencies
pip install -r requirements.txt

# 7. Work on project...

# 8. Deactivate when done
deactivate
```

### Using uv (Modern workflow)
```bash
# Initialize project
uv init myproject
cd myproject

# Add dependencies
uv add requests pandas numpy

# Add development dependencies
uv add pytest black flake8 --dev

# Run commands in project environment
uv run python main.py
uv run pytest

# Sync environment
uv sync
```

## Platform-Specific Considerations

### Arch Linux
- **Package Manager**: Use `pacman` for system packages, avoid `pip install --user`
- **AUR**: Many Python tools available through AUR (yay, paru)
- **Rolling Release**: Always up-to-date Python versions
- **Virtual Environments**: Strongly recommended to avoid conflicts

### Ubuntu/Debian
- **APT Packages**: Use `apt` for system packages when available
- **Python Versions**: May have older Python versions, use pyenv for latest
- **Dependencies**: Install build dependencies for compiling Python
- **Permissions**: May need `sudo` for system-wide installations

### Windows
- **Python Installation**: Use official installer from python.org
- **PATH Management**: Ensure Python is in PATH
- **PowerShell vs CMD**: PowerShell recommended for better experience
- **Line Endings**: Be aware of CRLF vs LF in cross-platform projects
- **Long Paths**: Enable long path support for deep directory structures

## Troubleshooting

### Common Issues

#### Permission Errors
```bash
# Linux/Mac: Don't use sudo with pip in virtual environments
# Instead, ensure virtual environment is activated

# Windows: Run as administrator if needed, but prefer user installs
pip install --user package_name
```

#### Path Issues
```bash
# Check Python location
which python  # Linux/Mac
where python   # Windows

# Check if in virtual environment
echo $VIRTUAL_ENV  # Linux/Mac
echo $env:VIRTUAL_ENV  # Windows PowerShell
```

#### SSL Certificate Errors
```bash
# Update certificates
# Linux:
sudo apt update && sudo apt install ca-certificates
# Mac:
brew install ca-certificates
# Windows: Usually automatic

# Or skip SSL verification (not recommended for production)
pip install --trusted-host pypi.org --trusted-host pypi.python.org package_name
```

### Platform-Specific Fixes

#### Arch Linux
```bash
# Update keyring if package verification fails
sudo pacman -S archlinux-keyring
sudo pacman -Syu

# Fix locale issues
sudo locale-gen
```

#### Ubuntu
```bash
# Fix broken packages
sudo apt --fix-broken install
sudo dpkg --configure -a

# Update package lists
sudo apt update && sudo apt upgrade
```

#### Windows
```powershell
# Fix execution policy for scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Repair Python installation
python -m pip install --upgrade --force-reinstall pip
```

## Best Practices

1. **Always use virtual environments** for project isolation
2. **Pin dependency versions** in production
3. **Use pyproject.toml** for modern Python projects
4. **Keep requirements files updated** and organized
5. **Document Python version requirements** clearly
6. **Test across platforms** if targeting multiple OS
7. **Use consistent line endings** in cross-platform projects
8. **Automate environment setup** with scripts