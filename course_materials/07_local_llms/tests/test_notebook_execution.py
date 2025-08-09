"""
Automated notebook execution testing for the local LLMs module.

This module provides functionality to automatically execute Jupyter notebooks
and validate their output, ensuring all educational content works correctly.
"""

import pytest
import sys
import os
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError


class NotebookTester:
    """
    Class for testing Jupyter notebook execution.
    """
    
    def __init__(self, timeout: int = 300, kernel_name: str = "python3"):
        """
        Initialize the notebook tester.
        
        Args:
            timeout: Maximum time to wait for cell execution (seconds)
            kernel_name: Jupyter kernel name to use
        """
        self.timeout = timeout
        self.kernel_name = kernel_name
        self.executor = ExecutePreprocessor(
            timeout=timeout,
            kernel_name=kernel_name,
            allow_errors=False
        )
    
    def execute_notebook(self, notebook_path: Path) -> Tuple[bool, Dict[str, Any]]:
        """
        Execute a Jupyter notebook and return results.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            Tuple of (success, results_dict)
        """
        results = {
            "notebook": str(notebook_path),
            "success": False,
            "execution_time": 0,
            "cells_executed": 0,
            "cells_failed": 0,
            "errors": [],
            "warnings": [],
            "outputs": []
        }
        
        try:
            # Read the notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
            
            # Execute the notebook
            import time
            start_time = time.time()
            
            executed_notebook, resources = self.executor.preprocess(notebook, {})
            
            results["execution_time"] = time.time() - start_time
            results["success"] = True
            
            # Analyze execution results
            for cell in executed_notebook.cells:
                if cell.cell_type == "code":
                    results["cells_executed"] += 1
                    
                    # Check for outputs
                    if hasattr(cell, 'outputs') and cell.outputs:
                        for output in cell.outputs:
                            if output.output_type == "error":
                                results["cells_failed"] += 1
                                results["errors"].append({
                                    "cell_index": len(results["outputs"]),
                                    "error_name": output.ename,
                                    "error_value": output.evalue,
                                    "traceback": output.traceback
                                })
                            elif output.output_type in ["stream", "display_data", "execute_result"]:
                                results["outputs"].append({
                                    "cell_index": len(results["outputs"]),
                                    "output_type": output.output_type,
                                    "data": getattr(output, 'data', {}),
                                    "text": getattr(output, 'text', '')
                                })
            
            return True, results
            
        except CellExecutionError as e:
            results["errors"].append({
                "type": "CellExecutionError",
                "message": str(e),
                "cell_index": getattr(e, 'cell_index', -1)
            })
            return False, results
            
        except Exception as e:
            results["errors"].append({
                "type": type(e).__name__,
                "message": str(e)
            })
            return False, results
    
    def validate_notebook_structure(self, notebook_path: Path) -> Dict[str, Any]:
        """
        Validate the structure and content of a notebook.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            "valid": True,
            "issues": [],
            "statistics": {
                "total_cells": 0,
                "code_cells": 0,
                "markdown_cells": 0,
                "empty_cells": 0,
                "cells_with_outputs": 0
            }
        }
        
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
            
            validation["statistics"]["total_cells"] = len(notebook.cells)
            
            for i, cell in enumerate(notebook.cells):
                if cell.cell_type == "code":
                    validation["statistics"]["code_cells"] += 1
                    
                    # Check for empty code cells
                    if not cell.source.strip():
                        validation["statistics"]["empty_cells"] += 1
                        validation["issues"].append(f"Empty code cell at index {i}")
                    
                    # Check for outputs (indicates pre-executed notebook)
                    if hasattr(cell, 'outputs') and cell.outputs:
                        validation["statistics"]["cells_with_outputs"] += 1
                
                elif cell.cell_type == "markdown":
                    validation["statistics"]["markdown_cells"] += 1
                    
                    # Check for empty markdown cells
                    if not cell.source.strip():
                        validation["statistics"]["empty_cells"] += 1
                        validation["issues"].append(f"Empty markdown cell at index {i}")
            
            # Validate notebook metadata
            if "kernelspec" not in notebook.metadata:
                validation["issues"].append("Missing kernelspec in notebook metadata")
            
            # Check for reasonable balance of code vs markdown
            total_content_cells = (validation["statistics"]["code_cells"] + 
                                 validation["statistics"]["markdown_cells"])
            
            if total_content_cells > 0:
                markdown_ratio = validation["statistics"]["markdown_cells"] / total_content_cells
                if markdown_ratio < 0.2:
                    validation["issues"].append("Low ratio of documentation (markdown) cells")
                elif markdown_ratio > 0.8:
                    validation["issues"].append("High ratio of documentation cells, may lack practical examples")
            
            validation["valid"] = len(validation["issues"]) == 0
            
        except Exception as e:
            validation["valid"] = False
            validation["issues"].append(f"Failed to read notebook: {e}")
        
        return validation
    
    def extract_notebook_requirements(self, notebook_path: Path) -> List[str]:
        """
        Extract Python package requirements from a notebook.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            List of detected package requirements
        """
        requirements = set()
        
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
            
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    source = cell.source
                    
                    # Look for import statements
                    import re
                    
                    # Standard import patterns
                    import_patterns = [
                        r'^import\s+(\w+)',
                        r'^from\s+(\w+)\s+import',
                        r'^\s*import\s+(\w+)',
                        r'^\s*from\s+(\w+)\s+import'
                    ]
                    
                    for line in source.split('\n'):
                        line = line.strip()
                        for pattern in import_patterns:
                            match = re.match(pattern, line)
                            if match:
                                package = match.group(1)
                                # Filter out standard library modules
                                if package not in ['os', 'sys', 'json', 'time', 'datetime', 
                                                 'collections', 'itertools', 'functools', 
                                                 'pathlib', 'typing', 're', 'math', 'random']:
                                    requirements.add(package)
                    
                    # Look for pip install commands
                    pip_patterns = [
                        r'!pip\s+install\s+([^\s]+)',
                        r'%pip\s+install\s+([^\s]+)'
                    ]
                    
                    for line in source.split('\n'):
                        for pattern in pip_patterns:
                            matches = re.findall(pattern, line)
                            for match in matches:
                                # Clean up package names
                                package = match.split('==')[0].split('>=')[0].split('<=')[0]
                                requirements.add(package)
        
        except Exception:
            pass  # Ignore errors in requirement extraction
        
        return sorted(list(requirements))


@pytest.mark.integration
class TestNotebookExecution:
    """Test cases for notebook execution."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tester = NotebookTester(timeout=300)
        self.notebooks_dir = Path(__file__).parent.parent / "notebooks"
    
    def test_notebook_directory_exists(self):
        """Test that the notebooks directory exists."""
        assert self.notebooks_dir.exists(), f"Notebooks directory not found: {self.notebooks_dir}"
        
        # Check for notebook files
        notebook_files = list(self.notebooks_dir.glob("*.ipynb"))
        assert len(notebook_files) > 0, "No notebook files found in notebooks directory"
    
    @pytest.mark.parametrize("notebook_name", [
        "01_ollama_introduction.ipynb",
        "02_transformers_basics.ipynb",
        "03_model_formats_explained.ipynb",
        "04_prompt_engineering.ipynb",
        "05_performance_optimization.ipynb"
    ])
    def test_individual_notebook_structure(self, notebook_name):
        """Test individual notebook structure and content."""
        notebook_path = self.notebooks_dir / notebook_name
        
        if not notebook_path.exists():
            pytest.skip(f"Notebook not found: {notebook_name}")
        
        validation = self.tester.validate_notebook_structure(notebook_path)
        
        # Check basic validation
        assert validation["valid"] or len(validation["issues"]) <= 2, \
            f"Notebook structure issues: {validation['issues']}"
        
        # Check statistics
        stats = validation["statistics"]
        assert stats["total_cells"] > 0, "Notebook has no cells"
        assert stats["code_cells"] > 0, "Notebook has no code cells"
        assert stats["markdown_cells"] > 0, "Notebook has no markdown cells"
    
    @pytest.mark.slow
    @pytest.mark.parametrize("notebook_name", [
        "01_ollama_introduction.ipynb",
        "02_transformers_basics.ipynb",
        "03_model_formats_explained.ipynb",
        "04_prompt_engineering.ipynb"
    ])
    def test_individual_notebook_execution(self, notebook_name):
        """Test individual notebook execution."""
        notebook_path = self.notebooks_dir / notebook_name
        
        if not notebook_path.exists():
            pytest.skip(f"Notebook not found: {notebook_name}")
        
        # Skip execution tests that require external services
        if "ollama" in notebook_name.lower():
            # Check if Ollama is available
            from ollama_manager import OllamaManager
            manager = OllamaManager()
            if not manager.is_server_running():
                pytest.skip("Ollama server not running")
        
        if "transformers" in notebook_name.lower():
            # Check if transformers is available and we have sufficient resources
            try:
                import transformers
                from test_utilities import check_system_requirements
                requirements = check_system_requirements()
                if not requirements["sufficient_memory"]:
                    pytest.skip("Insufficient memory for Transformers models")
            except ImportError:
                pytest.skip("Transformers library not available")
        
        # Execute the notebook
        success, results = self.tester.execute_notebook(notebook_path)
        
        # Check execution results
        if not success:
            error_messages = [error.get("message", str(error)) for error in results["errors"]]
            pytest.fail(f"Notebook execution failed: {'; '.join(error_messages)}")
        
        assert results["cells_executed"] > 0, "No cells were executed"
        assert results["cells_failed"] == 0, f"Some cells failed: {results['errors']}"
    
    def test_notebook_requirements_extraction(self):
        """Test extraction of requirements from notebooks."""
        notebook_files = list(self.notebooks_dir.glob("*.ipynb"))
        
        if not notebook_files:
            pytest.skip("No notebook files found")
        
        all_requirements = set()
        
        for notebook_path in notebook_files:
            requirements = self.tester.extract_notebook_requirements(notebook_path)
            all_requirements.update(requirements)
        
        # Check that we found some requirements
        assert len(all_requirements) > 0, "No requirements found in any notebook"
        
        # Check for expected packages
        expected_packages = ["torch", "transformers", "requests", "numpy"]
        found_expected = [pkg for pkg in expected_packages if pkg in all_requirements]
        assert len(found_expected) > 0, f"Expected packages not found: {expected_packages}"
    
    def test_all_notebooks_batch_validation(self):
        """Test batch validation of all notebooks."""
        notebook_files = list(self.notebooks_dir.glob("*.ipynb"))
        
        if not notebook_files:
            pytest.skip("No notebook files found")
        
        validation_results = {}
        
        for notebook_path in notebook_files:
            validation = self.tester.validate_notebook_structure(notebook_path)
            validation_results[notebook_path.name] = validation
        
        # Check that most notebooks pass validation
        valid_notebooks = sum(1 for v in validation_results.values() if v["valid"])
        total_notebooks = len(validation_results)
        
        assert valid_notebooks >= total_notebooks * 0.8, \
            f"Too many notebooks failed validation: {valid_notebooks}/{total_notebooks}"
        
        # Report issues for failed notebooks
        for notebook_name, validation in validation_results.items():
            if not validation["valid"]:
                print(f"Issues in {notebook_name}: {validation['issues']}")


class NotebookTestRunner:
    """
    Standalone notebook test runner that doesn't require pytest.
    """
    
    def __init__(self, notebooks_dir: Path):
        """
        Initialize the test runner.
        
        Args:
            notebooks_dir: Directory containing notebooks to test
        """
        self.notebooks_dir = Path(notebooks_dir)
        self.tester = NotebookTester()
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all notebook tests and return results.
        
        Returns:
            Dictionary with test results
        """
        results = {
            "total_notebooks": 0,
            "validated_notebooks": 0,
            "executed_notebooks": 0,
            "failed_notebooks": 0,
            "notebook_results": {},
            "summary": {}
        }
        
        if not self.notebooks_dir.exists():
            results["error"] = f"Notebooks directory not found: {self.notebooks_dir}"
            return results
        
        notebook_files = list(self.notebooks_dir.glob("*.ipynb"))
        results["total_notebooks"] = len(notebook_files)
        
        if not notebook_files:
            results["error"] = "No notebook files found"
            return results
        
        for notebook_path in notebook_files:
            notebook_name = notebook_path.name
            notebook_result = {
                "path": str(notebook_path),
                "validation": None,
                "execution": None,
                "requirements": []
            }
            
            # Validate structure
            try:
                validation = self.tester.validate_notebook_structure(notebook_path)
                notebook_result["validation"] = validation
                if validation["valid"]:
                    results["validated_notebooks"] += 1
            except Exception as e:
                notebook_result["validation"] = {
                    "valid": False,
                    "error": str(e)
                }
            
            # Extract requirements
            try:
                requirements = self.tester.extract_notebook_requirements(notebook_path)
                notebook_result["requirements"] = requirements
            except Exception as e:
                notebook_result["requirements_error"] = str(e)
            
            # Execute notebook (optional, can be skipped for speed)
            try:
                # Only execute smaller notebooks or those without external dependencies
                if self._should_execute_notebook(notebook_name):
                    success, execution_result = self.tester.execute_notebook(notebook_path)
                    notebook_result["execution"] = execution_result
                    if success:
                        results["executed_notebooks"] += 1
                    else:
                        results["failed_notebooks"] += 1
                else:
                    notebook_result["execution"] = {"skipped": True, "reason": "External dependencies"}
            except Exception as e:
                notebook_result["execution"] = {
                    "success": False,
                    "error": str(e)
                }
                results["failed_notebooks"] += 1
            
            results["notebook_results"][notebook_name] = notebook_result
        
        # Generate summary
        results["summary"] = {
            "validation_rate": results["validated_notebooks"] / results["total_notebooks"],
            "execution_rate": results["executed_notebooks"] / results["total_notebooks"] if results["total_notebooks"] > 0 else 0,
            "failure_rate": results["failed_notebooks"] / results["total_notebooks"] if results["total_notebooks"] > 0 else 0
        }
        
        return results
    
    def _should_execute_notebook(self, notebook_name: str) -> bool:
        """
        Determine if a notebook should be executed based on its dependencies.
        
        Args:
            notebook_name: Name of the notebook file
            
        Returns:
            True if notebook should be executed
        """
        # Skip notebooks that require external services
        skip_patterns = [
            "ollama",  # Requires Ollama server
            "performance_optimization"  # May require large models
        ]
        
        notebook_lower = notebook_name.lower()
        return not any(pattern in notebook_lower for pattern in skip_patterns)
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable test report.
        
        Args:
            results: Test results from run_all_tests()
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("Notebook Test Report")
        report.append("=" * 50)
        
        if "error" in results:
            report.append(f"Error: {results['error']}")
            return "\n".join(report)
        
        # Summary
        report.append(f"Total Notebooks: {results['total_notebooks']}")
        report.append(f"Validated: {results['validated_notebooks']}")
        report.append(f"Executed: {results['executed_notebooks']}")
        report.append(f"Failed: {results['failed_notebooks']}")
        report.append("")
        
        # Rates
        summary = results["summary"]
        report.append(f"Validation Rate: {summary['validation_rate']:.1%}")
        report.append(f"Execution Rate: {summary['execution_rate']:.1%}")
        report.append(f"Failure Rate: {summary['failure_rate']:.1%}")
        report.append("")
        
        # Individual notebook results
        report.append("Individual Results:")
        report.append("-" * 30)
        
        for notebook_name, result in results["notebook_results"].items():
            status_symbols = []
            
            # Validation status
            if result["validation"] and result["validation"]["valid"]:
                status_symbols.append("✓")
            else:
                status_symbols.append("✗")
            
            # Execution status
            if result["execution"]:
                if result["execution"].get("skipped"):
                    status_symbols.append("⚠")
                elif result["execution"].get("success"):
                    status_symbols.append("✓")
                else:
                    status_symbols.append("✗")
            else:
                status_symbols.append("-")
            
            status = " ".join(status_symbols)
            report.append(f"  {status} {notebook_name}")
            
            # Add details for failed notebooks
            if result["validation"] and not result["validation"]["valid"]:
                issues = result["validation"].get("issues", [])
                for issue in issues[:3]:  # Show first 3 issues
                    report.append(f"    - {issue}")
            
            if result["execution"] and not result["execution"].get("success", True):
                errors = result["execution"].get("errors", [])
                for error in errors[:2]:  # Show first 2 errors
                    report.append(f"    - {error.get('message', str(error))}")
        
        return "\n".join(report)


def run_notebook_tests(notebooks_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Run notebook tests from command line or programmatically.
    
    Args:
        notebooks_dir: Directory containing notebooks (optional)
        
    Returns:
        Test results dictionary
    """
    if notebooks_dir is None:
        notebooks_dir = Path(__file__).parent.parent / "notebooks"
    
    runner = NotebookTestRunner(notebooks_dir)
    return runner.run_all_tests()


if __name__ == "__main__":
    # Run notebook tests when executed directly
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Jupyter notebooks")
    parser.add_argument(
        "--notebooks-dir",
        type=Path,
        default=Path(__file__).parent.parent / "notebooks",
        help="Directory containing notebooks to test"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate detailed report"
    )
    
    args = parser.parse_args()
    
    print("Running Notebook Tests...")
    print(f"Notebooks directory: {args.notebooks_dir}")
    print()
    
    runner = NotebookTestRunner(args.notebooks_dir)
    results = runner.run_all_tests()
    
    if args.report:
        report = runner.generate_report(results)
        print(report)
    else:
        # Simple summary
        if "error" in results:
            print(f"Error: {results['error']}")
            sys.exit(1)
        
        print(f"Results: {results['validated_notebooks']}/{results['total_notebooks']} validated, "
              f"{results['executed_notebooks']} executed, {results['failed_notebooks']} failed")
        
        if results["failed_notebooks"] > 0:
            print("Some notebooks failed. Use --report for details.")
            sys.exit(1)
        else:
            print("All tests passed!")
            sys.exit(0)