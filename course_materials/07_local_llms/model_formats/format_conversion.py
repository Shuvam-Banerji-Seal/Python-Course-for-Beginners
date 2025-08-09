#!/usr/bin/env python3
"""
Model Format Conversion and Optimization Examples

This script demonstrates conversion between different LLM model formats:
- Converting PyTorch models to SafeTensors
- Converting models to GGUF format
- Creating Ollama Modelfiles from existing models
- Optimization techniques for different formats

Requirements:
    pip install torch transformers safetensors huggingface_hub
    # For GGUF conversion: llama.cpp tools
    # For Ollama: ollama installed

Usage:
    python format_conversion.py
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
    from safetensors.torch import save_file, load_file
    from huggingface_hub import snapshot_download, hf_hub_download
except ImportError as e:
    print(f"Required packages not installed: {e}")
    print("Run: pip install torch transformers safetensors huggingface_hub")
    sys.exit(1)


class ModelFormatConverter:
    """
    Utility class for converting between different LLM model formats.
    Supports PyTorch -> SafeTensors, PyTorch -> GGUF, and Modelfile creation.
    """
    
    def __init__(self, cache_dir: str = "./model_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.supported_formats = ['pytorch', 'safetensors', 'gguf', 'modelfile']
    
    def download_model(self, model_name: str, force_download: bool = False) -> str:
        """
        Download a model from Hugging Face Hub.
        
        Args:
            model_name: Model identifier (e.g., 'microsoft/DialoGPT-small')
            force_download: Force re-download even if cached
            
        Returns:
            str: Path to downloaded model directory
        """
        print(f"Downloading model: {model_name}")
        
        try:
            model_path = snapshot_download(
                repo_id=model_name,
                cache_dir=self.cache_dir,
                force_download=force_download,
                resume_download=True
            )
            
            print(f"Model downloaded to: {model_path}")
            return model_path
            
        except Exception as e:
            print(f"Error downloading model: {e}")
            raise
    
    def convert_to_safetensors(self, 
                              model_path: str, 
                              output_path: str,
                              model_name: Optional[str] = None) -> bool:
        """
        Convert PyTorch model to SafeTensors format.
        
        Args:
            model_path: Path to PyTorch model or model name
            output_path: Output path for SafeTensors file
            model_name: Model name for loading from Hub
            
        Returns:
            bool: True if conversion successful
        """
        print(f"Converting to SafeTensors: {model_path} -> {output_path}")
        
        try:
            # Load model and tokenizer
            if model_name or not Path(model_path).exists():
                # Load from Hugging Face Hub
                model_id = model_name or model_path
                print(f"Loading model from Hub: {model_id}")
                
                model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16,
                    device_map="auto" if torch.cuda.is_available() else "cpu",
                    trust_remote_code=True
                )
                tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
                
            else:
                # Load from local path
                print(f"Loading model from path: {model_path}")
                model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    torch_dtype=torch.float16,
                    device_map="auto" if torch.cuda.is_available() else "cpu",
                    trust_remote_code=True
                )
                tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            
            # Prepare output directory
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model in SafeTensors format
            model.save_pretrained(
                output_dir,
                safe_serialization=True,  # Use SafeTensors format
                max_shard_size="5GB"      # Shard large models
            )
            
            # Save tokenizer
            tokenizer.save_pretrained(output_dir)
            
            # Save configuration
            config = model.config
            config.save_pretrained(output_dir)
            
            print(f"✅ SafeTensors conversion completed: {output_dir}")
            
            # Verify the conversion
            safetensors_files = list(output_dir.glob("*.safetensors"))
            if safetensors_files:
                print(f"Generated SafeTensors files: {[f.name for f in safetensors_files]}")
                
                # Calculate total size
                total_size = sum(f.stat().st_size for f in safetensors_files)
                print(f"Total model size: {total_size / (1024**3):.2f} GB")
                
                return True
            else:
                print("❌ No SafeTensors files generated")
                return False
                
        except Exception as e:
            print(f"❌ Error converting to SafeTensors: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def convert_to_gguf(self, 
                       model_path: str, 
                       output_path: str,
                       quantization: str = "Q4_0",
                       context_size: int = 2048) -> bool:
        """
        Convert model to GGUF format using llama.cpp tools.
        
        Args:
            model_path: Path to source model
            output_path: Output path for GGUF file
            quantization: Quantization level (Q2_K, Q4_0, Q5_0, Q8_0, F16, F32)
            context_size: Context window size
            
        Returns:
            bool: True if conversion successful
        """
        print(f"Converting to GGUF: {model_path} -> {output_path}")
        print(f"Quantization: {quantization}, Context: {context_size}")
        
        # Check if llama.cpp tools are available
        convert_script = self._find_llama_cpp_convert()
        if not convert_script:
            print("❌ llama.cpp conversion tools not found")
            print("Please install llama.cpp and ensure convert.py is in PATH")
            return False
        
        try:
            # Step 1: Convert to GGML format first
            temp_dir = tempfile.mkdtemp()
            ggml_path = Path(temp_dir) / "model.ggml"
            
            print("Step 1: Converting to GGML format...")
            convert_cmd = [
                sys.executable, convert_script,
                str(model_path),
                "--outfile", str(ggml_path),
                "--outtype", "f16"  # Use f16 for intermediate format
            ]
            
            result = subprocess.run(convert_cmd, capture_output=True, text=True, timeout=1800)
            
            if result.returncode != 0:
                print(f"❌ GGML conversion failed: {result.stderr}")
                return False
            
            print("✅ GGML conversion completed")
            
            # Step 2: Quantize to final GGUF format
            quantize_tool = self._find_llama_cpp_quantize()
            if not quantize_tool:
                print("❌ llama.cpp quantize tool not found")
                return False
            
            print(f"Step 2: Quantizing to {quantization}...")
            quantize_cmd = [
                quantize_tool,
                str(ggml_path),
                str(output_path),
                quantization
            ]
            
            result = subprocess.run(quantize_cmd, capture_output=True, text=True, timeout=1800)
            
            if result.returncode != 0:
                print(f"❌ Quantization failed: {result.stderr}")
                return False
            
            print(f"✅ GGUF conversion completed: {output_path}")
            
            # Verify output file
            if Path(output_path).exists():
                file_size = Path(output_path).stat().st_size / (1024**3)
                print(f"Output file size: {file_size:.2f} GB")
                return True
            else:
                print("❌ Output file not created")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Conversion timed out")
            return False
        except Exception as e:
            print(f"❌ Error converting to GGUF: {e}")
            return False
        finally:
            # Cleanup temporary files
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _find_llama_cpp_convert(self) -> Optional[str]:
        """Find llama.cpp convert.py script."""
        possible_paths = [
            "convert.py",
            "llama.cpp/convert.py",
            "/usr/local/bin/convert.py",
            os.path.expanduser("~/llama.cpp/convert.py")
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        # Try to find in PATH
        try:
            result = subprocess.run(["which", "convert.py"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def _find_llama_cpp_quantize(self) -> Optional[str]:
        """Find llama.cpp quantize tool."""
        possible_names = ["quantize", "llama-quantize", "llama.cpp-quantize"]
        
        for name in possible_names:
            try:
                result = subprocess.run(["which", name], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                continue
        
        return None
    
    def create_modelfile_from_model(self, 
                                   model_path: str,
                                   model_name: str,
                                   output_path: str,
                                   system_prompt: Optional[str] = None,
                                   parameters: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create an Ollama Modelfile from an existing model.
        
        Args:
            model_path: Path to the model (GGUF or other format)
            model_name: Name for the Ollama model
            output_path: Output path for Modelfile
            system_prompt: Custom system prompt
            parameters: Model parameters
            
        Returns:
            bool: True if Modelfile created successfully
        """
        print(f"Creating Modelfile: {model_name}")
        
        # Default parameters
        default_params = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_ctx": 2048
        }
        
        if parameters:
            default_params.update(parameters)
        
        # Default system prompt
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant."
        
        try:
            # Create Modelfile content
            modelfile_lines = []
            
            # FROM directive - use the model path
            modelfile_lines.append(f"FROM {model_path}")
            modelfile_lines.append("")
            
            # SYSTEM prompt
            modelfile_lines.append('SYSTEM """')
            modelfile_lines.append(system_prompt)
            modelfile_lines.append('"""')
            modelfile_lines.append("")
            
            # PARAMETERS
            for param, value in default_params.items():
                modelfile_lines.append(f"PARAMETER {param} {value}")
            modelfile_lines.append("")
            
            # Write Modelfile
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(modelfile_lines))
            
            print(f"✅ Modelfile created: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Modelfile: {e}")
            return False
    
    def optimize_model_for_deployment(self, 
                                    model_path: str,
                                    target_format: str,
                                    deployment_target: str = "cpu",
                                    max_size_gb: float = 5.0) -> Dict[str, str]:
        """
        Optimize model for specific deployment scenarios.
        
        Args:
            model_path: Source model path
            target_format: Target format (safetensors, gguf)
            deployment_target: Deployment target (cpu, gpu, edge)
            max_size_gb: Maximum acceptable model size
            
        Returns:
            Dict with optimization results and output paths
        """
        print(f"Optimizing model for {deployment_target} deployment")
        
        results = {
            "original_path": model_path,
            "target_format": target_format,
            "deployment_target": deployment_target,
            "optimized_models": []
        }
        
        if target_format == "gguf":
            # Choose quantization based on deployment target and size constraints
            quantization_options = self._get_quantization_options(deployment_target, max_size_gb)
            
            for quant in quantization_options:
                output_name = f"optimized_{deployment_target}_{quant}.gguf"
                output_path = Path("optimized_models") / output_name
                output_path.parent.mkdir(exist_ok=True)
                
                if self.convert_to_gguf(model_path, str(output_path), quant):
                    file_size = output_path.stat().st_size / (1024**3)
                    results["optimized_models"].append({
                        "path": str(output_path),
                        "quantization": quant,
                        "size_gb": file_size,
                        "recommended_use": self._get_use_case_recommendation(quant, deployment_target)
                    })
        
        elif target_format == "safetensors":
            # For SafeTensors, focus on precision and security
            output_path = Path("optimized_models") / f"optimized_{deployment_target}.safetensors"
            output_path.parent.mkdir(exist_ok=True)
            
            if self.convert_to_safetensors(model_path, str(output_path.parent)):
                results["optimized_models"].append({
                    "path": str(output_path.parent),
                    "format": "safetensors",
                    "security": "high",
                    "recommended_use": "Production deployment with security requirements"
                })
        
        return results
    
    def _get_quantization_options(self, deployment_target: str, max_size_gb: float) -> List[str]:
        """Get appropriate quantization options for deployment target."""
        if deployment_target == "edge":
            return ["Q2_K", "Q4_0"]  # Smallest sizes for edge devices
        elif deployment_target == "cpu":
            if max_size_gb < 3:
                return ["Q4_0", "Q5_0"]
            else:
                return ["Q5_0", "Q8_0"]
        elif deployment_target == "gpu":
            return ["Q8_0", "F16"]  # Higher quality for GPU deployment
        else:
            return ["Q4_0", "Q5_0", "Q8_0"]  # Balanced options
    
    def _get_use_case_recommendation(self, quantization: str, deployment_target: str) -> str:
        """Get use case recommendation for quantization level."""
        recommendations = {
            "Q2_K": "Ultra-compact deployment, mobile/IoT devices",
            "Q4_0": "Good balance of size and quality, general CPU use",
            "Q5_0": "Better quality, moderate size increase",
            "Q8_0": "High quality, larger size, server deployment",
            "F16": "Maximum quality, GPU deployment"
        }
        return recommendations.get(quantization, "General purpose use")


def demonstrate_pytorch_to_safetensors():
    """Demonstrate converting PyTorch models to SafeTensors."""
    print("=== PyTorch to SafeTensors Conversion ===")
    
    converter = ModelFormatConverter()
    
    # Use a small model for demonstration
    model_name = "microsoft/DialoGPT-small"
    output_path = "converted_models/dialogpt_safetensors"
    
    print(f"Converting {model_name} to SafeTensors format...")
    
    success = converter.convert_to_safetensors(
        model_path=model_name,
        output_path=output_path,
        model_name=model_name
    )
    
    if success:
        print("✅ SafeTensors conversion completed successfully!")
        
        # Verify the conversion by loading the model
        try:
            from transformers import AutoModelForCausalLM
            model = AutoModelForCausalLM.from_pretrained(output_path)
            print("✅ Converted model loads successfully")
            
            # Show file structure
            safetensors_files = list(Path(output_path).glob("*.safetensors"))
            print(f"Generated files: {[f.name for f in safetensors_files]}")
            
        except Exception as e:
            print(f"⚠️  Error verifying converted model: {e}")
    else:
        print("❌ SafeTensors conversion failed")


def demonstrate_gguf_conversion():
    """Demonstrate converting models to GGUF format."""
    print("\n=== Model to GGUF Conversion ===")
    
    converter = ModelFormatConverter()
    
    # Check if conversion tools are available
    if not converter._find_llama_cpp_convert():
        print("❌ llama.cpp conversion tools not found")
        print("To enable GGUF conversion:")
        print("1. Clone llama.cpp: git clone https://github.com/ggerganov/llama.cpp")
        print("2. Build the tools: cd llama.cpp && make")
        print("3. Ensure convert.py and quantize are in PATH")
        return
    
    # Use a small model for demonstration
    model_path = "converted_models/dialogpt_safetensors"
    
    if not Path(model_path).exists():
        print(f"Source model not found: {model_path}")
        print("Run the SafeTensors conversion first")
        return
    
    # Convert with different quantization levels
    quantization_levels = ["Q4_0", "Q5_0", "Q8_0"]
    
    for quant in quantization_levels:
        output_path = f"converted_models/dialogpt_{quant.lower()}.gguf"
        
        print(f"\nConverting to GGUF with {quant} quantization...")
        
        success = converter.convert_to_gguf(
            model_path=model_path,
            output_path=output_path,
            quantization=quant
        )
        
        if success:
            print(f"✅ {quant} conversion completed: {output_path}")
        else:
            print(f"❌ {quant} conversion failed")


def demonstrate_modelfile_creation():
    """Demonstrate creating Modelfiles from converted models."""
    print("\n=== Modelfile Creation ===")
    
    converter = ModelFormatConverter()
    
    # Look for converted GGUF models
    import glob
    gguf_models = glob.glob("converted_models/*.gguf")
    
    if not gguf_models:
        print("No GGUF models found for Modelfile creation")
        print("Run GGUF conversion first")
        return
    
    # Create Modelfiles for different use cases
    modelfile_configs = [
        {
            "name": "chat-assistant",
            "system_prompt": "You are a helpful AI assistant focused on having natural conversations.",
            "parameters": {"temperature": 0.7, "top_p": 0.9}
        },
        {
            "name": "code-helper", 
            "system_prompt": "You are a programming assistant. Help users with coding questions and provide clear, working examples.",
            "parameters": {"temperature": 0.3, "top_p": 0.8}
        },
        {
            "name": "creative-writer",
            "system_prompt": "You are a creative writing assistant. Help with storytelling, character development, and creative ideas.",
            "parameters": {"temperature": 0.8, "top_p": 0.95}
        }
    ]
    
    # Create output directory
    Path("modelfiles").mkdir(exist_ok=True)
    
    for config in modelfile_configs:
        for gguf_model in gguf_models[:1]:  # Use first model for demo
            modelfile_path = f"modelfiles/{config['name']}.Modelfile"
            
            success = converter.create_modelfile_from_model(
                model_path=gguf_model,
                model_name=config['name'],
                output_path=modelfile_path,
                system_prompt=config['system_prompt'],
                parameters=config['parameters']
            )
            
            if success:
                print(f"✅ Modelfile created: {modelfile_path}")
                
                # Show the content
                with open(modelfile_path, 'r') as f:
                    content = f.read()
                    print(f"Content preview:\n{content[:200]}...")


def demonstrate_optimization_pipeline():
    """Demonstrate complete optimization pipeline for different deployment scenarios."""
    print("\n=== Model Optimization Pipeline ===")
    
    converter = ModelFormatConverter()
    
    # Define deployment scenarios
    scenarios = [
        {
            "name": "edge_deployment",
            "target": "edge",
            "max_size": 2.0,
            "description": "Mobile/IoT devices with limited resources"
        },
        {
            "name": "server_deployment", 
            "target": "cpu",
            "max_size": 8.0,
            "description": "Server deployment with moderate resources"
        },
        {
            "name": "gpu_deployment",
            "target": "gpu", 
            "max_size": 15.0,
            "description": "GPU-accelerated deployment for maximum quality"
        }
    ]
    
    # Use existing model if available
    source_model = "converted_models/dialogpt_safetensors"
    
    if not Path(source_model).exists():
        print(f"Source model not found: {source_model}")
        print("Run SafeTensors conversion first")
        return
    
    for scenario in scenarios:
        print(f"\n--- Optimizing for {scenario['name']} ---")
        print(f"Description: {scenario['description']}")
        print(f"Target: {scenario['target']}, Max size: {scenario['max_size']} GB")
        
        results = converter.optimize_model_for_deployment(
            model_path=source_model,
            target_format="gguf",
            deployment_target=scenario['target'],
            max_size_gb=scenario['max_size']
        )
        
        if results['optimized_models']:
            print("✅ Optimization completed:")
            for model in results['optimized_models']:
                print(f"  - {model['path']}")
                print(f"    Quantization: {model['quantization']}")
                print(f"    Size: {model['size_gb']:.2f} GB")
                print(f"    Use case: {model['recommended_use']}")
        else:
            print("❌ No optimized models generated")


def demonstrate_format_comparison():
    """Compare different formats in terms of size, loading speed, and compatibility."""
    print("\n=== Format Comparison ===")
    
    formats_to_compare = []
    
    # Check for SafeTensors
    safetensors_path = "converted_models/dialogpt_safetensors"
    if Path(safetensors_path).exists():
        safetensors_files = list(Path(safetensors_path).glob("*.safetensors"))
        if safetensors_files:
            total_size = sum(f.stat().st_size for f in safetensors_files) / (1024**3)
            formats_to_compare.append({
                "format": "SafeTensors",
                "path": safetensors_path,
                "size_gb": total_size,
                "security": "High",
                "loading_speed": "Fast",
                "compatibility": "Transformers, PyTorch"
            })
    
    # Check for GGUF models
    import glob
    gguf_models = glob.glob("converted_models/*.gguf")
    for gguf_path in gguf_models:
        size_gb = Path(gguf_path).stat().st_size / (1024**3)
        quant_type = Path(gguf_path).stem.split('_')[-1].upper()
        formats_to_compare.append({
            "format": f"GGUF ({quant_type})",
            "path": gguf_path,
            "size_gb": size_gb,
            "security": "Standard",
            "loading_speed": "Very Fast",
            "compatibility": "llama.cpp, Ollama"
        })
    
    if not formats_to_compare:
        print("No converted models found for comparison")
        return
    
    # Display comparison table
    print(f"{'Format':<15} {'Size (GB)':<10} {'Security':<10} {'Loading':<12} {'Compatibility':<20}")
    print("-" * 75)
    
    for fmt in formats_to_compare:
        print(f"{fmt['format']:<15} {fmt['size_gb']:<10.2f} {fmt['security']:<10} "
              f"{fmt['loading_speed']:<12} {fmt['compatibility']:<20}")
    
    # Recommendations
    print("\n📋 Format Recommendations:")
    print("- SafeTensors: Production use, security-critical applications")
    print("- GGUF Q4_0: General purpose, good balance of size/quality")
    print("- GGUF Q2_K: Edge deployment, maximum compression")
    print("- GGUF Q8_0: High quality, server deployment")


def main():
    """Main function demonstrating model format conversion workflows."""
    print("Model Format Conversion and Optimization Examples")
    print("=" * 70)
    
    # Create output directories
    for dir_name in ["converted_models", "optimized_models", "modelfiles"]:
        Path(dir_name).mkdir(exist_ok=True)
    
    try:
        # Run conversion demonstrations
        demonstrate_pytorch_to_safetensors()
        demonstrate_gguf_conversion()
        demonstrate_modelfile_creation()
        demonstrate_optimization_pipeline()
        demonstrate_format_comparison()
        
        print("\n" + "=" * 70)
        print("Format conversion examples completed!")
        
        print("\n📁 Generated files:")
        print("- converted_models/ - SafeTensors and GGUF conversions")
        print("- optimized_models/ - Deployment-optimized models")
        print("- modelfiles/ - Ollama Modelfile examples")
        
        print("\n🔑 Key concepts demonstrated:")
        print("- PyTorch to SafeTensors conversion for security")
        print("- GGUF quantization for efficiency")
        print("- Modelfile creation for behavior customization")
        print("- Deployment optimization strategies")
        print("- Format comparison and selection criteria")
        
        print("\n💡 Next steps:")
        print("- Test converted models with appropriate inference engines")
        print("- Benchmark performance across different formats")
        print("- Deploy optimized models to target environments")
        print("- Create custom Modelfiles for specific use cases")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()