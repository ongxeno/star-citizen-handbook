
# Project Overview: Star Citizen Handbook

**Last Updated:** August 16, 2025  
**Current Game Version:** Alpha 4.2.1 PTU  
**Hugo Version:** v0.148.1+extended  

## 1. Project Goal

Create a comprehensive, modern Thai-language guide for Star Citizen players that combines AI-powered content generation with enhanced web features. The website serves as a complete resource hub for new and intermediate players to master the game's complex systems and mechanics.

## 2. Project Status: Production Ready ✅

The project has evolved significantly beyond its initial roadmap and is now a fully functional, feature-rich website with:

- **50+ guides and articles** covering ships, gameplay, concepts, and development updates
- **AI-powered content generation** with Google Generative AI integration
- **Enhanced user experience** with responsive tables and image carousels
- **Modern Hugo architecture** with custom shortcodes and optimizations


## 3. Core Principles

* **Thai Language Excellence:** All content written in native Thai with conversational, friendly tone
* **Version Accuracy:** Content tagged with specific game versions (`game_version` parameter)
* **AI-Enhanced Workflow:** Google Generative AI integration for content creation and image generation
* **Modern Web Standards:** Responsive design, performance optimization, and accessibility
* **Community-Driven:** Open source with contribution guidelines and collaborative development


## 4. Implemented Features & Technology Stack

### Current Features ✅

#### Content Management
- **AI-Powered Generation:** Automated article creation with Google Generative AI
- **Cover Image Generation:** Automated cover images using AI image prompts
- **Template-Driven Workflow:** Markdown templates for consistent content structure
- **Version Management:** Game version tracking in all content front matter

#### Enhanced User Experience  
- **Responsive Tables:** Intelligent table breakout system for mobile devices with content-aware detection
- **Image Carousels:** Dynamic image galleries supporting page bundles with smooth transitions
- **Modern Styling:** Custom dark theme with CSS Grid/Flexbox responsive layouts
- **Performance Optimization:** Asset optimization and fast Hugo builds

#### Technical Architecture
- **Hugo v0.148+ Extended:** Latest static site generation with advanced features
- **Beautiful Hugo Theme:** Professional theme with extensive customizations
- **Custom Shortcodes:** `carousel`, `table-responsive`, and `youtube` shortcodes
- **JavaScript Enhancements:** Responsive tables, parallax effects, and lens effects
- **Page Bundle Architecture:** Organized content structure with co-located assets

### Technology Stack

#### Core Platform
- **Static Site Generator:** Hugo v0.148.1+extended
- **Theme:** Beautiful Hugo (heavily customized)
- **Language Configuration:** Thai (`th`) with UTF-8 support
- **Hosting:** GitHub Pages with automated deployment

#### Content Generation
- **AI Engine:** Google Generative AI (Gemini)
- **Python Scripts:** Content and image generation automation
- **Template System:** Markdown-based prompt templates
- **Image Processing:** AI-generated covers with custom styling

#### Front-End Enhancements
- **CSS:** Custom Sass with dark theme and responsive design
- **JavaScript:** Vanilla JS for table enhancements and visual effects
- **Performance:** Optimized assets and lazy loading
- **Mobile-First:** Responsive breakpoints and touch-friendly interactions

## 5. Content Organization & Current State

### Content Categories

#### Guides (`content/guides/`)
- **Basic Controls:** Flight control, UI interaction, camera systems
- **Gameplay Mechanics:** Trading, combat, equipment management
- **Advanced Features:** CCU guides, ASOP fleet manager, FPS weapons
- **Special Events:** Annual events and limited-time activities

#### Ships (`content/ships/`)
- **Ship Reviews:** Detailed analysis of popular ships (Gladius, Arrow, Cutlass, etc.)
- **Showcase Pages:** Visual presentations with carousels and specifications
- **Buying Guides:** Ship purchasing decisions and recommendations

#### Concepts (`content/concepts/`)
- **Game Systems:** Death mechanics, insurance, server environments
- **Lore & Events:** CitizenCon coverage, faction guides, story content
- **Economics:** Pledge store, CCU system, referral programs

#### Development (`content/development/`)
- **Monthly Reports:** Development updates and progress tracking
- **Technical Guides:** Behind-the-scenes development insights

### File Organization Standards

```
content/
├── category/
│   ├── _index.md                    # Category landing page
│   ├── simple-article.md            # Regular article
│   └── complex-article/             # Page bundle (preferred)
│       ├── index.md                # Main content
│       ├── cover.jpg              # Cover image
│       └── images/                # Article images
```

## 6. Development Workflow

### Content Creation Process

1. **Topic Planning:** Identify content needs based on game updates
2. **AI Generation:** Use `blog_generator.py` for initial content structure
3. **Content Development:** Write and refine Thai content with proper formatting
4. **Cover Image:** Generate using `generate_article_cover.py`
5. **Testing:** Local preview with `hugo server --buildDrafts`
6. **Publishing:** Commit and push for automatic deployment

### Quality Standards

- **Language Quality:** Native Thai writing with technical accuracy
- **Version Tracking:** All guides tagged with current game version
- **Visual Consistency:** Standardized formatting and image sizing
- **Mobile Optimization:** Responsive design testing across devices
- **Performance:** Fast loading times and optimized assets

## 7. Future Development Roadmap

### Near-Term Enhancements (Q3-Q4 2025)

#### Search & Navigation
- **Algolia DocSearch Integration:** Full-text search across all content
- **Advanced Filtering:** Filter by game version, content type, difficulty
- **Improved Navigation:** Breadcrumbs and related content suggestions

#### Content Features
- **Interactive Elements:** Calculators for trading, mining profits
- **Video Integration:** YouTube embedding with custom styling
- **Community Contributions:** Streamlined contribution workflow

### Medium-Term Goals (2026)

#### Advanced Features
- **Progressive Web App (PWA):** Offline reading capability
- **Multi-language Support:** English content alongside Thai
- **Advanced Analytics:** Content performance tracking and optimization

#### Community Building
- **User-Generated Content:** Community guide submissions
- **Discussion Integration:** Comment system or community forum links
- **Contributor Recognition:** Contributor profiles and acknowledgments

### Long-Term Vision

#### Platform Expansion
- **API Development:** Content API for third-party applications
- **Mobile App:** Native mobile app for enhanced mobile experience
- **Integration Ecosystem:** Tools and extensions for content creators

#### Data & Intelligence
- **Game Data Integration:** Live ship stats and pricing information
- **Recommendation Engine:** Personalized content recommendations
- **Automated Content Updates:** AI-powered content maintenance and updates

## 8. Technical Specifications

### Performance Targets
- **Page Load Time:** < 2 seconds on 3G connection
- **Lighthouse Score:** > 90 across all metrics
- **Mobile Optimization:** 100% mobile-friendly pages
- **SEO Optimization:** Rich snippets and structured data

### Browser Support
- **Modern Browsers:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Browsers:** iOS Safari 14+, Chrome Mobile 90+
- **Progressive Enhancement:** Graceful degradation for older browsers

### Security & Privacy
- **HTTPS Everywhere:** Secure connections for all resources
- **Privacy-First:** No tracking cookies or user data collection
- **Content Security:** Secure hosting and regular security updates