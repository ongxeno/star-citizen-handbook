#!/usr/bin/env python3
"""
Blog Cover Image Generator for Star Citizen Handbook

This script generates cover images for blog posts using the Gemini API.
It takes blog content as input, suggests image prompts, and generates images.

Usage:
    python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory"
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time
from PIL import Image
from io import BytesIO

# Import the genai utilities
from genai_utils import configure_genai, generate_image, get_project_paths

class BlogImageGenerator:
    """Generate cover images for Star Citizen Handbook blog posts"""
    
    def __init__(self):
        """Initialize the generator with API configuration"""
        try:
            # Get AI models
            self.models = configure_genai()
            
            # Project paths
            self.paths = get_project_paths()
            
            # Default image generation config
            self.image_configs = {
                "standard": {
                    "model_name": self.models["imagen_standard"]["model_name"],
                    "description": self.models["imagen_standard"]["description"]
                },
                "ultra": {
                    "model_name": self.models["imagen_ultra"]["model_name"],
                    "description": self.models["imagen_ultra"]["description"]
                },
                "legacy": {
                    "model_name": self.models["imagen_legacy"]["model_name"],
                    "description": self.models["imagen_legacy"]["description"]
                }
            }
            
            # Default settings
            self.current_model = "standard"
            self.number_of_images = 1
            self.aspect_ratio = "16:9"
            
            print("✅ Image generator initialized")
            
        except Exception as e:
            print(f"❌ Error initializing image generator: {e}")
            raise
    
    def generate_prompt_suggestions(self, content: str, num_suggestions: int = 3) -> List[str]:
        """
        Generate image prompt suggestions based on blog content
        
        Args:
            content (str): The blog post content
            num_suggestions (int): Number of prompt suggestions to generate
            
        Returns:
            List[str]: List of prompt suggestions
        """
        print(f"🧠 Generating {num_suggestions} image prompt suggestions...")
        
        try:
            # Create prompt for the AI
            system_prompt = """
            You are an expert image prompt creator for a blog about Star Citizen, a space simulation game.
            Given the content of a blog post, create compelling, detailed prompts for cover images.
            
            The prompts should be:
            1. Detailed and specific
            2. Visually interesting
            3. Relevant to the blog content
            4. Good for a 16:9 aspect ratio banner/hero image
            5. Include artistic style suggestions
            6. In English, even if the blog content is in another language
            
            Return EXACTLY {num_suggestions} distinct prompts as a JSON array of strings.
            Each prompt should be 1-3 sentences long and highly descriptive.
            DO NOT include any explanation or commentary - just the JSON array.
            """
            
            # Summarize content if it's very long
            content_summary = content
            if len(content) > 5000:
                # Create a summary first
                summary_prompt = f"Summarize this blog content in 500 words or less, focusing on the main topic and key points:\n\n{content[:5000]}..."
                summary_response = self.models["cost_effective"].generate_content(summary_prompt)
                content_summary = summary_response.text
            
            # Build the final prompt
            user_prompt = f"""
            Here's the blog content:
            
            {content_summary}
            
            Create {num_suggestions} distinct, detailed image prompts for a cover image that would work well with this blog post.
            """
            
            # Generate prompts using the deep research model
            response = self.models["deep_research"].generate_content([
                {"role": "system", "parts": [system_prompt]},
                {"role": "user", "parts": [user_prompt]}
            ])
            
            # Parse the response
            response_text = response.text.strip()
            
            # Clean the response if it's wrapped in code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse the JSON array
            prompt_suggestions = json.loads(response_text)
            
            print(f"✅ Generated {len(prompt_suggestions)} prompt suggestions")
            return prompt_suggestions
            
        except Exception as e:
            print(f"❌ Error generating prompt suggestions: {e}")
            print(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
            # Return some fallback suggestions
            return [
                "A spaceship from Star Citizen hovering over a planet, dramatic lighting, professional photography style.",
                "A detailed Star Citizen character in space suit standing on a landing pad with ships in the background.",
                "An epic space battle scene from Star Citizen with lasers and explosions, cinematic style."
            ]
    
    def improve_prompt(self, base_prompt: str, feedback: str, num_suggestions: int = 3) -> List[str]:
        """
        Improve an image prompt based on feedback
        
        Args:
            base_prompt (str): The original prompt to improve
            feedback (str): User feedback/comments for improvement
            num_suggestions (int): Number of improved prompts to generate
            
        Returns:
            List[str]: List of improved prompts
        """
        print(f"🔄 Improving prompt based on feedback...")
        
        try:
            # Create prompt for the AI
            system_prompt = """
            You are an expert image prompt creator specializing in improving existing prompts based on feedback.
            Given an original prompt and feedback, create several improved versions that address the feedback.
            
            Return EXACTLY {num_suggestions} distinct improved prompts as a JSON array of strings.
            Each prompt should be 1-3 sentences long and highly descriptive.
            DO NOT include any explanation or commentary - just the JSON array.
            """
            
            # Build the user prompt
            user_prompt = f"""
            Original prompt: "{base_prompt}"
            
            Feedback: "{feedback}"
            
            Create {num_suggestions} distinct, improved versions of this prompt that address the feedback.
            """
            
            # Generate improved prompts
            response = self.models["deep_research"].generate_content([
                {"role": "system", "parts": [system_prompt]},
                {"role": "user", "parts": [user_prompt]}
            ])
            
            # Parse the response
            response_text = response.text.strip()
            
            # Clean the response if it's wrapped in code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse the JSON array
            improved_prompts = json.loads(response_text)
            
            print(f"✅ Generated {len(improved_prompts)} improved prompts")
            return improved_prompts
            
        except Exception as e:
            print(f"❌ Error improving prompt: {e}")
            print(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
            # Return the original prompt with some variations
            return [
                f"{base_prompt} With improved lighting.",
                f"{base_prompt} With more dramatic composition.",
                f"{base_prompt} With enhanced details."
            ]
    
    def generate_and_save_image(self, prompt: str, output_path: Path) -> str:
        """
        Generate an image from a prompt and save it to the specified location
        
        Args:
            prompt (str): The prompt to generate the image from
            output_path (Path): The directory to save the image to
            
        Returns:
            str: The path to the saved image
        """
        print(f"🖼️ Generating image using {self.current_model} model...")
        print(f"📝 Prompt: {prompt}")
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get the model configuration
            model_config = self.image_configs[self.current_model]
            model_name = model_config["model_name"]
            
            # Generate the image
            generated_images = generate_image(
                prompt=prompt,
                model_name=model_name,
                number_of_images=self.number_of_images,
                aspect_ratio=self.aspect_ratio
            )
            
            if not generated_images:
                raise ValueError("No images were generated")
            
            # Save the first image
            image_data = generated_images[0].image.data
            
            # Convert to JPG if needed
            if output_path.suffix.lower() == '.jpg':
                # Convert PNG to JPG
                image = Image.open(BytesIO(image_data))
                # If the image has an alpha channel, create a white background
                if image.mode == 'RGBA':
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
                    image = background
                # Save as JPG
                image.save(output_path, 'JPEG', quality=95)
            else:
                # Save as PNG (original format)
                with open(output_path, 'wb') as f:
                    f.write(image_data)
            
            print(f"✅ Image saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            raise
    
    def interactive_workflow(self, content: str, output_dir: Path) -> str:
        """
        Run the interactive workflow to generate a blog cover image
        
        Args:
            content (str): The blog post content
            output_dir (Path): The directory to save the image to
            
        Returns:
            str: The path to the saved image
        """
        # Step 1: Generate prompt suggestions
        prompts = self.generate_prompt_suggestions(content)
        
        # Track the current prompts
        current_prompts = prompts
        
        while True:
            # Display the prompts
            print("\n📋 Prompt Options:")
            for i, prompt in enumerate(current_prompts, 1):
                print(f"{i}) {prompt}")
            
            # Get user choice
            choice = input("\n👉 Choose a prompt (1-3), 'i' to iterate with feedback, or 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                print("🛑 Exiting without generating an image")
                return None
            
            elif choice == 'i':
                # Get the prompt to iterate on
                prompt_idx = input("👉 Which prompt would you like to improve (1-3), or 'b' to go back? ").strip().lower()
                
                if prompt_idx == 'b':
                    # Go back to main loop
                    print("↩️ Going back to the main prompt selection...")
                    continue
                
                try:
                    prompt_idx = int(prompt_idx) - 1
                    if 0 <= prompt_idx < len(current_prompts):
                        base_prompt = current_prompts[prompt_idx]
                    else:
                        print("❌ Invalid prompt number")
                        continue
                except ValueError:
                    print("❌ Please enter a valid number")
                    continue
                
                # Get feedback
                feedback = input("💬 Enter your feedback for improving the prompt: ").strip()
                if not feedback:
                    print("⚠️ No feedback provided, keeping current prompts")
                    continue
                
                # Generate improved prompts
                improved_prompts = self.improve_prompt(base_prompt, feedback)
                
                # Add the improved prompts to the current pool
                current_prompts = improved_prompts
            
            elif choice.isdigit() and 1 <= int(choice) <= len(current_prompts):
                # User selected a prompt
                selected_idx = int(choice) - 1
                selected_prompt = current_prompts[selected_idx]
                
                # Confirm the selected prompt
                print(f"\n🔍 You selected this prompt:")
                print(f"   \"{selected_prompt}\"")
                confirm = input("👉 Do you want to use this prompt? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
                
                # Configure image generation
                print("\n⚙️ Image Generation Settings:")
                
                # Select model
                print(f"Current model: {self.current_model} ({self.image_configs[self.current_model]['description']})")
                print("Available models:")
                print(f"1) standard - {self.image_configs['standard']['description']}")
                print(f"2) ultra - {self.image_configs['ultra']['description']}")
                print(f"3) legacy - {self.image_configs['legacy']['description']}")
                
                model_choice = input("👉 Choose model (1-3) or press Enter to keep current: ").strip()
                if model_choice == '1':
                    self.current_model = 'standard'
                elif model_choice == '2':
                    self.current_model = 'ultra'
                elif model_choice == '3':
                    self.current_model = 'legacy'
                
                # Select aspect ratio
                print(f"Current aspect ratio: {self.aspect_ratio}")
                print("Available aspect ratios:")
                print("1) 1:1 - Square")
                print("2) 3:4 - Portrait")
                print("3) 4:3 - Landscape")
                print("4) 9:16 - Vertical")
                print("5) 16:9 - Widescreen")
                
                ratio_choice = input("👉 Choose aspect ratio (1-5) or press Enter to keep current: ").strip()
                if ratio_choice == '1':
                    self.aspect_ratio = "1:1"
                elif ratio_choice == '2':
                    self.aspect_ratio = "3:4"
                elif ratio_choice == '3':
                    self.aspect_ratio = "4:3"
                elif ratio_choice == '4':
                    self.aspect_ratio = "9:16"
                elif ratio_choice == '5':
                    self.aspect_ratio = "16:9"
                
                # Generate timestamp for unique filename
                timestamp = int(time.time())
                
                # Create output path with JPG extension
                output_path = output_dir / f"cover-image-{timestamp}.jpg"
                
                # Generate the image
                try:
                    image_path = self.generate_and_save_image(selected_prompt, output_path)
                    print(f"🎉 Image generation complete!")
                    return image_path
                except Exception as e:
                    print(f"❌ Error during image generation: {e}")
                    retry = input("👉 Would you like to try again with a different prompt? (y/n): ").strip().lower()
                    if retry != 'y':
                        return None
            
            else:
                print("❌ Invalid choice")

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description='Blog Cover Image Generator for Star Citizen Handbook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory"
  python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory" --aspect-ratio "16:9"
        """
    )
    
    parser.add_argument(
        '--content', '-c',
        help='Path to the blog content file or the content text itself',
        required=True
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Directory to save the generated image to',
        required=True
    )
    
    parser.add_argument(
        '--aspect-ratio', '-a',
        choices=['1:1', '3:4', '4:3', '9:16', '16:9'],
        default='16:9',
        help='Aspect ratio for the generated image'
    )
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = BlogImageGenerator()
    
    # Set the aspect ratio
    generator.aspect_ratio = args.aspect_ratio
    
    # Get the content
    content_path = Path(args.content)
    if content_path.exists() and content_path.is_file():
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Assume the content is provided directly
        content = args.content
    
    # Get the output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run the interactive workflow
    image_path = generator.interactive_workflow(content, output_dir)
    
    if image_path:
        print(f"✅ Image generated successfully: {image_path}")
        return 0
    else:
        print("❌ Image generation failed or was cancelled")
        return 1

if __name__ == "__main__":
    sys.exit(main())
