#!/usr/bin/env python3
"""
AI-Powered Hugo Blog Post Generator for Star Citizen Handbook

This script automates the creation of Thai-language blog posts for a Hugo website
using the beautifulhugo theme, with a multi-model AI workflow.

Usage:
    python blog_generator.py "topic for the blog post"

Requirements:
    - GEMINI_API_KEY in .env file
    - Google Generative AI library
    - python-dotenv
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HugoBlogGenerator:
    """AI-powered Hugo blog post generator for Star Citizen Handbook"""
    
    def __init__(self):
        """Initialize the generator with API configuration"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=self.api_key)
        
        # Safety settings to prevent over-filtering
        safety_settings = [
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_NONE
            },
            {
                "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": HarmBlockThreshold.BLOCK_NONE
            },
            {
                "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                "threshold": HarmBlockThreshold.BLOCK_NONE
            },
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": HarmBlockThreshold.BLOCK_NONE
            }
        ]
        
        # Models configuration
        self.cost_effective_model = genai.GenerativeModel(
            'gemini-2.5-flash',
            safety_settings=safety_settings
        )
        self.deep_research_model = genai.GenerativeModel(
            'gemini-2.5-pro',
            safety_settings=safety_settings
        )
        
        # Project paths
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.content_dir = self.project_root / "content"
        
        # Categories mapping
        self.categories = {
            "ships": "ยานอวกาศ",
            "concepts": "แนวคิดและระบบเกม", 
            "guides": "คู่มือการเล่น"
        }
        
    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        # Remove special characters and convert to lowercase
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug
    
    def step1_generate_structure(self, topic: str) -> Dict:
        """Step 1: Generate Hugo front matter and content outline"""
        print("🏗️  Step 1: Generating blog structure and outline...")
        
        prompt = f"""
        You are an expert Hugo content creator and Star Citizen game expert. You will be creating content for a Thai audience, but some parts of the metadata must be in English for technical reasons.

        Topic: {topic}

        Generate a complete blog structure with:
        1. Hugo front matter in YAML format.
        2. A content outline with main sections.
        3. The appropriate category.

        **CRITICAL RULES:**
        - **English-only for Metadata:** `slug`, `category`, `tags`, and `categories` (in front_matter) MUST be in English.
        - **Thai for User Content:** `title`, `subtitle`, `description`, and the `outline` MUST be in natural, conversational Thai. The writing style should be like a gamer talking to a friend, not a formal translation.

        **DETAILED REQUIREMENTS:**
        - **`slug`**: URL-friendly, English, based on the topic.
        - **`category`**: Must be one of: "ships", "concepts", "guides".
        - **`tags`**: A list of relevant English tags.
        - **`categories` (in front_matter)**: A list containing the single English category from above.
        - **`title` / `subtitle`**: Catchy and informative in Thai, with appropriate emoji.
        - **`description`**: SEO-friendly and written in natural Thai.
        - **`outline`**: All section and subsection titles must be in Thai. `anchor_id` must be in English.
        - **`date`**: Today's date.
        - **`game_version`**: "Alpha 4.2.1".
        - **`image`**: A placeholder path, e.g., "img/category/slug/hero_image.jpg".

        Return ONLY a valid JSON object with this structure:
        {{
            "front_matter": {{
                "title": "Thai title with emoji",
                "subtitle": "Thai subtitle",
                "date": "YYYY-MM-DD",
                "lastmod": "YYYY-MM-DD",
                "draft": false,
                "game_version": "Alpha 4.2.1",
                "tags": ["english-tag1", "english-tag2"],
                "categories": ["english-category"],
                "author": "Star Citizen Handbook Team",
                "weight": 5,
                "image": "img/category/slug/hero_image.jpg",
                "description": "Thai description"
            }},
            "category": "ships|concepts|guides",
            "slug": "english-url-friendly-slug",
            "outline": [
                {{
                    "section": "Thai section title",
                    "subsections": ["Thai subsection 1", "Thai subsection 2"],
                    "anchor_id": "english-anchor-id"
                }}
            ]
        }}
        """
        
        try:
            response = self.cost_effective_model.generate_content(prompt)
            
            # Debug: Print raw response
            print(f"🔍 Raw response: {response.text[:200]}...")
            
            # Check if response is empty
            if not response.text or not response.text.strip():
                raise ValueError("Empty response from AI model")
            
            # Try to clean the response text (remove code block markers if present)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            structure_data = json.loads(response_text)
            print(f"✅ Generated structure for category: {structure_data['category']}")
            return structure_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error in Step 1: {e}")
            print(f"🔍 Response text: {response.text}")
            raise
        except Exception as e:
            print(f"❌ Error in Step 1: {e}")
            if hasattr(e, 'response'):
                print(f"🔍 API Error details: {e.response}")
            raise
    
    def step2_create_research_prompt(self, structure: Dict, topic: str) -> str:
        """Step 2: Create detailed research prompt based on structure"""
        print("🔍 Step 2: Creating deep research prompt...")
        
        prompt = f"""
        You are an AI research coordinator. Based on the blog structure and topic provided, create a comprehensive research prompt that will guide a deep research AI to gather all necessary information.
        
        Original Topic: {topic}
        Blog Structure: {json.dumps(structure, indent=2, ensure_ascii=False)}
        
        Create a detailed research prompt that:
        1. Clearly defines what information is needed for each section
        2. Specifies the depth of research required
        3. Includes specific Star Citizen game mechanics, lore, or technical details needed
        4. Requests current game information (Alpha 4.2.1)
        5. Asks for practical examples and use cases
        6. Requests both beginner-friendly and advanced information where appropriate
        
        The research prompt should be comprehensive and specific to ensure the research AI can gather all necessary data to create a complete, informative blog post.
        
        Return only the research prompt text (no JSON wrapper).
        """
        
        try:
            response = self.cost_effective_model.generate_content(prompt)
            research_prompt = response.text.strip()
            print("✅ Research prompt created")
            return research_prompt
        except Exception as e:
            print(f"❌ Error in Step 2: {e}")
            raise
    
    def step3_deep_research(self, research_prompt: str) -> str:
        """Step 3: Conduct deep research using specialized model"""
        print("🔬 Step 3: Conducting deep research...")
        
        try:
            response = self.deep_research_model.generate_content(research_prompt)
            research_data = response.text.strip()
            print("✅ Deep research completed")
            return research_data
        except Exception as e:
            print(f"❌ Error in Step 3: {e}")
            raise
    
    def step4_format_content(self, structure: Dict, research_data: str, topic: str) -> str:
        """Step 4: Format research data into complete blog post"""
        print("✨ Step 4: Formatting and polishing blog content...")
        
        prompt = f"""
        You are an expert Hugo content creator and Star Citizen specialist writing for Thai players. Your primary goal is to produce content that is natural, engaging, and sounds like a real gamer talking to another gamer.

        Original Topic: {topic}
        Blog Structure: {json.dumps(structure, indent=2, ensure_ascii=False)}
        Research Data: {research_data}

        Create a complete, polished blog post in Markdown format.

        **WRITING STYLE (MOST IMPORTANT):**
        - **Natural & Conversational Thai:** Write in a natural, flowing Thai style. The tone should be friendly, engaging, and like a knowledgeable gamer sharing tips with a friend.
        - **AVOID "TRANSLATED" LANGUAGE:** Do not write in a way that sounds like a direct, literal translation from English. Use common Thai gamer slang and phrasing where appropriate.
        - **Helpful & Informative:** The tone should be helpful and easy to understand for both new and experienced players.

        CONTENT REQUIREMENTS:
        - Write ENTIRELY in Thai language (except for specific technical terms, ship names, code, and anchor IDs).
        - Use the research data to fill out the sections defined in the blog structure.
        - Include appropriate emoji throughout the content to make it more lively.
        - Create a table of contents (สารบัญ) at the beginning with clickable anchor links.
        - Add practical examples, pro-tips, and warnings.
        - Include relevant Star Citizen terminology.

        FORMATTING REQUIREMENTS:
        - Use proper Markdown syntax.
        - Create manual anchor IDs in English for all H2 and H3 headers: `## หัวข้อภาษาไทย {{ #english-anchor-id }}`
        - Use H2 for main sections and H3 for subsections as defined in the outline.
        - Use blockquotes (`>`) for important tips or warnings.
        - Use tables for comparative data (e.g., ship stats).
        - Include placeholder comments for images: `<!-- Photo: คำอธิบายรูปภาพภาษาไทย -->`

        HUGO-SPECIFIC REQUIREMENTS:
        - **Do NOT include front matter.** It will be added in a later step.
        - Avoid making up Hugo shortcodes. Use standard Markdown.
        - Ensure the final output is only the raw Markdown body of the article.

        Return only the Markdown content (no front matter, no code block wrappers).
        """
        
        try:
            response = self.cost_effective_model.generate_content(prompt)
            formatted_content = response.text.strip()
            
            # Clean up potential code block wrappers from the response
            if formatted_content.startswith("```markdown"):
                formatted_content = formatted_content[10:]
            if formatted_content.endswith("```"):
                formatted_content = formatted_content[:-3]
            
            print("✅ Content formatted and polished")
            return formatted_content.strip()
        except Exception as e:
            print(f"❌ Error in Step 4: {e}")
            raise
    
    def step5_integrate_content(self, structure: Dict, content: str) -> str:
        """Step 5: Integrate content into Hugo project"""
        print("🚀 Step 5: Integrating content into Hugo project...")
        
        # Create front matter in YAML format
        front_matter = structure['front_matter']
        
        # Format front matter
        yaml_front_matter = "---\n"
        for key, value in front_matter.items():
            if isinstance(value, str):
                yaml_front_matter += f'{key}: "{value}"\n'
            elif isinstance(value, bool):
                yaml_front_matter += f'{key}: {str(value).lower()}\n'
            elif isinstance(value, list):
                yaml_front_matter += f'{key}: {json.dumps(value, ensure_ascii=False)}\n'
            else:
                yaml_front_matter += f'{key}: {value}\n'
        yaml_front_matter += "---\n\n"
        
        # Combine front matter and content
        complete_content = yaml_front_matter + content
        
        # Create file path
        category = structure['category']
        slug = structure['slug']
        file_path = self.content_dir / category / f"{slug}.md"
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        
        print(f"✅ Content saved to: {file_path}")
        
        # Update category index
        self.update_category_index(category, structure)
        
        return str(file_path)
    
    def update_category_index(self, category: str, structure: Dict):
        """Update the category _index.md file with link to new post"""
        print(f"📝 Updating {category} category index...")
        
        index_path = self.content_dir / category / "_index.md"
        if not index_path.exists():
            print(f"⚠️  Category index not found: {index_path}")
            return
        
        try:
            # Read existing index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()
            
            # Create link entry
            title = structure['front_matter']['title']
            slug = structure['slug']
            description = structure['front_matter']['description']
            
            # Find a good place to insert the link (before the last closing tag or at the end)
            link_entry = f"\n- [{title}]({slug}) - {description}\n"
            
            # Simple approach: append to the end if no specific pattern found
            if "## รายการ" in index_content or "## หน้าในหมวดนี้" in index_content:
                # Find the list section and add there
                updated_content = index_content + link_entry
            else:
                # Add a new section if none exists
                updated_content = index_content + f"\n## รายการใหม่\n{link_entry}"
            
            # Write back
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated category index: {index_path}")
        except Exception as e:
            print(f"⚠️  Could not update category index: {e}")
    
    def generate_blog_post(self, topic: str) -> str:
        """Main method to generate a complete blog post"""
        print(f"🎯 Starting blog generation for topic: '{topic}'")
        print("=" * 60)
        
        try:
            # Step 1: Generate structure and outline
            structure = self.step1_generate_structure(topic)
            
            # Step 2: Create research prompt
            research_prompt = self.step2_create_research_prompt(structure, topic)
            
            # Step 3: Conduct deep research
            research_data = self.step3_deep_research(research_prompt)
            
            # Step 4: Format content
            formatted_content = self.step4_format_content(structure, research_data, topic)
            
            # Step 5: Integrate into Hugo project
            file_path = self.step5_integrate_content(structure, formatted_content)
            
            print("=" * 60)
            print(f"🎉 Blog post generation completed successfully!")
            print(f"📁 File created: {file_path}")
            print(f"🏷️  Category: {structure['category']}")
            print(f"🔗 Slug: {structure['slug']}")
            
            return file_path
            
        except Exception as e:
            print(f"💥 Blog generation failed: {e}")
            raise

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python blog_generator.py \"topic for the blog post\"")
        print("Example: python blog_generator.py \"Drake Cutlass Red medical ship guide\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    try:
        generator = HugoBlogGenerator()
        generator.generate_blog_post(topic)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
