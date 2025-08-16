/* 
 * Responsive Table Auto-Enhancement Script
 * Automatically wraps tables in responsive containers for horizontal scrolling
 * Enhanced with WebView-compatible viewport detection for Facebook's in-app browser
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize viewport detection for WebView compatibility
  initWebViewCompatibleViewport();
  
  enhanceTablesForMobile();
  
  // Re-run on window resize to handle dynamic content
  let resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      updateViewportCustomProperties();
      enhanceTablesForMobile();
    }, 250);
  });
});

/**
 * Initialize viewport detection that works reliably in WebView environments
 * like Facebook's in-app browser where vw units may not work correctly
 */
function initWebViewCompatibleViewport() {
  updateViewportCustomProperties();
  
  // Set up orientation change listener for mobile devices
  if (screen.orientation) {
    screen.orientation.addEventListener('change', function() {
      setTimeout(updateViewportCustomProperties, 100);
    });
  } else {
    // Fallback for older browsers
    window.addEventListener('orientationchange', function() {
      setTimeout(updateViewportCustomProperties, 100);
    });
  }
}

/**
 * Update CSS custom properties with JavaScript-calculated viewport values
 * This provides a fallback when CSS viewport units don't work properly
 */
function updateViewportCustomProperties() {
  // Get reliable viewport dimensions
  let viewportWidth;
  
  // Try multiple methods to get viewport width for maximum compatibility
  if (window.visualViewport && window.visualViewport.width) {
    // Modern browsers with Visual Viewport API
    viewportWidth = window.visualViewport.width;
  } else if (document.documentElement.clientWidth) {
    // Standard method
    viewportWidth = document.documentElement.clientWidth;
  } else if (window.innerWidth) {
    // Fallback method
    viewportWidth = window.innerWidth;
  } else {
    // Last resort
    viewportWidth = screen.width;
  }
  
  // Calculate breakout dimensions
  // Use 90% of viewport width for breakout, centered
  const breakoutWidth = Math.floor(viewportWidth * 0.9);
  const breakoutOffset = Math.floor(breakoutWidth * -0.5);
  
  // Update CSS custom properties
  const root = document.documentElement;
  root.style.setProperty('--viewport-width', viewportWidth + 'px');
  root.style.setProperty('--breakout-width', breakoutWidth + 'px');
  root.style.setProperty('--breakout-offset', breakoutOffset + 'px');
  
  // Debug logging (remove in production if desired)
  if (window.location.search.includes('debug=tables')) {
    console.log('Viewport Detection:', {
      method: window.visualViewport ? 'visualViewport' : 'fallback',
      viewportWidth: viewportWidth,
      breakoutWidth: breakoutWidth,
      breakoutOffset: breakoutOffset,
      userAgent: navigator.userAgent.includes('FBAN') ? 'Facebook' : 'other'
    });
  }
}

function enhanceTablesForMobile() {
  const tables = document.querySelectorAll('table');
  
  tables.forEach(function(table) {
    // Skip if already processed
    if (table.closest('.table-responsive')) {
      return;
    }
    
    // Create responsive wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'table-responsive';
    
    // Count columns to determine if table needs breakout
    // Try to count from header first, fallback to first row
    let columnCount = table.querySelectorAll('thead th').length;
    if (columnCount === 0) {
      columnCount = table.querySelectorAll('thead td').length;
    }
    if (columnCount === 0) {
      columnCount = table.querySelectorAll('tbody tr:first-child td, tbody tr:first-child th').length;
    }
    
    // Check for long text content in cells
    let hasLongContent = false;
    let totalContentLength = 0;
    let cellCount = 0;
    const cells = table.querySelectorAll('td, th');
    
    cells.forEach(function(cell) {
      const textLength = cell.textContent.trim().length;
      totalContentLength += textLength;
      cellCount++;
      
      // Consider content "long" if any cell has more than 50 characters
      if (textLength > 50) {
        hasLongContent = true;
      }
    });
    
    // Calculate average content length per cell
    const averageContentLength = cellCount > 0 ? totalContentLength / cellCount : 0;
    
    // Additional breakout triggers:
    // - Any single cell with 50+ characters
    // - Average cell content length > 25 characters (indicates data-heavy table)
    // - Table has more than 20 total cells (large data table)
    const hasLongAverageContent = averageContentLength > 25;
    const isLargeDataTable = cellCount > 20;
    
    // Apply breakout for tables with 5+ columns OR tables with long content
    if (columnCount >= 5 || hasLongContent || hasLongAverageContent || isLargeDataTable) {
      wrapper.classList.add('wide-table');
      // Add data attributes for debugging
      wrapper.setAttribute('data-columns', columnCount);
      wrapper.setAttribute('data-breakout-reason', 
        [
          columnCount >= 5 ? 'many-columns' : '',
          hasLongContent ? 'long-content' : '',
          hasLongAverageContent ? 'data-heavy' : '',
          isLargeDataTable ? 'large-table' : ''
        ].filter(Boolean).join(' ')
      );
      
      if (window.location.search.includes('debug=tables')) {
        let reasons = [];
        if (columnCount >= 5) reasons.push('many columns');
        if (hasLongContent) reasons.push('long content');
        if (hasLongAverageContent) reasons.push('data-heavy');
        if (isLargeDataTable) reasons.push('large table');
        
        console.log('Applied breakout layout to table with', columnCount, 'columns due to:', reasons.join(', '));
      }
    } else {
      if (window.location.search.includes('debug=tables')) {
        console.log('Applied compact layout to table with', columnCount, 'columns');
      }
    }
    
    // Wrap the table
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
  });
}

// Export functions for manual use if needed
window.ResponsiveTables = {
  enhance: enhanceTablesForMobile,
  updateViewport: updateViewportCustomProperties,
  init: initWebViewCompatibleViewport
};
