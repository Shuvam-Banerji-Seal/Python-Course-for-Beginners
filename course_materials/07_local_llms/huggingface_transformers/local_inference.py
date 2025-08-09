#!/usr/bin/env python3
"""
Hugging Face Transformers - Basic Model Loading and Inference Examples

This script demonstrates how to load and use various types of models
for local inference using Hugging Face Transformers.

Requirements: 2.1, 2.3
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification,
    pipeline, GPT2LMHeadModel, GPT2Tokenizer
)
import warnings
warnings.filterwarnings("ignore")


class TransformersManager:
    """
    A utility class for managing Hugging Face Transformers models
    """
    
    def __init__(self, model_name: str, device: str = "auto"):
        """
        Initialize the TransformersManager
        
        Args:
            model_name: Name of the model to load
            device: Device to use ('auto', 'cpu', 'cuda')
        """
        self.model_name = model_name
        self.device = self._get_device(device)
        self.tokenizer = None
        self.model = None
        
    def _get_device(self, device: str) -> str:
        """Determine the best device to use"""
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device
    
    def load_model(self, quantization: bool = False):
        """
        Load model with optional quantization
        
        Args:
            quantization: Whether to use 8-bit quantization
        """
        print(f"Loading model: {self.model_name}")
        print(f"Device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            if quantization and self.device == "cuda":
                print("Loading with 8-bit quantization...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    load_in_8bit=True,
                    device_map="auto"
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                self.model.to(self.device)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def generate_text(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        """
        Generate text using the loaded model
        
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Tokenize input
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        # Generate text
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text


def demo_basic_inference():
    """Demonstrate basic text generation"""
    print("=== Basic Text Generation Demo ===")
    
    # Use a small model for demonstration
    model_name = "gpt2"  # Small model that works well for demos
    
    manager = TransformersManager(model_name)
    manager.load_model()
    
    prompts = [
        "The future of artificial intelligence is",
        "Python programming is great because",
        "Local language models allow us to"
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        generated = manager.generate_text(prompt, max_length=80)
        print(f"Generated: {generated}")
        print("-" * 50)


def demo_pipeline_usage():
    """Demonstrate using pre-built pipelines"""
    print("\n=== Pipeline Usage Demo ===")
    
    # Text generation pipeline
    print("1. Text Generation Pipeline:")
    generator = pipeline("text-generation", model="gpt2", device=0 if torch.cuda.is_available() else -1)
    
    result = generator(
        "The benefits of running models locally include",
        max_length=60,
        num_return_sequences=1,
        temperature=0.7
    )
    print(f"Generated: {result[0]['generated_text']}")
    
    # Sentiment analysis pipeline
    print("\n2. Sentiment Analysis Pipeline:")
    classifier = pipeline("sentiment-analysis")
    
    texts = [
        "I love using local language models!",
        "This setup process is quite complicated.",
        "The performance is surprisingly good."
    ]
    
    for text in texts:
        result = classifier(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result[0]['label']} (confidence: {result[0]['score']:.3f})")
    
    # Question answering pipeline
    print("\n3. Question Answering Pipeline:")
    qa_pipeline = pipeline("question-answering")
    
    context = """
    Hugging Face Transformers is a library that provides pre-trained models
    for natural language processing tasks. It supports PyTorch and TensorFlow
    frameworks and makes it easy to use state-of-the-art models for various
    applications including text generation, classification, and question answering.
    """
    
    questions = [
        "What frameworks does Transformers support?",
        "What can you do with Transformers?",
        "What is Hugging Face Transformers?"
    ]
    
    for question in questions:
        result = qa_pipeline(question=question, context=context)
        print(f"Q: {question}")
        print(f"A: {result['answer']} (confidence: {result['score']:.3f})")


def demo_model_comparison():
    """Compare different model sizes and types"""
    print("\n=== Model Comparison Demo ===")
    
    models = [
        ("distilgpt2", "Small, fast model"),
        ("gpt2", "Medium-sized model"),
        # ("gpt2-medium", "Larger model (uncomment if you have enough memory)")
    ]
    
    prompt = "Artificial intelligence will"
    
    for model_name, description in models:
        print(f"\nTesting {model_name} ({description}):")
        try:
            manager = TransformersManager(model_name)
            manager.load_model()
            
            import time
            start_time = time.time()
            result = manager.generate_text(prompt, max_length=50)
            end_time = time.time()
            
            print(f"Generated: {result}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            print(f"Error with {model_name}: {e}")


def demo_device_usage():
    """Demonstrate CPU vs GPU usage"""
    print("\n=== Device Usage Demo ===")
    
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name()}")
        print(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    model_name = "distilgpt2"
    prompt = "Local models are useful because"
    
    # Test CPU
    print("\nTesting on CPU:")
    try:
        manager_cpu = TransformersManager(model_name, device="cpu")
        manager_cpu.load_model()
        
        import time
        start_time = time.time()
        result_cpu = manager_cpu.generate_text(prompt, max_length=40)
        cpu_time = time.time() - start_time
        
        print(f"CPU Result: {result_cpu}")
        print(f"CPU Time: {cpu_time:.2f} seconds")
        
    except Exception as e:
        print(f"CPU test failed: {e}")
    
    # Test GPU if available
    if torch.cuda.is_available():
        print("\nTesting on GPU:")
        try:
            manager_gpu = TransformersManager(model_name, device="cuda")
            manager_gpu.load_model()
            
            start_time = time.time()
            result_gpu = manager_gpu.generate_text(prompt, max_length=40)
            gpu_time = time.time() - start_time
            
            print(f"GPU Result: {result_gpu}")
            print(f"GPU Time: {gpu_time:.2f} seconds")
            
            if 'cpu_time' in locals():
                speedup = cpu_time / gpu_time
                print(f"GPU Speedup: {speedup:.2f}x")
                
        except Exception as e:
            print(f"GPU test failed: {e}")


def main():
    """Run all demonstrations"""
    print("Hugging Face Transformers - Local Inference Examples")
    print("=" * 55)
    
    try:
        # Basic inference demo
        demo_basic_inference()
        
        # Pipeline usage demo
        demo_pipeline_usage()
        
        # Model comparison demo
        demo_model_comparison()
        
        # Device usage demo
        demo_device_usage()
        
        print("\n" + "=" * 55)
        print("All demos completed successfully!")
        print("\nNext steps:")
        print("- Try different models and prompts")
        print("- Experiment with generation parameters")
        print("- Check out memory_optimization.py for advanced techniques")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install transformers torch accelerate")


if __name__ == "__main__":
    main()