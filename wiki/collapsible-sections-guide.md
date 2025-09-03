# Collapsible Sections - Complete Guide

## Visual Features ✨

Our collapsible sections include **animated arrow indicators**:
- **Collapsed**: ▼ rotated left (points right →)
- **Expanded**: ▼ pointing down
- **Smooth rotation** and **hover effects** with scaling
- **Three arrow styles available** (see CSS Customization section)

## Best Options (Ranked by Recommendation)

### 1. Hugo Built-in `details` (RECOMMENDED)
```markdown
{{< details summary="Your Title" >}}
Your content here
{{< /details >}}

{{< details summary="With options" open=true class="my-class" >}}
Content with open by default and custom class
{{< /details >}}
```

**All Parameters:**
- `summary` - The title text (required)
- `open` - Set to `true` to expand by default (optional)
- `class` - Custom CSS class (optional)
- `name` - Group related details together (optional)
- `title` - HTML title attribute for tooltip (optional)

### 2. Raw HTML (GitHub Compatible)
```html
<details>
<summary>Your Title</summary>

Your content here (blank line after summary required)

</details>

<details open>
<summary>Open by default</summary>
Content here
</details>
```

## ⚠️ Common Issues and Solutions

### Issue: Empty Summary Text
**Problem**: Using `summary="## Heading"` results in empty summary
**Solution**: Use plain text or inline formatting:

```markdown
<!-- ❌ DON'T: Block elements like headings -->
{{< details summary="## My Title" >}}

<!-- ✅ DO: Plain text or inline formatting -->
{{< details summary="Your Title" >}}
{{< details summary="**Your Bold Title**" >}}
{{< details summary="🔍 Your Title with Emoji" >}}
```

### Issue: Styling the Summary
**Solutions for different styling needs**:

```markdown
<!-- Bold text -->
{{< details summary="**Important Information**" >}}

<!-- HTML for advanced styling -->
{{< details summary="<strong style='color: #ff6b35;'>⚠️ Warning</strong>" >}}

<!-- Emojis and icons -->
{{< details summary="🎮 Game Settings" >}}
{{< details summary="⚙️ Configuration Guide" >}}
```

## Migration from old `detail-tag`

**Old (caused empty summary):**
```markdown
{{< detail-tag "## Your Title" >}}
Content
{{< /detail-tag >}}
```

**New (working properly):**
```markdown
{{< details summary="Your Title" >}}
Content
{{< /details >}}

<!-- Or with styling -->
{{< details summary="**Your Bold Title**" >}}
Content
{{< /details >}}
```

## Features Comparison

| Method | Syntax | Open by default | Custom CSS | GitHub Compatible | Summary Styling | Arrow Indicator |
|--------|--------|-----------------|------------|-------------------|-----------------|-----------------|
| `details` | Simple | ✅ | ✅ | ❌ | ✅ Markdown | ✅ Animated |
| Raw HTML | Simple | ✅ | ✅ | ✅ | ✅ Full HTML | ✅ Animated |
| Old `detail-tag` | Complex | ❌ | ✅ | ❌ | ❌ Broken | ❌ None |

## CSS Customization

### Arrow Styles Available

**Current (Default)**: Unicode ▼ rotated for consistency
- Collapsed: ▼ rotated -90° (points right)  
- Expanded: ▼ pointing down
- Smooth rotation with hover scaling

**Alternative 1**: CSS-drawn triangles
- Clean geometric triangles
- Rotate 90° from right to down

**Alternative 2**: Chevron arrows  
- Modern chevron style using borders
- Rotate from 45° to 135°

To switch arrow styles, edit `assets/css/custom.css` and uncomment your preferred section.

### Current Visual Features

- **Rounded corners** (8px border-radius)
- **Dark theme optimized** colors
- **Semi-transparent backgrounds**
- **Smooth hover transitions**
- **Consistent typography** (600 font-weight)
- **Proper spacing** (4.4rem left padding for arrows)

## Tips

1. **Don't use heading syntax (`##`)** in summary - use plain text or inline formatting
2. Use `summary="**Bold Text**"` for emphasis
3. Emojis work great: `summary="🔍 Search Options"`
4. Add `open=true` to expand by default  
5. Use `class="my-class"` for custom styling
6. Always add blank line after `<summary>` in raw HTML
7. HTML tags work in summary: `summary="<strong>Bold</strong>"`
8. Group related sections with `name="section-group"`

## CSS Classes Available

- `.collapse-content` - Content wrapper (automatically applied)
- Custom classes via `class="your-class"` parameter
- All content gets `padding: 1rem` automatically

## Advanced Examples

```markdown
<!-- Simple -->
{{< details summary="Click to expand" >}}
Basic content here
{{< /details >}}

<!-- Bold title -->
{{< details summary="**Important Details**" >}}
This has a bold title
{{< /details >}}

<!-- Open by default with custom class -->
{{< details summary="🎯 Performance Tips" open=true class="highlight-section" >}}
This starts expanded and has custom CSS class
{{< /details >}}

<!-- Grouped sections (only one can be open) -->
{{< details summary="Option A" name="settings" >}}
Content for option A
{{< /details >}}

{{< details summary="Option B" name="settings" >}}
Content for option B  
{{< /details >}}

<!-- Colored title using HTML -->
{{< details summary="<span style='color: #ff6b35;'>⚠️ Warning Section</span>" >}}
Warning content with colored title
{{< /details >}}

<!-- With tooltip -->
{{< details summary="⚙️ Advanced Settings" title="Click to show advanced configuration options" >}}
Advanced configuration content
{{< /details >}}
```

## Technical Implementation

- **Hugo Shortcode**: Custom override in `layouts/shortcodes/details.html`
- **Parameter Processing**: Uses `.Page.RenderString` for proper markdown rendering
- **CSS Styling**: Enhanced dark theme in `assets/css/custom.css`
- **Arrow Animation**: CSS `transform` with `transition` for smooth rotation
- **Browser Compatibility**: Hides default disclosure triangles across all browsers
