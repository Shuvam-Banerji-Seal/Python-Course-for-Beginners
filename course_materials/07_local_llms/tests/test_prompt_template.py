"""
Unit tests for PromptTemplate management system.

This module contains comprehensive tests for the PromptTemplate classes,
including template rendering, parameter substitution, validation, and sanitization.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Import the classes to test
import sys
sys.path.append(str(Path(__file__).parent.parent / "utils"))

from prompt_template import (
    PromptTemplate,
    PromptCategory,
    ValidationLevel,
    PromptSanitizer,
    PromptTemplateManager
)


class TestPromptCategory:
    """Test cases for PromptCategory enum."""
    
    def test_prompt_categories(self):
        """Test all prompt category values."""
        assert PromptCategory.ASSISTANT.value == "assistant"
        assert PromptCategory.CREATIVE.value == "creative"
        assert PromptCategory.TECHNICAL.value == "technical"
        assert PromptCategory.EDUCATIONAL.value == "educational"
        assert PromptCategory.ANALYSIS.value == "analysis"
        assert PromptCategory.CONVERSATION.value == "conversation"
        assert PromptCategory.CUSTOM.value == "custom"


class TestValidationLevel:
    """Test cases for ValidationLevel enum."""
    
    def test_validation_levels(self):
        """Test all validation level values."""
        assert ValidationLevel.NONE.value == "none"
        assert ValidationLevel.BASIC.value == "basic"
        assert ValidationLevel.STRICT.value == "strict"


class TestPromptTemplate:
    """Test cases for PromptTemplate class."""
    
    def test_prompt_template_creation(self):
        """Test basic PromptTemplate creation."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a helpful assistant.",
            user_template="Please help me with {task}.",
            description="A test template"
        )
        
        assert template.name == "test_template"
        assert template.category == PromptCategory.ASSISTANT
        assert template.system_prompt == "You are a helpful assistant."
        assert template.user_template == "Please help me with {task}."
        assert template.description == "A test template"
        assert template.parameters == {}
        assert template.example_inputs == []
        assert template.expected_behavior == ""
        assert template.tags == []
        assert template.version == "1.0"
    
    def test_prompt_template_with_string_category(self):
        """Test PromptTemplate creation with string category."""
        template = PromptTemplate(
            name="test_template",
            category="assistant",  # String instead of enum
            system_prompt="You are a helpful assistant.",
            user_template="Please help me with {task}."
        )
        
        assert template.category == PromptCategory.ASSISTANT
    
    def test_get_required_parameters(self):
        """Test extraction of required parameters."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant with {expertise}.",
            user_template="Please help me with {task} using {method}."
        )
        
        required_params = template.get_required_parameters()
        
        assert required_params == {"role", "expertise", "task", "method"}
    
    def test_get_required_parameters_no_params(self):
        """Test parameter extraction with no parameters."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a helpful assistant.",
            user_template="Please help me."
        )
        
        required_params = template.get_required_parameters()
        
        assert required_params == set()
    
    def test_validate_parameters_success(self):
        """Test successful parameter validation."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}.",
            parameters={"role": str, "task": str}
        )
        
        params = {"role": "helpful", "task": "coding"}
        errors = template.validate_parameters(params)
        
        assert errors == []
    
    def test_validate_parameters_missing(self):
        """Test parameter validation with missing parameters."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}."
        )
        
        params = {"role": "helpful"}  # Missing 'task'
        errors = template.validate_parameters(params)
        
        assert len(errors) == 1
        assert "Missing required parameters: task" in errors[0]
    
    def test_validate_parameters_extra(self):
        """Test parameter validation with extra parameters."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}."
        )
        
        params = {"role": "helpful", "task": "coding", "extra": "value"}
        errors = template.validate_parameters(params)
        
        assert len(errors) == 1
        assert "Unexpected parameters: extra" in errors[0]
    
    def test_validate_parameters_wrong_type(self):
        """Test parameter validation with wrong types."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}.",
            parameters={"role": str, "task": str}
        )
        
        params = {"role": "helpful", "task": 123}  # task should be str
        errors = template.validate_parameters(params)
        
        assert len(errors) == 1
        assert "Parameter 'task' should be str, got int" in errors[0]
    
    def test_render_success(self):
        """Test successful template rendering."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant with {expertise}.",
            user_template="Please help me with {task}."
        )
        
        params = {"role": "helpful", "expertise": "Python", "task": "debugging"}
        result = template.render(params)
        
        assert result["system"] == "You are a helpful assistant with Python."
        assert result["user"] == "Please help me with debugging."
    
    def test_render_validation_error(self):
        """Test template rendering with validation error."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}."
        )
        
        params = {"role": "helpful"}  # Missing 'task'
        
        with pytest.raises(ValueError) as exc_info:
            template.render(params)
        
        assert "Parameter validation failed" in str(exc_info.value)
    
    def test_render_missing_parameter(self):
        """Test template rendering with missing parameter."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}."
        )
        
        params = {"role": "helpful"}  # Missing 'task'
        
        with pytest.raises(ValueError) as exc_info:
            template.render(params, validate=False)
        
        assert "Missing parameter for template rendering" in str(exc_info.value)
    
    def test_to_dict(self):
        """Test template conversion to dictionary."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a helpful assistant.",
            user_template="Help with {task}.",
            tags=["test", "assistant"]
        )
        
        data = template.to_dict()
        
        assert data["name"] == "test_template"
        assert data["category"] == "assistant"
        assert data["system_prompt"] == "You are a helpful assistant."
        assert data["user_template"] == "Help with {task}."
        assert data["tags"] == ["test", "assistant"]
    
    def test_from_dict(self):
        """Test template creation from dictionary."""
        data = {
            "name": "test_template",
            "category": "assistant",
            "system_prompt": "You are a helpful assistant.",
            "user_template": "Help with {task}.",
            "description": "Test template",
            "tags": ["test"]
        }
        
        template = PromptTemplate.from_dict(data)
        
        assert template.name == "test_template"
        assert template.category == PromptCategory.ASSISTANT
        assert template.system_prompt == "You are a helpful assistant."
        assert template.user_template == "Help with {task}."
        assert template.description == "Test template"
        assert template.tags == ["test"]


class TestPromptSanitizer:
    """Test cases for PromptSanitizer class."""
    
    def test_sanitizer_initialization(self):
        """Test PromptSanitizer initialization."""
        sanitizer = PromptSanitizer()
        assert sanitizer.validation_level == ValidationLevel.BASIC
        
        sanitizer_strict = PromptSanitizer(ValidationLevel.STRICT)
        assert sanitizer_strict.validation_level == ValidationLevel.STRICT
    
    def test_sanitize_input_none_level(self):
        """Test sanitization with NONE validation level."""
        sanitizer = PromptSanitizer(ValidationLevel.NONE)
        
        text = "  Hello World!  "
        result = sanitizer.sanitize_input(text)
        
        assert result == "Hello World!"  # Only stripped
    
    def test_sanitize_input_basic_level(self):
        """Test sanitization with BASIC validation level."""
        sanitizer = PromptSanitizer(ValidationLevel.BASIC)
        
        text = "Hello\x00World\x01Test\n"
        result = sanitizer.sanitize_input(text)
        
        assert result == "HelloWorldTest\n"  # Control chars removed, newline kept
    
    def test_sanitize_input_strict_level(self):
        """Test sanitization with STRICT validation level."""
        sanitizer = PromptSanitizer(ValidationLevel.STRICT)
        
        text = "Hello <script>alert('xss')</script> World & Test"
        result = sanitizer.sanitize_input(text)
        
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
        assert "script" not in result  # HTML tags removed
    
    def test_sanitize_input_max_length(self):
        """Test sanitization with maximum length limit."""
        sanitizer = PromptSanitizer()
        
        text = "Hello World"
        
        with pytest.raises(ValueError) as exc_info:
            sanitizer.sanitize_input(text, max_length=5)
        
        assert "Input too long" in str(exc_info.value)
    
    def test_sanitize_input_non_string(self):
        """Test sanitization with non-string input."""
        sanitizer = PromptSanitizer()
        
        with pytest.raises(ValueError) as exc_info:
            sanitizer.sanitize_input(123)
        
        assert "Input must be string" in str(exc_info.value)
    
    def test_check_dangerous_patterns_script(self):
        """Test detection of dangerous script patterns."""
        sanitizer = PromptSanitizer(ValidationLevel.STRICT)
        
        dangerous_text = "Hello <script>alert('xss')</script> World"
        
        with pytest.raises(ValueError) as exc_info:
            sanitizer.sanitize_input(dangerous_text)
        
        assert "Potentially dangerous pattern detected" in str(exc_info.value)
    
    def test_check_dangerous_patterns_javascript(self):
        """Test detection of JavaScript URL patterns."""
        sanitizer = PromptSanitizer(ValidationLevel.STRICT)
        
        dangerous_text = "Click here: javascript:alert('xss')"
        
        with pytest.raises(ValueError) as exc_info:
            sanitizer.sanitize_input(dangerous_text)
        
        assert "Potentially dangerous pattern detected" in str(exc_info.value)
    
    def test_check_sql_injection_patterns(self):
        """Test detection of SQL injection patterns."""
        sanitizer = PromptSanitizer(ValidationLevel.STRICT)
        
        dangerous_text = "'; DROP TABLE users; --"
        
        with pytest.raises(ValueError) as exc_info:
            sanitizer.sanitize_input(dangerous_text)
        
        assert "Potential SQL injection pattern detected" in str(exc_info.value)
    
    def test_validate_parameters(self):
        """Test parameter validation and sanitization."""
        sanitizer = PromptSanitizer(ValidationLevel.BASIC)
        
        params = {
            "text_param": "  Hello World  ",
            "number_param": 42,
            "bool_param": True
        }
        
        result = sanitizer.validate_parameters(params)
        
        assert result["text_param"] == "Hello World"  # Sanitized
        assert result["number_param"] == 42  # Unchanged
        assert result["bool_param"] is True  # Unchanged


class TestPromptTemplateManager:
    """Test cases for PromptTemplateManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PromptTemplateManager()
    
    def test_manager_initialization(self):
        """Test PromptTemplateManager initialization."""
        manager = PromptTemplateManager()
        
        assert manager.templates == {}
        assert manager.templates_dir is None
        assert isinstance(manager.sanitizer, PromptSanitizer)
    
    def test_manager_initialization_with_dir(self):
        """Test PromptTemplateManager initialization with templates directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a test template file
            template_data = {
                "name": "test_template",
                "category": "assistant",
                "system_prompt": "You are helpful.",
                "user_template": "Help with {task}."
            }
            
            template_file = temp_path / "test_template.json"
            with open(template_file, 'w') as f:
                json.dump(template_data, f)
            
            manager = PromptTemplateManager(temp_path)
            
            assert manager.templates_dir == temp_path
            assert "test_template" in manager.templates
    
    def test_add_template_success(self):
        """Test successful template addition."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        self.manager.add_template(template)
        
        assert "test_template" in self.manager.templates
        assert self.manager.templates["test_template"] == template
    
    def test_add_template_duplicate_name(self):
        """Test adding template with duplicate name."""
        template1 = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        template2 = PromptTemplate(
            name="test_template",  # Same name
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Create {content}."
        )
        
        self.manager.add_template(template1)
        
        with pytest.raises(ValueError) as exc_info:
            self.manager.add_template(template2)
        
        assert "Template 'test_template' already exists" in str(exc_info.value)
    
    def test_get_template_success(self):
        """Test successful template retrieval."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        self.manager.add_template(template)
        retrieved = self.manager.get_template("test_template")
        
        assert retrieved == template
    
    def test_get_template_not_found(self):
        """Test template retrieval for non-existent template."""
        result = self.manager.get_template("nonexistent_template")
        
        assert result is None
    
    def test_list_templates_all(self):
        """Test listing all templates."""
        template1 = PromptTemplate(
            name="assistant_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        template2 = PromptTemplate(
            name="creative_template",
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Create {content}."
        )
        
        self.manager.add_template(template1)
        self.manager.add_template(template2)
        
        templates = self.manager.list_templates()
        
        assert set(templates) == {"assistant_template", "creative_template"}
    
    def test_list_templates_by_category(self):
        """Test listing templates filtered by category."""
        template1 = PromptTemplate(
            name="assistant_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        template2 = PromptTemplate(
            name="creative_template",
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Create {content}."
        )
        
        self.manager.add_template(template1)
        self.manager.add_template(template2)
        
        assistant_templates = self.manager.list_templates(PromptCategory.ASSISTANT)
        
        assert assistant_templates == ["assistant_template"]
    
    def test_search_templates_by_name(self):
        """Test searching templates by name."""
        template1 = PromptTemplate(
            name="code_assistant",
            category=PromptCategory.TECHNICAL,
            system_prompt="You help with code.",
            user_template="Review {code}."
        )
        
        template2 = PromptTemplate(
            name="creative_writer",
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Write {content}."
        )
        
        self.manager.add_template(template1)
        self.manager.add_template(template2)
        
        results = self.manager.search_templates("code")
        
        assert results == ["code_assistant"]
    
    def test_search_templates_by_description(self):
        """Test searching templates by description."""
        template = PromptTemplate(
            name="helper",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}.",
            description="A template for coding assistance"
        )
        
        self.manager.add_template(template)
        
        results = self.manager.search_templates("coding", ["description"])
        
        assert results == ["helper"]
    
    def test_search_templates_by_tags(self):
        """Test searching templates by tags."""
        template = PromptTemplate(
            name="helper",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}.",
            tags=["programming", "debugging", "assistance"]
        )
        
        self.manager.add_template(template)
        
        results = self.manager.search_templates("programming", ["tags"])
        
        assert results == ["helper"]
    
    def test_render_template_success(self):
        """Test successful template rendering."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are a {role} assistant.",
            user_template="Help with {task}."
        )
        
        self.manager.add_template(template)
        
        result = self.manager.render_template(
            "test_template",
            {"role": "helpful", "task": "coding"}
        )
        
        assert result["system"] == "You are a helpful assistant."
        assert result["user"] == "Help with coding."
    
    def test_render_template_not_found(self):
        """Test rendering non-existent template."""
        with pytest.raises(ValueError) as exc_info:
            self.manager.render_template("nonexistent", {"param": "value"})
        
        assert "Template 'nonexistent' not found" in str(exc_info.value)
    
    def test_render_template_with_sanitization(self):
        """Test template rendering with input sanitization."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        self.manager.add_template(template)
        
        result = self.manager.render_template(
            "test_template",
            {"task": "  coding task  "},  # Will be sanitized
            sanitize=True
        )
        
        assert result["user"] == "Help with coding task."
    
    def test_save_template(self):
        """Test saving template to file."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            self.manager.templates_dir = temp_path
            
            self.manager.save_template(template)
            
            saved_file = temp_path / "test_template.json"
            assert saved_file.exists()
            
            # Verify content
            with open(saved_file) as f:
                data = json.load(f)
            
            assert data["name"] == "test_template"
            assert data["category"] == "assistant"
    
    def test_save_template_custom_path(self):
        """Test saving template to custom file path."""
        template = PromptTemplate(
            name="test_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            self.manager.save_template(template, temp_path)
            
            assert temp_path.exists()
            
            # Verify content
            with open(temp_path) as f:
                data = json.load(f)
            
            assert data["name"] == "test_template"
        finally:
            temp_path.unlink()
    
    def test_load_template(self):
        """Test loading template from file."""
        template_data = {
            "name": "loaded_template",
            "category": "creative",
            "system_prompt": "You are creative.",
            "user_template": "Create {content}.",
            "description": "A creative template"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(template_data, temp_file)
            temp_path = Path(temp_file.name)
        
        try:
            template = self.manager.load_template(temp_path)
            
            assert template.name == "loaded_template"
            assert template.category == PromptCategory.CREATIVE
            assert template.system_prompt == "You are creative."
            assert "loaded_template" in self.manager.templates
        finally:
            temp_path.unlink()
    
    def test_load_template_invalid_file(self):
        """Test loading template from invalid file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("invalid json content")
            temp_path = Path(temp_file.name)
        
        try:
            with pytest.raises(ValueError) as exc_info:
                self.manager.load_template(temp_path)
            
            assert "Failed to load template" in str(exc_info.value)
        finally:
            temp_path.unlink()
    
    def test_load_templates_from_directory(self):
        """Test loading multiple templates from directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create multiple template files
            template1_data = {
                "name": "template1",
                "category": "assistant",
                "system_prompt": "You are helpful.",
                "user_template": "Help with {task}."
            }
            
            template2_data = {
                "name": "template2",
                "category": "creative",
                "system_prompt": "You are creative.",
                "user_template": "Create {content}."
            }
            
            with open(temp_path / "template1.json", 'w') as f:
                json.dump(template1_data, f)
            
            with open(temp_path / "template2.json", 'w') as f:
                json.dump(template2_data, f)
            
            # Create a non-JSON file (should be ignored)
            with open(temp_path / "readme.txt", 'w') as f:
                f.write("This is not a template")
            
            count = self.manager.load_templates_from_directory(temp_path)
            
            assert count == 2
            assert "template1" in self.manager.templates
            assert "template2" in self.manager.templates
    
    def test_export_templates(self):
        """Test exporting templates to directory."""
        template1 = PromptTemplate(
            name="assistant_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        template2 = PromptTemplate(
            name="creative_template",
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Create {content}."
        )
        
        self.manager.add_template(template1)
        self.manager.add_template(template2)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            count = self.manager.export_templates(temp_path)
            
            assert count == 2
            assert (temp_path / "assistant_template.json").exists()
            assert (temp_path / "creative_template.json").exists()
    
    def test_export_templates_by_category(self):
        """Test exporting templates filtered by category."""
        template1 = PromptTemplate(
            name="assistant_template",
            category=PromptCategory.ASSISTANT,
            system_prompt="You are helpful.",
            user_template="Help with {task}."
        )
        
        template2 = PromptTemplate(
            name="creative_template",
            category=PromptCategory.CREATIVE,
            system_prompt="You are creative.",
            user_template="Create {content}."
        )
        
        self.manager.add_template(template1)
        self.manager.add_template(template2)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            count = self.manager.export_templates(temp_path, PromptCategory.ASSISTANT)
            
            assert count == 1
            assert (temp_path / "assistant_template.json").exists()
            assert not (temp_path / "creative_template.json").exists()
    
    def test_create_builtin_templates(self):
        """Test creation of built-in templates."""
        self.manager.create_builtin_templates()
        
        templates = self.manager.list_templates()
        
        # Check that built-in templates are created
        assert "helpful_assistant" in templates
        assert "creative_writer" in templates
        assert "code_reviewer" in templates
        assert "educational_tutor" in templates
        
        # Test one of the templates
        assistant_template = self.manager.get_template("helpful_assistant")
        assert assistant_template.category == PromptCategory.ASSISTANT
        
        # Test rendering
        result = self.manager.render_template(
            "helpful_assistant",
            {"tone": "friendly", "user_input": "What is Python?"}
        )
        
        assert "friendly" in result["system"]
        assert "What is Python?" in result["user"]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])