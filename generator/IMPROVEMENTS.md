# Blog Generator Improvements

## Overview of Changes

The Star Citizen Handbook blog generator has been improved with the following enhancements:

1. **Cover Image Generation Workflow**
   - Simplified the workflow by always asking to generate a cover image for articles
   - Removed the cover image prompt extraction from the content
   - Image prompts are now generated directly from the article content

2. **Interactive Image Generation**
   - Added numbered options for model and aspect ratio selection
   - Added confirmation step before generating images
   - Enhanced prompt iteration workflow:
     - Option to go back to main selection from iteration mode
     - Improved prompts replace the current pool for easier selection
   - Better user experience with clear numbering and descriptions

## Usage Changes

### Blog Generation

The blog generation workflow now automatically offers to generate a cover image after the article is created:

```
✍️ Generating Short Article for: 'What is LTI?'
...
🎉 Short article generation completed successfully!
🖼️ Would you like to generate a cover image for this article?
Generate image? (y/n): 
```

### Image Generation

The image generator now has an improved interactive workflow:

1. Select a prompt (1-3), iterate with feedback ('i'), or quit ('q')
2. When iterating:
   - Choose which prompt to improve or 'b' to go back
   - Enter feedback for improving the prompt
   - The improved prompts replace the current options
3. When selecting a prompt:
   - Confirmation is required before proceeding
   - Model selection uses numbered options (1-3)
   - Aspect ratio selection uses numbered options (1-5)

## Technical Changes

1. Removed cover image prompt from the short-article.md template
2. Modified generate_short_article to always ask for image generation
3. Enhanced the interactive_workflow in blog_image_generator.py:
   - Added confirmation for selected prompts
   - Added numbered options for model and aspect ratio selection
   - Improved prompt iteration with back option
   - Improved prompts replace the current pool for easier selection
