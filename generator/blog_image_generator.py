#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Cover Image Generator for Star Citizen Handbook

This script generates cover images for blog posts using the Google Generative AI API.
It takes blog content as input, suggests image prompts, and generates images.

This module can be used both as a standalone script and as an imported library.

Usage as script:
    python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory"

Usage as library:
    from blog_image_generator import BlogImageGenerator
    generator = BlogImageGenerator()
    result = generator.auto_generate_cover_for_article(content, title, description, headings, output_path)
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from PIL import Image, ImageDraw
from io import BytesIO

# Import the genai utilities
from genai_utils import configure_genai, generate_text, generate_image, get_project_paths

class BlogImageGenerator:
    """Generate cover images for Star Citizen Handbook blog posts"""
    
    def __init__(self):
        """Initialize the generator with API configuration"""
        try:
            # Configure the API
            configure_genai()
            
            # Project paths
            self.paths = get_project_paths()
            
            # Default settings
            self.aspect_ratio = "16:9"
            
            print("✅ Image generator initialized")
            
        except Exception as e:
            print(f"❌ Error initializing image generator: {e}")
            raise
    
    def generate_image(self, prompt: str, output_path: Path) -> Dict:
        """
        Generate an image based on a prompt and save it to a file
        
        Args:
            prompt (str): The image prompt
            output_path (Path): The path to save the image to
            
        Returns:
            Dict: Response containing success status and image information
        """
        print(f"🖼️ Generating image with prompt: {prompt}")
        
        try:
            # Generate the image using the utility function from genai_utils.py
            response = generate_image(
                prompt=prompt,
                aspect_ratio=self.aspect_ratio,
                output_path=output_path
            )
            
            # Check for success
            if not response.get("success", False):
                print(f"⚠️ Image generation failed: {response.get('error', 'Unknown error')}")
            else:
                print(f"✅ Image generated successfully: {response.get('output_path', '')}")
                
            return response
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            
            # Create a simple error image with PIL
            try:
                img = Image.new('RGB', (1280, 720), color=(30, 30, 30))
                d = ImageDraw.Draw(img)
                
                # Add error text
                error_text = f"Error generating image: {str(e)[:100]}"
                prompt_text = f"Prompt: {prompt[:100]}"
                
                # Simple text
                d.text((40, 40), "IMAGE GENERATION ERROR", fill=(255, 50, 50))
                d.text((40, 80), error_text, fill=(255, 255, 255))
                d.text((40, 120), prompt_text, fill=(200, 200, 200))
                
                # Save the error image
                img.save(output_path)
                print(f"⚠️ Saved error placeholder image to: {output_path}")
                
                return {
                    "success": False,
                    "error": str(e),
                    "output_path": str(output_path)
                }
            except Exception as inner_e:
                print(f"❌ Failed to create error image: {inner_e}")
                return {
                    "success": False,
                    "error": f"{str(e)} (Failed to create error image: {str(inner_e)})"
                }
    
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
            prompt = f"""
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
            
            Here is the blog content:
            ---
            {content[:8000]}  # Limit content to 8000 chars to avoid token limits
            ---
            """
            
            # Generate suggestions using the text model
            response = generate_text(prompt, "deep_research")
            
            # Try to parse the response as JSON
            try:
                # Clean up the response to ensure it's valid JSON
                # Find the first [ and last ] to extract just the JSON array
                start_idx = response.find('[')
                end_idx = response.rfind(']') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    suggestions = json.loads(json_str)
                    
                    # Ensure we have the right number of suggestions
                    if len(suggestions) == num_suggestions:
                        print(f"✅ Generated {len(suggestions)} prompt suggestions")
                        return suggestions
                    else:
                        print(f"⚠️ Expected {num_suggestions} suggestions but got {len(suggestions)}")
                        # Return whatever we got if not exactly the right number
                        return suggestions[:num_suggestions]
                else:
                    # If we can't find JSON array delimiters, try parsing the whole thing
                    suggestions = json.loads(response)
                    return suggestions[:num_suggestions]
                    
            except json.JSONDecodeError:
                # If JSON parsing fails, just split by newlines and clean up
                print("⚠️ Could not parse response as JSON, falling back to text parsing")
                
                # Clean up the response and split by newlines
                clean_response = response.strip()
                
                # Split by numbered items (1., 2., etc.)
                import re
                suggestions = re.split(r'\d+\.', clean_response)
                
                # Remove empty strings and strip whitespace
                suggestions = [s.strip() for s in suggestions if s.strip()]
                
                # Ensure we have the right number
                if len(suggestions) >= num_suggestions:
                    return suggestions[:num_suggestions]
                
                # If we still don't have enough, just split by double newlines
                if len(suggestions) < num_suggestions:
                    suggestions = clean_response.split('\n\n')
                    suggestions = [s.strip() for s in suggestions if s.strip()]
                
                return suggestions[:num_suggestions]
                
        except Exception as e:
            print(f"❌ Error generating prompt suggestions: {e}")
            import traceback
            traceback.print_exc()
            
            # Return some default suggestions in case of error
            return [
                "A Star Citizen spaceship in orbit around a vibrant planet, with dramatic lighting and stars in the background.",
                "An immersive Star Citizen gameplay scene showing player interaction with game mechanics, with a futuristic UI overlay.",
                "A cinematic Star Citizen scene with detailed characters and environment, showcasing the game's high-fidelity graphics."
            ]
    
    def improve_prompt(self, base_prompt: str, feedback: str, num_variations: int = 3) -> List[str]:
        """
        Generate improved variations of a prompt based on user feedback
        
        Args:
            base_prompt (str): The original prompt to improve
            feedback (str): User feedback for improvement
            num_variations (int): Number of variations to generate
            
        Returns:
            List[str]: List of improved prompt variations
        """
        print(f"🔄 Generating {num_variations} improved variations based on feedback...")
        
        try:
            # Create prompt for the AI
            prompt = f"""
            You are an expert image prompt creator for a blog about Star Citizen, a space simulation game.
            
            Original prompt: {base_prompt}
            
            User feedback: {feedback}
            
            Based on this feedback, create {num_variations} improved variations of the original prompt.
            Each variation should:
            1. Address the user's feedback
            2. Be detailed and specific
            3. Be visually interesting
            4. Include artistic style suggestions
            5. Be 1-3 sentences long and highly descriptive
            
            Return EXACTLY {num_variations} distinct prompt variations as a JSON array of strings.
            DO NOT include any explanation or commentary - just the JSON array.
            """
            
            # Generate improved variations using the text model
            response = generate_text(prompt, "cost_effective")
            
            # Try to parse the response as JSON
            try:
                # Clean up the response to ensure it's valid JSON
                # Find the first [ and last ] to extract just the JSON array
                start_idx = response.find('[')
                end_idx = response.rfind(']') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    variations = json.loads(json_str)
                    
                    # Ensure we have the right number of variations
                    if len(variations) == num_variations:
                        print(f"✅ Generated {len(variations)} improved variations")
                        return variations
                    else:
                        print(f"⚠️ Expected {num_variations} variations but got {len(variations)}")
                        # Fill missing variations if needed
                        while len(variations) < num_variations:
                            variations.append(f"{base_prompt} (variation {len(variations)+1})")
                        # Return whatever we got if not exactly the right number
                        return variations[:num_variations]
                else:
                    # If we can't find JSON array delimiters, try parsing the whole thing
                    variations = json.loads(response)
                    return variations[:num_variations]
                    
            except json.JSONDecodeError:
                # If JSON parsing fails, just split by newlines and clean up
                print("⚠️ Could not parse response as JSON, falling back to text parsing")
                
                # Clean up the response and split by newlines
                clean_response = response.strip()
                
                # Split by numbered items (1., 2., etc.)
                import re
                variations = re.split(r'\d+\.', clean_response)
                
                # Remove empty strings and strip whitespace
                variations = [s.strip() for s in variations if s.strip()]
                
                # Ensure we have the right number
                if len(variations) >= num_variations:
                    return variations[:num_variations]
                
                # If we still don't have enough, just split by double newlines
                if len(variations) < num_variations:
                    variations = clean_response.split('\n\n')
                    variations = [s.strip() for s in variations if s.strip()]
                
                # If we still don't have enough, add the original with slight variations
                while len(variations) < num_variations:
                    variations.append(f"{base_prompt} (variation {len(variations)+1})")
                
                return variations[:num_variations]
                
        except Exception as e:
            print(f"❌ Error generating improved prompt variations: {e}")
            import traceback
            traceback.print_exc()
            
            # Return the original prompt and two simple variations
            return [
                base_prompt,
                f"{base_prompt} (with {feedback.split()[0] if feedback else 'improved'} style)",
                f"{base_prompt} (enhanced with {feedback.split()[-1] if feedback else 'better'} details)"
            ]
    
    def interactive_workflow(self, content: str, output_dir: Path) -> Union[str, Dict, None]:
        """
        Run the interactive workflow to generate a blog cover image
        
        Args:
            content (str): The blog post content
            output_dir (Path): The directory to save the image to
            
        Returns:
            Union[str, Dict, None]: The path to the saved image, response dict, or None if cancelled
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
                
                # Improve the prompt based on feedback
                improved_prompts = self.improve_prompt(base_prompt, feedback)
                
                # Update current prompts with the improved variations
                current_prompts += improved_prompts
            
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
                
                # Select aspect ratio if needed
                print(f"Current aspect ratio: {self.aspect_ratio}")
                print("Available aspect ratios:")
                print("1) 1:1 - Square")
                print("2) 3:4 - Portrait")
                print("3) 4:3 - Landscape")
                print("4) 9:16 - Vertical")
                print("5) 16:9 - Widescreen (default)")
                
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
                    result = self.generate_image(selected_prompt, output_path)
                    if result.get("success", False):
                        print(f"🎉 Image generation complete!")
                        return result.get("output_path")
                    else:
                        print(f"⚠️ Image generation failed: {result.get('error', 'Unknown error')}")
                        retry = input("👉 Would you like to try again with a different prompt? (y/n): ").strip().lower()
                        if retry != 'y':
                            return None
                        return None
                except Exception as e:
                    print(f"❌ Error during image generation: {e}")
                    retry = input("👉 Would you like to try again with a different prompt? (y/n): ").strip().lower()
                    if retry != 'y':
                        return None
            
            else:
                print("❌ Invalid choice")
    
    # The auto_generate_cover_for_article method has been removed 
    # since we now use the interactive_workflow method instead

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
    
    parser.add_argument(
        '--non-interactive', '-n',
        action='store_true',
        help='Run in non-interactive mode (auto-selects first prompt)'
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
    
    # Generate timestamp for unique filename
    timestamp = int(time.time())
    output_path = output_dir / f"cover-image-{timestamp}.jpg"
    
    if args.non_interactive:
        # Run the non-interactive workflow
        result = generator.generate_prompt_suggestions(content, 1)
        if result and len(result) > 0:
            selected_prompt = result[0]
            print(f"🔍 Automatically selected prompt: \"{selected_prompt}\"")
            result = generator.generate_image(selected_prompt, output_path)
        else:
            print("❌ Failed to generate prompt suggestions")
            return 1
        
        if result and result.get("success", False):
            print(f"✅ Image generated successfully: {result.get('output_path', '')}")
            return 0
        else:
            print(f"❌ Image generation failed: {result.get('error', 'Unknown error')}")
            return 1
    else:
        # Run the interactive workflow
        result = generator.interactive_workflow(content, output_dir)
        if result:
            if isinstance(result, dict):
                output_path = result.get("output_path", "")
                if result.get("success", False):
                    print(f"✅ Image generated successfully: {output_path}")
                    return 0
                else:
                    print(f"❌ Image generation failed: {result.get('error', 'Unknown error')}")
                    return 1
            else:
                print(f"✅ Image generated successfully: {result}")
                return 0
        else:
            print("❌ Image generation was cancelled or failed")
            return 1

if __name__ == "__main__":
    sys.exit(main())
