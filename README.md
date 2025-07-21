# Star Citizen Handbook

An open-source guide for new and returning Star Citizen players, covering ships, missions, and core gameplay mechanics.

## Overview

**Star Citizen Handbook** is a community-driven resource designed to help players of all experience levels navigate the universe of Star Citizen. The handbook provides detailed guides, ship overviews, gameplay tips, and more, all organized for easy access and regular updates.

## Features

- **Beginner and Advanced Guides:** Step-by-step instructions for core gameplay, advanced mechanics, and in-game systems.
- **Ship Database:** Information and tips for a wide range of ships.
- **Concepts & Tips:** Explanations of key game concepts, trading tips, and referral information.
- **Visual Aids:** Screenshots and images to help illustrate guides and concepts.
- **Community Contributions:** Open to pull requests and suggestions from the community.

## Project Structure

```
archetypes/         # Hugo archetypes for new content
assets/css/         # Custom CSS for site styling
content/                # Main content directory
  guides/               # Step-by-step guides for gameplay and mechanics
  ships/                # Ship overviews, stats, and tips
  concepts/             # Explanations of game concepts and systems
  _index.md             # Section index and landing page
layouts/            # Hugo templates and partials
static/             # Static files (images, etc.)
themes/             # Hugo themes (Beautiful Hugo)
raw/                # Source material and drafts
hugo.toml           # Hugo configuration
```

## Getting Started

This project uses [Hugo](https://gohugo.io/) for static site generation.

### Prerequisites

- [Hugo](https://gohugo.io/getting-started/installing/) (extended version recommended)

### Running Locally

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/star-citizen-handbook.git
   cd star-citizen-handbook
   ```
2. Start the Hugo server:
   ```sh
   hugo server -D
   ```
3. Open your browser and go to `http://localhost:1313/` to view the site.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear messages.
4. Open a pull request describing your changes.

See `DEVELOPMENT_NOTES.md` for more details on content structure and style guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Beautiful Hugo](https://themes.gohugo.io/themes/beautifulhugo/) theme
- The Star Citizen community for ongoing support and contributions
