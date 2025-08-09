#!/usr/bin/env python3
"""
Generative AI Utilities for Star Citizen Handbook

This module provides common utilities for working with Google Generative AI models,
including initialization, configuration, and helper functions.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_genai() -> Dict:
    """
    Configure Google Generative AI with API key and common settings.
    
    Returns:
        Dict: Dictionary containing configured model instances
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    genai.configure(api_key=api_key)
    
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
    models = {
        "cost_effective": genai.GenerativeModel(
            'gemini-2.5-flash',
            safety_settings=safety_settings
        ),
        "deep_research": genai.GenerativeModel(
            'gemini-2.5-pro',
            safety_settings=safety_settings
        ),
        "imagen_standard": {
            "model_name": "imagen-4.0-generate-preview-06-06",
            "description": "Standard image generation model (up to 4 images)"
        },
        "imagen_ultra": {
            "model_name": "imagen-4.0-ultra-generate-preview-06-06",
            "description": "Ultra-quality image generation model (1 image)"
        },
        "imagen_legacy": {
            "model_name": "imagen-3.0-generate-002",
            "description": "Legacy image generation model (up to 4 images)"
        }
    }
    
    return models

def generate_image(prompt: str, model_name: str = "imagen-4.0-generate-preview-06-06", 
                   number_of_images: int = 1, aspect_ratio: str = "1:1") -> List:
    """
    Generate images using Google's Imagen models
    
    Args:
        prompt (str): Text prompt for image generation
        model_name (str): Imagen model name to use
        number_of_images (int): Number of images to generate (1-4)
        aspect_ratio (str): Aspect ratio for the generated image ("1:1", "3:4", "4:3", "9:16", "16:9")
        
    Returns:
        List: List of generated image objects
    """
    # Create client
    client = genai.Client()
    
    # Validate model name
    valid_models = [
        "imagen-4.0-generate-preview-06-06",
        "imagen-4.0-ultra-generate-preview-06-06",
        "imagen-3.0-generate-002"
    ]
    
    if model_name not in valid_models:
        raise ValueError(f"Invalid model name. Must be one of: {', '.join(valid_models)}")
    
    # For ultra model, only 1 image can be generated
    if model_name == "imagen-4.0-ultra-generate-preview-06-06" and number_of_images > 1:
        print(f"⚠️ Ultra model only supports generating 1 image. Setting number_of_images to 1.")
        number_of_images = 1
    
    # Validate number of images
    if number_of_images < 1 or number_of_images > 4:
        raise ValueError("Number of images must be between 1 and 4")
    
    # Validate aspect ratio
    valid_aspect_ratios = ["1:1", "3:4", "4:3", "9:16", "16:9"]
    if aspect_ratio not in valid_aspect_ratios:
        raise ValueError(f"Invalid aspect ratio. Must be one of: {', '.join(valid_aspect_ratios)}")
    
    # Generate images
    from google.genai import types
    response = client.models.generate_images(
        model=model_name,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=number_of_images,
            aspect_ratio=aspect_ratio,
        )
    )
    
    return response.generated_images

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
