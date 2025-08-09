#!/usr/bin/env python3
"""
Interactive Prompt Experimentation Scripts

This module provides interactive scripts for experimenting with different prompt
techniques, demonstrating how various prompting strategies affect LLM behavior.
"""

import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import random


class PromptTechnique(Enum):
    """Different prompting techniques"""
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    ROLE_PLAYING = "role_playing"
    CONSTRAINT_BASED = "constraint_based"
    ITERATIVE_REFINEMENT = "iterative_refinement"


@dataclass
class ExperimentResult:
    """Results from a prompt experiment"""
    technique: PromptTechnique
    prompt: str
    expected_behavior: str
    sample_response: str
    effectiveness_score: float
    notes: str


class PromptExperimentFramework:
    """Framework for conducting prompt experiments"""
    
    def __init__(self):
        self.experiments = []
        self.results = []
    
    def run_experiment(self, technique: PromptTechnique, prompt: str, 
                      expected_behavior: str, sample_response: str = None) -> ExperimentResult:
        """Run a single prompt experiment"""
        # In a real implementation, this would call an actual LLM
        # For demonstration, we'll use predefined sample responses
        
        if sample_response is None:
            sample_response = self._generate_sample_response(technique, prompt)
        
        effectiveness_score = self._evaluate_effectiveness(technique, prompt, sample_response)
        
        result = ExperimentResult(
            technique=technique,
            prompt=prompt,
            expected_behavior=expected_behavior,
            sample_response=sample_response,
            effectiveness_score=effectiveness_score,
            notes=self._generate_notes(technique, effectiveness_score)
        )
        
        self.results.append(result)
        return result
    
    def _generate_sample_response(self, technique: PromptTechnique, prompt: str) -> str:
        """Generate sample responses for demonstration purposes"""
        responses = {
            PromptTechnique.ZERO_SHOT: "Direct response based on the prompt without examples.",
            PromptTechnique.FEW_SHOT: "Response that follows the pattern established by the examples.",
            PromptTechnique.CHAIN_OF_THOUGHT: "Step-by-step reasoning: First... Then... Therefore...",
            PromptTechnique.ROLE_PLAYING: "Response in character, matching the specified role and expertise.",
            PromptTechnique.CONSTRAINT_BASED: "Response that carefully adheres to all specified constraints.",
            PromptTechnique.ITERATIVE_REFINEMENT: "Improved response after multiple iterations and feedback."
        }
        return responses.get(technique, "Sample response for demonstration.")
    
    def _evaluate_effectiveness(self, technique: PromptTechnique, prompt: str, response: str) -> float:
        """Evaluate the effectiveness of a prompt technique (simplified for demo)"""
        # In practice, this would involve more sophisticated evaluation
        base_scores = {
            PromptTechnique.ZERO_SHOT: 0.7,
            PromptTechnique.FEW_SHOT: 0.85,
            PromptTechnique.CHAIN_OF_THOUGHT: 0.9,
            PromptTechnique.ROLE_PLAYING: 0.8,
            PromptTechnique.CONSTRAINT_BASED: 0.75,
            PromptTechnique.ITERATIVE_REFINEMENT: 0.95
        }
        return base_scores.get(technique, 0.5) + random.uniform(-0.1, 0.1)
    
    def _generate_notes(self, technique: PromptTechnique, score: float) -> str:
        """Generate notes about the experiment results"""
        if score > 0.9:
            return "Excellent results - technique highly effective for this use case."
        elif score > 0.8:
            return "Good results - technique works well with minor room for improvement."
        elif score > 0.7:
            return "Moderate results - technique is functional but could be optimized."
        else:
            return "Poor results - consider alternative techniques or prompt refinement."


class ZeroShotExperiments:
    """Zero-shot prompting experiments"""
    
    @staticmethod
    def basic_zero_shot():
        """Demonstrate basic zero-shot prompting"""
        experiments = [
            {
                "name": "Code Generation",
                "prompt": "Write a Python function that calculates the factorial of a number.",
                "expected": "Direct code generation without examples",
                "sample_response": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)"""
            },
            {
                "name": "Text Analysis",
                "prompt": "Analyze the sentiment of this text: 'I love this new feature!'",
                "expected": "Sentiment classification without training examples",
                "sample_response": "The sentiment of this text is positive. The use of 'love' indicates strong positive emotion toward the feature."
            },
            {
                "name": "Problem Solving",
                "prompt": "How would you optimize a slow database query?",
                "expected": "General optimization advice without specific context",
                "sample_response": """To optimize a slow database query:
1. Add appropriate indexes
2. Analyze the query execution plan
3. Avoid SELECT * statements
4. Use LIMIT when appropriate
5. Consider query restructuring"""
            }
        ]
        
        return experiments
    
    @staticmethod
    def demonstrate_zero_shot():
        """Demonstrate zero-shot prompting techniques"""
        print("=== Zero-Shot Prompting Experiments ===\n")
        
        experiments = ZeroShotExperiments.basic_zero_shot()
        framework = PromptExperimentFramework()
        
        for exp in experiments:
            print(f"Experiment: {exp['name']}")
            print(f"Prompt: {exp['prompt']}")
            print(f"Expected Behavior: {exp['expected']}")
            
            result = framework.run_experiment(
                PromptTechnique.ZERO_SHOT,
                exp['prompt'],
                exp['expected'],
                exp['sample_response']
            )
            
            print(f"Sample Response: {result.sample_response}")
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("-" * 50)


class FewShotExperiments:
    """Few-shot learning experiments"""
    
    @staticmethod
    def create_few_shot_prompt(task_description: str, examples: List[Tuple[str, str]], 
                              new_input: str) -> str:
        """Create a few-shot prompt with examples"""
        prompt = f"{task_description}\n\n"
        
        for i, (input_ex, output_ex) in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Input: {input_ex}\n"
            prompt += f"Output: {output_ex}\n\n"
        
        prompt += f"Now apply the same pattern:\n"
        prompt += f"Input: {new_input}\n"
        prompt += f"Output:"
        
        return prompt
    
    @staticmethod
    def code_pattern_learning():
        """Demonstrate few-shot learning for code patterns"""
        examples = [
            ("Create a list of numbers from 1 to 5", "numbers = list(range(1, 6))"),
            ("Create a list of even numbers from 2 to 10", "even_numbers = list(range(2, 11, 2))"),
            ("Create a list of squares from 1 to 4", "squares = [i**2 for i in range(1, 5)]")
        ]
        
        prompt = FewShotExperiments.create_few_shot_prompt(
            "Convert natural language descriptions to Python list comprehensions or range functions:",
            examples,
            "Create a list of odd numbers from 1 to 9"
        )
        
        expected_response = "odd_numbers = list(range(1, 10, 2))"
        
        return {
            "name": "Code Pattern Learning",
            "prompt": prompt,
            "expected": "Learn the pattern from examples and apply to new case",
            "sample_response": expected_response
        }
    
    @staticmethod
    def text_classification():
        """Demonstrate few-shot text classification"""
        examples = [
            ("The movie was absolutely fantastic!", "Positive"),
            ("I hated every minute of it.", "Negative"),
            ("It was okay, nothing special.", "Neutral")
        ]
        
        prompt = FewShotExperiments.create_few_shot_prompt(
            "Classify the sentiment of movie reviews:",
            examples,
            "The film exceeded all my expectations!"
        )
        
        return {
            "name": "Sentiment Classification",
            "prompt": prompt,
            "expected": "Classify sentiment based on learned patterns",
            "sample_response": "Positive"
        }
    
    @staticmethod
    def demonstrate_few_shot():
        """Demonstrate few-shot learning techniques"""
        print("=== Few-Shot Learning Experiments ===\n")
        
        experiments = [
            FewShotExperiments.code_pattern_learning(),
            FewShotExperiments.text_classification()
        ]
        
        framework = PromptExperimentFramework()
        
        for exp in experiments:
            print(f"Experiment: {exp['name']}")
            print(f"Prompt:\n{exp['prompt']}")
            print(f"\nExpected Behavior: {exp['expected']}")
            
            result = framework.run_experiment(
                PromptTechnique.FEW_SHOT,
                exp['prompt'],
                exp['expected'],
                exp['sample_response']
            )
            
            print(f"Sample Response: {result.sample_response}")
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("=" * 60)


class ChainOfThoughtExperiments:
    """Chain-of-thought prompting experiments"""
    
    @staticmethod
    def mathematical_reasoning():
        """Demonstrate chain-of-thought for mathematical problems"""
        prompt = """Solve this step by step:

Problem: A store has 24 apples. They sell 3/8 of them in the morning and 1/4 of the remaining apples in the afternoon. How many apples are left?

Let me work through this step by step:

Step 1: Calculate how many apples were sold in the morning
- 3/8 of 24 apples = (3/8) × 24 = 9 apples

Step 2: Calculate how many apples remain after the morning
- 24 - 9 = 15 apples remaining

Step 3: Calculate how many apples were sold in the afternoon
- 1/4 of the remaining 15 apples = (1/4) × 15 = 3.75 ≈ 4 apples (rounding up)

Step 4: Calculate final remaining apples
- 15 - 4 = 11 apples left

Therefore, there are 11 apples left at the end of the day."""
        
        return {
            "name": "Mathematical Reasoning",
            "prompt": prompt,
            "expected": "Step-by-step mathematical problem solving",
            "sample_response": "The model breaks down the problem into clear steps, showing all calculations and reasoning."
        }
    
    @staticmethod
    def debugging_process():
        """Demonstrate chain-of-thought for debugging"""
        prompt = """Debug this Python code step by step:

```python
def find_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test case that fails
result = find_average([])
print(result)
```

Let me debug this step by step:

Step 1: Identify the error
- The code throws a ZeroDivisionError when an empty list is passed

Step 2: Analyze why this happens
- When numbers = [], len(numbers) = 0
- Division by zero occurs in the return statement: total / 0

Step 3: Determine the expected behavior
- Should we return 0, None, or raise a meaningful error for empty lists?

Step 4: Implement the fix
```python
def find_average(numbers):
    if not numbers:  # Check for empty list
        return 0  # or raise ValueError("Cannot calculate average of empty list")
    
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

Step 5: Test the fix
- find_average([]) now returns 0 instead of crashing
- find_average([1, 2, 3]) still returns 2.0 as expected"""
        
        return {
            "name": "Code Debugging Process",
            "prompt": prompt,
            "expected": "Systematic debugging with clear reasoning steps",
            "sample_response": "The model identifies the issue, explains the cause, and provides a step-by-step solution."
        }
    
    @staticmethod
    def demonstrate_chain_of_thought():
        """Demonstrate chain-of-thought prompting"""
        print("=== Chain-of-Thought Prompting Experiments ===\n")
        
        experiments = [
            ChainOfThoughtExperiments.mathematical_reasoning(),
            ChainOfThoughtExperiments.debugging_process()
        ]
        
        framework = PromptExperimentFramework()
        
        for exp in experiments:
            print(f"Experiment: {exp['name']}")
            print(f"Expected Behavior: {exp['expected']}")
            print(f"Sample Response: {exp['sample_response']}")
            
            result = framework.run_experiment(
                PromptTechnique.CHAIN_OF_THOUGHT,
                exp['prompt'],
                exp['expected'],
                exp['sample_response']
            )
            
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("=" * 60)


class RolePlayingExperiments:
    """Role-playing prompt experiments"""
    
    @staticmethod
    def expert_consultant():
        """Demonstrate role-playing as different experts"""
        roles = [
            {
                "role": "Senior Python Developer",
                "prompt": """You are a senior Python developer with 10 years of experience in web development and data science. You're known for writing clean, efficient code and mentoring junior developers.

Task: Review this code and provide feedback:

```python
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
```

Provide your expert feedback:""",
                "expected_response": """As a senior developer, I see several areas for improvement:

1. **Function naming**: The name 'process_data' is too generic. Consider 'double_positive_numbers' or similar.

2. **Type hints**: Add type annotations for better code documentation:
   ```python
   def double_positive_numbers(data: List[float]) -> List[float]:
   ```

3. **List comprehension**: This can be more Pythonic:
   ```python
   return [item * 2 for item in data if item > 0]
   ```

4. **Input validation**: Consider handling edge cases like empty lists or non-numeric data.

5. **Documentation**: Add a docstring explaining the function's purpose and parameters."""
            },
            {
                "role": "Creative Writing Coach",
                "prompt": """You are an experienced creative writing coach who has helped hundreds of writers improve their craft. You're encouraging but provide specific, actionable feedback.

Task: Help improve this opening paragraph:

"It was a dark and stormy night. John walked down the street. He was scared."

Provide your coaching feedback:""",
                "expected_response": """I appreciate you sharing your opening! Let's work together to make it more engaging:

**Strengths**: You've established atmosphere and character emotion quickly.

**Areas to develop**:
1. **Show, don't tell**: Instead of "He was scared," show us through his actions: "John's hands trembled as he pulled his coat tighter."

2. **Sensory details**: Add what John experiences: "Rain lashed against his face" or "His footsteps echoed off empty storefronts."

3. **Fresh opening**: The "dark and stormy night" opening is famously overused. Try something more original.

**Revision suggestion**:
"Rain hammered the empty street as John hurried past darkened shop windows, his breath forming quick puffs in the cold air. Every shadow seemed to shift, every sound made him glance over his shoulder."

This shows his fear through physical reactions and creates atmosphere without clichés."""
            }
        ]
        
        return roles
    
    @staticmethod
    def demonstrate_role_playing():
        """Demonstrate role-playing experiments"""
        print("=== Role-Playing Prompt Experiments ===\n")
        
        roles = RolePlayingExperiments.expert_consultant()
        framework = PromptExperimentFramework()
        
        for role_data in roles:
            print(f"Role: {role_data['role']}")
            print(f"Prompt: {role_data['prompt']}")
            print(f"Expected Response Style: Professional expertise with specific feedback")
            
            result = framework.run_experiment(
                PromptTechnique.ROLE_PLAYING,
                role_data['prompt'],
                f"Response as {role_data['role']} with appropriate expertise",
                role_data['expected_response']
            )
            
            print(f"Sample Response: {result.sample_response[:200]}...")
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("=" * 60)


class ConstraintBasedExperiments:
    """Constraint-based prompting experiments"""
    
    @staticmethod
    def format_constraints():
        """Demonstrate format-based constraints"""
        constraints = [
            {
                "name": "JSON Output Constraint",
                "prompt": """Generate a Python function description with these EXACT constraints:
- Output must be valid JSON
- Must include: name, parameters, return_type, description, example
- Description must be exactly 20 words
- Example must be executable Python code

Function to describe: A function that calculates compound interest""",
                "expected_response": """{
  "name": "calculate_compound_interest",
  "parameters": ["principal", "rate", "time", "compounds_per_year"],
  "return_type": "float",
  "description": "Calculates compound interest using principal amount, annual interest rate, time period, and compounding frequency per year.",
  "example": "calculate_compound_interest(1000, 0.05, 2, 4)"
}"""
            },
            {
                "name": "Length and Style Constraints",
                "prompt": """Write a product description with these constraints:
- Exactly 50 words
- Must include the words: "innovative", "efficient", "user-friendly"
- Written in second person ("you")
- No exclamation marks
- Must end with a question

Product: A new code editor for Python developers""",
                "expected_response": """You'll love this innovative Python code editor designed for modern developers. Its efficient syntax highlighting and user-friendly interface streamline your coding workflow. Advanced debugging tools and intelligent autocomplete features help you write better code faster. Smart project management keeps your files organized and accessible. Ready to boost your productivity?"""
            }
        ]
        
        return constraints
    
    @staticmethod
    def demonstrate_constraint_based():
        """Demonstrate constraint-based prompting"""
        print("=== Constraint-Based Prompting Experiments ===\n")
        
        constraints = ConstraintBasedExperiments.format_constraints()
        framework = PromptExperimentFramework()
        
        for constraint in constraints:
            print(f"Experiment: {constraint['name']}")
            print(f"Prompt: {constraint['prompt']}")
            print(f"Expected: Response following all specified constraints")
            
            result = framework.run_experiment(
                PromptTechnique.CONSTRAINT_BASED,
                constraint['prompt'],
                "Response adhering to all constraints",
                constraint['expected_response']
            )
            
            print(f"Sample Response: {result.sample_response}")
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("=" * 60)


class IterativeRefinementExperiments:
    """Iterative refinement experiments"""
    
    @staticmethod
    def code_improvement_iterations():
        """Demonstrate iterative code improvement"""
        iterations = [
            {
                "iteration": 1,
                "prompt": "Write a function to find the maximum number in a list",
                "response": """def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num""",
                "feedback": "Good start, but what if the list is empty? Also consider using built-in functions."
            },
            {
                "iteration": 2,
                "prompt": "Improve the function to handle edge cases and be more Pythonic",
                "response": """def find_max(numbers):
    if not numbers:
        raise ValueError("Cannot find maximum of empty list")
    return max(numbers)""",
                "feedback": "Much better! Now add type hints and documentation."
            },
            {
                "iteration": 3,
                "prompt": "Add type hints, documentation, and consider optional default behavior",
                "response": """from typing import List, Union, Optional

def find_max(numbers: List[Union[int, float]], 
             default: Optional[Union[int, float]] = None) -> Union[int, float]:
    \"\"\"
    Find the maximum number in a list.
    
    Args:
        numbers: List of numbers to search
        default: Value to return if list is empty (if None, raises ValueError)
    
    Returns:
        The maximum number in the list
        
    Raises:
        ValueError: If list is empty and no default provided
        
    Example:
        >>> find_max([1, 3, 2])
        3
        >>> find_max([], default=0)
        0
    \"\"\"
    if not numbers:
        if default is not None:
            return default
        raise ValueError("Cannot find maximum of empty list")
    return max(numbers)""",
                "feedback": "Excellent! This is production-ready code with proper error handling, documentation, and flexibility."
            }
        ]
        
        return iterations
    
    @staticmethod
    def demonstrate_iterative_refinement():
        """Demonstrate iterative refinement process"""
        print("=== Iterative Refinement Experiments ===\n")
        
        iterations = IterativeRefinementExperiments.code_improvement_iterations()
        framework = PromptExperimentFramework()
        
        print("Demonstrating iterative improvement of a simple function:\n")
        
        for iteration_data in iterations:
            print(f"Iteration {iteration_data['iteration']}:")
            print(f"Prompt: {iteration_data['prompt']}")
            print(f"Response:\n{iteration_data['response']}")
            print(f"Feedback: {iteration_data['feedback']}")
            
            result = framework.run_experiment(
                PromptTechnique.ITERATIVE_REFINEMENT,
                iteration_data['prompt'],
                "Improved code based on feedback",
                iteration_data['response']
            )
            
            print(f"Effectiveness Score: {result.effectiveness_score:.2f}")
            print("-" * 50)


class InteractivePromptLab:
    """Interactive laboratory for prompt experimentation"""
    
    def __init__(self):
        self.framework = PromptExperimentFramework()
        self.session_results = []
    
    def run_comparison_experiment(self, task: str, techniques: List[PromptTechnique]):
        """Compare different techniques on the same task"""
        print(f"=== Comparing Techniques for: {task} ===\n")
        
        results = []
        for technique in techniques:
            prompt = self._create_prompt_for_technique(task, technique)
            result = self.framework.run_experiment(
                technique, prompt, f"Complete task: {task}"
            )
            results.append(result)
            
            print(f"Technique: {technique.value}")
            print(f"Effectiveness: {result.effectiveness_score:.2f}")
            print(f"Notes: {result.notes}")
            print("-" * 40)
        
        # Find best technique
        best_result = max(results, key=lambda r: r.effectiveness_score)
        print(f"\nBest technique for this task: {best_result.technique.value}")
        print(f"Score: {best_result.effectiveness_score:.2f}")
        
        return results
    
    def _create_prompt_for_technique(self, task: str, technique: PromptTechnique) -> str:
        """Create appropriate prompt based on technique"""
        base_prompts = {
            PromptTechnique.ZERO_SHOT: f"Complete this task: {task}",
            PromptTechnique.FEW_SHOT: f"Here are examples of similar tasks:\n[Examples would go here]\n\nNow complete: {task}",
            PromptTechnique.CHAIN_OF_THOUGHT: f"Think step by step to complete this task: {task}",
            PromptTechnique.ROLE_PLAYING: f"As an expert in this domain, complete this task: {task}",
            PromptTechnique.CONSTRAINT_BASED: f"Complete this task with specific constraints: {task}",
            PromptTechnique.ITERATIVE_REFINEMENT: f"Complete this task, then improve your solution: {task}"
        }
        return base_prompts.get(technique, f"Complete this task: {task}")
    
    def demonstrate_behavior_changes(self):
        """Demonstrate how different prompts change behavior"""
        print("=== Demonstrating Behavior Changes ===\n")
        
        task = "Explain how to sort a list in Python"
        techniques = [
            PromptTechnique.ZERO_SHOT,
            PromptTechnique.FEW_SHOT,
            PromptTechnique.CHAIN_OF_THOUGHT,
            PromptTechnique.ROLE_PLAYING
        ]
        
        results = self.run_comparison_experiment(task, techniques)
        
        print("\nKey Observations:")
        print("- Zero-shot gives direct answers")
        print("- Few-shot follows learned patterns")
        print("- Chain-of-thought shows reasoning")
        print("- Role-playing adds expertise context")
        
        return results


def main():
    """Main demonstration function"""
    print("🧪 Interactive Prompt Experimentation Lab 🧪\n")
    print("This script demonstrates various prompt engineering techniques")
    print("and how they affect LLM behavior.\n")
    
    # Run all demonstrations
    ZeroShotExperiments.demonstrate_zero_shot()
    print("\n" + "="*80 + "\n")
    
    FewShotExperiments.demonstrate_few_shot()
    print("\n" + "="*80 + "\n")
    
    ChainOfThoughtExperiments.demonstrate_chain_of_thought()
    print("\n" + "="*80 + "\n")
    
    RolePlayingExperiments.demonstrate_role_playing()
    print("\n" + "="*80 + "\n")
    
    ConstraintBasedExperiments.demonstrate_constraint_based()
    print("\n" + "="*80 + "\n")
    
    IterativeRefinementExperiments.demonstrate_iterative_refinement()
    print("\n" + "="*80 + "\n")
    
    # Interactive comparison
    lab = InteractivePromptLab()
    lab.demonstrate_behavior_changes()
    
    print("\n🎯 Experiment Complete!")
    print("Key Takeaways:")
    print("1. Different techniques work better for different tasks")
    print("2. Few-shot learning improves consistency")
    print("3. Chain-of-thought enhances reasoning")
    print("4. Role-playing adds domain expertise")
    print("5. Constraints ensure specific output formats")
    print("6. Iteration leads to better results")


if __name__ == "__main__":
    main()