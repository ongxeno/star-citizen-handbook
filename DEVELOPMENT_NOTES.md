# Hugo Thai Content - Development Notes

## Navigation Fix
- **Problem**: Hugo's auto-generated Thai anchor IDs are unpredictable
- **Solution**: Use manual anchor IDs: `## Thai Heading {#english-id}`
- **Table of Contents**: Reference with `[Thai Text](#english-id)`

## Content Best Practices
- **New pages**: Add link to category index
- **Frontmatter**: Include `image` for Open Graph sharing
- **Anchors**: Use English IDs for Thai headings (`{#getting-up}`)
- **Files**: kebab-case names, avoid special characters in images
- **Testing**: Always verify table of contents navigation works
