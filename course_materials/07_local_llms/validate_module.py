#!/usr/bin/env python3
"""
Simple validation script for the local LLMs module.

This script performs basic validation without requiring external dependencies,
checking file structure, imports, and basic functionality.
"""

import os
import sys
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional


class ModuleValidator:
    """
    Simple validator for the local LLMs module.
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.module_dir = Path(__file__).parent
        self.results = {
            "structure_check": {},
            "import_check": {},
            "notebook_check": {},
            "documentation_check": {},
            "summary": {}
        }
    
    def validate_structure(self) -> Dict[str, Any]:
        """
        Validate the module directory structure.
        
        Returns:
            Dictionary with structure validation results
        """
        print("Validating Module Structure...")
        print("-" * 30)
        
        expected_structure = {
            "directories": [
                "ollama_basics",
                "huggingface_transformers", 
                "model_formats",
                "system_prompts",
                "setup_scripts",
                "notebooks",
                "utils",
                "tests"
            ],
            "files": [
                "README.md",
                "requirements.txt",
                "requirements-gpu.txt",
                "requirements-dev.txt",
                "REQUIREMENTS.md"
            ]
        }
        
        results = {
            "missing_directories": [],
            "missing_files": [],
            "extra_items": [],
            "total_expected": len(expected_structure["directories"]) + len(expected_structure["files"]),
            "found_items": 0
        }
        
        # Check directories
        for directory in expected_structure["directories"]:
            dir_path = self.module_dir / directory
            if dir_path.exists() and dir_path.is_dir():
                results["found_items"] += 1
                print(f"  ✓ Directory: {directory}")
            else:
                results["missing_directories"].append(directory)
                print(f"  ✗ Missing directory: {directory}")
        
        # Check files
        for file in expected_structure["files"]:
            file_path = self.module_dir / file
            if file_path.exists() and file_path.is_file():
                results["found_items"] += 1
                print(f"  ✓ File: {file}")
            else:
                results["missing_files"].append(file)
                print(f"  ✗ Missing file: {file}")
        
        results["structure_valid"] = (
            len(results["missing_directories"]) == 0 and 
            len(results["missing_files"]) == 0
        )
        
        return results
    
    def validate_imports(self) -> Dict[str, Any]:
        """
        Validate that Python modules can be imported.
        
        Returns:
            Dictionary with import validation results
        """
        print("\nValidating Python Imports...")
        print("-" * 30)
        
        # Key Python files to test
        python_files = [
            "utils/ollama_manager.py",
            "utils/transformers_manager.py", 
            "utils/prompt_template.py",
            "utils/test_utilities.py",
            "ollama_basics/ollama_features.py",
            "ollama_basics/api_examples.py",
            "ollama_basics/model_management.py",
            "huggingface_transformers/local_inference.py",
            "huggingface_transformers/memory_optimization.py",
            "model_formats/gguf_examples.py",
            "model_formats/modelfile_creation.py",
            "system_prompts/assistant_prompts.py",
            "system_prompts/creative_prompts.py",
            "setup_scripts/test_installation.py"
        ]
        
        results = {
            "total_files": len(python_files),
            "importable_files": 0,
            "failed_imports": [],
            "import_errors": {},
            "syntax_valid": 0,
            "syntax_errors": {}
        }
        
        for py_file in python_files:
            file_path = self.module_dir / py_file
            
            if not file_path.exists():
                results["failed_imports"].append(py_file)
                results["import_errors"][py_file] = "File not found"
                print(f"  ✗ {py_file} (not found)")
                continue
            
            # Check syntax by compiling
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                compile(source_code, str(file_path), 'exec')
                results["syntax_valid"] += 1
                
                # Try to import if it's a module
                if py_file.endswith('.py'):
                    try:
                        spec = importlib.util.spec_from_file_location(
                            py_file.replace('/', '.').replace('.py', ''),
                            file_path
                        )
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            # Don't actually execute the module to avoid dependencies
                            results["importable_files"] += 1
                            print(f"  ✓ {py_file}")
                        else:
                            results["failed_imports"].append(py_file)
                            results["import_errors"][py_file] = "Could not create module spec"
                            print(f"  ⚠ {py_file} (spec creation failed)")
                    except Exception as e:
                        results["failed_imports"].append(py_file)
                        results["import_errors"][py_file] = str(e)
                        print(f"  ⚠ {py_file} (import issue: {str(e)[:50]}...)")
                
            except SyntaxError as e:
                results["failed_imports"].append(py_file)
                results["syntax_errors"][py_file] = str(e)
                print(f"  ✗ {py_file} (syntax error: {e})")
            except Exception as e:
                results["failed_imports"].append(py_file)
                results["import_errors"][py_file] = str(e)
                print(f"  ✗ {py_file} (error: {str(e)[:50]}...)")
        
        results["imports_valid"] = len(results["failed_imports"]) == 0
        
        return results
    
    def validate_notebooks(self) -> Dict[str, Any]:
        """
        Validate Jupyter notebooks.
        
        Returns:
            Dictionary with notebook validation results
        """
        print("\nValidating Jupyter Notebooks...")
        print("-" * 30)
        
        notebooks_dir = self.module_dir / "notebooks"
        
        if not notebooks_dir.exists():
            print("  ✗ Notebooks directory not found")
            return {
                "notebooks_found": 0,
                "valid_notebooks": 0,
                "invalid_notebooks": [],
                "validation_errors": {},
                "notebooks_valid": False
            }
        
        notebook_files = list(notebooks_dir.glob("*.ipynb"))
        
        results = {
            "notebooks_found": len(notebook_files),
            "valid_notebooks": 0,
            "invalid_notebooks": [],
            "validation_errors": {},
            "notebooks_valid": True
        }
        
        for notebook_path in notebook_files:
            try:
                with open(notebook_path, 'r', encoding='utf-8') as f:
                    notebook_content = json.load(f)
                
                # Basic notebook structure validation
                required_keys = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
                missing_keys = [key for key in required_keys if key not in notebook_content]
                
                if missing_keys:
                    results["invalid_notebooks"].append(notebook_path.name)
                    results["validation_errors"][notebook_path.name] = f"Missing keys: {missing_keys}"
                    print(f"  ✗ {notebook_path.name} (missing keys: {missing_keys})")
                else:
                    results["valid_notebooks"] += 1
                    print(f"  ✓ {notebook_path.name}")
                
            except json.JSONDecodeError as e:
                results["invalid_notebooks"].append(notebook_path.name)
                results["validation_errors"][notebook_path.name] = f"JSON decode error: {e}"
                print(f"  ✗ {notebook_path.name} (JSON error)")
            except Exception as e:
                results["invalid_notebooks"].append(notebook_path.name)
                results["validation_errors"][notebook_path.name] = str(e)
                print(f"  ✗ {notebook_path.name} (error: {e})")
        
        results["notebooks_valid"] = len(results["invalid_notebooks"]) == 0
        
        return results
    
    def validate_documentation(self) -> Dict[str, Any]:
        """
        Validate documentation files.
        
        Returns:
            Dictionary with documentation validation results
        """
        print("\nValidating Documentation...")
        print("-" * 30)
        
        # Key documentation files to check
        doc_files = [
            "README.md",
            "REQUIREMENTS.md",
            "ollama_basics/README.md",
            "ollama_basics/installation_guide.md",
            "huggingface_transformers/README.md",
            "huggingface_transformers/transformers_setup.md",
            "model_formats/README.md",
            "model_formats/format_overview.md",
            "system_prompts/README.md",
            "system_prompts/prompt_engineering.md",
            "setup_scripts/README.md",
            "setup_scripts/troubleshooting.md",
            "notebooks/README.md"
        ]
        
        results = {
            "total_docs": len(doc_files),
            "found_docs": 0,
            "missing_docs": [],
            "empty_docs": [],
            "doc_sizes": {},
            "docs_valid": True
        }
        
        for doc_file in doc_files:
            doc_path = self.module_dir / doc_file
            
            if not doc_path.exists():
                results["missing_docs"].append(doc_file)
                print(f"  ✗ {doc_file} (not found)")
                continue
            
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if len(content) == 0:
                    results["empty_docs"].append(doc_file)
                    print(f"  ⚠ {doc_file} (empty)")
                elif len(content) < 100:
                    print(f"  ⚠ {doc_file} (very short: {len(content)} chars)")
                else:
                    print(f"  ✓ {doc_file} ({len(content)} chars)")
                
                results["found_docs"] += 1
                results["doc_sizes"][doc_file] = len(content)
                
            except Exception as e:
                print(f"  ✗ {doc_file} (read error: {e})")
        
        results["docs_valid"] = (
            len(results["missing_docs"]) == 0 and 
            len(results["empty_docs"]) == 0
        )
        
        return results
    
    def run_validation(self) -> Dict[str, Any]:
        """
        Run all validation checks.
        
        Returns:
            Complete validation results
        """
        print("Local LLMs Module - Validation Suite")
        print("=" * 50)
        
        # Run all validation checks
        self.results["structure_check"] = self.validate_structure()
        self.results["import_check"] = self.validate_imports()
        self.results["notebook_check"] = self.validate_notebooks()
        self.results["documentation_check"] = self.validate_documentation()
        
        # Calculate summary
        self.results["summary"] = self._calculate_summary()
        
        # Print final summary
        self._print_summary()
        
        return self.results
    
    def _calculate_summary(self) -> Dict[str, Any]:
        """Calculate validation summary."""
        structure_valid = self.results["structure_check"]["structure_valid"]
        imports_valid = self.results["import_check"]["imports_valid"]
        notebooks_valid = self.results["notebook_check"]["notebooks_valid"]
        docs_valid = self.results["documentation_check"]["docs_valid"]
        
        overall_valid = structure_valid and imports_valid and notebooks_valid and docs_valid
        
        return {
            "overall_valid": overall_valid,
            "structure_valid": structure_valid,
            "imports_valid": imports_valid,
            "notebooks_valid": notebooks_valid,
            "docs_valid": docs_valid,
            "total_checks": 4,
            "passed_checks": sum([structure_valid, imports_valid, notebooks_valid, docs_valid])
        }
    
    def _print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        
        summary = self.results["summary"]
        
        # Overall status
        status_symbol = "✓" if summary["overall_valid"] else "✗"
        print(f"Overall Status: {status_symbol} {'VALID' if summary['overall_valid'] else 'INVALID'}")
        print(f"Checks Passed: {summary['passed_checks']}/{summary['total_checks']}")
        print()
        
        # Individual check results
        checks = [
            ("Structure", "structure_valid"),
            ("Imports", "imports_valid"),
            ("Notebooks", "notebooks_valid"),
            ("Documentation", "docs_valid")
        ]
        
        for check_name, check_key in checks:
            status = "✓" if summary[check_key] else "✗"
            print(f"  {status} {check_name}")
        
        # Detailed results
        if not summary["overall_valid"]:
            print("\nIssues Found:")
            
            structure = self.results["structure_check"]
            if structure["missing_directories"]:
                print(f"  - Missing directories: {', '.join(structure['missing_directories'])}")
            if structure["missing_files"]:
                print(f"  - Missing files: {', '.join(structure['missing_files'])}")
            
            imports = self.results["import_check"]
            if imports["failed_imports"]:
                print(f"  - Failed imports: {len(imports['failed_imports'])} files")
            
            notebooks = self.results["notebook_check"]
            if notebooks["invalid_notebooks"]:
                print(f"  - Invalid notebooks: {', '.join(notebooks['invalid_notebooks'])}")
            
            docs = self.results["documentation_check"]
            if docs["missing_docs"]:
                print(f"  - Missing docs: {', '.join(docs['missing_docs'])}")
            if docs["empty_docs"]:
                print(f"  - Empty docs: {', '.join(docs['empty_docs'])}")


def main():
    """Main entry point."""
    validator = ModuleValidator()
    results = validator.run_validation()
    
    # Exit with appropriate code
    if results["summary"]["overall_valid"]:
        print("\n🎉 Module validation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Module validation failed. Please address the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()