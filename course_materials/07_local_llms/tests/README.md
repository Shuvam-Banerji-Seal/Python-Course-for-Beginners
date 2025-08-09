# Local LLMs Testing Suite

This directory contains comprehensive testing and validation tools for the local LLMs module, ensuring code quality, functionality, and educational content accuracy.

## Test Structure

### Unit Tests
- **`test_ollama_manager.py`** - Comprehensive tests for OllamaManager utility class
- **`test_transformers_manager.py`** - Tests for TransformersManager with quantization and memory optimization
- **`test_prompt_template.py`** - Tests for prompt template management system
- **`test_utilities.py`** - Tests for utility functions and helper methods

### Integration Tests
- **`integration_tests.py`** - End-to-end workflow tests and cross-platform compatibility
- **`test_notebook_execution.py`** - Automated Jupyter notebook execution and validation

### Test Configuration
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`run_all_tests.py`** - Comprehensive test runner for all test suites

### Utility Modules
- **`test_utilities.py`** (in utils/) - Utility functions for testing and validation
- **`validate_utilities.py`** (in utils/) - Validation functions for responses and configurations

## Running Tests

### Quick Test Run
```bash
# Run basic unit tests
python course_materials/07_local_llms/tests/run_all_tests.py --unit-only

# Run notebook validation only
python course_materials/07_local_llms/tests/run_all_tests.py --notebooks-only
```

### Comprehensive Test Suite
```bash
# Run all tests including integration tests
python course_materials/07_local_llms/tests/run_all_tests.py --integration --verbose

# Save results to file
python course_materials/07_local_llms/tests/run_all_tests.py --output test_results.json
```

### Individual Test Components

#### Unit Tests (with pytest if available)
```bash
pytest course_materials/07_local_llms/tests/test_ollama_manager.py -v
pytest course_materials/07_local_llms/tests/test_transformers_manager.py -v
pytest course_materials/07_local_llms/tests/test_prompt_template.py -v
```

#### Integration Tests
```bash
python course_materials/07_local_llms/tests/integration_tests.py
```

#### Notebook Testing
```bash
python course_materials/07_local_llms/tests/test_notebook_execution.py --report
```

## Test Categories

### Unit Tests
- **Model Management**: Test model loading, unloading, and information retrieval
- **Response Generation**: Test text generation with various configurations
- **Template Processing**: Test prompt template rendering and validation
- **Utility Functions**: Test helper functions for formatting, validation, and system checks
- **Error Handling**: Test exception handling and error recovery

### Integration Tests
- **Ollama Integration**: End-to-end tests with actual Ollama server (when available)
- **Transformers Integration**: Tests with Hugging Face Transformers models
- **Cross-Platform Compatibility**: Path handling, memory detection, file operations
- **Complete Workflows**: Full pipeline from setup to inference

### Notebook Tests
- **Structure Validation**: Check notebook cell structure and content balance
- **Execution Testing**: Automated execution of notebook cells
- **Dependency Extraction**: Identify required packages from notebooks
- **Output Validation**: Verify notebook outputs and error handling

## Test Features

### Mocking and Fixtures
- Mock external dependencies (requests, torch, transformers)
- Provide sample data for consistent testing
- Handle missing dependencies gracefully

### Performance Testing
- Memory usage monitoring
- Execution time measurement
- Resource optimization validation

### Error Simulation
- Network connectivity issues
- Out-of-memory conditions
- Invalid input handling
- Service unavailability

### Cross-Platform Support
- Windows, macOS, and Linux compatibility
- Different Python versions
- Various hardware configurations

## Test Configuration

### Markers
- `@pytest.mark.integration` - Tests requiring external services
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.gpu` - Tests requiring GPU hardware

### Environment Variables
- `OLLAMA_BASE_URL` - Custom Ollama server URL
- `HF_HOME` - Hugging Face cache directory
- `PYTEST_TIMEOUT` - Test timeout in seconds

### Dependencies
The test suite handles missing dependencies gracefully:
- **Required**: Python 3.7+, basic standard library
- **Optional**: pytest, requests, torch, transformers, psutil, nbformat
- **External**: Ollama server (for integration tests)

## Test Results

### Success Criteria
- All unit tests pass
- Integration tests pass when services are available
- Notebooks execute without errors
- Cross-platform compatibility verified

### Failure Handling
- Graceful degradation when optional dependencies are missing
- Clear error messages for configuration issues
- Detailed logging for debugging

### Reporting
- Console output with progress indicators
- JSON output for CI/CD integration
- Detailed error reporting with stack traces
- Performance metrics and timing information

## Continuous Integration

The test suite is designed for CI/CD environments:
- Automatic dependency detection
- Configurable test selection
- Machine-readable output formats
- Exit codes for build systems

### Example CI Configuration
```yaml
# Example GitHub Actions workflow
- name: Run Local LLMs Tests
  run: |
    python course_materials/07_local_llms/tests/run_all_tests.py \
      --output test_results.json \
      --verbose
```

## Contributing

When adding new functionality:
1. Write corresponding unit tests
2. Add integration tests for external dependencies
3. Update notebook tests if educational content changes
4. Ensure cross-platform compatibility
5. Update this documentation

### Test Guidelines
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies appropriately
- Add performance considerations for slow operations
- Document any special setup requirements