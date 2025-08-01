# AI-Powered Hugo Blog Post Generator

An intelligent Python script that automates the creation of Thai-language blog posts for the Star Citizen Handbook Hugo website using a multi-model AI workflow.

## Features

- 🤖 **Multi-Model AI Workflow**: Uses different AI models optimized for specific tasks
- 🇹🇭 **Thai Language Content**: Generates content specifically for Thai Star Citizen players
- 🏗️ **Hugo Integration**: Automatically creates properly formatted Hugo posts with front matter
- 📱 **Category Management**: Automatically places content in appropriate categories (ships, concepts, guides)
- 🔗 **SEO Optimized**: Generates SEO-friendly slugs, descriptions, and metadata
- 📝 **Markdown Formatting**: Creates properly formatted Markdown with Thai headers and English anchor IDs

## Workflow Steps

### Step 1: Structure Generation
Uses Gemini 2.5 Flash for fast, cost-effective content structuring.

### Step 2: Research Prompt Creation  
Also uses Gemini 2.5 Flash to create detailed research prompts.

### Step 3: Deep Research
Uses Gemini 2.5 Pro for its enhanced thinking, reasoning, and multimodal understanding to gather comprehensive information.

### Step 4: Content Formatting
Polishes the research data into a complete, well-formatted blog post with:
- Appropriate Thai language and tone
- Emoji integration
- Table of contents with anchor links
- Proper Hugo Markdown formatting

### Step 5: Project Integration
Adds the finished blog to the correct Hugo content directory and updates category indexes.

## Setup

### 1. Install Dependencies

```bash
cd generator
pip install -r requirements.txt
```

### 2. Configure API Key

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

3. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

Run the script with a topic as an argument:

```bash
python blog_generator.py "topic for the blog post"
```

### Examples

```bash
# Generate a ship guide
python blog_generator.py "Drake Cutlass Red medical ship complete guide"

# Generate a concept explanation  
python blog_generator.py "Star Citizen insurance system explained"

# Generate a gameplay guide
python blog_generator.py "How to mine quantanium efficiently"
```

## Content Categories

The script automatically determines the appropriate category:

- **ships** (ยานอวกาศ) - For spacecraft guides and reviews
- **concepts** (แนวคิดและระบบเกม) - For game mechanics and systems
- **guides** (คู่มือการเล่น) - For tutorials and how-to content

## Output

The script generates:

1. **Markdown File**: `content/{category}/{slug}.md` with:
   - YAML front matter with Thai metadata
   - Complete Thai content with proper formatting
   - Manual anchor IDs for navigation
   - Table of contents
   - Image placeholders

2. **Category Index Update**: Adds link to new post in the category's `_index.md`

## Content Guidelines

The generated content follows the project's coding instructions:

- ✅ All user-facing content in Thai language
- ✅ Technical terms and code remain in English  
- ✅ Manual anchor IDs: `## Thai Heading {#english-id}`
- ✅ Clear, helpful tone for gamers
- ✅ Appropriate emoji usage
- ✅ Hugo best practices

## File Structure

```
generator/
├── blog_generator.py      # Main script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your API key (git-ignored)
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Permission Errors**: Ensure write permissions to `content/` directory
4. **API Limits**: Check your Gemini API quota and rate limits

### Error Messages

- `GEMINI_API_KEY not found in .env file` - Add your API key to `.env`
- `Error in Step X` - Check API connectivity and quota
- `Category index not found` - Ensure category `_index.md` files exist

## Development

### Adding New Categories

1. Add category mapping in `HugoBlogGenerator.__init__()`:
```python
self.categories = {
    "ships": "ยานอวกาศ",
    "concepts": "แนวคิดและระบบเกม", 
    "guides": "คู่มือการเล่น",
    "new_category": "หมวดใหม่"
}
```

2. Create corresponding directory and `_index.md` in `content/`

### Customizing Models

Update model selection in `__init__()`:
```python
self.cost_effective_model = genai.GenerativeModel('gemini-2.5-flash')
self.deep_research_model = genai.GenerativeModel('gemini-2.5-pro')
```

## License

This generator follows the same license as the main Star Citizen Handbook project.
