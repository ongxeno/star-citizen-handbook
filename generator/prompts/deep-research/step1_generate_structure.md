You are an expert Hugo content creator and Star Citizen game expert. You will be creating content for a Thai audience, but some parts of the metadata must be in English for technical reasons.

Topic: {{TOPIC}}

Generate a complete blog structure with:
1. Hugo front matter in YAML format.
2. A content outline with main sections.
3. The appropriate category.

**`category`**: Must be one of: {{MAIN_CATEGORIES}}.
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
    "category": "{{MAIN_CATEGORIES}}",
    "slug": "english-url-friendly-slug",
    "outline": [
        {{
            "section": "Thai section title",
            "subsections": ["Thai subsection 1", "Thai subsection 2"],
            "anchor_id": "english-anchor-id"
        }}
    ]
}}
