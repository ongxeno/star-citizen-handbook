# Refactoring Summary - Blog Image Generator

## Overview of Changes

I've refactored the Star Citizen Handbook blog generator to separate the image generation functionality into a dedicated script. The refactoring includes:

1. Created a shared utilities module for Generative AI configuration
2. Developed a standalone blog image generator with an interactive workflow
3. Updated the main blog generator to use these new components
4. Improved the prompt template to better extract image prompts

## New Files

1. `genai_utils.py` - Common utilities for Generative AI configuration and functions
2. `blog_image_generator.py` - Standalone image generator script
3. `README_IMAGE_GENERATOR.md` - Documentation for the image generator

## Modified Files

1. `blog_generator.py` - Updated to use the shared utilities and integrate with the image generator
2. `prompts/short-article/short-article.md` - Updated format for cover image prompts

## Workflow

The new image generation workflow works as follows:

1. The blog generator extracts the cover image prompt from the generated content
2. If a prompt is found, it asks the user if they want to generate an image
3. If yes, it launches the image generator script with the blog content for context
4. The image generator:
   - Analyzes the content and suggests 3 prompt options
   - Lets the user select a prompt, iterate on it with feedback, or quit
   - When a prompt is selected, it generates an image using the chosen model and settings
   - Saves the image to the appropriate location
5. The blog generator updates the front matter with the correct image path

## Image Generation Configuration

The image generator supports three models:
- Imagen 4.0 Standard (`imagen-4.0-generate-preview-06-06`)
- Imagen 4.0 Ultra (`imagen-4.0-ultra-generate-preview-06-06`)
- Imagen 3.0 Legacy (`imagen-3.0-generate-002`)

These can be configured in the `genai_utils.py` file if needed.

## Usage Examples

### Standalone Image Generator

```bash
python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory" --aspect-ratio "16:9"
```

### From Blog Generator

The standard blog generation process will now include an option to generate a cover image:

```bash
python blog_generator.py --mode short-article "What is LTI?"
```

When the article is generated, you'll be prompted if you want to generate a cover image.
