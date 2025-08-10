#!/usr/bin/env python3
"""
Generative AI Utilities for Star Citizen Handbook

This module provides common utilities for working with Google Generative AI models,
including initialization, configuration, and helper functions for both text and image generation.
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from google import genai
from google.genai import types
from PIL import Image, ImageDraw
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_genai() -> Dict:
    """
    Configure Google Generative AI with API key and common settings.
    
    Returns:
        Dict: Dictionary containing configured model instances and info
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    # Create the client
    client = genai.Client(api_key=api_key)
    
    # Text generation models information
    text_models = {
        "cost_effective": "gemini-2.5-flash",
        "deep_research": "gemini-2.5-pro"
    }
    
    # Image generation models information (Imagen - not accessible to most users)
    imagen_models = {
        "standard": {
            "model_name": "imagen-4.0-generate-preview-06-06",
            "description": "Imagen 4"
        },
        "premium": {
            "model_name": "imagen-4.0-ultra-generate-preview-06-06",
            "description": "Imagen 4 Ultra"
        },
        "legacy": {
            "model_name": "imagen-3.0-generate-002",
            "description": "Imagen 3"
        }
    }
    
    # Gemini image generation model
    gemini_image_model = "gemini-2.0-flash-preview-image-generation"
    
    return {
        "client": client,
        "text_models": text_models,
        "imagen_models": imagen_models,
        "gemini_image_model": gemini_image_model
    }

def generate_text(prompt: str, model_key: str = "deep_research") -> str:
    """
    Generate text using Google's Gemini models
    
    Args:
        prompt (str): Text prompt for generation
        model_key (str): Key for the model to use (e.g., "cost_effective" or "deep_research")
        
    Returns:
        str: Generated text response
    """

    models = configure_genai()
    client = models["client"]
    text_models = models["text_models"]
    
    # Validate model exists
    if model_key not in text_models:
        raise ValueError(f"Model key '{model_key}' not found. Available models: {list(text_models.keys())}")
    
    # Get the model name
    model_name = text_models[model_key]
    
    # Generate content
    response = client.models.generate_content(
        model=model_name, 
        contents=prompt
    )
    
    # Return the response text
    return response.text

def generate_image_imagen(prompt: str, model_key: str = "standard", aspect_ratio: str = "16:9", output_path: Optional[Path] = None) -> Dict:
    """
    Generate images using Google's Imagen API (not accessible to most users)
    
    Args:
        prompt (str): Text prompt for image generation
        model_key (str): Key for the model to use (e.g., "standard" or "premium")
        aspect_ratio (str): Aspect ratio for the generated image ("1:1", "16:9", etc.)
        output_path (Optional[Path]): If provided, save the generated image to this path
        
    Returns:
        Dict: Dictionary containing image data and metadata
    """
    # Configure and get the API key
    models = configure_genai()
    client = models["client"]
    imagen_models = models["imagen_models"]
    
    # Validate model exists
    if model_key not in imagen_models:
        raise ValueError(f"Model key '{model_key}' not found. Available models: {list(imagen_models.keys())}")
    
    model_info = imagen_models[model_key]
    model_name = model_info["model_name"]
    
    try:
        # Create an enhanced prompt with aspect ratio information
        enhanced_prompt = f"""
        Create a detailed, high-quality image for a Star Citizen game blog with the following description:
        
        {prompt}
        
        The image should be in {aspect_ratio} aspect ratio and suitable as a cover image for a blog post.
        """
        
        # Generate the image
        response = client.models.generate_images(
            model=model_name,
            prompt=enhanced_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # Process the response
        if response.generated_images and len(response.generated_images) > 0:
            # Extract the first image
            generated_image = response.generated_images[0]
            
            # Convert to bytes
            img_bytes = BytesIO()
            generated_image.image.save(img_bytes, format="JPEG")
            img_bytes.seek(0)
            
            # Save to output_path if provided
            if output_path:
                # Ensure parent directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                # Save the image
                generated_image.image.save(output_path, format="JPEG")
                print(f"✅ Image saved to: {output_path.absolute()}")
            
            return {
                "success": True,
                "model": model_key,
                "prompt": prompt,
                "image_data": img_bytes.getvalue(),
                "mime_type": "image/jpeg",
                "output_path": str(output_path) if output_path else None
            }
        else:
            return {
                "success": False,
                "error": "No images were generated in the response"
            }
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_image(prompt: str, aspect_ratio: str = "16:9", output_path: Optional[Path] = None) -> Dict:
    """
    Generate images using Gemini's built-in image generation capability
    
    Args:
        prompt (str): Text prompt for image generation
        aspect_ratio (str): Aspect ratio for the generated image ("1:1", "16:9", etc.)
        output_path (Optional[Path]): If provided, save the generated image to this path
        
    Returns:
        Dict: Dictionary containing image data and metadata
    """
    # Configure and get models
    models = configure_genai()
    client = models["client"]
    model_name = models["gemini_image_model"]
    
    try:
        # Create an enhanced prompt with aspect ratio information
        contents = f"Create a detailed, high-quality image for a Star Citizen game blog with the following description: {prompt}. The image should be in {aspect_ratio} aspect ratio and suitable as a cover image for a blog post."
        
        # Generate content with image - strictly following the sample
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        # Process the response - following the sample pattern
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
                text_response = part.text
            elif part.inline_data is not None:
                # Save the image directly to output_path if provided
                image = Image.open(BytesIO(part.inline_data.data))
                image_bytes = BytesIO()
                image.save(image_bytes, format="PNG")
                image_bytes.seek(0)

                if output_path:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(output_path)
                    print(f"✅ Image saved to: {output_path.absolute()}")

                image_data = image_bytes.getvalue()

                return {
                    "success": True,
                    "model": "gemini",
                    "prompt": prompt,
                    "image_data": image_data,
                    "mime_type": "image/png",
                    "output_path": str(output_path) if output_path else None
                }
        
        # If we get here, create a placeholder with the text response
        if 'text_response' in locals():
            # Create a simple placeholder image with PIL
            img = Image.new('RGB', (1280, 720), color=(30, 30, 30))
            d = ImageDraw.Draw(img)
            
            # Add text
            title = "GENERATED TEXT (NO IMAGE)"
            prompt_text = f"Prompt: {prompt[:80]}"
            response_text = text_response[:300] + "..." if len(text_response) > 300 else text_response
            
            # Simple text rendering
            d.text((40, 40), title, fill=(255, 200, 0))
            d.text((40, 80), prompt_text, fill=(255, 255, 255))
            d.text((40, 120), response_text, fill=(200, 200, 200), spacing=10)
            
            # Save the image
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            # Save to output_path if provided
            if output_path:
                # Ensure parent directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                # Save the image
                img.save(output_path)
                print(f"✅ Placeholder image saved to: {output_path.absolute()}")
            
            return {
                "success": True,
                "model": "gemini-text",
                "prompt": prompt,
                "image_data": img_bytes.getvalue(),
                "mime_type": "image/png",
                "text_response": text_response,
                "output_path": str(output_path) if output_path else None
            }
            
        else:
            return {
                "success": False,
                "error": "No candidates or parts found in the response"
            }
    except Exception as e:
        print(f"❌ Error generating image with Gemini: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def get_project_paths() -> Dict[str, Path]:
    """
    Get common project paths
    
    Returns:
        Dict[str, Path]: Dictionary of common project paths
    """
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / "content"
    static_dir = project_root / "static"
    img_dir = static_dir / "img"
    
    return {
        "script_dir": script_dir,
        "project_root": project_root,
        "content_dir": content_dir,
        "static_dir": static_dir,
        "img_dir": img_dir
    }
