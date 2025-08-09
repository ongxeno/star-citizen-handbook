#!/usr/bin/env python3
"""
Comprehensive Test Script for Star Citizen Handbook Generator

This script tests all the AI generation capabilities:
1. Text generation with cost-effective model (gemini-2.5-flash)
2. Text generation with deep research model (gemini-2.5-pro)
3. Image generation with Imagen API (generate_image_imagen)
4. Image generation with Gemini (generate_image)

All generated images are saved to the generator/build/test directory.
"""

import os
import sys
from pathlib import Path
from PIL import Image
from io import BytesIO
import time

# Add the current directory to the path so we can import genai_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the utils module
from genai_utils import configure_genai, generate_text, generate_image, generate_image_imagen

# Test configuration
TEST_OUTPUT_DIR = Path(__file__).parent / "build" / "test"
# Ensure the test output directory exists
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def test_text_generation_cost_effective():
    """Test text generation with the cost-effective model (gemini-2.5-flash)"""
    print("\n========== Testing Text Generation (Cost Effective) ==========")
    
    # Test prompt
    prompt = "Write a one-paragraph introduction about Star Citizen game for new players"
    print(f"Prompt: {prompt}")
    
    try:
        # Generate text
        start_time = time.time()
        response = generate_text(prompt, model_key="cost_effective")
        end_time = time.time()
        
        # Print results
        print(f"✅ Generation completed in {end_time - start_time:.2f} seconds")
        print("\nGenerated text:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        # Save the output to a file
        output_path = TEST_OUTPUT_DIR / "text_cost_effective.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\n")
            f.write(response)
        
        print(f"✅ Output saved to: {output_path.absolute()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_generation_deep_research():
    """Test text generation with the deep research model (gemini-2.5-pro)"""
    print("\n========== Testing Text Generation (Deep Research) ==========")
    
    # Test prompt
    prompt = "Explain the concept of 'Death of a Spaceman' in Star Citizen and how it affects gameplay"
    print(f"Prompt: {prompt}")
    
    try:
        # Generate text
        start_time = time.time()
        response = generate_text(prompt, model_key="deep_research"s)
        end_time = time.time()
        
        # Print results
        print(f"✅ Generation completed in {end_time - start_time:.2f} seconds")
        print("\nGenerated text:")
        print("-" * 80)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 80)
        
        # Save the output to a file
        output_path = TEST_OUTPUT_DIR / "text_deep_research.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\n")
            f.write(response)
        
        print(f"✅ Output saved to: {output_path.absolute()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_generation_imagen():
    """Test image generation with Imagen API (likely not accessible to most users)"""
    print("\n========== Testing Image Generation (Imagen API) ==========")
    
    # Test prompt
    prompt = "A Star Citizen Bengal carrier spacecraft orbiting a moon, with detailed mechanical features"
    print(f"Prompt: {prompt}")
    
    try:
        # Generate image
        output_path = TEST_OUTPUT_DIR / "image_imagen.png"
        start_time = time.time()
        
        response = generate_image_imagen(
            prompt=prompt,
            model_key="standard",  # Using the standard quality
            aspect_ratio="16:9",
            output_path=output_path
        )
        
        end_time = time.time()
        
        # Check results
        print(f"✅ Generation completed in {end_time - start_time:.2f} seconds")
        print(f"Response success: {response['success']}")
        print(f"Model used: {response.get('model', 'unknown')}")
        
        if response["success"] and response.get("image_data"):
            print(f"✅ Image saved to: {output_path.absolute()}")
            
            try:
                # Verify the image
                img = Image.open(output_path)
                print(f"Image size: {img.size}")
                print(f"Image format: {img.format}")
                print("✅ Valid image generated!")
                return True
            except Exception as img_err:
                print(f"⚠️ Image validation failed: {img_err}")
                return False
        else:
            print(f"❌ Image generation failed: {response.get('error', 'Unknown error')}")
            
            # If we have a text response, save it
            if response.get("text_response"):
                text_path = TEST_OUTPUT_DIR / "image_imagen_text_response.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(response["text_response"])
                print(f"⚠️ Text response saved to: {text_path.absolute()}")
            
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_generation_gemini():
    """Test image generation with Gemini"""
    print("\n========== Testing Image Generation (Gemini) ==========")
    
    # Test prompt
    prompt = "A Star Citizen character in a spacesuit exploring a crashed spaceship on an alien planet"
    print(f"Prompt: {prompt}")
    
    try:
        # Generate image
        output_path = TEST_OUTPUT_DIR / "image_gemini.png"
        start_time = time.time()
        
        response = generate_image(
            prompt=prompt,
            aspect_ratio="16:9",
            output_path=output_path
        )
        
        end_time = time.time()
        
        # Check results
        print(f"✅ Generation completed in {end_time - start_time:.2f} seconds")
        print(f"Response success: {response['success']}")
        print(f"Model used: {response.get('model', 'unknown')}")
        
        if response["success"] and response.get("image_data"):
            print(f"✅ Image saved to: {output_path.absolute()}")
            
            try:
                # Verify the image
                img = Image.open(output_path)
                print(f"Image size: {img.size}")
                print(f"Image format: {img.format}")
                print("✅ Valid image generated!")
                
                # For text-based image responses, also show the text
                if response.get("text_response"):
                    print(f"📝 Image based on text response: {response['text_response'][:100]}...")
                    
                    # Save the text response
                    text_path = TEST_OUTPUT_DIR / "image_gemini_text_response.txt"
                    with open(text_path, "w", encoding="utf-8") as f:
                        f.write(response["text_response"])
                    print(f"✅ Text response saved to: {text_path.absolute()}")
                
                return True
            except Exception as img_err:
                print(f"⚠️ Image validation failed: {img_err}")
                return False
        else:
            print(f"❌ Image generation failed: {response.get('error', 'Unknown error')}")
            
            # If we have a text response, save it
            if response.get("text_response"):
                text_path = TEST_OUTPUT_DIR / "image_gemini_text_response.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(response["text_response"])
                print(f"⚠️ Text response saved to: {text_path.absolute()}")
            
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all the tests and provide a summary"""
    print("=" * 80)
    print("Starting Comprehensive Test Suite for Star Citizen Handbook Generator")
    print("=" * 80)
    
    # Run all tests
    results = {}
    
    print("\nTesting text generation...")
    results["text_cost_effective"] = test_text_generation_cost_effective()
    results["text_deep_research"] = test_text_generation_deep_research()
    
    print("\nTesting image generation...")
    results["image_imagen"] = test_image_generation_imagen()
    results["image_gemini"] = test_image_generation_gemini()
    
    # Print summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    print("\nText Generation:")
    print(f"  Cost Effective Model: {'✅ Passed' if results['text_cost_effective'] else '❌ Failed'}")
    print(f"  Deep Research Model: {'✅ Passed' if results['text_deep_research'] else '❌ Failed'}")
    
    print("\nImage Generation:")
    print(f"  Imagen API: {'✅ Passed' if results['image_imagen'] else '❌ Failed'}")
    print(f"  Gemini: {'✅ Passed' if results['image_gemini'] else '❌ Failed'}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ All tests passed successfully!")
    else:
        print("⚠️ Some tests failed. See details above.")
    print("=" * 80)
    
    # Print output directory
    print(f"\nAll test outputs are saved in: {TEST_OUTPUT_DIR.absolute()}")

if __name__ == "__main__":
    main()
