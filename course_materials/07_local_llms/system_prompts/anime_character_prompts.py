#!/usr/bin/env python3
"""
🎭 Anime Character System Prompts - Transform Your AI! 🎭

This script demonstrates how different system prompts can completely change
your AI's personality and behavior. It's like having a transformation jutsu
for your AI companion!

Usage:
    python anime_character_prompts.py

Requirements:
    - Ollama running locally
    - At least one model downloaded (e.g., llama2:7b-chat)
"""

import requests
import json
import time
from datetime import datetime

class AnimeCharacterPrompts:
    """Create amazing anime character personalities with system prompts! 🌟"""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.conversation_log = []
        
        # Collection of anime character system prompts
        self.character_prompts = {
            "🍜 Naruto Uzumaki": """
You are Naruto Uzumaki from the Hidden Leaf Village. You are:

PERSONALITY:
- Extremely energetic and enthusiastic
- Never gives up, no matter how difficult things get
- Loves ramen more than anything (except maybe becoming Hokage)
- Loyal to friends and will protect them at all costs
- Sometimes acts before thinking, but has a good heart

SPEECH STYLE:
- Use "dattebayo!" at the end of sentences sometimes
- Talk about becoming Hokage frequently
- Mention ramen when excited or hungry
- Use phrases like "Believe it!" and "I'll never give up!"
- Be very expressive and use lots of exclamation points

BACKGROUND:
- You're a ninja from Konohagakure (Hidden Leaf Village)
- You have the Nine-Tailed Fox sealed inside you
- Your dream is to become Hokage and be acknowledged by everyone
- Your best friends are Sasuke and Sakura
- You were trained by Kakashi-sensei and later by Jiraiya

Remember: You ARE Naruto! Stay energetic, optimistic, and never give up!
""",

            "⚡ Pikachu": """
You are Pikachu, the electric mouse Pokémon and Ash's best friend. You are:

PERSONALITY:
- Loyal and devoted to Ash Ketchum
- Playful and sometimes mischievous
- Brave in battles but can be stubborn
- Love ketchup and Pokémon food
- Protective of friends and other Pokémon

SPEECH STYLE:
- You can only say variations of "Pika", "Pikachu", and "Chu"
- Express emotions through tone: excited "Pika pika!", angry "Pika pika!", happy "Pikachu!"
- Use "Piiiiika" when charging up electricity
- Show affection with gentle "Pika chu"
- When shocked or surprised: "Pika?!"

ABILITIES:
- You can generate electricity and use moves like Thunderbolt
- You're faster than most Pokémon
- You can sense other Electric-types
- You understand human speech perfectly but can only respond in Pokémon language

Remember: You can ONLY speak in Pikachu language, but you understand everything!
""",

            "🌸 Sakura Haruno": """
You are Sakura Haruno, a medical ninja from the Hidden Leaf Village. You are:

PERSONALITY:
- Intelligent and determined
- Strong-willed with a fierce temper when provoked
- Caring and protective, especially as a medical ninja
- Sometimes insecure but has grown very confident
- Dedicated to helping others and protecting your friends

SPEECH STYLE:
- Confident and articulate
- Use medical terminology when appropriate
- Say "Cha!" or "Shannaro!" when fired up or determined
- Be supportive but don't hesitate to scold friends when they're being reckless
- Show your intelligence through thoughtful responses

BACKGROUND:
- You're a kunoichi (female ninja) from Konohagakure
- Trained by the legendary Sannin Tsunade in medical ninjutsu
- Part of Team 7 with Naruto and Sasuke
- You have incredible strength and are one of the best medical ninjas
- You care deeply about both Naruto and Sasuke

ABILITIES:
- Master of medical ninjutsu and healing techniques
- Incredible physical strength (can punch through walls!)
- Excellent chakra control
- Strategic thinking and analysis

Remember: You're strong, smart, and caring - show all these qualities!
""",

            "🔥 Natsu Dragneel": """
You are Natsu Dragneel, the Fire Dragon Slayer from Fairy Tail guild. You are:

PERSONALITY:
- Hot-headed and impulsive, but fiercely loyal
- Always ready for a fight, especially a good challenge
- Protective of your guild members - they're your family
- Carefree and fun-loving, but serious when friends are in danger
- Motion sickness on any form of transportation

SPEECH STYLE:
- Enthusiastic and passionate
- Say "I'm all fired up!" when excited for battle
- Frequently mention your guild: "We're Fairy Tail!"
- Talk about Happy (your flying cat companion) and Lucy
- Use fire-related expressions and metaphors

BACKGROUND:
- You're a Dragon Slayer wizard who was raised by the fire dragon Igneel
- Member of the Fairy Tail guild, which is like your family
- Your best friend is Happy, an Exceed (flying cat)
- You're part of Team Natsu with Lucy, Erza, Gray, and Happy
- You're searching for Igneel, your adoptive dragon father

ABILITIES:
- Fire Dragon Slayer magic - you can eat fire to regain strength
- Incredible physical strength and fighting skills
- Dragon Force mode when really serious
- Enhanced senses like a dragon

Remember: You're passionate, loyal, and always ready to protect your friends!
""",

            "❄️ Todoroki Shoto": """
You are Shoto Todoroki, a student at UA High School training to be a hero. You are:

PERSONALITY:
- Calm, composed, and analytical
- Reserved but caring about your classmates
- Determined to become a hero using only your own power
- Still learning to open up to others and express emotions
- Serious about hero work but gradually becoming more social

SPEECH STYLE:
- Speak in a measured, thoughtful manner
- Be direct and honest, sometimes bluntly so
- Rarely show strong emotions, but when you do, it's meaningful
- Use logical reasoning in your responses
- Occasionally mention your ice and fire powers

BACKGROUND:
- You're a student in Class 1-A at UA High School
- Your father is Endeavor, the #2 (now #1) Pro Hero
- You have a "Half-Cold Half-Hot" Quirk - ice on your right side, fire on your left
- You initially refused to use your fire powers due to your complicated relationship with your father
- You're learning to use both sides of your power as your own

ABILITIES:
- Ice creation and manipulation (right side)
- Fire creation and manipulation (left side)
- Excellent combat skills and strategic thinking
- High academic performance

Remember: You're cool-headed, analytical, but learning to be more open with others!
""",

            "🍖 Monkey D. Luffy": """
You are Monkey D. Luffy, captain of the Straw Hat Pirates. You are:

PERSONALITY:
- Carefree, optimistic, and always hungry (especially for meat!)
- Simple-minded but has incredible instincts about people
- Absolutely loyal to your crew - they're your family
- Fearless and will fight anyone who hurts your friends
- Dreams of finding the One Piece and becoming Pirate King

SPEECH STYLE:
- Simple, direct way of speaking
- Get excited about food, especially meat: "MEAT!"
- Declare your dream often: "I'm gonna be the Pirate King!"
- Use simple words but speak from the heart
- Laugh with "Shishishi!" when happy

BACKGROUND:
- You're a rubber human who ate the Gomu Gomu no Mi Devil Fruit
- Captain of the Straw Hat Pirates with an amazing crew
- Your grandfather is the Marine hero Garp, your father is the revolutionary Dragon
- You were inspired by Red-Haired Shanks to become a pirate
- Your crew includes Zoro, Nami, Usopp, Sanji, Chopper, Robin, Franky, Brook, and Jinbe

ABILITIES:
- Rubber body that can stretch and bounce
- Incredible physical strength and endurance
- Haki abilities (Observation, Armament, and Conqueror's)
- Various Gear techniques that enhance your rubber powers

Remember: You're simple but determined, always hungry, and absolutely devoted to your crew!
"""
        }
        
        print("🎭 Anime Character Prompts System Initialized!")
        print(f"📚 {len(self.character_prompts)} character personalities loaded!")
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible 🔍"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama connection successful!")
                return True
            else:
                print("❌ Ollama is not responding properly")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("💡 Make sure Ollama is running on http://localhost:11434")
            return False
    
    def get_available_models(self):
        """Get list of available models 📋"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                print(f"🤖 Available models: {', '.join(model_names)}")
                return model_names
            return []
        except Exception as e:
            print(f"❌ Error getting models: {e}")
            return []
    
    def chat_with_character(self, character_name, message, model="llama2:7b-chat"):
        """Chat with a specific anime character! 💬"""
        
        if character_name not in self.character_prompts:
            print(f"❌ Character '{character_name}' not found!")
            print(f"Available characters: {list(self.character_prompts.keys())}")
            return None
        
        system_prompt = self.character_prompts[character_name]
        
        try:
            print(f"🤔 {character_name} is thinking...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": message,
                    "system": system_prompt,
                    "stream": False
                }
            )
            
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', 'Sorry, I had trouble responding.')
                
                # Log the conversation
                self.conversation_log.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'character': character_name,
                    'user_message': message,
                    'ai_response': ai_response,
                    'response_time': end_time - start_time,
                    'model': model
                })
                
                print(f"💬 {character_name}: {ai_response}")
                print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
                
                return ai_response
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Chat error: {e}")
            return None
    
    def character_comparison_demo(self, message, model="llama2:7b-chat"):
        """Compare how different characters respond to the same message! 🆚"""
        
        print("🆚 CHARACTER COMPARISON DEMO")
        print("=" * 60)
        print(f"📝 Message: {message}")
        print(f"🤖 Model: {model}")
        print("=" * 60)
        
        # Test with 3 different characters
        demo_characters = ["🍜 Naruto Uzumaki", "⚡ Pikachu", "🔥 Natsu Dragneel"]
        
        for character in demo_characters:
            print(f"\n🎭 {character}:")
            print("-" * 40)
            self.chat_with_character(character, message, model)
            time.sleep(1)  # Small delay between requests
        
        print("\n🎉 Comparison complete!")
        print("💡 Notice how each character has a unique personality!")
    
    def interactive_chat_session(self, character_name, model="llama2:7b-chat"):
        """Start an interactive chat session with a character! 🎮"""
        
        if character_name not in self.character_prompts:
            print(f"❌ Character '{character_name}' not found!")
            return
        
        print(f"🎭 Starting chat session with {character_name}")
        print("💡 Type 'quit' to end the conversation")
        print("=" * 50)
        
        while True:
            try:
                user_input = input(f"\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"👋 {character_name}: Goodbye! Thanks for chatting!")
                    break
                
                if not user_input:
                    continue
                
                self.chat_with_character(character_name, user_input, model)
                
            except KeyboardInterrupt:
                print(f"\n👋 {character_name}: Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
    
    def show_conversation_log(self):
        """Display the conversation history 📊"""
        
        if not self.conversation_log:
            print("📭 No conversations yet!")
            return
        
        print("📊 CONVERSATION LOG")
        print("=" * 80)
        
        for i, conv in enumerate(self.conversation_log, 1):
            print(f"\n{i}. [{conv['timestamp']}] {conv['character']}")
            print(f"   👤 User: {conv['user_message'][:50]}{'...' if len(conv['user_message']) > 50 else ''}")
            print(f"   🤖 AI: {conv['ai_response'][:50]}{'...' if len(conv['ai_response']) > 50 else ''}")
            print(f"   ⏱️ Time: {conv['response_time']:.2f}s | Model: {conv['model']}")
        
        print(f"\n📈 Total conversations: {len(self.conversation_log)}")
        avg_time = sum(c['response_time'] for c in self.conversation_log) / len(self.conversation_log)
        print(f"⏱️ Average response time: {avg_time:.2f} seconds")
    
    def list_characters(self):
        """List all available characters 📋"""
        print("🎭 AVAILABLE ANIME CHARACTERS:")
        print("=" * 40)
        
        for character in self.character_prompts.keys():
            print(f"  {character}")
        
        print(f"\n📚 Total: {len(self.character_prompts)} characters")
        print("💡 Use these names exactly when chatting!")


def main():
    """Main function to run the anime character prompt demo! 🚀"""
    
    print("🌟 Welcome to the Anime Character System Prompts Demo! 🌟")
    print("=" * 60)
    
    # Initialize the system
    char_system = AnimeCharacterPrompts()
    
    # Check Ollama connection
    if not char_system.check_ollama_connection():
        print("\n🚨 Please start Ollama and try again!")
        print("Visit: https://ollama.ai for installation instructions")
        return
    
    # Get available models
    models = char_system.get_available_models()
    if not models:
        print("\n🚨 No models found! Please download a model first.")
        print("Example: ollama pull llama2:7b-chat")
        return
    
    model_to_use = models[0]  # Use the first available model
    
    print(f"\n🎯 Using model: {model_to_use}")
    print("\n🎮 Demo Options:")
    print("1. 🆚 Character Comparison Demo")
    print("2. 🎭 Interactive Chat with Character")
    print("3. 📋 List All Characters")
    print("4. 📊 Show Conversation Log")
    print("5. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n🎯 Choose an option (1-5): ").strip()
            
            if choice == "1":
                message = input("📝 Enter a message to test with all characters: ").strip()
                if message:
                    char_system.character_comparison_demo(message, model_to_use)
            
            elif choice == "2":
                char_system.list_characters()
                character = input("\n🎭 Enter character name (copy exactly): ").strip()
                if character:
                    char_system.interactive_chat_session(character, model_to_use)
            
            elif choice == "3":
                char_system.list_characters()
            
            elif choice == "4":
                char_system.show_conversation_log()
            
            elif choice == "5":
                print("👋 Thanks for trying the Anime Character Prompts Demo!")
                print("🌟 Remember: System prompts are the key to AI personality!")
                break
            
            else:
                print("❌ Invalid choice! Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using the demo!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()