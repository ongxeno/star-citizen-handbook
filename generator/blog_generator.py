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
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

# Import the shared genai utilities
from genai_utils import generate_text, get_project_paths
from blog_image_generator import BlogImageGenerator

class HugoBlogGenerator:
    """AI-powered Hugo blog post generator for Star Citizen Handbook"""
    
    def __init__(self):

        # Project paths
        paths = get_project_paths()
        self.script_dir = paths["script_dir"]
        self.project_root = paths["project_root"]
        self.content_dir = paths["content_dir"]
        self.static_dir = paths["static_dir"]
        self.img_dir = paths["img_dir"]
        
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
        
        try:
            from constants import MAIN_CATEGORIES
            prompt_path = self.script_dir / "prompts" / "deep-research" / "step1_generate_structure.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Inject MAIN_CATEGORIES as a pipe-separated string
            main_categories_str = "|".join(MAIN_CATEGORIES)
            prompt = prompt_template.replace("{{MAIN_CATEGORIES}}", main_categories_str)
            prompt = prompt_template.replace("{{TOPIC}}", topic)

            response_text = generate_text(prompt=prompt, model_key="cost_effective")

            # Debug: Print raw response
            print(f"🔍 Raw response: {response_text[:200]}...")
            
            # Check if response is empty
            if not response_text or not response_text.strip():
                raise ValueError("Empty response from AI model")
            
            # Try to clean the response text (remove code block markers if present)
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
            print(f"🔍 Response text: {response_text}")
            raise
        except Exception as e:
            print(f"❌ Error in Step 1: {e}")
            if hasattr(e, 'response'):
                print(f"🔍 API Error details: {e.response}")
            raise
    
    def step2_create_research_prompt(self, structure: Dict, topic: str) -> str:
        """Step 2: Create detailed research prompt based on structure"""
        print("🔍 Step 2: Creating deep research prompt...")
        
        try:
            prompt_path = self.script_dir / "prompts" / "deep-research" / "step2_create_research_prompt.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()

            prompt = prompt_template.replace("{{TOPIC}}", topic)
            prompt = prompt.replace("{{STRUCTURE}}", json.dumps(structure, indent=2, ensure_ascii=False))

            response_text = generate_text(prompt = prompt, model_key = "cost_effective")
            research_prompt = response_text.strip()
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
        
        try:
            prompt_path = self.script_dir / "prompts" / "deep-research" / "step4_format_content.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            prompt = prompt_template.replace("{{TOPIC}}", topic)
            prompt = prompt.replace("{{STRUCTURE}}", json.dumps(structure, indent=2, ensure_ascii=False))
            prompt = prompt.replace("{{RESEARCH_DATA}}", research_data)

            response_text = generate_text(prompt = prompt, model_key = "cost_effective")
            formatted_content = response_text.strip()
            
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
        
        # Create file path in folder/index.md format
        category = structure['category']
        slug = structure['slug']
        file_path = self.content_dir / category / slug / "index.md"
        
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
            prompt_path = self.script_dir / "prompts" / "ships" / "generate-ship-data.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder
            prompt = prompt_template.replace("{{SHIP_NAME}}", ship_name)

            response_text = generate_text(prompt = prompt, model_key = "cost_effective")
            
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            ship_data = json.loads(response_text)
            print("✅ Ship metadata generated")
            return ship_data
        except FileNotFoundError:
            print(f"    ❌ Error: Prompt file not found at {prompt_path}")
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
                prompt_path = self.script_dir / "prompts" / "ships" / prompt_file
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    section_prompt = f.read()
                
                # Replace placeholders in the prompt
                section_prompt = section_prompt.replace("{{SHIP_NAME}}", ship_data.get('ship_name', ship_name))
                section_prompt = section_prompt.replace("{{MANUFACTURER}}", ship_data.get('manufacturer', ''))
                
                # Generate content for this section
                response_text = generate_text(prompt = section_prompt, model_key = "deep_research")
                section_content = response_text.strip()
                
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
            prompt_path = self.script_dir / "prompts" / "ships" / "polish-thai-content.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder with actual content
            prompt = prompt_template.replace("{{CONTENT}}", content)

            response_text = generate_text(prompt = prompt, model_key = "deep_research")
            polished_content = response_text.strip()
            
            # Clean up potential code block wrappers
            if polished_content.startswith("```markdown"):
                polished_content = polished_content[10:]
            if polished_content.endswith("```"):
                polished_content = polished_content[:-3]
            
            print("    ✅ Content polished for natural Thai language")
            return polished_content.strip()
        except FileNotFoundError:
            print(f"    ❌ Error: Polishing prompt file not found at {prompt_path}")
            print("    📝 Using original content")
            return content
        except Exception as e:
            print(f"    ⚠️  Warning: Content polishing failed: {e}")
            print("    📝 Using original content")
            return content

    def save_ship_handbook(self, content: str, ship_data: Dict) -> str:
        """Save the ship handbook to a file"""
        print("💾 Step 4: Saving ship handbook...")
        
        # Create file path in folder/index.md format
        ship_slug = ship_data.get('ship_name_slug', 'unknown-ship')
        file_path = self.content_dir / "ships" / ship_slug / "index.md"
        
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

    def generate_short_article(self, topic: str, context_sources: Optional[List[str]] = None) -> str:
        """Generates a complete short article in a single step."""
        print(f"✍️  Starting Short Article generation for: '{topic}'")
        if context_sources:
            print(f"📚 Using {len(context_sources)} additional context source(s)")
        print("=" * 60)

        try:
            # Step 1: Load the prompt template
            prompt_path = self.script_dir / "prompts" / "short-article" / "short-article.md"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Step 2: Create the final prompt with context sources
            prompt = prompt_template.replace("{{TOPIC}}", topic)
            
            # Add context sources if provided
            if context_sources and len(context_sources) > 0:
                context_section = "\n\n## Additional Context Sources:\n"
                for i, source in enumerate(context_sources, 1):
                    context_section += f"{i}. {source}\n"
                context_section += "\nNote: Please use these sources as reference material alongside your existing knowledge. You are not limited to only these sources - feel free to incorporate your broader understanding of Star Citizen and related topics.\n"
                prompt = prompt.replace("{{CONTEXT_SOURCES}}", context_section)
            else:
                prompt = prompt.replace("{{CONTEXT_SOURCES}}", "")
            
            # Step 3: Generate content and structure from AI
            print("🤖 Calling AI to generate the article...")
            response_text = generate_text(prompt = prompt, model_key = "deep_research")
            
            # Clean and parse JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            result_data = json.loads(response_text)
            structure = result_data['structure']
            content = result_data['content']
            print("✅ AI generation complete.")
            
            # Step 4: Integrate into Hugo project
            file_path = self.step5_integrate_content(structure, content)
            
            # Step 5: Generate cover image
            print("🖼️ Would you like to generate a cover image for this article?")
            generate_image = input("Generate image? (y/n): ").strip().lower() == 'y'
            
            if generate_image:
                # Determine the image directory path based on category and slug
                category = structure['category']
                slug = structure['slug']
                img_output_dir = self.img_dir / category / slug
                img_output_dir.mkdir(parents=True, exist_ok=True)
                    
                # Call the blog image generator directly
                print(f"🚀 Launching image generator...")
                
                try:
                    # Initialize the BlogImageGenerator
                    image_generator = BlogImageGenerator()
                    
                    # Prepare the combined content for image generation
                    # Read image prompt template and fill in values
                    image_prompt_path = self.script_dir / "prompts" / "short-article" / "image_prompt.md"
                    with open(image_prompt_path, 'r', encoding='utf-8') as imgf:
                        image_prompt_template = imgf.read()
                    combined_content = image_prompt_template \
                        .replace("{{TITLE}}", structure['front_matter'].get('title', '')) \
                        .replace("{{DESCRIPTION}}", structure['front_matter'].get('description', '')) \
                        .replace("{{CONTENT}}", content)
                    
                    # Run the interactive workflow to generate the image
                    print("🚀 Starting interactive image generation workflow...")
                    print(f"📂 Output directory: {img_output_dir}")
                    print("⏳ This interactive process requires your input to select and refine image prompts.")
                    
                    # Set default aspect ratio
                    image_generator.aspect_ratio = "16:9"
                    
                    # Run the interactive workflow
                    generated_image_path = image_generator.interactive_workflow(combined_content, img_output_dir)
                    
                    # Check if the image generation was successful
                    if generated_image_path:
                        print(f"✅ Image generation completed successfully")
                        
                        # Convert to relative path for Hugo
                        rel_path = Path(generated_image_path).relative_to(self.static_dir)
                        # Use forward slashes for Hugo paths but no leading slash
                        hugo_path = f"{str(rel_path).replace('\\', '/')}"
                        
                        # Update the front matter in the article file
                        self.update_front_matter_image(file_path, hugo_path)
                    else:
                        print(f"⚠️ Image generation was cancelled or failed")
                except Exception as e:
                    print(f"⚠️ Error running image generator: {e}")
                    import traceback
                    traceback.print_exc()
            
            print("=" * 60)
            print(f"🎉 Short article generation completed successfully!")
            print(f"📁 File created: {file_path}")
            print(f"🏷️  Category: {structure['category']}")
            print(f"🔗 Slug: {structure['slug']}")
            
            return file_path

        except FileNotFoundError:
            print(f"❌ Error: Prompt file not found at {prompt_path}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error in Short Article generation: {e}")
            print(f"🔍 Response text: {response_text}")
            raise
        except Exception as e:
            print(f"💥 Short Article generation failed: {e}")
            raise
    
    def update_front_matter_image(self, file_path: str, image_path: str):
        """Update the image path in the front matter of a Hugo content file"""
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove leading slash from image path if it exists
            if image_path.startswith('/'):
                image_path = image_path[1:]
                
            # Check if the image tag already exists
            image_match = re.search(r'image: "([^"]+)"', content)
            
            if image_match:
                # Update existing image path
                updated_content = content.replace(image_match.group(0), f'image: "{image_path}"')
            else:
                # Add image path at the end of front matter
                updated_content = content.replace('---\n\n', f'---\nimage: "{image_path}"\n\n', 1)
            
            # Add the cover image markdown right after frontmatter
            # First, check if there's already a cover image line after frontmatter using a more robust pattern
            # This will match the frontmatter closing and the cover image line with various whitespace patterns
            cover_image_pattern = r'---\s*\n+\s*!\[cover\]\([^)]+\)'
            cover_image_match = re.search(cover_image_pattern, updated_content)
            
            if cover_image_match:
                # Replace the existing cover image with the new one
                cover_markdown = f"![cover](../../{image_path})"
                # Use the original pattern to replace exactly what was matched
                updated_content = re.sub(cover_image_pattern, f"---\n\n{cover_markdown}", updated_content)
                print(f"✅ Replaced existing cover image markdown with new image")
            else:
                # Add new cover image markdown after frontmatter
                cover_markdown = f"\n![cover](../../{image_path})\n"
                updated_content = updated_content.replace('---\n\n', f'---\n{cover_markdown}\n', 1)
                print(f"✅ Added new cover image markdown after frontmatter")
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated front matter image path to: {image_path}")
        except Exception as e:
            print(f"⚠️ Error updating front matter image path: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI-Powered Hugo Blog Post Generator for Star Citizen Handbook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python blog_generator.py --mode ship "Anvil F7C Hornet"
  python blog_generator.py --mode deep-research "Crime in the 'Verse"
  python blog_generator.py --mode short-article "What is LTI?"
  python blog_generator.py --mode short-article "Chairman's Club" --context "https://robertsspaceindustries.com/comm-link/transmission/12978-Introducing-The-Chairman-s-Club"
  python blog_generator.py --mode short-article "New Ship Sale" --context "https://rsi.com/sale-page" "Additional reference material"
  python blog_generator.py "Drake Cutlass Red"  (interactive mode)
        """
    )
    
    parser.add_argument(
        'topic',
        help='The topic or ship name for the blog post'
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['ship', 'deep-research', 'short-article'],
        help='Content generation mode: "ship" for standardized ship handbook, "deep-research" for flexible content, "short-article" for a brief article.'
    )
    
    parser.add_argument(
        '--context', '-c',
        nargs='*',
        help='Additional context sources (URLs, references, etc.) for short-article mode. Can be used multiple times.'
    )
    
    args = parser.parse_args()
    topic = args.topic
    
    # If mode is specified via command line, use it
    if args.mode:
        if args.mode == 'ship':
            mode_choice = '1'
            mode_name = "Ship Handbook"
        elif args.mode == 'deep-research':
            mode_choice = '2'
            mode_name = "Deep Research"
        else: # short-article
            mode_choice = '3'
            mode_name = "Short Article"

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
        print("2) Deep Research - Flexible content structure")
        print("3) Short Article - Quick, concise article")
        print()
        
        while True:
            try:
                mode_choice = input("Enter your choice (1, 2, or 3): ").strip()
                if mode_choice in ['1', '2', '3']:
                    break
                else:
                    print("❌ Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    try:
        generator = HugoBlogGenerator()
        
        if mode_choice == '1':
            print(f"\n🛸 Generating Ship Handbook for: '{topic}'")
            generator.generate_ship_handbook(topic)
        elif mode_choice == '2':
            print(f"\n✨ Generating Deep Research content for: '{topic}'")
            generator.generate_blog_post(topic)
        else: # mode_choice == '3'
            print(f"\n✍️  Generating Short Article for: '{topic}'")
            
            # Handle context sources
            if args.mode:
                # Command line mode - use provided context
                context_sources = args.context if args.context else None
            else:
                # Interactive mode - ask for context sources
                context_sources = []
                print("\n📚 Optional: Add context sources (URLs, references, etc.)")
                print("   Press Enter without typing anything to skip.")
                print("   Type 'done' when finished adding sources.")
                
                while True:
                    try:
                        source = input("   Enter source (or 'done'): ").strip()
                        if source == '' or source.lower() == 'done':
                            break
                        context_sources.append(source)
                        print(f"   ✅ Added: {source}")
                    except KeyboardInterrupt:
                        print("\n👋 Goodbye!")
                        sys.exit(0)
                
                context_sources = context_sources if context_sources else None
                if context_sources:
                    print(f"   📝 Using {len(context_sources)} context source(s)")
            
            generator.generate_short_article(topic, context_sources)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
