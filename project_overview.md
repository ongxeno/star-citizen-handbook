# Project Overview: Star Citizen Handbook

**Last Updated:** 2025-07-18

## 1. Project Goal

The primary goal of this project is to create a clear, user-friendly, and multilingual guide for new and intermediate Star Citizen players. The website, `star-citizen-handbook`, will be hosted on GitHub Pages and serve as a go-to reference to help players become self-sufficient in the 'Verse.

## 2. Core Principles

* **Multilingual Support:** The site is built to support multiple languages from the ground up.
    * **Initial Languages:** Thai (`th`) and English (`en`).
    * **Default Language:** Thai (`th`).
    * **Structure:** All content is separated into language-specific directories (`content/th/`, `content/en/`).

* **Content Versioning:** This is a critical feature. Every guide and content page must be tagged with the specific game version it applies to, using the `game_version` parameter in the front matter (e.g., `game_version: "Alpha 3.23.1"`).

## 3. Website Features & Functionality

* **Clean, Modern UI:**
    * Utilize a dark theme that complements the Star Citizen aesthetic (e.g., dark grays, blues, and oranges).
    * Ensure an uncluttered layout with ample white space to improve readability.
    * Use a modern, legible font for all text content.
* **Excellent Navigation:**
    * A persistent top navigation bar with clear, logical sections (e.g., "Getting Started", "Gameplay Guides", "Ships").
    * A powerful, site-wide search bar that is always visible and provides instant results.
    * Breadcrumbs on content pages to show the user their location within the site structure (e.g., Home > Gameplay Guides > Basic Mining).
* **Mobile-First Responsive Design:**
    * The website layout must adapt seamlessly to all screen sizes, from large desktop monitors to small mobile phones.
    * All functionality, including navigation and search, must be perfectly usable on touch devices.
    * Images and text should resize appropriately without requiring horizontal scrolling.
* **Language Selector:**
    * An easily identifiable language switcher (e.g., a globe icon or a dropdown with "English" / "ภาษาไทย") in the main navigation bar.
    * The site should remember the user's language preference for future visits.
* **Version Display:**
    * The game version a guide applies to (e.g., "For Alpha 3.23.1") must be prominently displayed at the top of every content page.
    * Consider adding a visual indicator (e.g., a warning banner) if a user is viewing a guide for an older game version.
* **Image Lightboxes & Copy-to-Clipboard functionality:**
    * Clicking on any image within a guide should open a larger, high-resolution version in a lightbox overlay.
    * For code blocks, keybinds, or reference data, provide a simple "Copy" button that copies the content to the user's clipboard with a single click.

## 4. Technology Stack

* **Static Site Generator:** Hugo (Extended Version)
* **Theme:** Docsy, managed via Hugo Modules.
* **Front-end Dependencies:** Managed with `npm` and a `package.json` file.
* **Hosting & Deployment:** GitHub Pages, with automated deployment via GitHub Actions.
* **Version Control:** Git, hosted on GitHub.

---

## 5. Development Roadmap

### **Phase 1: The Multilingual Foundation (Completed)**

* **Objective:** Build a functional, multilingual website foundation that can display versioned content.
* **Deliverables:**
    * [x] Hugo project structure initialized.
    * [x] Go, Node.js, and all theme dependencies installed and configured.
    * [x] `hugo.toml` configured for Thai (default) and English languages.
    * [x] Docsy theme installed and working via Hugo Modules.
    * [x] GitHub Actions workflow created for automatic deployment.
    * [x] Initial "From Hab to Orbit" guide created in both English and Thai as a content template.
    * [x] Website is live and functional.

### **Phase 2: Content & Feature Expansion (Current Phase)**

* **Objective:** Broaden the content library and add essential user-facing features.
* **Key Tasks:**
    * **Content: Gameplay Guides:**
        * Create guides for core gameplay loops:
            * Basic Mining (Vulture, ROC)
            * Bounty Hunting (VLRT/LRT contracts)
            * Delivery & Courier Missions
        * Create guides for core concepts:
            * CCU (Cross-Chassis Upgrades) Explained
            * Ship Insurance and Claiming
            * Inventory Management (Local, Ship, Personal)
    * **Content: Ship Information Hub:**
        * Create a data file (`data/ships.yml` or similar) to store ship stats.
        * Develop a Hugo layout (`layouts/ships/single.html`) to render individual ship pages from the data file.
        * Populate with data for 10-15 common starter ships (e.g., Aurora, Mustang, Avenger Titan, Cutter, C8X Pisces).
    * **Feature: Search:**
        * Implement a site-wide search functionality.
        * Ensure search results are language-aware and respect the user's currently selected language.
    * **Content: Reference Data:**
        * Create simple markdown tables for quick reference:
            * Mineable Materials and where to sell them.
            * Common Keybinds Cheatsheet.

### **Phase 3: Polish & Community**

* **Objective:** Refine the user experience and open the project to community contributions.
* **Key Tasks:**
    * **UI/UX Refinements:**
        * Review and adjust the Docsy theme styling for better readability and aesthetics.
        * Improve mobile responsiveness if any issues are found.
    * **Community Contributions:**
        * Create a "How to Contribute" page explaining how users can submit corrections or new content via GitHub pull requests.
    * **Advanced Feature: Auto-Translation:**
        * Investigate and implement a client-side JavaScript solution to auto-translate content when a manual translation is not available.
        * Clearly label machine-translated content to manage user expectations.