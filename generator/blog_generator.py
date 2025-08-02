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
import argparse
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
    
    def generate_ship_handbook(self, ship_name: str) -> str:
        """Generate a ship handbook using the standardized template"""
        print(f"🛸 Starting Ship Handbook generation for: '{ship_name}'")
        print("=" * 60)
        
        try:
            # Step 1: Load template
            template_path = self.script_dir / "ship-handbook-template.md"
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Step 2: Generate ship data using AI
            ship_data = self.generate_ship_data(ship_name)
            
            # Step 3: Replace placeholders in template
            complete_content = self.populate_ship_template(template_content, ship_data, ship_name)
            
            # Step 4: Generate content for each section
            final_content = self.generate_ship_sections(complete_content, ship_data, ship_name)
            
            # Step 5: Save to file
            file_path = self.save_ship_handbook(final_content, ship_data)
            
            print("=" * 60)
            print(f"🎉 Ship Handbook generation completed successfully!")
            print(f"📁 File created: {file_path}")
            print(f"🛸 Ship: {ship_name}")
            
            return file_path
            
        except Exception as e:
            print(f"💥 Ship Handbook generation failed: {e}")
            raise

    def generate_ship_data(self, ship_name: str) -> Dict:
        """Generate ship metadata and basic information"""
        print("🔍 Step 1: Generating ship metadata...")
        
        try:
            # Load the prompt from file
            prompt_path = self.script_dir / "prompts" / "generate-ship-data.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder
            prompt = prompt_template.replace("{{SHIP_NAME}}", ship_name)

            response = self.cost_effective_model.generate_content(prompt)
            
            # Clean JSON response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            ship_data = json.loads(response_text)
            print("✅ Ship metadata generated")
            return ship_data
        except FileNotFoundError:
            print(f"    ❌ Error: Prompt file not found at prompts/generate-ship-data.md")
            raise
        except Exception as e:
            print(f"❌ Error generating ship data: {e}")
            raise

    def populate_ship_template(self, template_content: str, ship_data: Dict, ship_name: str) -> str:
        """Replace placeholders in the template with actual data"""
        print("🔧 Step 2: Populating template with ship data...")
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Replace placeholders
        populated_content = template_content.replace("{{MANUFACTURER}}", ship_data.get('manufacturer', ''))
        populated_content = populated_content.replace("{{SHIP_NAME}}", ship_data.get('ship_name', ship_name))
        populated_content = populated_content.replace("{{PRIMARY_ROLE_DESCRIPTION}}", ship_data.get('primary_role_description', ''))
        populated_content = populated_content.replace("{{THAI_SUBTITLE}}", ship_data.get('thai_subtitle', ''))
        populated_content = populated_content.replace("{{DATE}}", current_date)
        populated_content = populated_content.replace("{{WEIGHT}}", str(ship_data.get('weight', 5)))
        populated_content = populated_content.replace("{{SHIP_NAME_SLUG}}", ship_data.get('ship_name_slug', ''))
        populated_content = populated_content.replace("{{THAI_DESCRIPTION}}", ship_data.get('thai_description', ''))
        populated_content = populated_content.replace("{{HERO_SHOT_DESCRIPTION}}", ship_data.get('hero_shot_description', ''))
        
        # Handle keywords
        keywords = ship_data.get('keywords', [])
        if len(keywords) >= 2:
            populated_content = populated_content.replace("{{KEYWORD_1}}", keywords[0])
            populated_content = populated_content.replace("{{KEYWORD_2}}", keywords[1])
        
        populated_content = populated_content.replace("{{THAI_KEYWORD}}", ship_data.get('thai_keyword', ''))
        
        print("✅ Template populated with ship data")
        return populated_content

    def generate_ship_sections(self, template_content: str, ship_data: Dict, ship_name: str) -> str:
        """Generate content for each section using individual focused prompts"""
        print("✨ Step 3: Generating content for each section...")
        
        # List of section prompts to process
        section_prompts = [
            "section-1-overview.md",
            "section-2-exterior.md", 
            "section-3-interior.md",
            "section-4-flight.md",
            "section-5-components.md",
            "section-6-defenses.md",
            "section-7-comparisons.md",
            "section-8-tactics.md",
            "section-9-who-is-this-for.md"
        ]
        
        generated_sections = {}
        
        # Generate each section individually
        for i, prompt_file in enumerate(section_prompts, 1):
            print(f"  📝 Generating section {i}/9: {prompt_file}")
            
            try:
                # Load the section prompt
                prompt_path = self.script_dir / "prompts" / prompt_file
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    section_prompt = f.read()
                
                # Replace placeholders in the prompt
                section_prompt = section_prompt.replace("{{SHIP_NAME}}", ship_data.get('ship_name', ship_name))
                section_prompt = section_prompt.replace("{{MANUFACTURER}}", ship_data.get('manufacturer', ''))
                
                # Generate content for this section
                response = self.deep_research_model.generate_content(section_prompt)
                section_content = response.text.strip()
                
                # Clean up potential code block wrappers
                if section_content.startswith("```markdown"):
                    section_content = section_content[10:]
                if section_content.endswith("```"):
                    section_content = section_content[:-3]
                
                # Store the generated section
                section_key = f"section_{i}"
                generated_sections[section_key] = section_content.strip()
                
                print(f"    ✅ Section {i} completed")
                
            except Exception as e:
                print(f"    ❌ Error generating section {i}: {e}")
                # Use placeholder content if generation fails
                generated_sections[section_key] = f"<!-- Section {i} generation failed -->"
        
        # Now combine all sections into a body section
        print("  🔧 Combining all sections into body content...")
        body_content = self.combine_sections_into_body(generated_sections)
        
        # Polish the entire body content using deep research model
        print("  ✨ Polishing body content with deep research model...")
        polished_body = self.polish_thai_content(body_content)
        
        # Finally combine the polished body with the template
        print("  📝 Assembling final content with template...")
        final_content = self.combine_body_with_template(template_content, polished_body)
        
        print("✅ All sections generated, combined, and polished")
        return final_content

    def combine_sections_into_body(self, generated_sections: Dict[str, str]) -> str:
        """Combine all generated sections into a single body content"""
        
        # The sections are already in the correct order (1-9)
        body_parts = []
        
        for i in range(1, 10):  # sections 1-9
            section_key = f"section_{i}"
            if section_key in generated_sections:
                section_content = generated_sections[section_key].strip()
                if section_content and not section_content.startswith("<!-- Section"):
                    body_parts.append(section_content)
        
        # Join all sections with double newlines
        body_content = "\n\n".join(body_parts)
        return body_content
    
    def combine_body_with_template(self, template_content: str, polished_body: str) -> str:
        """Combine the polished body content with the template structure"""
        
        # Replace the single body placeholder with the polished content
        body_placeholder = "<!-- AI will generate body content -->"
        
        if body_placeholder in template_content:
            final_content = template_content.replace(body_placeholder, polished_body)
            return final_content
        
        # Fallback: if placeholder not found, insert after table of contents
        toc_end_marker = "9. [ยานลำนี้เหมาะกับใคร?](#who-is-this-for)"
        
        if toc_end_marker in template_content:
            parts = template_content.split(toc_end_marker, 1)
            if len(parts) == 2:
                before_body = parts[0] + toc_end_marker + "\n\n"
                after_body = parts[1]
                final_content = before_body + polished_body + after_body
                return final_content
        
        # Last resort: append to the end
        return template_content + "\n\n" + polished_body

    def polish_thai_content(self, content: str) -> str:
        """Polish the Thai content using deep research model for more natural language"""
        
        try:
            # Load the polishing prompt from file
            prompt_path = self.script_dir / "prompts" / "polish-thai-content.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder with actual content
            prompt = prompt_template.replace("{{CONTENT}}", content)

            response = self.deep_research_model.generate_content(prompt)
            polished_content = response.text.strip()
            
            # Clean up potential code block wrappers
            if polished_content.startswith("```markdown"):
                polished_content = polished_content[10:]
            if polished_content.endswith("```"):
                polished_content = polished_content[:-3]
            
            print("    ✅ Content polished for natural Thai language")
            return polished_content.strip()
        except FileNotFoundError:
            print(f"    ❌ Error: Polishing prompt file not found at prompts/polish-thai-content.md")
            print("    📝 Using original content")
            return content
        except Exception as e:
            print(f"    ⚠️  Warning: Content polishing failed: {e}")
            print("    📝 Using original content")
            return content

    def save_ship_handbook(self, content: str, ship_data: Dict) -> str:
        """Save the ship handbook to a file"""
        print("💾 Step 4: Saving ship handbook...")
        
        # Create file path
        ship_slug = ship_data.get('ship_name_slug', 'unknown-ship')
        file_path = self.content_dir / "ships" / f"{ship_slug}.md"
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Ship handbook saved to: {file_path}")
        
        # Update category index
        self.update_ships_category_index(ship_data)
        
        return str(file_path)

    def update_ships_category_index(self, ship_data: Dict):
        """Update the ships category index with the new handbook"""
        print("📝 Updating ships category index...")
        
        index_path = self.content_dir / "ships" / "_index.md"
        if not index_path.exists():
            print(f"⚠️  Ships index not found: {index_path}")
            return
        
        try:
            # Read existing index
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()
            
            # Create link entry
            manufacturer = ship_data.get('manufacturer', '')
            ship_name = ship_data.get('ship_name', '')
            slug = ship_data.get('ship_name_slug', '')
            description = ship_data.get('thai_description', '')
            
            title = f"{manufacturer} {ship_name}"
            link_entry = f"\n- [{title}]({slug}) - {description}\n"
            
            # Append to the end
            updated_content = index_content + link_entry
            
            # Write back
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated ships category index")
        except Exception as e:
            print(f"⚠️  Could not update ships category index: {e}")

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
    parser = argparse.ArgumentParser(
        description='AI-Powered Hugo Blog Post Generator for Star Citizen Handbook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python blog_generator.py --mode ship "Anvil F7C Hornet"
  python blog_generator.py --mode freestyle "Crime in the 'Verse"
  python blog_generator.py "Drake Cutlass Red"  (interactive mode)
        """
    )
    
    parser.add_argument(
        'topic',
        help='The topic or ship name for the blog post'
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['ship', 'freestyle'],
        help='Content generation mode: "ship" for standardized ship handbook, "freestyle" for flexible content'
    )
    
    args = parser.parse_args()
    topic = args.topic
    
    # If mode is specified via command line, use it
    if args.mode:
        mode_choice = '1' if args.mode == 'ship' else '2'
        mode_name = "Ship Handbook" if args.mode == 'ship' else "Free Style"
        print(f"🚀 Star Citizen Handbook Generator")
        print("=" * 40)
        print(f"Mode: {mode_name}")
        print(f"Topic: {topic}")
        print()
    else:
        # Interactive mode selection
        print("🚀 Star Citizen Handbook Generator")
        print("=" * 40)
        print("Please choose a content mode:")
        print("1) Ship Handbook - Standardized ship guide format")
        print("2) Free Style - Flexible content structure")
        print()
        
        while True:
            try:
                mode_choice = input("Enter your choice (1 or 2): ").strip()
                if mode_choice in ['1', '2']:
                    break
                else:
                    print("❌ Please enter 1 or 2")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    try:
        generator = HugoBlogGenerator()
        
        if mode_choice == '1':
            print(f"\n🛸 Generating Ship Handbook for: '{topic}'")
            generator.generate_ship_handbook(topic)
        else:
            print(f"\n✨ Generating Free Style content for: '{topic}'")
            generator.generate_blog_post(topic)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
