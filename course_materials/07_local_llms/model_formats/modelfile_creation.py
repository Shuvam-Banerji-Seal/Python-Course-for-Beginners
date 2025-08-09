#!/usr/bin/env python3
"""
Modelfile Creation and Customization Examples

This script demonstrates how to create and customize Ollama Modelfiles for different use cases:
- Creating basic Modelfiles
- Customizing system prompts and parameters
- Building specialized AI assistants
- Managing Modelfile templates

Requirements:
    - Ollama installed and running
    - Base models available in Ollama

Usage:
    python modelfile_creation.py
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ModelfileConfig:
    """Configuration class for Modelfile creation."""
    name: str
    base_model: str
    system_prompt: str
    parameters: Dict[str, Any]
    template: Optional[str] = None
    adapter: Optional[str] = None
    license: Optional[str] = None
    description: str = ""


class ModelfileBuilder:
    """
    A utility class for building and managing Ollama Modelfiles.
    Provides methods for creating, customizing, and deploying Modelfiles.
    """
    
    def __init__(self):
        self.templates = {}
        self.load_common_templates()
    
    def load_common_templates(self):
        """Load common chat templates for different model types."""
        self.templates = {
            'llama2_chat': '''{{ if .System }}<s>[INST] <<SYS>>
{{ .System }}
<</SYS>>

{{ end }}{{ if .Prompt }}{{ .Prompt }} [/INST] {{ end }}{{ .Response }}</s>''',
            
            'mistral_instruct': '''{{ if .System }}{{ .System }}

{{ end }}{{ if .Prompt }}<s>[INST] {{ .Prompt }} [/INST]{{ end }}{{ if .Response }} {{ .Response }}</s>{{ end }}''',
            
            'codellama': '''{{ if .System }}{{ .System }}

{{ end }}{{ if .Prompt }}### Instruction:
{{ .Prompt }}

### Response:
{{ end }}{{ .Response }}''',
            
            'alpaca': '''{{ if .System }}{{ .System }}

{{ end }}{{ if .Prompt }}### Instruction:
{{ .Prompt }}

### Response:
{{ end }}{{ .Response }}''',
            
            'vicuna': '''{{ if .System }}{{ .System }}

{{ end }}{{ if .Prompt }}USER: {{ .Prompt }}
ASSISTANT:{{ end }} {{ .Response }}''',
            
            'simple': '''{{ if .System }}{{ .System }}

{{ end }}{{ if .Prompt }}{{ .Prompt }}{{ end }}{{ .Response }}'''
        }
    
    def create_modelfile(self, config: ModelfileConfig) -> str:
        """
        Create a Modelfile string from configuration.
        
        Args:
            config: ModelfileConfig object with all settings
            
        Returns:
            str: Complete Modelfile content
        """
        lines = []
        
        # FROM directive (required)
        lines.append(f"FROM {config.base_model}")
        lines.append("")
        
        # SYSTEM prompt
        if config.system_prompt:
            lines.append('SYSTEM """')
            lines.append(config.system_prompt)
            lines.append('"""')
            lines.append("")
        
        # PARAMETERS
        if config.parameters:
            for param, value in config.parameters.items():
                lines.append(f"PARAMETER {param} {value}")
            lines.append("")
        
        # TEMPLATE
        if config.template:
            lines.append('TEMPLATE """')
            lines.append(config.template)
            lines.append('"""')
            lines.append("")
        
        # ADAPTER
        if config.adapter:
            lines.append(f"ADAPTER {config.adapter}")
            lines.append("")
        
        # LICENSE
        if config.license:
            lines.append('LICENSE """')
            lines.append(config.license)
            lines.append('"""')
            lines.append("")
        
        return "\n".join(lines)
    
    def save_modelfile(self, config: ModelfileConfig, output_path: str) -> bool:
        """
        Save Modelfile to disk.
        
        Args:
            config: ModelfileConfig object
            output_path: Path to save the Modelfile
            
        Returns:
            bool: True if saved successfully
        """
        try:
            modelfile_content = self.create_modelfile(config)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(modelfile_content)
            
            print(f"Modelfile saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving Modelfile: {e}")
            return False
    
    def create_ollama_model(self, config: ModelfileConfig, temp_dir: Optional[str] = None) -> bool:
        """
        Create an Ollama model from Modelfile configuration.
        
        Args:
            config: ModelfileConfig object
            temp_dir: Temporary directory for Modelfile (optional)
            
        Returns:
            bool: True if model created successfully
        """
        # Create temporary Modelfile
        if temp_dir is None:
            temp_dir = tempfile.mkdtemp()
        
        modelfile_path = Path(temp_dir) / "Modelfile"
        
        if not self.save_modelfile(config, str(modelfile_path)):
            return False
        
        try:
            # Run ollama create command
            cmd = ["ollama", "create", config.name, "-f", str(modelfile_path)]
            print(f"Creating Ollama model: {config.name}")
            print(f"Command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Model '{config.name}' created successfully!")
                return True
            else:
                print(f"❌ Error creating model: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Model creation timed out")
            return False
        except FileNotFoundError:
            print("❌ Ollama not found. Please install Ollama first.")
            return False
        except Exception as e:
            print(f"❌ Error creating model: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """Get list of available base models in Ollama."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = [line.split()[0] for line in lines if line.strip()]
                return models
            else:
                print("Error listing models:", result.stderr)
                return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []


def create_assistant_modelfiles():
    """Create various AI assistant Modelfiles for different use cases."""
    print("=== Creating AI Assistant Modelfiles ===")
    
    builder = ModelfileBuilder()
    
    # 1. Helpful General Assistant
    general_assistant = ModelfileConfig(
        name="helpful-assistant",
        base_model="llama2:7b",
        system_prompt="""You are a helpful, harmless, and honest AI assistant. You provide clear, accurate, and useful responses to user questions. You admit when you don't know something and avoid making up information. You are friendly but professional in your communication style.""",
        parameters={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_ctx": 2048
        },
        description="A general-purpose helpful AI assistant"
    )
    
    # 2. Code Review Assistant
    code_reviewer = ModelfileConfig(
        name="code-reviewer",
        base_model="codellama:7b",
        system_prompt="""You are an expert code reviewer with deep knowledge of software engineering best practices, security, performance optimization, and clean code principles. 

When reviewing code, you should:
- Identify potential bugs, security vulnerabilities, and performance issues
- Suggest improvements for readability and maintainability
- Check for adherence to coding standards and best practices
- Provide specific, actionable feedback with examples
- Be constructive and educational in your comments
- Consider the broader architectural implications

Focus on being thorough but concise. Prioritize critical issues over minor style preferences.""",
        parameters={
            "temperature": 0.3,  # Lower temperature for more focused responses
            "top_p": 0.8,
            "top_k": 30,
            "repeat_penalty": 1.05,
            "num_ctx": 4096  # Larger context for code analysis
        },
        template=builder.templates['codellama'],
        description="Specialized assistant for code review and analysis"
    )
    
    # 3. Creative Writing Assistant
    creative_writer = ModelfileConfig(
        name="creative-writer",
        base_model="llama2:13b",
        system_prompt="""You are a creative writing assistant with expertise in storytelling, character development, plot structure, and various literary genres. You help writers brainstorm ideas, develop characters, craft compelling narratives, and improve their writing style.

Your approach should be:
- Imaginative and inspiring while being practical
- Supportive of the writer's vision while offering constructive suggestions
- Knowledgeable about different genres, narrative techniques, and literary devices
- Able to adapt your style to match the writer's needs (fiction, poetry, screenwriting, etc.)
- Encouraging creativity while maintaining narrative coherence

You can help with plot development, character arcs, dialogue, world-building, and overcoming writer's block.""",
        parameters={
            "temperature": 0.8,  # Higher temperature for creativity
            "top_p": 0.95,
            "top_k": 50,
            "repeat_penalty": 1.15,
            "num_ctx": 3072
        },
        description="Creative writing and storytelling assistant"
    )
    
    # 4. Technical Documentation Assistant
    tech_writer = ModelfileConfig(
        name="tech-writer",
        base_model="llama2:7b",
        system_prompt="""You are a technical writing specialist focused on creating clear, comprehensive, and user-friendly documentation. You excel at explaining complex technical concepts in accessible language while maintaining accuracy and completeness.

Your expertise includes:
- API documentation and developer guides
- User manuals and tutorials
- Technical specifications and requirements
- README files and project documentation
- Code comments and inline documentation

Your writing should be:
- Clear and concise, avoiding unnecessary jargon
- Well-structured with logical flow and proper headings
- Inclusive of examples and practical use cases
- Consistent in terminology and formatting
- Accessible to the target audience's technical level""",
        parameters={
            "temperature": 0.4,  # Lower temperature for consistency
            "top_p": 0.85,
            "top_k": 35,
            "repeat_penalty": 1.08,
            "num_ctx": 2048
        },
        description="Technical documentation and writing assistant"
    )
    
    # 5. Data Analysis Assistant
    data_analyst = ModelfileConfig(
        name="data-analyst",
        base_model="codellama:7b",
        system_prompt="""You are a data analysis expert specializing in statistical analysis, data visualization, and insights generation. You help users understand their data, choose appropriate analytical methods, and interpret results.

Your capabilities include:
- Statistical analysis and hypothesis testing
- Data cleaning and preprocessing guidance
- Visualization recommendations and best practices
- Python/R code for data analysis tasks
- Interpretation of statistical results
- Recommendations for data collection and experimental design

You should:
- Ask clarifying questions about the data and analysis goals
- Suggest appropriate statistical methods and tools
- Explain statistical concepts in understandable terms
- Provide practical, actionable insights
- Consider data quality and limitations in your recommendations""",
        parameters={
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_ctx": 3072
        },
        template=builder.templates['codellama'],
        description="Data analysis and statistics assistant"
    )
    
    # Create all assistant models
    assistants = [general_assistant, code_reviewer, creative_writer, tech_writer, data_analyst]
    
    # Check available base models
    available_models = builder.list_available_models()
    print(f"Available base models: {available_models}")
    
    for assistant in assistants:
        print(f"\n--- Creating {assistant.name} ---")
        
        # Check if base model is available
        if assistant.base_model not in available_models:
            print(f"⚠️  Base model '{assistant.base_model}' not available. Skipping...")
            print(f"   To use this assistant, first run: ollama pull {assistant.base_model}")
            continue
        
        # Save Modelfile for inspection
        modelfile_path = f"modelfiles/{assistant.name}.Modelfile"
        os.makedirs("modelfiles", exist_ok=True)
        builder.save_modelfile(assistant, modelfile_path)
        
        # Create the model in Ollama
        success = builder.create_ollama_model(assistant)
        
        if success:
            print(f"✅ {assistant.name} ready to use!")
            print(f"   Test with: ollama run {assistant.name}")
        else:
            print(f"❌ Failed to create {assistant.name}")


def create_specialized_modelfiles():
    """Create specialized Modelfiles for specific domains."""
    print("\n=== Creating Specialized Domain Modelfiles ===")
    
    builder = ModelfileBuilder()
    
    # 1. Python Tutor
    python_tutor = ModelfileConfig(
        name="python-tutor",
        base_model="codellama:7b",
        system_prompt="""You are an expert Python programming tutor. Your goal is to help students learn Python programming through clear explanations, practical examples, and guided practice.

Teaching approach:
- Start with fundamentals and build complexity gradually
- Provide working code examples for every concept
- Explain not just "how" but "why" things work
- Encourage best practices and Pythonic code
- Help debug code and explain error messages
- Suggest practice exercises and projects
- Adapt explanations to the student's skill level

Topics you cover include:
- Python syntax and basic programming concepts
- Data structures (lists, dictionaries, sets, tuples)
- Functions, classes, and object-oriented programming
- File handling and data processing
- Popular libraries (NumPy, Pandas, Matplotlib)
- Web development basics (Flask, Django)
- Testing and debugging techniques

Always provide runnable code examples and explain each part clearly.""",
        parameters={
            "temperature": 0.6,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_ctx": 3072
        },
        template=builder.templates['codellama'],
        description="Python programming tutor and mentor"
    )
    
    # 2. DevOps Assistant
    devops_assistant = ModelfileConfig(
        name="devops-helper",
        base_model="llama2:7b",
        system_prompt="""You are a DevOps and infrastructure expert specializing in automation, deployment, monitoring, and cloud technologies. You help teams implement reliable, scalable, and secure infrastructure solutions.

Your expertise covers:
- CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Containerization (Docker, Kubernetes)
- Cloud platforms (AWS, Azure, GCP)
- Infrastructure as Code (Terraform, CloudFormation)
- Configuration management (Ansible, Chef, Puppet)
- Monitoring and logging (Prometheus, Grafana, ELK stack)
- Security best practices and compliance
- Performance optimization and scaling

You should:
- Provide practical, production-ready solutions
- Consider security, scalability, and maintainability
- Suggest industry best practices and standards
- Help troubleshoot infrastructure issues
- Recommend appropriate tools for specific use cases
- Include configuration examples and scripts when helpful""",
        parameters={
            "temperature": 0.4,
            "top_p": 0.85,
            "top_k": 35,
            "repeat_penalty": 1.08,
            "num_ctx": 2048
        },
        description="DevOps and infrastructure automation assistant"
    )
    
    # 3. Academic Research Assistant
    research_assistant = ModelfileConfig(
        name="research-helper",
        base_model="llama2:13b",
        system_prompt="""You are an academic research assistant with expertise in research methodology, literature review, data analysis, and academic writing. You help researchers across various disciplines conduct rigorous and impactful research.

Your capabilities include:
- Research design and methodology guidance
- Literature review strategies and synthesis
- Statistical analysis and interpretation
- Academic writing and citation formatting
- Grant proposal development
- Peer review and manuscript preparation
- Research ethics and best practices
- Data management and visualization

You should:
- Maintain high standards of academic rigor
- Suggest appropriate research methods for different questions
- Help identify gaps in existing literature
- Provide guidance on statistical analysis and interpretation
- Assist with clear, scholarly communication
- Consider ethical implications of research
- Recommend relevant databases and resources
- Support evidence-based conclusions""",
        parameters={
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "num_ctx": 4096
        },
        description="Academic research and methodology assistant"
    )
    
    specialized_models = [python_tutor, devops_assistant, research_assistant]
    
    # Check available base models
    available_models = builder.list_available_models()
    
    for model in specialized_models:
        print(f"\n--- Creating {model.name} ---")
        
        if model.base_model not in available_models:
            print(f"⚠️  Base model '{model.base_model}' not available. Skipping...")
            continue
        
        # Save Modelfile
        modelfile_path = f"modelfiles/{model.name}.Modelfile"
        os.makedirs("modelfiles", exist_ok=True)
        builder.save_modelfile(model, modelfile_path)
        
        # Create model
        success = builder.create_ollama_model(model)
        
        if success:
            print(f"✅ {model.name} ready to use!")


def demonstrate_parameter_tuning():
    """Demonstrate how different parameters affect model behavior."""
    print("\n=== Parameter Tuning Demonstration ===")
    
    builder = ModelfileBuilder()
    available_models = builder.list_available_models()
    
    if not available_models:
        print("No base models available for parameter tuning demo")
        return
    
    base_model = available_models[0]  # Use first available model
    
    # Create models with different temperature settings
    temperature_configs = [
        ("conservative-assistant", 0.2, "Very focused and deterministic responses"),
        ("balanced-assistant", 0.7, "Good balance of creativity and consistency"),
        ("creative-assistant", 1.0, "More creative and varied responses")
    ]
    
    system_prompt = """You are a helpful AI assistant. Respond to user questions clearly and helpfully."""
    
    for name, temp, description in temperature_configs:
        config = ModelfileConfig(
            name=name,
            base_model=base_model,
            system_prompt=system_prompt,
            parameters={
                "temperature": temp,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1
            },
            description=description
        )
        
        print(f"\nCreating {name} (temperature={temp})...")
        
        # Save Modelfile for inspection
        modelfile_path = f"modelfiles/{name}.Modelfile"
        os.makedirs("modelfiles", exist_ok=True)
        builder.save_modelfile(config, modelfile_path)
        
        print(f"Modelfile saved to: {modelfile_path}")
        print(f"Description: {description}")


def create_template_examples():
    """Create examples showing different chat templates."""
    print("\n=== Chat Template Examples ===")
    
    builder = ModelfileBuilder()
    
    # Create a simple example for each template type
    templates_to_demo = ['llama2_chat', 'mistral_instruct', 'alpaca', 'simple']
    
    for template_name in templates_to_demo:
        config = ModelfileConfig(
            name=f"template-{template_name.replace('_', '-')}",
            base_model="llama2:7b",
            system_prompt="You are a helpful AI assistant.",
            parameters={"temperature": 0.7},
            template=builder.templates[template_name],
            description=f"Example using {template_name} template"
        )
        
        # Save Modelfile to show template structure
        modelfile_path = f"modelfiles/template-{template_name}.Modelfile"
        os.makedirs("modelfiles", exist_ok=True)
        builder.save_modelfile(config, modelfile_path)
        
        print(f"Template example saved: {modelfile_path}")


def main():
    """Main function demonstrating Modelfile creation and customization."""
    print("Modelfile Creation and Customization Examples")
    print("=" * 60)
    
    # Check if Ollama is available
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Ollama not found. Please install Ollama first.")
            print("Visit: https://ollama.ai/download")
            return
        print(f"✅ Ollama version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
        return
    
    try:
        # Create various types of Modelfiles
        create_assistant_modelfiles()
        create_specialized_modelfiles()
        demonstrate_parameter_tuning()
        create_template_examples()
        
        print("\n" + "=" * 60)
        print("Modelfile creation examples completed!")
        print("\nGenerated files:")
        print("- modelfiles/ directory contains all Modelfile examples")
        print("- Use 'ollama create <name> -f <modelfile>' to create models")
        print("- Test models with 'ollama run <name>'")
        
        print("\nKey concepts demonstrated:")
        print("- System prompt customization for different roles")
        print("- Parameter tuning for behavior control")
        print("- Chat template configuration")
        print("- Specialized domain assistants")
        print("- Production-ready Modelfile patterns")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()