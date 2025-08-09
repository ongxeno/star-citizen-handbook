# Blog Image Generator for Star Citizen Handbook

This utility generates cover images for blog posts using Google's Gemini AI models.

## Features

- Generates image prompt suggestions based on blog content
- Interactive workflow for selecting and refining prompts
- Supports multiple image generation models:
  - Imagen 4.0 Standard (up to 4 images)
  - Imagen 4.0 Ultra (highest quality, 1 image)
  - Imagen 3.0 (legacy)
- Multiple aspect ratios (1:1, 3:4, 4:3, 9:16, 16:9)
- Automatic conversion from PNG to JPG when needed

## Usage

### Standalone Mode

```bash
python blog_image_generator.py --content "path/to/content.md" --output "path/to/output/directory" --aspect-ratio "16:9"
```

Arguments:
- `--content, -c`: Path to the blog content file or the content text itself
- `--output, -o`: Directory to save the generated image to
- `--aspect-ratio, -a`: Aspect ratio for the image (1:1, 3:4, 4:3, 9:16, 16:9) - default: 16:9

### Used by Blog Generator

The main blog generator script will automatically extract image prompts from the generated content and offer to run the image generator. The workflow is:

1. Blog content is generated with an embedded image prompt
2. User is prompted whether to generate an image
3. If yes, the image generator is launched with the blog content for context
4. The user can select from generated prompts or refine them
5. The generated image is saved to the appropriate location
6. The blog's front matter is updated with the correct image path

## Configuration

The image generation models and parameters are configured in the `genai_utils.py` file.

## Requirements

- Google Generative AI library
- Python dotenv
- Pillow (PIL) for image processing
