#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cover Image Generator for Existing Star Citizen Handbook Articles

This script generates a cover image for an existing article file.
It parses the article content, generates an appropriate image, and updates the front matter.

Usage:
    python generate_article_cover.py path/to/article.md
    python generate_article_cover.py --no-update path/to/article.md

Args:
    article_path: The path to the article file
    --no-update: Optional flag to skip updating the front matter
"""

import os
import sys
import re
import argparse
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

# Import the shared genai utilities and the BlogImageGenerator

from genai_utils import get_project_paths
from blog_image_generator import BlogImageGenerator
from util import ensure_new_article_structure

# Global configuration
timeout = 300  # Default timeout in seconds

def extract_front_matter(content: str) -> Tuple[Dict, str]:
    """
    Extract front matter and content from a markdown file
    
    Args:
        content (str): The full markdown content with front matter
        
    Returns:
        Tuple[Dict, str]: A tuple containing front matter dict and content
    """
    # Check if the content starts with front matter delimiters
    if not content.startswith('---'):
        return {}, content
    
    # Find the end of the front matter
    end_index = content.find('---', 3)
    if end_index == -1:
        return {}, content
    
    # Extract front matter and content
    front_matter_text = content[3:end_index].strip()
    main_content = content[end_index + 3:].strip()
    
    # Parse front matter
    front_matter = {}
    for line in front_matter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
                
            front_matter[key] = value
    
    return front_matter, main_content

def update_front_matter_image(article_path_abs: str, image_path_abs: str) -> bool:
    """
    Update the image path in the front matter and cover image tag of a Hugo content file.
    Args:
        article_path_abs (str): Absolute path to the article file
        image_path_abs (str): Absolute path to the image file
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the file
        with open(article_path_abs, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find front matter block
        fm_start = content.find('---')
        fm_end = content.find('---', fm_start + 3)
        if fm_start != 0 or fm_end == -1:
            print("❌ No valid front matter block found.")
            return False

        front_matter = content[fm_start+3:fm_end].strip('\n')
        after_fm = content[fm_end+3:]

        # Calculate relative paths
        article_dir = Path(article_path_abs).parent.resolve()
        # Use project paths to get content_dir
        paths = get_project_paths()
        content_dir = Path(paths["content_dir"]).resolve()
        try:
            rel_image_path_for_front_matter = str(Path(image_path_abs).relative_to(content_dir)).replace('\\', '/')
        except Exception:
            print("⚠️ Could not compute image path relative to content dir.")
            rel_image_path_for_front_matter = os.path.basename(image_path_abs)
        rel_image_path_for_cover_tag = str(Path(image_path_abs).relative_to(article_dir)).replace('\\', '/')

        # Update or insert image field in front matter
        fm_lines = front_matter.split('\n') if front_matter else []
        image_line = f'image: "{rel_image_path_for_front_matter}"'
        found = False
        for idx, line in enumerate(fm_lines):
            if line.strip().startswith('image:'):
                fm_lines[idx] = image_line
                found = True
                break
        if not found:
            fm_lines.append(image_line)

        new_front_matter = '\n'.join(fm_lines)
        updated_content = f"---\n{new_front_matter}\n---{after_fm}"

        # Add or update the cover image markdown after front matter
        # Remove any existing cover image markdown immediately after front matter
        cover_image_pattern = r'^(\s*!\[cover\]\([^)]+\)\s*)'
        after_fm_stripped = after_fm.lstrip('\n')
        after_fm_new = re.sub(cover_image_pattern, '', after_fm_stripped, count=1, flags=re.MULTILINE)
        cover_markdown = f"\n![cover]({rel_image_path_for_cover_tag})\n\n"
        updated_content = f"---\n{new_front_matter}\n---\n{cover_markdown}{after_fm_new}"

        # Write the updated content back to the file
        with open(article_path_abs, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✅ Updated front matter image path to: {rel_image_path_for_front_matter}")
        return True
    except Exception as e:
        print(f"⚠️ Error updating front matter image path: {e}")
        return False

def generate_cover_image(article_path: str, update_front_matter: bool = True) -> Optional[str]:
    """
    Generate a cover image for an existing article and optionally update its front matter
    
    Args:
        article_path (str): Path to the article file
        update_front_matter (bool): Whether to update the front matter with the image path
        
    Returns:
        Optional[str]: Path to the generated image, or None if generation failed
    """
    print(f"🎯 Generating cover image for article: {article_path}")
    print("=" * 60)
    
    try:
        # Get project paths
        paths = get_project_paths()
        project_root = paths["project_root"]
        static_dir = paths["static_dir"]
        
        # Read the article file
        article_path = Path(article_path)
        if not article_path.exists():
            print(f"❌ Article file not found: {article_path}")
            return None
        
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter and content
        front_matter, main_content = extract_front_matter(content)
        
        # Move/rename article if needed and get output dir
        article_path, img_output_dir = ensure_new_article_structure(article_path)
        img_output_dir.mkdir(parents=True, exist_ok=True)
        cover_image_path = img_output_dir / "cover.jpg"
        
        # Prepare for image generation
        # Extract the title and description
        title = front_matter.get('title')
        description = front_matter.get('description')

        # Initialize the image generator
        image_generator = BlogImageGenerator()
        
        # Print generation information
        print(f"🚀 Generating image using BlogImageGenerator...")
        print(f"📂 Output directory: {img_output_dir}")
        print("⏳ This may take some time. Generating image...")
                  
        # Prepare the combined content for image generation
        # Read image prompt template and fill in values
        image_prompt_path = get_project_paths()["script_dir"] / "prompts" / "short-article" / "image_prompt.md"
        with open(image_prompt_path, 'r', encoding='utf-8') as imgf:
            image_prompt_template = imgf.read()
        combined_content = image_prompt_template \
            .replace("{{TITLE}}", title) \
            .replace("{{DESCRIPTION}}", description) \
            .replace("{{CONTENT}}", main_content)

        # Run the interactive workflow to generate the image
        print("🚀 Starting interactive image generation workflow...")
        print(f"📂 Output directory: {img_output_dir}")
        print("⏳ This interactive process requires your input to select and refine image prompts.")

        # Set default aspect ratio
        image_generator.aspect_ratio = "16:9"

        # Run the interactive workflow, save as cover.jpg
        generated_image_path = image_generator.interactive_workflow(combined_content, img_output_dir)

        # Compute image path relative to content folder
        if generated_image_path:
            print(f"✅ Image generation completed successfully")
            try:
                abs_image_path = Path(generated_image_path).resolve()
                article_path_abs = Path(article_path).resolve()
            except Exception as e:
                print(f"⚠️ Could not resolve absolute paths: {e}")
                return generated_image_path
            if update_front_matter:
                update_front_matter_image(str(article_path_abs), str(abs_image_path))
            else:
                print(f"ℹ️ Front matter update skipped. Image path: {abs_image_path}")
            return generated_image_path
        else:
            print(f"⚠️ Image generation was cancelled or failed")
            return None
        
    except Exception as e:
        print(f"💥 Cover image generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Cover Image Generator for Existing Star Citizen Handbook Articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_article_cover.py path/to/article.md
  python generate_article_cover.py --no-update path/to/article.md
  python generate_article_cover.py --timeout 600 path/to/article.md
        """
    )
    
    parser.add_argument(
        'article_path',
        help='Path to the article file'
    )
    
    parser.add_argument(
        '--no-update',
        action='store_true',
        help='Skip updating the front matter with the image path'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Timeout in seconds for image generation (default: 300)'
    )
    
    args = parser.parse_args()

    
    # Set timeout
    global timeout
    timeout = args.timeout
    print(f"⏱️ Timeout set to {timeout} seconds")
    
    # Generate cover image
    result = generate_cover_image(args.article_path, not args.no_update)
    
    if result:
        print("=" * 60)
        print(f"🎉 Cover image generation completed successfully!")
        print(f"📁 Image created: {result}")
        return 0
    else:
        print("=" * 60)
        print("❌ Cover image generation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
