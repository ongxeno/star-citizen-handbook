
# Star Citizen Handbook

A comprehensive Thai-language guide for Star Citizen players, covering ships, gameplay mechanics, guides, and concepts. Built with Hugo and enhanced with AI-powered content generation and modern web features.

## Overview

**Star Citizen Handbook** is a modern, feature-rich resource for Star Citizen players, focused on Thai-language content. The handbook provides:

- **Comprehensive Content:** Detailed guides, ship reviews, gameplay mechanics, and concepts
- **AI-Powered Generation:** Automated content and cover image generation using Google Generative AI
- **Enhanced User Experience:** Responsive tables, image carousels, and modern web features
- **Thai Language Focus:** Native Thai content with consistent, friendly writing style


## Features

### Content & Automation
- **AI-Powered Content Generation:** Python scripts with Google Generative AI for automated article creation
- **Cover Image Generation:** Automated cover images for articles and guides
- **Template-Driven Workflow:** Markdown templates for consistent content structure
- **Thai Language Excellence:** Native Thai content with conversational tone and appropriate context

### Enhanced User Experience  
- **Responsive Tables:** Intelligent table breakout system for mobile devices
- **Image Carousels:** Dynamic image galleries for ship showcases and guides
- **Modern Hugo Architecture:** Page bundles, shortcodes, and optimized performance
- **Custom Styling:** Dark theme with responsive design and custom CSS

### Technical Features
- **Hugo v0.148+:** Modern static site generation with extended features
- **Beautiful Hugo Theme:** Professional theme with customizations
- **Responsive Design:** Mobile-first approach with CSS Grid and Flexbox
- **Performance Optimized:** Fast loading with optimized assets and images

## Project Structure

```
├── content/                    # Main content directory (Thai language)
│   ├── guides/                # Step-by-step gameplay guides
│   ├── ships/                 # Ship reviews, stats, and showcases
│   ├── concepts/              # Game mechanics and system explanations
│   ├── development/           # Monthly reports and project updates
│   └── _index.md             # Homepage content
├── generator/                 # AI-powered content generation tools
│   ├── blog_generator.py     # Main article generator with AI
│   ├── generate_article_cover.py  # Cover image generator
│   ├── blog_image_generator.py    # Image generation utilities
│   ├── constants.py          # Category and configuration constants
│   ├── prompts/             # Markdown templates for AI prompts
│   └── requirements.txt     # Python dependencies
├── layouts/                  # Hugo templates and customizations
│   ├── shortcodes/          # Custom shortcodes (carousel, tables, etc.)
│   ├── partials/            # Reusable template components
│   └── _default/            # Default page layouts
├── assets/css/              # Custom CSS and styling
├── static/                  # Static files (images, JavaScript)
│   ├── js/                  # Custom JavaScript (tables, effects)
│   └── img/                 # Site images and assets
├── wiki/                    # Development documentation
├── themes/beautifulhugo/    # Hugo theme
└── hugo.toml               # Hugo configuration
```


## Getting Started

### Prerequisites

- **Hugo v0.148+ (Extended):** [Download from Hugo website](https://gohugo.io/getting-started/installing/)
- **Python 3.10+:** For content generation scripts
- **Google Generative AI API Key:** [Get your API key](https://ai.google.dev/)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ongxeno/star-citizen-handbook.git
   cd star-citizen-handbook
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r generator/requirements.txt
   ```

3. **Configure API key:**
   Create a `.env` file in the `generator/` directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Start the development server:**
   ```bash
   hugo server --buildDrafts
   ```

5. **Open your browser:**
   Navigate to `http://localhost:1313/star-citizen-handbook/`


## Content Creation Workflow

### 1. Generate New Articles
```bash
# Generate a new article with AI assistance
python generator/blog_generator.py "Your Article Topic"

# Example: Generate a mining guide
python generator/blog_generator.py "Mining Guide for Beginners"
```

### 2. Create Cover Images  
```bash
# Generate cover image for existing article
python generator/generate_article_cover.py content/guides/your-article/index.md
```

### 3. Enhanced Content Features

#### Image Carousels (Page Bundles Only)
```markdown
<!-- Basic carousel -->
{{< carousel >}}

<!-- Carousel with custom settings -->
{{< carousel height="500px" interval="8000" >}}

<!-- Carousel from subdirectory -->
{{< carousel path="gallery/" >}}
```

#### Responsive Tables
```markdown
<!-- Tables automatically become responsive on mobile -->
{{< table-responsive >}}
| Ship | Price | Role |
|------|--------|------|
| Gladius | 90,000 aUEC | Light Fighter |
{{< /table-responsive >}}
```

### 4. Writing Guidelines
- **Language:** All content in Thai with friendly, conversational tone
- **Structure:** Use clear headings, bullet points, and summaries
- **Versioning:** Include `game_version` in front matter
- **Images:** Use page bundles for better organization


## Contributing

We welcome contributions from the Star Citizen community! Here's how you can help:

### Ways to Contribute
- **Content Updates:** Keep guides current with latest game versions
- **New Guides:** Write guides for new game mechanics or ships
- **Bug Reports:** Report issues with the website or content
- **Feature Requests:** Suggest new features or improvements

### Contribution Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-guide`
3. Make your changes following our style guidelines
4. Test locally with `hugo server --buildDrafts`
5. Commit with clear messages: `git commit -m "Add mining guide for Alpha 4.2"`
6. Push and create a Pull Request

### Documentation
See `wiki/` directory for detailed documentation:
- `manual-page-creation-guide.md` - Content creation guidelines
- `carousel-guide.md` - Image carousel usage
- `responsive-tables-guide.md` - Table enhancement guide

## Development Status

### Current Features ✅
- **Content Generation:** AI-powered article creation with Thai language
- **Enhanced Tables:** Responsive table system with intelligent breakout
- **Image Carousels:** Dynamic galleries for page bundles  
- **Modern Styling:** Custom CSS with dark theme
- **Performance:** Optimized Hugo build and asset loading

### Roadmap 🚧
- Search functionality (Algolia integration)
- Advanced image processing and optimization
- Community features and user interaction
- Multi-language support expansion
- Enhanced mobile experience


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Beautiful Hugo](https://themes.gohugo.io/themes/beautifulhugo/) theme
- Google Generative AI for content and image generation
- The Star Citizen community for ongoing support and contributions
