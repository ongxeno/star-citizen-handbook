# Project Overview: Star Citizen Handbook

**Last Updated:** 2025-07-18

## 1. Project Goal

The primary goal of this project is to create a clear, user-friendly, and multilingual guide for new and intermediate Star Citizen players. The website, `star-citizen-handbook`, will be hosted on GitHub Pages and serve as a go-to reference to help players become self-sufficient in the 'Verse.

## 2. Core Principles

* **Multilingual Support:** The site is built to support multiple languages from the ground up.
    * **Initial Languages:** Thai (`th`) and English (`en`).
    * **Default Language:** Thai (`th`).
    * **Structure:** Multilingual content managed through Jekyll's [Polyglot](https://github.com/untra/polyglot) plugin.

* **Content Versioning:** This is a critical feature. Every guide and content page must be tagged with the specific game version it applies to, using the `game_version` parameter in the front matter (e.g., `game_version: "Alpha 3.23.1"`).

## 3. Website Features & Functionality

* **Clean, Modern UI:**
    * Material Design-inspired dark theme that complements Star Citizen's aesthetic.
    * Uncluttered layout with proper whitespace for improved readability.
    * System fonts with Noto Sans Thai for optimal performance and Thai language support.

* **Smart Navigation:**
    * Sticky navigation header with auto-hiding behavior on scroll.
    * Algolia DocSearch integration for powerful, fast searching.
    * Auto-generated breadcrumbs using Jekyll's built-in collection features.

* **Mobile-First Design:**
    * Responsive layout using CSS Grid and Flexbox.
    * Touch-optimized menus and interactions.
    * Optimized images using Jekyll Picture Tag plugin.

* **Language Features:**
    * Language selector in the header (English/ภาษาไทย).
    * LocalStorage-based language preference.
    * Fallback content handling when translations are missing.

* **Version Management:**
    * Game version banner on all guide pages.
    * Visual indicators for outdated content.
    * Version filtering in search results.

* **Enhanced Content:**
    * Lightbox galleries using PhotoSwipe.
    * Copy buttons for code blocks using Clipboard.js.
    * Syntax highlighting with Rouge.

## 4. Technology Stack

* **Static Site Generator:** Jekyll 4.3+
* **Key Plugins:**
    * `jekyll-polyglot` - Multilingual support
    * `jekyll-algolia` - Search functionality
    * `jekyll-picture-tag` - Responsive images
    * `jekyll-feed` - RSS feeds
    * `jekyll-seo-tag` - SEO optimization
    * `jekyll-sitemap` - Sitemap generation

* **Front-end:**
    * Vanilla JavaScript (no heavy frameworks)
    * Sass for styling
    * CSS Grid & Flexbox for layouts
    * PhotoSwipe for image galleries
    * Clipboard.js for copy functionality

* **Development Tools:**
    * Ruby 3.2+ (Jekyll requirement)
    * Bundler for dependency management
    * Node.js & npm for front-end tooling
    * GitHub Actions for CI/CD

---

## 5. Development Roadmap

### **Phase 1: Project Setup & Foundation**

* **Objective:** Set up Jekyll project with multilingual support and basic functionality.
* **Key Tasks:**
    * [ ] Initialize Jekyll project with recommended structure:
        ```
        .
        ├── _config.yml
        ├── _data/
        │   ├── i18n/
        │   │   ├── en.yml
        │   │   └── th.yml
        │   └── ships.yml
        ├── _includes/
        ├── _layouts/
        ├── _plugins/
        ├── _sass/
        ├── assets/
        └── collections/
            ├── _guides/
            ├── _ships/
            └── _concepts/
        ```
    * [ ] Configure Jekyll plugins and dependencies:
        * Set up Bundler and Gemfile
        * Configure jekyll-polyglot for multilingual support
        * Set up jekyll-algolia for search
    * [ ] Create base layouts and includes:
        * Default layout with language switcher
        * Guide layout with version banner
        * Ship template for vessel information
    * [ ] Implement core styling:
        * Dark theme setup using Sass
        * Responsive navigation
        * Typography system

### **Phase 2: Core Features & Initial Content**

* **Objective:** Implement key features and create essential guides.
* **Key Tasks:**
    * [ ] **Search Implementation:**
        * Set up Algolia DocSearch
        * Create search UI components
        * Configure language-aware indexing
    * [ ] **Ship Database:**
        * Create ship collection structure
        * Design ship detail templates
        * Add initial ship data (10-15 starter ships)
    * [ ] **Core Guides:**
        * From Hab to Orbit (Template Guide)
        * Basic Mining Guide
        * Bounty Hunting Primer
        * Delivery Mission Guide
    * [ ] **Reference Content:**
        * Mining Locations & Prices
        * Key Bindings Reference
        * Ship Insurance Guide

### **Phase 3: Polish & Community Features**

* **Objective:** Enhance UX and implement community features.
* **Key Tasks:**
    * [ ] **UI Enhancements:**
        * Add PhotoSwipe for image galleries
        * Implement copy-to-clipboard functionality
        * Add reading progress indicator
        * Optimize for mobile devices
    * [ ] **Community Features:**
        * Create contribution guidelines
        * Set up issue templates
        * Add commenting system (optional)
    * [ ] **Translation Management:**
        * Implement translation status tracking
        * Add missing translation indicators
        * Set up automated translation workflows