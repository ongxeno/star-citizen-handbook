# Adding Image Carousel to Hugo Pages

## Overview
This guide shows how to add a functional image carousel to any Hugo page in the Star Citizen Handbook using our custom Hugo shortcode. The carousel automatically detects images and uses Bootstrap 3 styling with jQuery for functionality.

## Features
- ✅ **Automatic image detection** from Page Bundle or static directory
- ✅ Auto-advance slideshow (configurable interval)
- ✅ Manual navigation with left/right arrows
- ✅ Clickable indicator dots for direct slide access
- ✅ Hover-to-pause functionality
- ✅ Infinite loop cycling
- ✅ Responsive design
- ✅ Multiple carousels per page support
- ✅ **Zero manual configuration** - just add images and use shortcode
- ✅ Deployment-safe (uses theme's included Bootstrap and jQuery)

## Quick Start (Recommended Method)

### Method 1: Page Bundle Approach (Recommended)
This is the easiest and most maintainable approach:

1. **Create a Page Bundle structure:**
   ```
   content/guides/your-guide/
   ├── index.md          # Your main content file (MUST be named index.md)
   ├── image1.png        # Your carousel images
   ├── image2.jpg
   └── image3.png
   ```

2. **Add the shortcode to your markdown:**
   ```markdown
   {{< carousel >}}
   ```

3. **Done!** The carousel automatically finds all images in the same directory.

### Method 2: Static Directory Approach
For images you want to reuse across multiple pages:

1. **Put images in static directory:**
   ```
   static/img/your-folder/
   ├── image1.png
   ├── image2.jpg
   └── image3.png
   ```

2. **Use shortcode with path parameter:**
   ```markdown
   {{< carousel path="img/your-folder" >}}
   ```

## Shortcode Parameters

The `carousel` shortcode accepts these optional parameters:

- **`path`** - Path to static directory containing images (e.g., `"img/guides/events"`)
- **`height`** - Height of carousel images (default: `"400px"`)
- **`interval`** - Auto-advance interval in milliseconds (default: `"5000"`)

### Examples:
```markdown
{{< carousel >}}                                    # Uses page bundle images, default settings
{{< carousel height="300px" >}}                     # Custom height
{{< carousel height="500px" interval="8000" >}}     # Custom height and slower timing
{{< carousel path="img/ships" height="600px" >}}    # Static directory with custom height
```

## Image Requirements

### Supported Formats
- ✅ PNG (`.png`)
- ✅ JPEG (`.jpg`, `.jpeg`)
- ✅ GIF (`.gif`)  
- ✅ WebP (`.webp`)

### Best Practices
- **Consistent aspect ratio**: Use same dimensions for all images in a carousel
- **Optimized file size**: Compress images for web (< 500KB recommended)
- **Clean filenames**: Avoid spaces and special characters in filenames
- **Descriptive names**: Use meaningful names like `ship-exterior.jpg` instead of `IMG_001.jpg`

## Advanced Usage

### Multiple Carousels on One Page
Each carousel automatically gets a unique ID, so you can have multiple carousels:

```markdown
## Ship Exterior Photos
{{< carousel path="img/ships/exterior" height="500px" >}}

## Ship Interior Photos  
{{< carousel path="img/ships/interior" height="400px" >}}

## Comparison Screenshots
{{< carousel height="300px" interval="3000" >}}
```

### Page Bundle vs Static Directory

**Use Page Bundle when:**
- Images are specific to one page/guide
- You want to keep content and images together
- You prefer automatic organization

**Use Static Directory when:**
- Images are shared across multiple pages
- You want centralized image management
- You have existing organized static folders

## File Organization Examples

### Page Bundle Structure (Recommended)
```
content/
└── guides/
    └── annual-events/          # Your guide directory
        ├── index.md           # Main content (MUST be index.md)
        ├── screenshot1.png    # Carousel images
        ├── screenshot2.png
        └── screenshot3.png
```

### Static Directory Structure
```
static/
└── img/
    └── guides/
        ├── events/            # Event-related images
        │   ├── red-festival.jpg
        │   └── iae-2025.jpg
        └── ships/             # Ship-related images
            ├── cutlass-exterior.jpg
            └── cutlass-interior.jpg
```

## Troubleshooting

### "No images found for carousel" Message
This means the shortcode couldn't find any images. Check:

1. **Page Bundle setup**: 
   - File MUST be named `index.md` (not `your-page.md`)
   - Images must be in the same directory as `index.md`

2. **Static directory setup**:
   - Use correct `path` parameter
   - Verify images exist in `static/img/your-path/`

3. **File formats**: Only `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` are supported

### Images Not Loading
1. **Check file paths**: Ensure images are in correct location
2. **Verify filenames**: Avoid spaces and special characters
3. **Case sensitivity**: Match exact filename case on Linux deployments

### Carousel Not Auto-Advancing
1. **Check browser console**: Look for JavaScript errors
2. **Verify jQuery**: Theme must include jQuery (Beautiful Hugo includes it)
3. **Check interval value**: Must be a number in milliseconds

## Working Examples

### 1. Annual Events Guide (Page Bundle)
Location: `content/guides/annual-events/index.md`
```markdown
---
title: "คู่มือ: ปฏิทินอีเวนต์ประจำปีใน Star Citizen"
---

{{< carousel height="400px" interval="5000" >}}
```

This automatically displays all Screenshot images in the same directory.

### 2. Ship Guide with Multiple Carousels
```markdown
---
title: "Drake Cutlass Black Guide"
---

## Exterior Views
{{< carousel path="img/ships/cutlass/exterior" height="500px" >}}

## Interior Layout  
{{< carousel path="img/ships/cutlass/interior" height="400px" >}}

## Cockpit Details
{{< carousel path="img/ships/cutlass/cockpit" height="300px" interval="3000" >}}
```

## Hugo Frontmatter Integration

Include a representative carousel image in your page frontmatter for social sharing:

```yaml
---
title: "Your Guide Title"
subtitle: "Helpful description"
image: "img/guides/your-guide/featured-image.jpg"  # Pick one from your carousel
tags: ["Guide", "Tutorial"]
categories: ["Guides"]
---
```

## Technical Details

### Shortcode Location
The carousel shortcode is defined in:
```
layouts/shortcodes/carousel.html
```

### Dependencies
- **Bootstrap 3.4.1**: Included in Beautiful Hugo theme
- **jQuery 3.7.0**: Included in Beautiful Hugo theme  
- **Hugo Page Resources**: For automatic image detection

### Generated HTML Structure
The shortcode generates standard Bootstrap 3 carousel markup:
- Carousel container with unique ID
- Indicator dots for navigation
- Image slides with responsive sizing
- Previous/Next controls
- JavaScript initialization

## Deployment Notes

- ✅ **GitHub Pages compatible**: Uses Hugo's built-in resource system
- ✅ **Theme compatible**: Works with Beautiful Hugo and similar Bootstrap themes
- ✅ **Zero maintenance**: No manual HTML or JavaScript updates needed
- ✅ **Performance**: Automatic image optimization through Hugo
- ✅ **SEO friendly**: Generates proper alt tags and semantic HTML
- ✅ **Accessibility**: Includes ARIA labels and keyboard navigation support

---

## Need Help?

If you encounter issues:
1. Check this troubleshooting guide first
2. Verify your file structure matches the examples
3. Test with a simple case (2-3 images) before adding more
4. Use browser developer tools to check for JavaScript errors

The shortcode approach is much simpler and more maintainable than manual HTML implementation!
