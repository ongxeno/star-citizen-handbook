
# Project Overview: Star Citizen Handbook

**Last Updated:** 2025-07-18

## 1. Project Goal

The primary goal of this project is to create a clear, user-friendly, Thai-language guide for new and intermediate Star Citizen players. The website, `star-citizen-handbook`, will be hosted on GitHub Pages and serve as a go-to reference to help players become self-sufficient in the 'Verse.


## 2. Core Principles

* **Thai Language Only:** All content is written and maintained in Thai (`th`).
* **Content Versioning:** Every guide and content page must be tagged with the specific game version it applies to, using the `game_version` parameter in the front matter (e.g., `game_version: "Alpha 3.23.1"`).


## 3. Website Features & Functionality

* **Clean, Modern UI:**
    * Material Design-inspired dark theme that complements Star Citizen's aesthetic.
    * Uncluttered layout with proper whitespace for improved readability.
    * System fonts with Noto Sans Thai for optimal performance and Thai language support.

* **Smart Navigation:**
    * Sticky navigation header with auto-hiding behavior on scroll.
    * Algolia DocSearch integration for powerful, fast searching.
    * Auto-generated breadcrumbs using Hugo's built-in features.

* **Mobile-First Design:**
    * Responsive layout using CSS Grid and Flexbox.
    * Touch-optimized menus and interactions.
    * Optimized images using Hugo image processing.

* **Version Management:**
    * Game version banner on all guide pages.
    * Visual indicators for outdated content.
    * Version filtering in search results.

* **Enhanced Content:**
    * Lightbox galleries using PhotoSwipe.
    * Copy buttons for code blocks using Clipboard.js.
    * Syntax highlighting with Chroma (Hugo default).


## 4. Technology Stack

* **Static Site Generator:** Hugo (latest)
* **Key Hugo Modules/Plugins:**
    * Algolia search integration
    * Hugo image processing
    * RSS feeds
    * SEO optimization
    * Sitemap generation

* **Front-end:**
    * Vanilla JavaScript (no heavy frameworks)
    * Sass for styling
    * CSS Grid & Flexbox for layouts
    * PhotoSwipe for image galleries
    * Clipboard.js for copy functionality

* **Development Tools:**
    * Go (Hugo requirement)
    * Node.js & npm for front-end tooling
    * GitHub Actions for CI/CD

---

## 5. Development Roadmap


### **Phase 1: Project Setup & Foundation**

* **Objective:** Set up Hugo project with Thai language support and basic functionality.
* **Key Tasks:**
    * [ ] Initialize Hugo project with recommended structure:
        ```
        .
        ├── config.toml
        ├── content/
        │   ├── guides/
        │   ├── ships/
        │   └── concepts/
        ├── data/
        │   └── ships.yml
        ├── layouts/
        │   ├── _default/
        │   ├── guides/
        │   ├── ships/
        │   └── concepts/
        ├── assets/
        ├── static/
        └── themes/
        ```
    * [ ] Configure Hugo modules and dependencies:
        * Set up Algolia search integration
        * Configure SEO and sitemap
    * [ ] Create base layouts and partials:
        * Default layout
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
    * [ ] **Ship Database:**
        * Create ship content structure
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