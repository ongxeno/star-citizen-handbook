// Dynamic Parallax Star Field Effect with Configurable Density
document.addEventListener('DOMContentLoaded', function() {
    let ticking = false;
    let scrollY = 0;
    
    // Star configuration - easily adjustable
    const starConfig = {
        // Star density (stars per 10000 square pixels) - 5 layers for better depth
        farthestDensity: 40,   // Farthest stars (tiny, most numerous)
        distantDensity: 20,    // Distant stars (small, many)
        midDensity: 10,        // Mid-distance stars (medium)
        nearDensity: 2,        // Near stars (larger, fewer)
        closestDensity: 1,     // Closest stars (largest, fewest)
        
        // Parallax speeds - progressive depth layers
        farthestSpeed: -0.01,  // Almost stationary
        distantSpeed: -0.03,   // Very slow movement
        midSpeed: -0.07,       // Medium speed
        nearSpeed: -0.12,      // Faster movement
        closestSpeed: -0.18,   // Fastest movement
        
        // Star colors by stellar type (realistic astronomy)
        starColors: {
            // Hot blue/white stars (O, B, A types)
            hot: ['#9bb0ff', '#aabfff', '#cad7ff', '#b6c5ff', '#87ceeb', '#b0c4de'],
            // White stars (A, F types)  
            white: ['#ffffff', '#f8f7ff', '#fffafa', '#f5f5f5', '#fff2e0', '#fffacd'],
            // Yellow stars (G type - like our Sun)
            yellow: ['#ffff88', '#ffffc0', '#ffd700', '#fff8dc', '#ffffe0', '#f0e68c'],
            // Orange stars (K type)
            orange: ['#ffd0a0', '#ffcc99', '#ffa500', '#ff8c00', '#daa520', '#ff7f50'],
            // Red stars (M type - coolest)
            red: ['#ffb380', '#ff9966', '#ff6347', '#cd5c5c', '#dc143c']
        }
    };
    
    // Track current viewport dimensions for resize optimization
    let currentWidth = window.innerWidth;
    let currentHeight = window.innerHeight;
    let resizeTimeout = null;
    
    // Mobile detection and viewport utilities
    function isMobileDevice() {
        // Check user agent for mobile patterns
        const mobileUserAgent = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        // Check for touch-capable MacOS devices (iPad Pro running as desktop)
        const touchMac = !!(navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /MacIntel/.test(navigator.platform));
        
        return mobileUserAgent || touchMac;
    }
    
    function getStableViewportHeight() {
        // Use Visual Viewport API if available (modern browsers)
        if (window.visualViewport) {
            return window.visualViewport.height;
        }
        // Fallback to window.innerHeight
        return window.innerHeight;
    }
    
    // Create star layers using Canvas for better performance
    function createStarLayer(density, minSize, maxSize, colors, className, zIndex, targetWidth = null, targetHeight = null) {
        const width = targetWidth || window.innerWidth;
        const height = targetHeight || getStableViewportHeight();
        
        // Create canvas element
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas properties
        canvas.className = className;
        canvas.width = width;
        canvas.height = height * 3; // Extended height for seamless parallax repeat
        
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            pointer-events: none;
            z-index: ${zIndex};
            will-change: transform;
        `;
        
        // Generate star data
        const viewportArea = width * height;
        const starCount = Math.floor((viewportArea / 10000) * density);
        const stars = [];
        
        for (let i = 0; i < starCount; i++) {
            const star = {
                x: Math.random() * width,
                y: Math.random() * (height * 3), // Match extended canvas height
                size: minSize + Math.random() * (maxSize - minSize),
                color: colors[Math.floor(Math.random() * colors.length)],
                opacity: 0.3 + Math.random() * 0.7
            };
            stars.push(star);
        }
        
        // Draw stars on canvas
        drawStars(ctx, stars);
        
        // Store star data for potential redrawing
        canvas.starData = stars;
        
        return canvas;
    }
    
    // Draw stars on canvas with radial gradient effect
    function drawStars(ctx, stars) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        
        stars.forEach(star => {
            // Create radial gradient for star glow effect
            const gradient = ctx.createRadialGradient(
                star.x, star.y, 0,
                star.x, star.y, star.size * 0.8  // Much smaller glow radius
            );
            
            // Convert hex color to rgba for gradient
            const rgba = hexToRgba(star.color, star.opacity);
            gradient.addColorStop(0, rgba);
            gradient.addColorStop(0.7, hexToRgba(star.color, star.opacity * 0.3));
            gradient.addColorStop(1, 'transparent');
            
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);  // Use actual star size, not doubled
            ctx.fill();
        });
    }
    
    // Helper function to convert hex color to rgba
    function hexToRgba(hex, alpha) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }
    
    // Initialize star field
    function initStarField(fadeTransition = false) {
        const existingCanvases = document.querySelectorAll('.star-layer-farthest, .star-layer-distant, .star-layer-mid, .star-layer-near, .star-layer-closest');
        
        if (fadeTransition && existingCanvases.length > 0) {
            // Create new canvases with fade-in effect
            createNewStarLayers(true);
            
            // Fade out old canvases
            existingCanvases.forEach((canvas, index) => {
                canvas.style.transition = 'opacity 0.8s ease-out';
                canvas.style.opacity = '0';
                
                // Remove old canvases after fade completes
                setTimeout(() => {
                    if (canvas.parentNode) {
                        canvas.parentNode.removeChild(canvas);
                    }
                }, 800);
            });
        } else {
            // Remove existing canvases immediately
            existingCanvases.forEach(canvas => canvas.remove());
            createNewStarLayers(false);
        }
    }
    
    // Create new star layers with optional fade-in
    function createNewStarLayers(fadeIn = false) {
        // Update current dimensions using stable viewport measurements
        currentWidth = window.innerWidth;
        currentHeight = getStableViewportHeight();
        
        // Get all star colors
        const allColors = [
            ...starConfig.starColors.hot,
            ...starConfig.starColors.white,
            ...starConfig.starColors.yellow,
            ...starConfig.starColors.orange,
            ...starConfig.starColors.red
        ];
        
        // Create farthest star canvas (tiniest, most numerous, cool colors)
        const farthestCanvas = createStarLayer(
            starConfig.farthestDensity, 
            0.3, 0.8, 
            [...starConfig.starColors.hot, ...starConfig.starColors.white], 
            'star-layer-farthest',
            -5
        );
        
        // Create distant star canvas (small, many, blue-white dominant)
        const distantCanvas = createStarLayer(
            starConfig.distantDensity, 
            0.5, 1.2, 
            [...starConfig.starColors.hot, ...starConfig.starColors.white], 
            'star-layer-distant',
            -4
        );
        
        // Create mid-distance star canvas (medium, mixed colors)
        const midCanvas = createStarLayer(
            starConfig.midDensity,
            0.8, 2.0,
            [...starConfig.starColors.white, ...starConfig.starColors.yellow],
            'star-layer-mid',
            -3
        );
        
        // Create near star canvas (larger, fewer, warm colors)
        const nearCanvas = createStarLayer(
            starConfig.nearDensity,
            1.5, 3.0,
            [...starConfig.starColors.yellow, ...starConfig.starColors.orange],
            'star-layer-near',
            -2
        );
        
        // Create closest star canvas (largest, fewest, all colors including red giants)
        const closestCanvas = createStarLayer(
            starConfig.closestDensity,
            2.5, 5.0,
            allColors,
            'star-layer-closest',
            -1
        );
        
        const canvases = [farthestCanvas, distantCanvas, midCanvas, nearCanvas, closestCanvas];
        
        if (fadeIn) {
            // Start with opacity 0 and fade in
            canvases.forEach(canvas => {
                canvas.style.opacity = '0';
                canvas.style.transition = 'opacity 0.8s ease-in';
            });
        }
        
        // Add to DOM
        canvases.forEach(canvas => document.body.appendChild(canvas));
        
        if (fadeIn) {
            // Trigger fade-in after a short delay
            setTimeout(() => {
                canvases.forEach(canvas => {
                    canvas.style.opacity = '1';
                });
            }, 50);
        }
        
        console.log(`Star field ${fadeIn ? 'recreated with crossfade' : 'initialized'}: ${Math.floor((currentWidth * currentHeight / 10000) * (starConfig.farthestDensity + starConfig.distantDensity + starConfig.midDensity + starConfig.nearDensity + starConfig.closestDensity))} total stars using 5-layer Canvas`);
    }
    
    // Optimized resize handler - uses crossfade for all significant changes
    function handleResize() {
        // Clear existing timeout
        if (resizeTimeout) {
            clearTimeout(resizeTimeout);
        }
        
        // Debounce the resize handling
        resizeTimeout = setTimeout(() => {
            const newWidth = window.innerWidth;
            const newHeight = getStableViewportHeight();
            const isMobile = isMobileDevice();
            
            // Check if there's a significant size change
            const widthChange = Math.abs(newWidth - currentWidth) / currentWidth;
            const heightChange = Math.abs(newHeight - currentHeight) / currentHeight;
            
            // Mobile-specific logic to prevent address bar triggered regeneration
            if (isMobile) {
                // On mobile, only regenerate for width changes or very large height changes
                // Address bar changes are typically 50-100px, which on most phones is < 15% of viewport
                const shouldRegenerate = widthChange > 0.05 || heightChange > 0.15;
                
                if (shouldRegenerate) {
                    console.log(`Mobile screen resized from ${currentWidth}x${currentHeight} to ${newWidth}x${newHeight}, regenerating with crossfade`);
                    initStarField(true);
                } else {
                    // Minor change (likely address bar) - just update tracking dimensions
                    currentWidth = newWidth;
                    currentHeight = newHeight;
                }
            } else {
                // Desktop: use original 5% threshold for both dimensions
                if (widthChange > 0.05 || heightChange > 0.05) {
                    console.log(`Desktop screen resized from ${currentWidth}x${currentHeight} to ${newWidth}x${newHeight}, regenerating with crossfade`);
                    initStarField(true);
                } else {
                    // Minor change - just update tracking dimensions
                    currentWidth = newWidth;
                    currentHeight = newHeight;
                }
            }
        }, 150); // Slightly longer debounce for smoother experience
    }
    
    // Parallax update function with seamless repeat
    function updateParallax() {
        scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        const farthestCanvas = document.querySelector('.star-layer-farthest');
        const distantCanvas = document.querySelector('.star-layer-distant');
        const midCanvas = document.querySelector('.star-layer-mid');
        const nearCanvas = document.querySelector('.star-layer-near');
        const closestCanvas = document.querySelector('.star-layer-closest');
        
        if (farthestCanvas) {
            const offset = (scrollY * starConfig.farthestSpeed) % (currentHeight * 2);
            farthestCanvas.style.transform = `translateX(-50%) translateY(${offset}px)`;
        }
        if (distantCanvas) {
            const offset = (scrollY * starConfig.distantSpeed) % (currentHeight * 2);
            distantCanvas.style.transform = `translateX(-50%) translateY(${offset}px)`;
        }
        if (midCanvas) {
            const offset = (scrollY * starConfig.midSpeed) % (currentHeight * 2);
            midCanvas.style.transform = `translateX(-50%) translateY(${offset}px)`;
        }
        if (nearCanvas) {
            const offset = (scrollY * starConfig.nearSpeed) % (currentHeight * 2);
            nearCanvas.style.transform = `translateX(-50%) translateY(${offset}px)`;
        }
        if (closestCanvas) {
            const offset = (scrollY * starConfig.closestSpeed) % (currentHeight * 2);
            closestCanvas.style.transform = `translateX(-50%) translateY(${offset}px)`;
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    // Event listeners
    window.addEventListener('scroll', requestTick, { passive: true });
    window.addEventListener('resize', handleResize, { passive: true });
    
    // Initialize everything
    initStarField();
    updateParallax();
    
    // Expose configuration for easy tweaking
    window.starFieldConfig = starConfig;
    window.regenerateStars = () => initStarField(true); // Always use crossfade for manual regeneration
    
    console.log('Dynamic parallax star field initialized! Use window.starFieldConfig to adjust settings and window.regenerateStars() to apply changes.');
});
