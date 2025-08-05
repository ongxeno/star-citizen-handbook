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
    
    // Create star layers
    function createStarLayer(density, minSize, maxSize, colors, className, zIndex, targetWidth = null, targetHeight = null) {
        const width = targetWidth || window.innerWidth;
        const height = targetHeight || window.innerHeight;
        
        const layer = document.createElement('div');
        layer.className = className;
        layer.style.cssText = `
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: ${width}px;
            height: ${height * 1.2}px;
            pointer-events: none;
            z-index: ${zIndex};
            will-change: transform;
        `;
        
        const viewportArea = width * height;
        const starCount = Math.floor((viewportArea / 10000) * density);
        
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            const size = minSize + Math.random() * (maxSize - minSize);
            const color = colors[Math.floor(Math.random() * colors.length)];
            const x = Math.random() * 100;
            const y = Math.random() * 120; // Extended height for parallax
            const opacity = 0.3 + Math.random() * 0.7;
            
            star.style.cssText = `
                position: absolute;
                left: ${x}%;
                top: ${y}%;
                width: ${size}px;
                height: ${size}px;
                background: radial-gradient(circle, ${color} 0%, transparent 70%);
                border-radius: 50%;
                opacity: ${opacity};
            `;
            
            layer.appendChild(star);
        }
        
        return layer;
    }
    
    // Initialize star field
    function initStarField(fadeTransition = false) {
        const existingLayers = document.querySelectorAll('.star-layer-distant, .star-layer-mid, .star-layer-close');
        
        if (fadeTransition && existingLayers.length > 0) {
            // Create new layers with fade-in effect
            createNewStarLayers(true);
            
            // Fade out old layers
            existingLayers.forEach((layer, index) => {
                layer.style.transition = 'opacity 0.8s ease-out';
                layer.style.opacity = '0';
                
                // Remove old layers after fade completes
                setTimeout(() => {
                    if (layer.parentNode) {
                        layer.parentNode.removeChild(layer);
                    }
                }, 800);
            });
        } else {
            // Remove existing layers immediately
            existingLayers.forEach(layer => layer.remove());
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
        
        // Create distant star layer (smallest, most numerous)
        const distantLayer = createStarLayer(
            starConfig.distantDensity, 
            0.5, 1.5, 
            [...starConfig.starColors.hot, ...starConfig.starColors.white], 
            'star-layer-distant',
            -3
        );
        
        // Create mid-distance star layer
        const midLayer = createStarLayer(
            starConfig.midDensity,
            1, 2.5,
            [...starConfig.starColors.white, ...starConfig.starColors.yellow],
            'star-layer-mid',
            -2
        );
        
        // Create close star layer (largest, fewest)
        const closeLayer = createStarLayer(
            starConfig.closeDensity,
            2, 4,
            allColors,
            'star-layer-close',
            -1
        );
        
        if (fadeIn) {
            // Start with opacity 0 and fade in
            [distantLayer, midLayer, closeLayer].forEach(layer => {
                layer.style.opacity = '0';
                layer.style.transition = 'opacity 0.8s ease-in';
            });
        }
        
        // Add to DOM
        document.body.appendChild(distantLayer);
        document.body.appendChild(midLayer);
        document.body.appendChild(closeLayer);
        
        if (fadeIn) {
            // Trigger fade-in after a short delay
            setTimeout(() => {
                [distantLayer, midLayer, closeLayer].forEach(layer => {
                    layer.style.opacity = '1';
                });
            }, 50);
        }
        
        console.log(`Star field ${fadeIn ? 'recreated with crossfade' : 'initialized'}: ${Math.floor((currentWidth * currentHeight / 10000) * (starConfig.distantDensity + starConfig.midDensity + starConfig.closeDensity))} total stars`);
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
        
        const distantLayer = document.querySelector('.star-layer-distant');
        const midLayer = document.querySelector('.star-layer-mid');
        const closeLayer = document.querySelector('.star-layer-close');
        
        if (distantLayer) {
            distantLayer.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.distantSpeed}px)`;
        }
        if (midLayer) {
            midLayer.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.midSpeed}px)`;
        }
        if (closeLayer) {
            closeLayer.style.transform = `translateX(-50%) translateY(${scrollY * starConfig.closeSpeed}px)`;
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
