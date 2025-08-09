"""
Utility classes and helper functions for local LLMs module.

This package provides utility classes for managing different LLM frameworks
and prompt templates, making it easier to work with local language models.
"""

from .ollama_manager import OllamaManager
from .transformers_manager import TransformersManager
from .prompt_template import PromptTemplate, PromptTemplateManager

__all__ = [
    'OllamaManager',
    'TransformersManager', 
    'PromptTemplate',
    'PromptTemplateManager'
]