# UV Project Example

This is an example FastAPI project managed with `uv`, demonstrating modern Python dependency management.

## Setup with uv

1. **Install uv** (if not already installed):
   ```bash
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or with pip
   pip install uv
   ```

2. **Initialize and sync the project**:
   ```bash
   # Clone or create the project directory
   cd uv_project_example
   
   # Sync dependencies (creates virtual environment automatically)
   uv sync
   ```

3. **Run the application**:
   ```bash
   # Run with uv (automatically uses project environment)
   uv run python main.py
   
   # Or run uvicorn directly
   uv run uvicorn main:app --reload
   ```

4. **Add new dependencies**:
   ```bash
   # Add production dependency
   uv add requests
   
   # Add development dependency
   uv add pytest --dev
   ```

5. **Run development tools**:
   ```bash
   # Format code
   uv run black .
   
   # Lint code
   uv run ruff check .
   
   # Type checking
   uv run mypy .
   
   # Run tests
   uv run pytest
   ```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /external` - Fetch external data

## Development

The project uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **httpx** for async HTTP requests
- **uvicorn** for the ASGI server

Development tools:
- **pytest** for testing
- **black** for code formatting
- **ruff** for linting
- **mypy** for type checking

## Traditional vs uv Workflow

### Traditional workflow:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### uv workflow:
```bash
uv sync
uv run python main.py
```

The uv approach is faster, handles virtual environments automatically, and provides better dependency resolution.