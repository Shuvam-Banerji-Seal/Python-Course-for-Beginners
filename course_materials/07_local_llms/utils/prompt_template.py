"""
PromptTemplate management system for local LLMs.

This module provides classes and functions for managing prompt templates,
including template rendering, parameter substitution, validation, and
sanitization for prompt inputs.
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Union, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
import string
from datetime import datetime


class PromptCategory(Enum):
    """Categories for prompt templates."""
    ASSISTANT = "assistant"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    EDUCATIONAL = "educational"
    ANALYSIS = "analysis"
    CONVERSATION = "conversation"
    CUSTOM = "custom"


class ValidationLevel(Enum):
    """Validation levels for prompt inputs."""
    NONE = "none"
    BASIC = "basic"
    STRICT = "strict"


@dataclass
class PromptTemplate:
    """
    A template for generating prompts with parameter substitution.
    """
    name: str
    category: PromptCategory
    system_prompt: str
    user_template: str
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    example_inputs: List[Dict[str, str]] = field(default_factory=list)
    expected_behavior: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0"
    
    def __post_init__(self):
        """Post-initialization validation."""
        if isinstance(self.category, str):
            self.category = PromptCategory(self.category)
    
    def get_required_parameters(self) -> Set[str]:
        """
        Extract required parameters from templates.
        
        Returns:
            Set of parameter names required by the templates
        """
        # Find parameters in both system and user templates
        system_params = set(re.findall(r'\{(\w+)\}', self.system_prompt))
        user_params = set(re.findall(r'\{(\w+)\}', self.user_template))
        return system_params.union(user_params)
    
    def validate_parameters(self, params: Dict[str, Any]) -> List[str]:
        """
        Validate provided parameters against template requirements.
        
        Args:
            params: Parameters to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        required_params = self.get_required_parameters()
        
        # Check for missing parameters
        missing_params = required_params - set(params.keys())
        if missing_params:
            errors.append(f"Missing required parameters: {', '.join(missing_params)}")
        
        # Check for extra parameters
        extra_params = set(params.keys()) - required_params
        if extra_params:
            errors.append(f"Unexpected parameters: {', '.join(extra_params)}")
        
        # Validate parameter types if specified
        for param_name, expected_type in self.parameters.items():
            if param_name in params:
                param_value = params[param_name]
                if expected_type and not isinstance(param_value, expected_type):
                    errors.append(
                        f"Parameter '{param_name}' should be {expected_type.__name__}, "
                        f"got {type(param_value).__name__}"
                    )
        
        return errors
    
    def render(self, params: Dict[str, Any], validate: bool = True) -> Dict[str, str]:
        """
        Render the template with provided parameters.
        
        Args:
            params: Parameters for template substitution
            validate: Whether to validate parameters
            
        Returns:
            Dictionary with rendered system and user prompts
            
        Raises:
            ValueError: If validation fails or rendering fails
        """
        if validate:
            errors = self.validate_parameters(params)
            if errors:
                raise ValueError(f"Parameter validation failed: {'; '.join(errors)}")
        
        try:
            # Render system prompt
            system_rendered = self.system_prompt.format(**params)
            
            # Render user template
            user_rendered = self.user_template.format(**params)
            
            return {
                "system": system_rendered,
                "user": user_rendered
            }
            
        except KeyError as e:
            raise ValueError(f"Missing parameter for template rendering: {e}") from e
        except Exception as e:
            raise ValueError(f"Template rendering failed: {e}") from e
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        data = asdict(self)
        data["category"] = self.category.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptTemplate":
        """Create template from dictionary."""
        if "category" in data and isinstance(data["category"], str):
            data["category"] = PromptCategory(data["category"])
        return cls(**data)


class PromptSanitizer:
    """
    Utility class for sanitizing and validating prompt inputs.
    """
    
    # Potentially dangerous patterns
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript URLs
        r'on\w+\s*=',  # Event handlers
        r'eval\s*\(',  # eval() calls
        r'exec\s*\(',  # exec() calls
        r'import\s+os',  # OS imports
        r'__import__',  # Dynamic imports
        r'subprocess',  # Subprocess calls
        r'system\s*\(',  # System calls
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r'union\s+select',
        r'drop\s+table',
        r'delete\s+from',
        r'insert\s+into',
        r'update\s+.*\s+set',
        r'--\s*$',  # SQL comments
        r'/\*.*?\*/',  # SQL block comments
    ]
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.BASIC):
        """
        Initialize sanitizer with validation level.
        
        Args:
            validation_level: Level of validation to apply
        """
        self.validation_level = validation_level
        self.logger = logging.getLogger(__name__)
    
    def sanitize_input(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize input text based on validation level.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
            
        Raises:
            ValueError: If input fails validation
        """
        if not isinstance(text, str):
            raise ValueError(f"Input must be string, got {type(text).__name__}")
        
        # Length check
        if max_length and len(text) > max_length:
            raise ValueError(f"Input too long: {len(text)} > {max_length}")
        
        if self.validation_level == ValidationLevel.NONE:
            return text
        
        # Basic sanitization
        sanitized = text.strip()
        
        if self.validation_level == ValidationLevel.BASIC:
            # Remove null bytes and control characters
            sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\r\t')
            return sanitized
        
        if self.validation_level == ValidationLevel.STRICT:
            # Check for dangerous patterns
            self._check_dangerous_patterns(sanitized)
            
            # Additional strict sanitization
            sanitized = self._strict_sanitize(sanitized)
            
        return sanitized
    
    def _check_dangerous_patterns(self, text: str) -> None:
        """Check for potentially dangerous patterns."""
        text_lower = text.lower()
        
        # Check dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
                raise ValueError(f"Potentially dangerous pattern detected: {pattern}")
        
        # Check SQL injection patterns
        for pattern in self.SQL_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                raise ValueError(f"Potential SQL injection pattern detected: {pattern}")
    
    def _strict_sanitize(self, text: str) -> str:
        """Apply strict sanitization rules."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Escape special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text
    
    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize all parameters.
        
        Args:
            params: Parameters to validate
            
        Returns:
            Sanitized parameters
        """
        sanitized_params = {}
        
        for key, value in params.items():
            if isinstance(value, str):
                sanitized_params[key] = self.sanitize_input(value)
            else:
                sanitized_params[key] = value
        
        return sanitized_params


class PromptTemplateManager:
    """
    Manager class for handling multiple prompt templates.
    """
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the template manager.
        
        Args:
            templates_dir: Directory containing template files
        """
        self.templates: Dict[str, PromptTemplate] = {}
        self.templates_dir = templates_dir
        self.sanitizer = PromptSanitizer()
        self.logger = logging.getLogger(__name__)
        
        # Load templates from directory if provided
        if templates_dir and templates_dir.exists():
            self.load_templates_from_directory(templates_dir)
    
    def add_template(self, template: PromptTemplate) -> None:
        """
        Add a template to the manager.
        
        Args:
            template: Template to add
            
        Raises:
            ValueError: If template name already exists
        """
        if template.name in self.templates:
            raise ValueError(f"Template '{template.name}' already exists")
        
        self.templates[template.name] = template
        self.logger.info(f"Added template: {template.name}")
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template or None if not found
        """
        return self.templates.get(name)
    
    def list_templates(self, category: Optional[PromptCategory] = None) -> List[str]:
        """
        List available template names.
        
        Args:
            category: Filter by category (optional)
            
        Returns:
            List of template names
        """
        if category is None:
            return list(self.templates.keys())
        
        return [
            name for name, template in self.templates.items()
            if template.category == category
        ]
    
    def search_templates(self, query: str, search_fields: List[str] = None) -> List[str]:
        """
        Search templates by query string.
        
        Args:
            query: Search query
            search_fields: Fields to search in (name, description, tags)
            
        Returns:
            List of matching template names
        """
        if search_fields is None:
            search_fields = ["name", "description", "tags"]
        
        query_lower = query.lower()
        matches = []
        
        for name, template in self.templates.items():
            # Search in specified fields
            if "name" in search_fields and query_lower in name.lower():
                matches.append(name)
                continue
            
            if "description" in search_fields and query_lower in template.description.lower():
                matches.append(name)
                continue
            
            if "tags" in search_fields:
                for tag in template.tags:
                    if query_lower in tag.lower():
                        matches.append(name)
                        break
        
        return matches
    
    def render_template(
        self,
        template_name: str,
        params: Dict[str, Any],
        sanitize: bool = True,
        validation_level: ValidationLevel = ValidationLevel.BASIC
    ) -> Dict[str, str]:
        """
        Render a template with parameters.
        
        Args:
            template_name: Name of template to render
            params: Parameters for rendering
            sanitize: Whether to sanitize inputs
            validation_level: Level of input validation
            
        Returns:
            Rendered prompt dictionary
            
        Raises:
            ValueError: If template not found or rendering fails
        """
        template = self.get_template(template_name)
        if template is None:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Sanitize parameters if requested
        if sanitize:
            sanitizer = PromptSanitizer(validation_level)
            params = sanitizer.validate_parameters(params)
        
        return template.render(params)
    
    def save_template(self, template: PromptTemplate, filepath: Optional[Path] = None) -> None:
        """
        Save a template to file.
        
        Args:
            template: Template to save
            filepath: File path (optional, uses templates_dir if not provided)
        """
        if filepath is None:
            if self.templates_dir is None:
                raise ValueError("No templates directory configured")
            filepath = self.templates_dir / f"{template.name}.json"
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved template to: {filepath}")
    
    def load_template(self, filepath: Path) -> PromptTemplate:
        """
        Load a template from file.
        
        Args:
            filepath: Path to template file
            
        Returns:
            Loaded template
            
        Raises:
            ValueError: If file cannot be loaded or parsed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            template = PromptTemplate.from_dict(data)
            self.add_template(template)
            return template
            
        except Exception as e:
            raise ValueError(f"Failed to load template from {filepath}: {e}") from e
    
    def load_templates_from_directory(self, directory: Path) -> int:
        """
        Load all templates from a directory.
        
        Args:
            directory: Directory containing template files
            
        Returns:
            Number of templates loaded
        """
        loaded_count = 0
        
        for filepath in directory.glob("*.json"):
            try:
                self.load_template(filepath)
                loaded_count += 1
            except Exception as e:
                self.logger.error(f"Failed to load template from {filepath}: {e}")
        
        self.logger.info(f"Loaded {loaded_count} templates from {directory}")
        return loaded_count
    
    def export_templates(self, output_dir: Path, category: Optional[PromptCategory] = None) -> int:
        """
        Export templates to directory.
        
        Args:
            output_dir: Output directory
            category: Filter by category (optional)
            
        Returns:
            Number of templates exported
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        exported_count = 0
        
        templates_to_export = self.templates.values()
        if category:
            templates_to_export = [t for t in templates_to_export if t.category == category]
        
        for template in templates_to_export:
            try:
                self.save_template(template, output_dir / f"{template.name}.json")
                exported_count += 1
            except Exception as e:
                self.logger.error(f"Failed to export template {template.name}: {e}")
        
        self.logger.info(f"Exported {exported_count} templates to {output_dir}")
        return exported_count
    
    def create_builtin_templates(self) -> None:
        """Create a set of built-in templates for common use cases."""
        
        # Assistant template
        assistant_template = PromptTemplate(
            name="helpful_assistant",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a helpful, harmless, and honest AI assistant. "
                         "Provide accurate and useful information while being {tone} in your responses.",
            user_template="{user_input}",
            description="General-purpose helpful assistant",
            parameters={"tone": str, "user_input": str},
            example_inputs=[
                {"tone": "friendly", "user_input": "What is Python?"},
                {"tone": "professional", "user_input": "Explain machine learning"}
            ],
            expected_behavior="Provides helpful, accurate responses in the specified tone",
            tags=["assistant", "general", "helpful"]
        )
        
        # Creative writing template
        creative_template = PromptTemplate(
            name="creative_writer",
            category=PromptCategory.CREATIVE,
            system_prompt="You are a creative writer specializing in {genre}. "
                         "Write engaging, imaginative content that captures the reader's attention. "
                         "Use vivid descriptions and compelling narratives.",
            user_template="Write a {length} {content_type} about: {topic}",
            description="Creative writing assistant for various genres",
            parameters={"genre": str, "length": str, "content_type": str, "topic": str},
            example_inputs=[
                {
                    "genre": "science fiction",
                    "length": "short",
                    "content_type": "story",
                    "topic": "time travel"
                }
            ],
            expected_behavior="Creates engaging creative content in specified genre and format",
            tags=["creative", "writing", "storytelling"]
        )
        
        # Code review template
        code_review_template = PromptTemplate(
            name="code_reviewer",
            category=PromptCategory.TECHNICAL,
            system_prompt="You are an experienced software engineer conducting a code review. "
                         "Focus on {review_aspects}. Provide constructive feedback that helps "
                         "improve code quality, maintainability, and performance.",
            user_template="Please review this {language} code:\n\n```{language}\n{code}\n```\n\n"
                         "Specific concerns: {concerns}",
            description="Code review assistant for various programming languages",
            parameters={
                "review_aspects": str,
                "language": str,
                "code": str,
                "concerns": str
            },
            example_inputs=[
                {
                    "review_aspects": "security, performance, and readability",
                    "language": "python",
                    "code": "def example(): pass",
                    "concerns": "Is this function efficient?"
                }
            ],
            expected_behavior="Provides detailed, constructive code review feedback",
            tags=["technical", "code", "review", "programming"]
        )
        
        # Educational tutor template
        tutor_template = PromptTemplate(
            name="educational_tutor",
            category=PromptCategory.EDUCATIONAL,
            system_prompt="You are a patient and knowledgeable tutor teaching {subject} "
                         "to {student_level} students. Break down complex concepts into "
                         "understandable parts and provide examples when helpful.",
            user_template="Please explain {topic} and help me understand {specific_question}",
            description="Educational tutor for various subjects and levels",
            parameters={
                "subject": str,
                "student_level": str,
                "topic": str,
                "specific_question": str
            },
            example_inputs=[
                {
                    "subject": "mathematics",
                    "student_level": "high school",
                    "topic": "quadratic equations",
                    "specific_question": "how to find the roots"
                }
            ],
            expected_behavior="Provides clear, educational explanations appropriate for student level",
            tags=["educational", "tutor", "teaching", "learning"]
        )
        
        # Add all templates
        templates = [assistant_template, creative_template, code_review_template, tutor_template]
        for template in templates:
            try:
                self.add_template(template)
            except ValueError:
                # Template already exists
                pass


# Example usage and testing functions
def example_usage():
    """Example usage of PromptTemplate management system."""
    # Create manager
    manager = PromptTemplateManager()
    
    # Create built-in templates
    manager.create_builtin_templates()
    
    # List available templates
    print("Available templates:")
    for template_name in manager.list_templates():
        print(f"  - {template_name}")
    
    # Use the helpful assistant template
    try:
        result = manager.render_template(
            "helpful_assistant",
            {
                "tone": "friendly",
                "user_input": "What is machine learning?"
            }
        )
        
        print(f"\nRendered template:")
        print(f"System: {result['system']}")
        print(f"User: {result['user']}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Search templates
    search_results = manager.search_templates("code")
    print(f"\nTemplates matching 'code': {search_results}")


if __name__ == "__main__":
    example_usage()