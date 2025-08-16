---
title: "Image Carousel Shortcode Guide"
date: 2024-12-17T00:00:00Z
draft: false
---

# Hugo Carousel Shortcode Guide

The carousel shortcode provides a clean, responsive image carousel for your Hugo site. **Important: This carousel only works with Page Bundles (index.md files).**

## ⚠️ Limitation

**This carousel shortcode ONLY works with Page Bundles (`index.md` files).** Regular pages (like `test.md`) are not supported due to Hugo's resource processing limitations.

## Basic Usage

### Page Bundle Setup (Required)

1. **Create a Page Bundle:**
   ```
   content/
     my-article/
       index.md          ← Must be named "index.md"
       image1.jpg
       image2.png
       cover.jpg
   ```

2. **Use the shortcode in `index.md`:**
   ```markdown
   {{< carousel >}}
   ```

### Subdirectory Approach

If you prefer organized image folders:

1. **Create subdirectory in your page bundle:**
   ```
   content/
     my-article/
       index.md
       images/           ← Subdirectory for images
         photo1.jpg
         photo2.png
         photo3.gif
   ```

2. **Use with path parameter:**
   ```markdown
   {{< carousel path="images/" >}}
   ```

## Shortcode Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | string | `""` | Optional. Subdirectory within the page bundle |
| `height` | string | `"400px"` | Height of carousel container |
| `interval` | string | `"5000"` | Auto-advance interval in milliseconds |

## Examples

### Basic Carousel
```markdown
{{< carousel >}}
```
Uses all images in the page bundle root.

### Custom Height
```markdown
{{< carousel height="300px" >}}
```

### Subdirectory with Custom Settings
```markdown
{{< carousel path="gallery/" height="500px" interval="8000" >}}
```

### Disable Auto-advance
```markdown
{{< carousel interval="0" >}}
```
Setting interval to "0" disables auto-advance.

## File Organization

### ✅ Supported Structure (Page Bundle)
```
content/
  ships/
    aegis-gladius/
      index.md          ← Works!
      image1.jpg
      image2.png
      screenshots/
        shot1.jpg
        shot2.png
```

### ❌ Not Supported (Regular Pages)
```
content/
  ships/
    aegis-gladius.md    ← Won't work
  static/
    images/
      ship1.jpg         ← Can't access from regular pages
```

## Troubleshooting

### "No images found for carousel"

This usually means:

1. **You're using a regular page instead of a page bundle**
   - **Solution:** Convert your `.md` file to `index.md` in a folder

2. **Images are in the wrong location**
   - **Page bundle:** Images must be in the same folder as `index.md`
   - **Subdirectory:** Use the `path` parameter to specify subdirectory

3. **Unsupported image format**
   - **Supported:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
   - **Case insensitive:** `Image.JPG` works fine

### Converting Regular Pages to Page Bundles

If you have `content/articles/my-post.md`, convert it to:

1. **Create folder:** `content/articles/my-post/`
2. **Rename file:** `content/articles/my-post/index.md`
3. **Move images:** Put them in `content/articles/my-post/`
4. **Update links:** Change `![](../images/photo.jpg)` to `![](photo.jpg)`

## Features

- **Responsive:** Automatically adjusts to container width
- **Touch-friendly:** Works on mobile devices
- **Auto-advance:** Configurable automatic slideshow
- **Hover pause:** Pauses on mouse hover
- **Keyboard navigation:** Arrow keys work when focused
- **Smooth transitions:** Crossfade effect between images
- **Aspect ratio preserved:** Maintains original image proportions

## Advanced Usage

### Multiple Carousels on Same Page

Each carousel gets a unique ID automatically:

```markdown
## Section 1
{{< carousel path="section1/" >}}

## Section 2  
{{< carousel path="section2/" height="300px" >}}
```

### Custom Styling

The carousel uses these CSS classes:
- `.carousel` - Main container
- `.carousel-indicators` - Dot indicators
- `.carousel-inner` - Image container
- `.carousel-control` - Navigation arrows

You can override styles in your custom CSS:

```css
.carousel {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.carousel-indicators li {
  background-color: #gold;
}
```

## Supported Image Formats

- **JPEG:** `.jpg`, `.jpeg`
- **PNG:** `.png`
- **GIF:** `.gif`
- **WebP:** `.webp`
- **Case insensitive:** `Image.JPG`, `photo.PNG` work fine

The simplified carousel follows Hugo best practices and is more reliable than complex multi-scenario approaches.
