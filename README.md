
# Star Citizen Handbook

An open-source, AI-powered Thai-language guide for new and returning Star Citizen players, covering ships, missions, and core gameplay mechanics. Includes automated content and image generation, and native Thai writing style.


## Overview

**Star Citizen Handbook** is a community-driven, automation-enhanced resource for Star Citizen, focused on Thai-language content. The handbook provides:
- Detailed guides, ship overviews, gameplay tips, and more
- Automated article and cover image generation using Python scripts and Google Generative AI
- Consistent, friendly Thai writing style with summaries and appropriate emoji


## Features

- **Automated Content Generation:**
   - Python scripts (`generator/blog_generator.py`, `generator/generate_article_cover.py`) automate article structure, front matter, and cover image creation.
   - Uses Google Generative AI for Thai-language content and image prompt generation.
- **Template-Driven Workflow:**
   - Markdown templates for article structure and image prompts (see `generator/prompts/`).
- **Consistent Thai Writing Style:**
   - Friendly, conversational tone with summaries and appropriate emoji.
   - All content is written and maintained in Thai.
- **Modern Hugo Site Structure:**
   - Each article in its own folder with `index.md` and a generated cover image.
   - Dynamic navigation using `_index.md` files.
- **Community Contributions:**
   - Open to pull requests and suggestions from the community.

archetypes/         # Hugo archetypes for new content

## Project Structure

```
archetypes/         # Hugo archetypes for new content
assets/css/         # Custom CSS for site styling
content/            # Main content directory (Thai, organized by category)
   guides/           # Step-by-step guides for gameplay and mechanics
   ships/            # Ship overviews, stats, and tips
   concepts/         # Explanations of game concepts and systems
   development/      # Monthly reports, dev notes, and project updates
   _index.md         # Section index and landing page
generator/          # Python automation scripts and templates
   blog_generator.py         # Main article/content generator
   generate_article_cover.py # Cover image and structure generator
   blog_image_generator.py   # Image generation utility
   constants.py              # Centralized category config
   prompts/                  # Markdown templates for AI prompts
layouts/            # Hugo templates and partials
static/             # Static files (images, etc.)
themes/             # Hugo themes (Beautiful Hugo)
raw/                # Source material and drafts
hugo.toml           # Hugo configuration
```


## Getting Started

This project uses [Hugo](https://gohugo.io/) for static site generation, and Python for content automation.

### Prerequisites

- [Hugo](https://gohugo.io/getting-started/installing/) (extended version recommended)
- Python 3.10+
- [Google Generative AI API key](https://ai.google.dev/)
- `pip install -r generator/requirements.txt`

### Running Locally

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/star-citizen-handbook.git
   cd star-citizen-handbook
   ```
2. Install Python dependencies:
   ```sh
   pip install -r generator/requirements.txt
   ```
3. Add your `GEMINI_API_KEY` to a `.env` file in the `generator/` directory.
4. Start the Hugo server:
   ```sh
   hugo server -D
   ```
5. Open your browser and go to `http://localhost:1313/` to view the site.


## Content & Automation Workflow

### Article Generation
- Use `python generator/blog_generator.py "<topic>"` to generate a new article structure and content outline in Thai, with Hugo front matter and dynamic category selection.
- The script uses markdown prompt templates in `generator/prompts/` and category config in `generator/constants.py`.

### Cover Image Generation
- Use `python generator/generate_article_cover.py path/to/article/index.md` to generate a cover image and update the article front matter.
- Image prompts are generated using the template in `generator/prompts/short-article/image_prompt.md`.

### Templates & Localization
- All prompt templates are markdown files in `generator/prompts/`.
- All content is written in Thai, with a friendly, conversational style and appropriate emoji.
- Summaries and references are included at the end of each article.


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear messages.
4. Open a pull request describing your changes.

See `DEVELOPMENT_NOTES.md` for more details on content structure, automation, and style guidelines.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Beautiful Hugo](https://themes.gohugo.io/themes/beautifulhugo/) theme
- Google Generative AI for content and image generation
- The Star Citizen community for ongoing support and contributions
