# Responsive Tables Implementation Guide

## Problem
Tables with many columns overflow on mobile devices, causing horizontal scrolling and poor user experience. This is especially problematic for specification tables, comparison tables, and data-heavy content.

## Solutions Implemented

### 1. Automatic Enhancement (Recommended)
All tables are automatically enhanced with responsive behavior through JavaScript. No manual intervention required.

**Features:**
- Automatic detection and wrapping of tables
- Smart detection of wide content
- Mobile card layout for tables with 4+ columns
- Horizontal scrolling for smaller tables
- Data labels for mobile card layout

### 2. Manual Control with Shortcodes

#### Basic Responsive Table
```hugo
{{< table-responsive >}}
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
{{< /table-responsive >}}
```

#### Force Card Layout on Mobile
```hugo
{{< table-responsive mode="card" >}}
| รายการ | รายละเอียด | ราคา | คะแนน |
|--------|-------------|------|-------|
| สินค้า A | ข้อมูลยาวๆ | 100 | ⭐⭐⭐⭐⭐ |
{{< /table-responsive >}}
```

### 3. CSS Classes for Custom Control

#### Horizontal Scroll Only
```html
<div class="table-responsive">
  <table>
    <!-- table content -->
  </table>
</div>
```

#### Force Card Layout
```html
<div class="table-responsive table-card-mobile">
  <table>
    <!-- table content -->
  </table>
</div>
```

## Mobile Breakpoints

### Tablet and Small Desktop (≤768px)
- Horizontal scrolling
- Reduced font size (0.85em)
- Compressed padding
- Minimum table width (600px)

### Mobile Phones (≤480px)
- Card layout for complex tables
- Stacked rows with labels
- Headers hidden
- Each row becomes a card

## Best Practices

### 1. Content Strategy
- Keep cell content concise
- Use abbreviations where appropriate
- Consider splitting complex tables into multiple smaller tables
- Use line breaks (`<br>`) sparingly as they trigger card layout

### 2. Design Considerations
- Tables with 4+ columns automatically use card layout on mobile
- Long text content (>50 characters) triggers card layout
- URLs and complex formatting trigger card layout

### 3. Testing
- Always test on actual mobile devices
- Use browser dev tools to simulate different screen sizes
- Check both portrait and landscape orientations

## Technical Details

### CSS Classes Applied
- `.table-responsive`: Wrapper for horizontal scrolling
- `.table-card-mobile`: Forces card layout on mobile
- `data-label` attributes: Automatically added for mobile labels

### JavaScript Enhancement
The `responsive-tables.js` script:
1. Runs on page load and window resize
2. Detects tables without responsive wrappers
3. Analyzes content complexity
4. Applies appropriate responsive strategy
5. Adds mobile data labels

### Performance
- Lightweight JavaScript (~2KB minified)
- CSS uses modern features (flexbox, CSS Grid fallbacks)
- No external dependencies
- Automatic cleanup on dynamic content changes

## Migration from Existing Tables

### Before (Problematic on Mobile)
```markdown
| รายการ | รายละเอียด | ความเร็ว | อาวุธ | ราคา |
|--------|-------------|----------|-------|------|
| Wolf   | Light Fighter | 230 m/s | 2x S4 | 100$ |
```

### After (Automatically Enhanced)
No changes needed! The JavaScript automatically wraps and enhances all tables.

### Manual Enhancement (Optional)
```hugo
{{< table-responsive mode="card" >}}
| รายการ | รายละเอียด | ความเร็ว | อาวุธ | ราคา |
|--------|-------------|----------|-------|------|
| Wolf   | Light Fighter | 230 m/s | 2x S4 | 100$ |
{{< /table-responsive >}}
```

## Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- iOS Safari 12+
- Chrome Mobile 60+

## Troubleshooting

### Table Not Responsive?
1. Check if JavaScript is enabled
2. Verify `responsive-tables.js` is loaded
3. Check browser console for errors

### Card Layout Not Working?
1. Ensure table has proper headers (`<th>` elements)
2. Check if `data-label` attributes are present
3. Test with screen width <480px

### Styling Issues?
1. Check CSS specificity conflicts
2. Verify custom CSS is loaded after theme CSS
3. Test with different table content types
