"""
Comprehensive test runner for the local LLMs module.

This script runs all tests including unit tests, integration tests,
and notebook execution tests, providing a complete validation suite.
"""

import sys
import os
import subprocess
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent / "utils"))


class TestRunner:
    """
    Comprehensive test runner for the local LLMs module.
    """
    
    def __init__(self, verbose: bool = False, include_slow: bool = False, include_integration: bool = False):
        """
        Initialize the test runner.
        
        Args:
            verbose: Enable verbose output
            include_slow: Include slow-running tests
            include_integration: Include integration tests
        """
        self.verbose = verbose
        self.include_slow = include_slow
        self.include_integration = include_integration
        self.test_dir = Path(__file__).parent
        self.results = {
            "unit_tests": {},
            "integration_tests": {},
            "notebook_tests": {},
            "summary": {}
        }
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """
        Run unit tests using pytest.
        
        Returns:
            Dictionary with test results
        """
        print("Running Unit Tests...")
        print("-" * 30)
        
        # List of unit test files
        unit_test_files = [
            "test_ollama_manager.py",
            "test_transformers_manager.py",
            "test_prompt_template.py",
            "test_utilities.py"
        ]
        
        results = {
            "total_files": len(unit_test_files),
            "passed_files": 0,
            "failed_files": 0,
            "file_results": {},
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0
        }
        
        for test_file in unit_test_files:
            test_path = self.test_dir / test_file
            
            if not test_path.exists():
                print(f"  ⚠ Test file not found: {test_file}")
                results["file_results"][test_file] = {
                    "status": "missing",
                    "error": "File not found"
                }
                continue
            
            # Run pytest on the specific file
            cmd = [
                sys.executable, "-m", "pytest",
                str(test_path),
                "-v" if self.verbose else "-q",
                "--tb=short",
                "--json-report",
                "--json-report-file=/tmp/pytest_report.json"
            ]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per file
                )
                
                # Parse pytest results
                file_result = self._parse_pytest_output(result, test_file)
                results["file_results"][test_file] = file_result
                
                if file_result["status"] == "passed":
                    results["passed_files"] += 1
                    print(f"  ✓ {test_file}")
                else:
                    results["failed_files"] += 1
                    print(f"  ✗ {test_file}")
                    if self.verbose and file_result.get("error"):
                        print(f"    Error: {file_result['error']}")
                
                # Aggregate test counts
                results["total_tests"] += file_result.get("total", 0)
                results["passed_tests"] += file_result.get("passed", 0)
                results["failed_tests"] += file_result.get("failed", 0)
                results["skipped_tests"] += file_result.get("skipped", 0)
                
            except subprocess.TimeoutExpired:
                results["failed_files"] += 1
                results["file_results"][test_file] = {
                    "status": "timeout",
                    "error": "Test execution timed out"
                }
                print(f"  ⏰ {test_file} (timeout)")
            
            except Exception as e:
                results["failed_files"] += 1
                results["file_results"][test_file] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"  ✗ {test_file} (error: {e})")
        
        return results
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """
        Run integration tests.
        
        Returns:
            Dictionary with test results
        """
        print("\nRunning Integration Tests...")
        print("-" * 30)
        
        if not self.include_integration:
            print("  ⚠ Integration tests skipped (use --integration to enable)")
            return {"skipped": True, "reason": "Not enabled"}
        
        try:
            # Import and run integration tests
            from integration_tests import run_integration_test_suite
            
            results = run_integration_test_suite()
            
            # Print summary
            print(f"  Total: {results['total_tests']}")
            print(f"  Passed: {results['passed_tests']}")
            print(f"  Failed: {results['failed_tests']}")
            print(f"  Skipped: {results['skipped_tests']}")
            
            if self.verbose:
                for test_result in results["test_results"]:
                    status_symbol = {
                        "PASSED": "✓",
                        "FAILED": "✗",
                        "SKIPPED": "⚠"
                    }.get(test_result["status"], "?")
                    print(f"    {status_symbol} {test_result['test']}")
            
            return results
            
        except Exception as e:
            print(f"  ✗ Integration tests failed: {e}")
            return {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 1,
                "skipped_tests": 0,
                "error": str(e)
            }
    
    def run_notebook_tests(self) -> Dict[str, Any]:
        """
        Run notebook execution tests.
        
        Returns:
            Dictionary with test results
        """
        print("\nRunning Notebook Tests...")
        print("-" * 30)
        
        try:
            from test_notebook_execution import run_notebook_tests
            
            notebooks_dir = self.test_dir.parent / "notebooks"
            results = run_notebook_tests(notebooks_dir)
            
            if "error" in results:
                print(f"  ✗ {results['error']}")
                return results
            
            # Print summary
            print(f"  Total notebooks: {results['total_notebooks']}")
            print(f"  Validated: {results['validated_notebooks']}")
            print(f"  Executed: {results['executed_notebooks']}")
            print(f"  Failed: {results['failed_notebooks']}")
            
            if self.verbose:
                for notebook_name, result in results["notebook_results"].items():
                    validation_status = "✓" if result["validation"] and result["validation"]["valid"] else "✗"
                    execution_status = "✓" if result["execution"] and result["execution"].get("success") else "⚠"
                    print(f"    {validation_status}{execution_status} {notebook_name}")
            
            return results
            
        except Exception as e:
            print(f"  ✗ Notebook tests failed: {e}")
            return {
                "total_notebooks": 0,
                "validated_notebooks": 0,
                "executed_notebooks": 0,
                "failed_notebooks": 1,
                "error": str(e)
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all test suites.
        
        Returns:
            Complete test results
        """
        start_time = time.time()
        
        print("Local LLMs Module - Comprehensive Test Suite")
        print("=" * 50)
        
        # Run unit tests
        self.results["unit_tests"] = self.run_unit_tests()
        
        # Run integration tests
        self.results["integration_tests"] = self.run_integration_tests()
        
        # Run notebook tests
        self.results["notebook_tests"] = self.run_notebook_tests()
        
        # Calculate summary
        total_time = time.time() - start_time
        self.results["summary"] = self._calculate_summary(total_time)
        
        # Print final summary
        self._print_final_summary()
        
        return self.results
    
    def _parse_pytest_output(self, result: subprocess.CompletedProcess, test_file: str) -> Dict[str, Any]:
        """
        Parse pytest output to extract test results.
        
        Args:
            result: Subprocess result from pytest
            test_file: Name of the test file
            
        Returns:
            Dictionary with parsed results
        """
        file_result = {
            "status": "unknown",
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "error": None
        }
        
        if result.returncode == 0:
            file_result["status"] = "passed"
        else:
            file_result["status"] = "failed"
            file_result["error"] = result.stderr.strip() if result.stderr else "Unknown error"
        
        # Try to parse test counts from output
        output = result.stdout
        
        # Look for pytest summary line
        import re
        
        # Pattern for pytest summary: "X passed, Y failed, Z skipped"
        summary_pattern = r'(\d+) passed(?:, (\d+) failed)?(?:, (\d+) skipped)?'
        match = re.search(summary_pattern, output)
        
        if match:
            file_result["passed"] = int(match.group(1) or 0)
            file_result["failed"] = int(match.group(2) or 0)
            file_result["skipped"] = int(match.group(3) or 0)
            file_result["total"] = file_result["passed"] + file_result["failed"] + file_result["skipped"]
        
        return file_result
    
    def _calculate_summary(self, total_time: float) -> Dict[str, Any]:
        """
        Calculate overall test summary.
        
        Args:
            total_time: Total execution time in seconds
            
        Returns:
            Summary dictionary
        """
        summary = {
            "total_time": total_time,
            "overall_status": "passed",
            "unit_test_summary": {},
            "integration_test_summary": {},
            "notebook_test_summary": {}
        }
        
        # Unit test summary
        unit_results = self.results["unit_tests"]
        summary["unit_test_summary"] = {
            "files_passed": unit_results.get("passed_files", 0),
            "files_failed": unit_results.get("failed_files", 0),
            "tests_passed": unit_results.get("passed_tests", 0),
            "tests_failed": unit_results.get("failed_tests", 0),
            "tests_skipped": unit_results.get("skipped_tests", 0)
        }
        
        # Integration test summary
        integration_results = self.results["integration_tests"]
        if not integration_results.get("skipped"):
            summary["integration_test_summary"] = {
                "tests_passed": integration_results.get("passed_tests", 0),
                "tests_failed": integration_results.get("failed_tests", 0),
                "tests_skipped": integration_results.get("skipped_tests", 0)
            }
        else:
            summary["integration_test_summary"] = {"skipped": True}
        
        # Notebook test summary
        notebook_results = self.results["notebook_tests"]
        if "error" not in notebook_results:
            summary["notebook_test_summary"] = {
                "notebooks_validated": notebook_results.get("validated_notebooks", 0),
                "notebooks_executed": notebook_results.get("executed_notebooks", 0),
                "notebooks_failed": notebook_results.get("failed_notebooks", 0)
            }
        else:
            summary["notebook_test_summary"] = {"error": notebook_results["error"]}
        
        # Determine overall status
        if (unit_results.get("failed_files", 0) > 0 or 
            integration_results.get("failed_tests", 0) > 0 or
            notebook_results.get("failed_notebooks", 0) > 0):
            summary["overall_status"] = "failed"
        
        return summary
    
    def _print_final_summary(self):
        """Print the final test summary."""
        print("\n" + "=" * 50)
        print("FINAL TEST SUMMARY")
        print("=" * 50)
        
        summary = self.results["summary"]
        
        # Overall status
        status_symbol = "✓" if summary["overall_status"] == "passed" else "✗"
        print(f"Overall Status: {status_symbol} {summary['overall_status'].upper()}")
        print(f"Total Time: {summary['total_time']:.2f} seconds")
        print()
        
        # Unit tests
        unit_summary = summary["unit_test_summary"]
        print(f"Unit Tests:")
        print(f"  Files: {unit_summary['files_passed']}/{unit_summary['files_passed'] + unit_summary['files_failed']} passed")
        print(f"  Tests: {unit_summary['tests_passed']} passed, {unit_summary['tests_failed']} failed, {unit_summary['tests_skipped']} skipped")
        
        # Integration tests
        integration_summary = summary["integration_test_summary"]
        if integration_summary.get("skipped"):
            print(f"Integration Tests: SKIPPED")
        else:
            print(f"Integration Tests:")
            print(f"  Tests: {integration_summary['tests_passed']} passed, {integration_summary['tests_failed']} failed, {integration_summary['tests_skipped']} skipped")
        
        # Notebook tests
        notebook_summary = summary["notebook_test_summary"]
        if "error" in notebook_summary:
            print(f"Notebook Tests: ERROR - {notebook_summary['error']}")
        else:
            print(f"Notebook Tests:")
            print(f"  Notebooks: {notebook_summary['notebooks_validated']} validated, {notebook_summary['notebooks_executed']} executed, {notebook_summary['notebooks_failed']} failed")
    
    def save_results(self, output_file: Path):
        """
        Save test results to a JSON file.
        
        Args:
            output_file: Path to output file
        """
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\nTest results saved to: {output_file}")


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run comprehensive tests for local LLMs module")
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Include integration tests (may require external services)"
    )
    
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Include slow-running tests"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Save results to JSON file"
    )
    
    parser.add_argument(
        "--unit-only",
        action="store_true",
        help="Run only unit tests"
    )
    
    parser.add_argument(
        "--notebooks-only",
        action="store_true",
        help="Run only notebook tests"
    )
    
    args = parser.parse_args()
    
    # Create test runner
    runner = TestRunner(
        verbose=args.verbose,
        include_slow=args.slow,
        include_integration=args.integration
    )
    
    # Run tests based on arguments
    if args.unit_only:
        print("Running Unit Tests Only...")
        results = {"unit_tests": runner.run_unit_tests()}
    elif args.notebooks_only:
        print("Running Notebook Tests Only...")
        results = {"notebook_tests": runner.run_notebook_tests()}
    else:
        results = runner.run_all_tests()
    
    # Save results if requested
    if args.output:
        runner.save_results(args.output)
    
    # Exit with appropriate code
    if results.get("summary", {}).get("overall_status") == "failed":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()