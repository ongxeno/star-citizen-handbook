// Dynamic Parallax Star Field Effect with Configurable Density
document.addEventListener('DOMContentLoaded', function() {
    let ticking = false;
    let scrollY = 0;
    
    // Star configuration - easily adjustable
    const starConfig = {
        // Star density (stars per 10000 square pixels)
        distantDensity: 50,    // Distant stars (lots of small ones)
        midDensity: 15,        // Mid-distance stars  
        closeDensity: 2,     // Close stars (fewer, bigger ones)
        
        // Parallax speeds
        distantSpeed: -0.02,    // Very slow movement
        midSpeed: -0.08,        // Medium speed
        closeSpeed: -0.15,      // Fastest movement
        
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
    
    // Create star layers using Canvas for better performance
    function createStarLayer(density, minSize, maxSize, colors, className, zIndex, targetWidth = null, targetHeight = null) {
        const width = targetWidth || window.innerWidth;
        const height = targetHeight || window.innerHeight;
        
        // Create canvas element
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas properties
        canvas.className = className;
        canvas.width = width;
        canvas.height = height * 1.2; // Extended height for parallax
        
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
                y: Math.random() * (height * 1.2),
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
        const existingCanvases = document.querySelectorAll('.star-layer-distant, .star-layer-mid, .star-layer-close');
        
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
        // Update current dimensions
        currentWidth = window.innerWidth;
        currentHeight = window.innerHeight;
        
        // Get all star colors
        const allColors = [
            ...starConfig.starColors.hot,
            ...starConfig.starColors.white,
            ...starConfig.starColors.yellow,
            ...starConfig.starColors.orange,
            ...starConfig.starColors.red
        ];
        
        // Create distant star canvas (smallest, most numerous)
        const distantCanvas = createStarLayer(
            starConfig.distantDensity, 
            0.5, 1.5, 
            [...starConfig.starColors.hot, ...starConfig.starColors.white], 
            'star-layer-distant',
            -3
        );
        
        // Create mid-distance star canvas
        const midCanvas = createStarLayer(
            starConfig.midDensity,
            1, 2.5,
            [...starConfig.starColors.white, ...starConfig.starColors.yellow],
            'star-layer-mid',
            -2
        );
        
        // Create close star canvas (largest, fewest)
        const closeCanvas = createStarLayer(
            starConfig.closeDensity,
            2, 4,
            allColors,
            'star-layer-close',
            -1
        );
        
        if (fadeIn) {
            // Start with opacity 0 and fade in
            [distantCanvas, midCanvas, closeCanvas].forEach(canvas => {
                canvas.style.opacity = '0';
                canvas.style.transition = 'opacity 0.8s ease-in';
            });
        }
        
        // Add to DOM
        document.body.appendChild(distantCanvas);
        document.body.appendChild(midCanvas);
        document.body.appendChild(closeCanvas);
        
        if (fadeIn) {
            // Trigger fade-in after a short delay
            setTimeout(() => {
                [distantCanvas, midCanvas, closeCanvas].forEach(canvas => {
                    canvas.style.opacity = '1';
                });
            }, 50);
        }
        
        console.log(`Star field ${fadeIn ? 'recreated with crossfade' : 'initialized'}: ${Math.floor((currentWidth * currentHeight / 10000) * (starConfig.distantDensity + starConfig.midDensity + starConfig.closeDensity))} total stars using Canvas`);
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
            const newHeight = window.innerHeight;
            
            // Check if there's a significant size change (5% threshold)
            const widthChange = Math.abs(newWidth - currentWidth) / currentWidth;
            const heightChange = Math.abs(newHeight - currentHeight) / currentHeight;
            
            if (widthChange > 0.05 || heightChange > 0.05) {
                // Significant change - use crossfade for smooth transition
                console.log(`Screen resized from ${currentWidth}x${currentHeight} to ${newWidth}x${newHeight}, regenerating with crossfade`);
                initStarField(true); // Always use crossfade for any significant resize
            } else {
                // Minor change - just update tracking dimensions
                currentWidth = newWidth;
                currentHeight = newHeight;
            }
        }, 150); // Slightly longer debounce for smoother experience
    }
    
    // Parallax update function
    function updateParallax() {
        scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        const distantCanvas = document.querySelector('.star-layer-distant');
        const midCanvas = document.querySelector('.star-layer-mid');
        const closeCanvas = document.querySelector('.star-layer-close');
        
        if (distantCanvas) {
            distantCanvas.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.distantSpeed}px)`;
        }
        if (midCanvas) {
            midCanvas.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.midSpeed}px)`;
        }
        if (closeCanvas) {
            closeCanvas.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.closeSpeed}px)`;
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
