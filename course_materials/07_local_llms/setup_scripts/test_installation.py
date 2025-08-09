#!/usr/bin/env python3
"""
Installation Validation and Testing Script
Tests all components of the local LLMs setup to ensure everything is working correctly.
"""

import sys
import subprocess
import importlib
import json
import time
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

def print_status(message: str):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def print_error(message: str):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def print_test_header(test_name: str):
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.CYAN}Testing: {test_name}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")

class InstallationTester:
    def __init__(self):
        self.results = {}
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict:
        """Collect system information"""
        return {
            'platform': platform.platform(),
            'python_version': sys.version,
            'python_executable': sys.executable,
            'architecture': platform.architecture(),
            'processor': platform.processor(),
        }
    
    def _test_import(self, module_name: str, package_name: str = None) -> Tuple[bool, str, Optional[str]]:
        """Test if a module can be imported and get its version"""
        try:
            module = importlib.import_module(module_name)
            
            # Try to get version
            version = None
            for attr in ['__version__', 'version', 'VERSION']:
                if hasattr(module, attr):
                    version = getattr(module, attr)
                    break
            
            return True, f"Successfully imported {module_name}", version
        except ImportError as e:
            return False, f"Failed to import {module_name}: {str(e)}", None
        except Exception as e:
            return False, f"Error importing {module_name}: {str(e)}", None
    
    def _run_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
        """Run a shell command and return success status, stdout, stderr"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, "", str(e)
    
    def test_python_environment(self) -> bool:
        """Test Python environment and basic requirements"""
        print_test_header("Python Environment")
        
        # Check Python version
        python_version = sys.version_info
        min_version = (3, 8)
        
        if python_version >= min_version:
            print_success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            print_error(f"Python version {python_version.major}.{python_version.minor} is below minimum required {min_version[0]}.{min_version[1]}")
            return False
        
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print_success("Running in virtual environment")
        else:
            print_warning("Not running in virtual environment (recommended but not required)")
        
        # Display system info
        print_status(f"Platform: {self.system_info['platform']}")
        print_status(f"Architecture: {self.system_info['architecture'][0]}")
        
        return True
    
    def test_core_packages(self) -> bool:
        """Test core Python packages"""
        print_test_header("Core Python Packages")
        
        core_packages = [
            ('numpy', 'numpy'),
            ('requests', 'requests'),
            ('json', None),  # Built-in
            ('pathlib', None),  # Built-in
            ('subprocess', None),  # Built-in
        ]
        
        all_passed = True
        for module_name, package_name in core_packages:
            success, message, version = self._test_import(module_name, package_name)
            if success:
                version_str = f" (v{version})" if version else ""
                print_success(f"{module_name}{version_str}")
            else:
                print_error(message)
                all_passed = False
        
        return all_passed
    
    def test_pytorch(self) -> bool:
        """Test PyTorch installation and GPU support"""
        print_test_header("PyTorch")
        
        # Test PyTorch import
        success, message, version = self._test_import('torch')
        if not success:
            print_error(message)
            return False
        
        print_success(f"PyTorch v{version}")
        
        try:
            import torch
            
            # Test CUDA availability
            if torch.cuda.is_available():
                print_success(f"CUDA available: {torch.version.cuda}")
                print_success(f"GPU count: {torch.cuda.device_count()}")
                
                # List available GPUs
                for i in range(torch.cuda.device_count()):
                    gpu_name = torch.cuda.get_device_name(i)
                    print_status(f"GPU {i}: {gpu_name}")
            else:
                print_warning("CUDA not available (CPU-only mode)")
            
            # Test MPS (Apple Silicon) availability
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print_success("MPS (Apple Silicon) support available")
            
            # Test basic tensor operations
            try:
                x = torch.randn(3, 3)
                y = torch.randn(3, 3)
                z = torch.matmul(x, y)
                print_success("Basic tensor operations working")
            except Exception as e:
                print_error(f"Tensor operations failed: {e}")
                return False
                
        except Exception as e:
            print_error(f"PyTorch functionality test failed: {e}")
            return False
        
        return True
    
    def test_transformers(self) -> bool:
        """Test Hugging Face Transformers"""
        print_test_header("Hugging Face Transformers")
        
        success, message, version = self._test_import('transformers')
        if not success:
            print_error(message)
            return False
        
        print_success(f"Transformers v{version}")
        
        try:
            from transformers import AutoTokenizer
            
            # Test tokenizer loading (this is lightweight)
            print_status("Testing tokenizer loading...")
            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            
            # Test basic tokenization
            test_text = "Hello, world!"
            tokens = tokenizer.encode(test_text)
            decoded = tokenizer.decode(tokens)
            
            if decoded.strip() == test_text:
                print_success("Tokenizer working correctly")
            else:
                print_warning("Tokenizer test produced unexpected output")
            
        except Exception as e:
            print_error(f"Transformers functionality test failed: {e}")
            return False
        
        return True
    
    def test_ollama_client(self) -> bool:
        """Test Ollama Python client"""
        print_test_header("Ollama Python Client")
        
        success, message, version = self._test_import('ollama')
        if not success:
            print_error(message)
            print_warning("Install with: pip install ollama")
            return False
        
        print_success(f"Ollama client imported successfully")
        
        try:
            import ollama
            
            # Test connection to Ollama server
            print_status("Testing connection to Ollama server...")
            try:
                models = ollama.list()
                print_success("Connected to Ollama server")
                
                if models.get('models'):
                    print_status(f"Available models: {len(models['models'])}")
                    for model in models['models'][:3]:  # Show first 3 models
                        print_status(f"  - {model['name']}")
                else:
                    print_warning("No models installed")
                    print_status("Install a model with: ollama pull llama3.2:1b")
                
            except Exception as e:
                print_warning(f"Could not connect to Ollama server: {e}")
                print_status("Make sure Ollama is running: ollama serve")
                return False
                
        except Exception as e:
            print_error(f"Ollama client test failed: {e}")
            return False
        
        return True
    
    def test_ollama_server(self) -> bool:
        """Test Ollama server installation"""
        print_test_header("Ollama Server")
        
        # Check if ollama command exists
        success, stdout, stderr = self._run_command(['ollama', '--version'])
        if not success:
            print_error("Ollama command not found")
            print_status("Install Ollama from: https://ollama.ai")
            return False
        
        version = stdout.strip()
        print_success(f"Ollama server: {version}")
        
        # Test server connectivity
        success, stdout, stderr = self._run_command(['ollama', 'list'])
        if success:
            print_success("Ollama server is running")
            
            # Parse model list
            lines = stdout.strip().split('\n')[1:]  # Skip header
            if lines and lines[0].strip():
                print_status(f"Installed models: {len(lines)}")
                for line in lines[:3]:  # Show first 3
                    model_name = line.split()[0]
                    print_status(f"  - {model_name}")
            else:
                print_warning("No models installed")
                print_status("Install a model with: ollama pull llama3.2:1b")
        else:
            print_warning("Ollama server not responding")
            print_status("Start server with: ollama serve")
            return False
        
        return True
    
    def test_jupyter(self) -> bool:
        """Test Jupyter installation"""
        print_test_header("Jupyter")
        
        success, message, version = self._test_import('jupyter')
        if not success:
            print_error(message)
            return False
        
        print_success("Jupyter imported successfully")
        
        # Test jupyter command
        success, stdout, stderr = self._run_command(['jupyter', '--version'])
        if success:
            print_success("Jupyter command available")
            # Parse version info
            for line in stdout.strip().split('\n'):
                if line.strip():
                    print_status(f"  {line.strip()}")
        else:
            print_warning("Jupyter command not available in PATH")
        
        return True
    
    def test_optional_packages(self) -> bool:
        """Test optional packages"""
        print_test_header("Optional Packages")
        
        optional_packages = [
            ('matplotlib', 'matplotlib'),
            ('seaborn', 'seaborn'),
            ('plotly', 'plotly'),
            ('tqdm', 'tqdm'),
            ('rich', 'rich'),
            ('accelerate', 'accelerate'),
            ('bitsandbytes', 'bitsandbytes'),
        ]
        
        passed_count = 0
        for module_name, package_name in optional_packages:
            success, message, version = self._test_import(module_name, package_name)
            if success:
                version_str = f" (v{version})" if version else ""
                print_success(f"{module_name}{version_str}")
                passed_count += 1
            else:
                print_warning(f"{module_name} not available")
        
        print_status(f"Optional packages available: {passed_count}/{len(optional_packages)}")
        return True
    
    def run_performance_test(self) -> bool:
        """Run basic performance tests"""
        print_test_header("Performance Tests")
        
        try:
            import torch
            import time
            
            # CPU tensor operations
            print_status("Testing CPU performance...")
            start_time = time.time()
            
            # Matrix multiplication test
            a = torch.randn(1000, 1000)
            b = torch.randn(1000, 1000)
            c = torch.matmul(a, b)
            
            cpu_time = time.time() - start_time
            print_success(f"CPU matrix multiplication (1000x1000): {cpu_time:.3f}s")
            
            # GPU test if available
            if torch.cuda.is_available():
                print_status("Testing GPU performance...")
                start_time = time.time()
                
                a_gpu = a.cuda()
                b_gpu = b.cuda()
                c_gpu = torch.matmul(a_gpu, b_gpu)
                torch.cuda.synchronize()
                
                gpu_time = time.time() - start_time
                print_success(f"GPU matrix multiplication (1000x1000): {gpu_time:.3f}s")
                print_status(f"GPU speedup: {cpu_time/gpu_time:.1f}x")
            
        except Exception as e:
            print_error(f"Performance test failed: {e}")
            return False
        
        return True
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive test report"""
        print_test_header("Generating Test Report")
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': self.system_info,
            'test_results': self.results,
            'summary': {
                'total_tests': len(self.results),
                'passed_tests': sum(1 for result in self.results.values() if result),
                'failed_tests': sum(1 for result in self.results.values() if not result),
            }
        }
        
        # Save report to file
        report_file = Path('installation_test_report.json')
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print_success(f"Test report saved to: {report_file}")
        except Exception as e:
            print_warning(f"Could not save report: {e}")
        
        return report
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall success status"""
        print_status("Local LLMs Installation Test Suite")
        print_status("=" * 50)
        
        tests = [
            ('Python Environment', self.test_python_environment),
            ('Core Packages', self.test_core_packages),
            ('PyTorch', self.test_pytorch),
            ('Transformers', self.test_transformers),
            ('Ollama Client', self.test_ollama_client),
            ('Ollama Server', self.test_ollama_server),
            ('Jupyter', self.test_jupyter),
            ('Optional Packages', self.test_optional_packages),
            ('Performance', self.run_performance_test),
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            try:
                result = test_func()
                self.results[test_name] = result
                if not result:
                    all_passed = False
            except Exception as e:
                print_error(f"Test '{test_name}' crashed: {e}")
                self.results[test_name] = False
                all_passed = False
        
        # Generate report
        report = self.generate_report()
        
        # Print summary
        print_test_header("Test Summary")
        passed = report['summary']['passed_tests']
        total = report['summary']['total_tests']
        
        if all_passed:
            print_success(f"All tests passed! ({passed}/{total})")
            print_success("Your local LLMs environment is ready to use!")
        else:
            failed = report['summary']['failed_tests']
            print_warning(f"Some tests failed: {passed} passed, {failed} failed")
            print_status("Check the output above for specific issues")
        
        # Provide next steps
        print_test_header("Next Steps")
        if all_passed:
            print_status("You can now:")
            print_status("1. Start Jupyter: jupyter notebook")
            print_status("2. Run Ollama models: ollama run llama3.2:1b")
            print_status("3. Explore the course materials in course_materials/07_local_llms/")
        else:
            print_status("To fix issues:")
            print_status("1. Check the error messages above")
            print_status("2. Reinstall failed components")
            print_status("3. Run this test again: python test_installation.py")
        
        return all_passed

def main():
    """Main function"""
    tester = InstallationTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()