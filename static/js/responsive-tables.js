/* 
 * Responsive Table Auto-Enhancement Script
 * Automatically wraps tables in responsive containers for horizontal scrolling
 * Enhanced with WebView-compatible viewport detection for Facebook's in-app browser
 * Based on research from https://blog.tomayac.com/2019/12/09/inspecting-facebooks-webview/
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
 * Detect if we're running in Facebook's in-app browser or other WebView
 * Based on user-agent analysis from Facebook WebView research
 */
function detectWebViewEnvironment() {
  const ua = navigator.userAgent;
  const isWebView = {
    facebook: /\[FB_IAB\/FB4A;/.test(ua) || /FBAN|FBAV/.test(ua),
    instagram: /Instagram/.test(ua),
    twitter: /TwitterAndroid/.test(ua),
    linkedin: /LinkedInApp/.test(ua),
    genericWebView: /; wv\)/.test(ua), // Generic WebView indicator
    isAnyWebView: function() {
      return this.facebook || this.instagram || this.twitter || this.linkedin || this.genericWebView;
    }
  };
  
  return isWebView;
}

/**
 * Initialize viewport detection that works reliably in WebView environments
 * like Facebook's in-app browser where vw units may not work correctly
 */
function initWebViewCompatibleViewport() {
  const webViewInfo = detectWebViewEnvironment();
  
  // Log WebView detection for debugging
  if (window.location.search.includes('debug=tables')) {
    console.log('WebView Detection:', webViewInfo);
  }
  
  updateViewportCustomProperties();
  
  // Enhanced orientation change handling for WebView environments
  if (screen.orientation) {
    screen.orientation.addEventListener('change', function() {
      // WebView environments often need more time to recalculate viewport
      setTimeout(updateViewportCustomProperties, webViewInfo.isAnyWebView() ? 200 : 100);
    });
  } else {
    // Fallback for older browsers
    window.addEventListener('orientationchange', function() {
      setTimeout(updateViewportCustomProperties, webViewInfo.isAnyWebView() ? 200 : 100);
    });
  }
  
  // Additional resize listener with debouncing for WebView stability
  let viewportUpdateTimer;
  window.addEventListener('resize', function() {
    clearTimeout(viewportUpdateTimer);
    // WebView environments benefit from longer debounce times
    const debounceTime = webViewInfo.isAnyWebView() ? 300 : 150;
    viewportUpdateTimer = setTimeout(updateViewportCustomProperties, debounceTime);
  });
}

/**
 * Update CSS custom properties with JavaScript-calculated viewport values
 * Enhanced for Facebook WebView compatibility issues
 */
function updateViewportCustomProperties() {
  const webViewInfo = detectWebViewEnvironment();
  let viewportWidth;
  let detectionMethod = 'unknown';
  
  // Try multiple methods to get viewport width with WebView-specific prioritization
  if (window.visualViewport && window.visualViewport.width && !webViewInfo.isAnyWebView()) {
    // Modern browsers with Visual Viewport API - but skip for WebViews due to inconsistencies
    viewportWidth = window.visualViewport.width;
    detectionMethod = 'visualViewport';
  } else if (document.documentElement.clientWidth) {
    // Most reliable method for WebViews - prioritize this for in-app browsers
    viewportWidth = document.documentElement.clientWidth;
    detectionMethod = 'clientWidth';
  } else if (window.innerWidth) {
    // Fallback method
    viewportWidth = window.innerWidth;
    detectionMethod = 'innerWidth';
  } else if (screen.width) {
    // Last resort - may not reflect actual viewport in WebViews
    viewportWidth = screen.width;
    detectionMethod = 'screenWidth';
  } else {
    // Emergency fallback for extremely limited environments
    viewportWidth = 320; // Assume minimum mobile width
    detectionMethod = 'fallback';
  }
  
  // WebView-specific adjustments
  if (webViewInfo.isAnyWebView()) {
    // Some WebViews report incorrect viewport dimensions
    // Add conservative adjustment if viewport seems too small
    if (viewportWidth < 320) {
      viewportWidth = 320;
      detectionMethod += '-adjusted-min';
    }
    // Cap extremely large values that might be screen dimensions instead of viewport
    if (viewportWidth > 2560) {
      viewportWidth = Math.min(viewportWidth, 1200);
      detectionMethod += '-adjusted-max';
    }
  }
  
  // Calculate breakout dimensions with WebView-safe values
  // Use 85% for WebViews (more conservative) vs 90% for regular browsers
  const breakoutPercentage = webViewInfo.isAnyWebView() ? 0.85 : 0.90;
  const breakoutWidth = Math.floor(viewportWidth * breakoutPercentage);
  const breakoutOffset = Math.floor(breakoutWidth * -0.5);
  
  // Update CSS custom properties with fallback values
  const root = document.documentElement;
  root.style.setProperty('--viewport-width', viewportWidth + 'px');
  root.style.setProperty('--breakout-width', breakoutWidth + 'px');
  root.style.setProperty('--breakout-offset', breakoutOffset + 'px');
  
  // Add data attribute for CSS debugging
  root.setAttribute('data-viewport-method', detectionMethod);
  
  // Enhanced debug logging
  if (window.location.search.includes('debug=tables')) {
    console.log('Viewport Update:', {
      environment: webViewInfo.isAnyWebView() ? 'WebView' : 'Regular Browser',
      userAgent: webViewInfo,
      method: detectionMethod,
      viewportWidth: viewportWidth,
      breakoutWidth: breakoutWidth,
      breakoutOffset: breakoutOffset,
      breakoutPercentage: Math.round(breakoutPercentage * 100) + '%'
    });
  }
}

function enhanceTablesForMobile() {
  const tables = document.querySelectorAll('table');
  const webViewInfo = detectWebViewEnvironment();
  
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
    // In WebView environments, be slightly more aggressive with breakouts for better UX
    const columnThreshold = webViewInfo.isAnyWebView() ? 4 : 5;
    
    if (columnCount >= columnThreshold || hasLongContent || hasLongAverageContent || isLargeDataTable) {
      wrapper.classList.add('wide-table');
      // Add data attributes for debugging
      wrapper.setAttribute('data-columns', columnCount);
      wrapper.setAttribute('data-environment', webViewInfo.isAnyWebView() ? 'webview' : 'browser');
      wrapper.setAttribute('data-breakout-reason', 
        [
          columnCount >= columnThreshold ? 'many-columns' : '',
          hasLongContent ? 'long-content' : '',
          hasLongAverageContent ? 'data-heavy' : '',
          isLargeDataTable ? 'large-table' : ''
        ].filter(Boolean).join(' ')
      );
      
      if (window.location.search.includes('debug=tables')) {
        let reasons = [];
        if (columnCount >= columnThreshold) reasons.push('many columns (' + columnCount + ')');
        if (hasLongContent) reasons.push('long content');
        if (hasLongAverageContent) reasons.push('data-heavy');
        if (isLargeDataTable) reasons.push('large table');
        
        console.log('Applied breakout layout to table due to:', reasons.join(', '));
        console.log('Environment:', webViewInfo.isAnyWebView() ? 'WebView' : 'Regular Browser');
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
  init: initWebViewCompatibleViewport,
  detectWebView: detectWebViewEnvironment
};
