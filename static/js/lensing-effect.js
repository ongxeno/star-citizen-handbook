/**
 * Gravitational Lensing Background Effect with Multiple Black Holes
 * 
 * This script creates a high-performance, WebGL-based starfield with multiple 
 * gravitational lensing effects that can be easily integrated into any website.
 * 
 * Author: Gemini
 * Version: 2.0.0
 * 
 * Dependencies:
 * - three.js (r128)
 * - EffectComposer.js
 * - RenderPass.js
 * - ShaderPass.js
 * - FXAAShader.js
 * 
 * Instructions:
 * 1. Include the required Three.js scripts in your HTML file before this one.
 * 2. Create a new instance of the `LensingEffect` class.
 * 3. Call the `init()` method.
 * 4. Use the public API to add/remove/modify black holes.
 * 
 * Example:
 * const effect = new LensingEffect({
 *   container: document.body,
 *   config: {
 *     mass: 300.0,
 *     eventHorizonRadius: 20.0,
 *     lensingRadiusMultiplier: 10.0
 *   }
 * });
 * effect.init();
 * 
 * // Add additional black holes
 * effect.addBlackHole(100, 200, 250, 15, 8);
 * effect.addBlackHole(500, 300, 400, 25, 12);
 * 
 * // Remove a black hole
 * effect.removeBlackHole(1);
 * 
 * // Update black hole position
 * effect.updateBlackHolePosition(0, 250, 250);
 */

class StarField {
    constructor(config, renderer) {
        this.config = config;
        this.renderer = renderer;
        this.scene = null;
        this.material = null;
    }

    init() {
        // Get document dimensions first
        const getDocumentHeight = () => Math.max(
            document.body.scrollHeight, document.body.offsetHeight,
            document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight
        );
        const documentHeight = getDocumentHeight();
        const viewportWidth = window.innerWidth;

        this.scene = new THREE.Scene();
        const starGeometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];
        const brightnessMultipliers = [];

        const starColorsConfig = {
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
        };
        const allStarColorsHex = Object.values(starColorsConfig).flat();
        const allStarColors = allStarColorsHex.map(c => new THREE.Color(c));

        // Generate stars across the entire document area
        const generationWidth = viewportWidth;
        const generationHeight = documentHeight;

        // Calculate number of stars based on density and total area
        const totalArea = generationWidth * generationHeight;
        const calculatedStarCount = Math.floor(totalArea * this.config.starDensity);
        
        console.log(`Star generation: ${generationWidth}x${generationHeight} area = ${totalArea} pixels, density = ${this.config.starDensity}, stars = ${calculatedStarCount}`);

        for (let i = 0; i < calculatedStarCount; i++) {
            positions.push(
                (Math.random() - 0.5) * generationWidth,
                (Math.random() - 0.5) * generationHeight,
                this.config.starfieldMinZ + Math.random() * (this.config.starfieldMaxZ - this.config.starfieldMinZ)
            );
            const randomColor = allStarColors[Math.floor(Math.random() * allStarColors.length)];
            colors.push(randomColor.r, randomColor.g, randomColor.b);
            
            // Generate individual brightness multiplier for each star
            const brightnessMultiplier = this.config.starBrightnessMultiplierMin + 
                Math.random() * (this.config.starBrightnessMultiplierMax - this.config.starBrightnessMultiplierMin);
            brightnessMultipliers.push(brightnessMultiplier);
        }
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        starGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        starGeometry.setAttribute('brightnessMultiplier', new THREE.Float32BufferAttribute(brightnessMultipliers, 1));

        this.material = new THREE.ShaderMaterial({
            uniforms: {
                size: { value: this.config.starBaseSize * this.renderer.getPixelRatio() },
                u_starfieldMinZ: { value: this.config.starfieldMinZ },
                u_starfieldMaxZ: { value: this.config.starfieldMaxZ },
                u_starfieldMinBrightness: { value: this.config.starfieldMinBrightness },
                u_starfieldMaxBrightness: { value: this.config.starfieldMaxBrightness }
            },
            vertexShader: `
                attribute float brightnessMultiplier;
                varying vec3 vColor;
                varying float vDepth;
                varying float vBrightnessMultiplier;
                uniform float size;
                void main() {
                    vColor = color;
                    vBrightnessMultiplier = brightnessMultiplier;
                    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                    vDepth = -mvPosition.z;
                    float pointSize = size * (10.0 / -mvPosition.z);
                    gl_PointSize = pointSize;
                    gl_Position = projectionMatrix * mvPosition;
                }
            `,
            fragmentShader: `
                varying vec3 vColor;
                varying float vDepth;
                varying float vBrightnessMultiplier;
                uniform float u_starfieldMinZ;
                uniform float u_starfieldMaxZ;
                uniform float u_starfieldMinBrightness;
                uniform float u_starfieldMaxBrightness;

                void main() {
                    // Center of the star, offset to the "north" (smaller Y in gl_PointCoord)
                    vec2 center = vec2(0.5, 0.5); 
                    
                    // Calculate distance from the fragment to the offset center
                    float dist = length(gl_PointCoord - center);

                    // Create a gradient that is 1.0 at the center and falls off to 0.0 at the edge
                    // This creates a soft, spherical appearance.
                    float gradient = 1.0 - smoothstep(0.2, 0.5, dist);

                    // Discard pixels that are fully transparent
                    if (gradient <= 0.0) discard;

                    // --- Existing brightness calculation based on depth ---
                    float minDepth = -u_starfieldMaxZ; 
                    float maxDepth = -u_starfieldMinZ; 
                    float depthRange = maxDepth - minDepth;
                    float brightnessRange = u_starfieldMaxBrightness - u_starfieldMinBrightness;
                    
                    float normalizedDepth = (vDepth - minDepth) / depthRange;
                    
                    float baseBrightness = u_starfieldMaxBrightness - normalizedDepth * brightnessRange;
                    baseBrightness = clamp(baseBrightness, u_starfieldMinBrightness, u_starfieldMaxBrightness);
                    
                    // Apply individual star brightness multiplier
                    float finalBrightness = baseBrightness * vBrightnessMultiplier;

                    // The gradient now controls the alpha, making the star opaque in the center
                    // and transparent at the edges. The color is no longer multiplied by the gradient.
                    gl_FragColor = vec4(vColor * finalBrightness, gradient);
                }
            `,
            blending: THREE.NormalBlending,
            depthTest: true,
            transparent: true,
            vertexColors: true
        });

        const starPoints = new THREE.Points(starGeometry, this.material);
        this.scene.add(starPoints);
    }

    updateSize() {
        if (this.material) {
            this.material.uniforms.size.value = this.config.starBaseSize * this.renderer.getPixelRatio();
        }
    }
}

class GravitationalLens {
    constructor(config) {
        this.config = config;
        this.material = null;
        this.pass = null;
        this.blackHoles = []; // Array to store multiple black holes
        this.maxBlackHoles = config.maxBlackHoles || 50; // Dynamic max based on config
    }

    // Add a black hole at specified position
    addBlackHole(x, y, mass = null, eventHorizonRadius = null, lensingRadiusMultiplier = null, debugColor = null) {
        const blackHole = {
            position: new THREE.Vector2(x, y),
            mass: mass || this.config.mass,
            eventHorizonRadius: eventHorizonRadius || this.config.eventHorizonRadius,
            lensingRadiusMultiplier: lensingRadiusMultiplier || this.config.lensingRadiusMultiplier,
            debugColor: debugColor || null // Store custom debug color if provided
        };
        this.blackHoles.push(blackHole);
        this.updateUniforms();
        return blackHole;
    }

    // Remove a black hole
    removeBlackHole(index) {
        if (index >= 0 && index < this.blackHoles.length) {
            this.blackHoles.splice(index, 1);
            this.updateUniforms();
        }
    }

    // Update a specific black hole's position
    updateBlackHolePosition(index, x, y) {
        if (index >= 0 && index < this.blackHoles.length) {
            this.blackHoles[index].position.set(x, y);
            this.updateUniforms();
        }
    }

    // Update all black hole positions (for scroll effects)
    updateAllPositions(offsetY = 0) {
        this.blackHoles.forEach((blackHole, index) => {
            // Update Y position based on scroll offset
            const baseY = blackHole.baseY || blackHole.position.y;
            if (blackHole.baseY === undefined) {
                blackHole.baseY = blackHole.position.y;
            }
            blackHole.position.y = baseY + offsetY;
        });
        this.updateUniforms();
    }

    // Update shader uniforms with current black hole data
    updateUniforms() {
        if (!this.material) return;

        const positions = new Float32Array(this.maxBlackHoles * 2); // x, y pairs
        const masses = new Float32Array(this.maxBlackHoles);
        const eventHorizonRadii = new Float32Array(this.maxBlackHoles);
        const lensingRadiusMultipliers = new Float32Array(this.maxBlackHoles);
        const debugColors = new Float32Array(this.maxBlackHoles * 3); // rgb triplets for each black hole

        // Fill arrays with black hole data
        for (let i = 0; i < this.maxBlackHoles; i++) {
            if (i < this.blackHoles.length) {
                const bh = this.blackHoles[i];
                positions[i * 2] = bh.position.x;
                positions[i * 2 + 1] = bh.position.y;
                masses[i] = bh.mass;
                eventHorizonRadii[i] = bh.eventHorizonRadius;
                lensingRadiusMultipliers[i] = bh.lensingRadiusMultiplier;
                
                // Set debug color if provided, otherwise set default color based on index
                if (bh.debugColor) {
                    // Convert hex color to RGB components if it's a string
                    if (typeof bh.debugColor === 'string') {
                        const color = new THREE.Color(bh.debugColor);
                        debugColors[i * 3] = color.r;
                        debugColors[i * 3 + 1] = color.g;
                        debugColors[i * 3 + 2] = color.b;
                    } 
                    // If it's already a THREE.Color object
                    else if (bh.debugColor instanceof THREE.Color) {
                        debugColors[i * 3] = bh.debugColor.r;
                        debugColors[i * 3 + 1] = bh.debugColor.g;
                        debugColors[i * 3 + 2] = bh.debugColor.b;
                    }
                    // If it's a RGB array
                    else if (Array.isArray(bh.debugColor) && bh.debugColor.length >= 3) {
                        debugColors[i * 3] = bh.debugColor[0];
                        debugColors[i * 3 + 1] = bh.debugColor[1];
                        debugColors[i * 3 + 2] = bh.debugColor[2];
                    }
                } else {
                    // Default color-coding based on index
                    debugColors[i * 3] = (i % 3) / 2.0;
                    debugColors[i * 3 + 1] = ((i + 1) % 3) / 2.0;
                    debugColors[i * 3 + 2] = ((i + 2) % 3) / 2.0;
                }
            } else {
                // Fill remaining slots with inactive black holes (mass = 0)
                positions[i * 2] = 0;
                positions[i * 2 + 1] = 0;
                masses[i] = 0;
                eventHorizonRadii[i] = 0;
                lensingRadiusMultipliers[i] = 0;
                debugColors[i * 3] = 0;
                debugColors[i * 3 + 1] = 0;
                debugColors[i * 3 + 2] = 0;
            }
        }

        this.material.uniforms.u_blackHoleCount.value = Math.min(this.blackHoles.length, this.maxBlackHoles);
        this.material.uniforms.u_blackHolePositions.value = positions;
        this.material.uniforms.u_masses.value = masses;
        this.material.uniforms.u_eventHorizonRadii.value = eventHorizonRadii;
        this.material.uniforms.u_lensingRadiusMultipliers.value = lensingRadiusMultipliers;
        this.material.uniforms.u_debugColors.value = debugColors;

        // Warn if we exceed the maximum
        if (this.blackHoles.length > this.maxBlackHoles) {
            console.warn(`Warning: ${this.blackHoles.length} black holes created, but only ${this.maxBlackHoles} will be rendered. Increase maxBlackHoles in config to render more.`);
        }
    }

    createMaterial() {
        // Generate dynamic shader code based on maxBlackHoles
        const fragmentShaderCode = this.generateFragmentShader();
        
        this.material = new THREE.ShaderMaterial({
            uniforms: {
                tDiffuse: { value: null },
                u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight * this.config.verticalOverRenderMultiplier) },
                u_blackHoleCount: { value: 0 },
                u_blackHolePositions: { value: new Float32Array(this.maxBlackHoles * 2) },
                u_masses: { value: new Float32Array(this.maxBlackHoles) },
                u_eventHorizonRadii: { value: new Float32Array(this.maxBlackHoles) },
                u_lensingRadiusMultipliers: { value: new Float32Array(this.maxBlackHoles) },
                u_debugColors: { value: new Float32Array(this.maxBlackHoles * 3) }, // RGB colors for each black hole
                u_debug: { value: this.config.debug }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: fragmentShaderCode
        });
        this.pass = new THREE.ShaderPass(this.material);
        return this.pass;
    }

    generateFragmentShader() {
        return `
            uniform sampler2D tDiffuse; 
            uniform vec2 u_resolution;
            uniform int u_blackHoleCount;
            uniform float u_blackHolePositions[${this.maxBlackHoles * 2}]; // Dynamic array size
            uniform float u_masses[${this.maxBlackHoles}];
            uniform float u_eventHorizonRadii[${this.maxBlackHoles}];
            uniform float u_lensingRadiusMultipliers[${this.maxBlackHoles}];
            uniform float u_debugColors[${this.maxBlackHoles * 3}]; // RGB colors for each black hole
            uniform bool u_debug;

            varying vec2 vUv;

            void main() {
                vec2 pixelCoords = vUv * u_resolution;
                vec2 totalDisplacement = vec2(0.0);
                bool inEventHorizon = false;
                
                // Process each black hole - dynamic loop limit
                for (int i = 0; i < ${this.maxBlackHoles}; i++) {
                    if (i >= u_blackHoleCount) break;
                    
                    vec2 blackHolePos = vec2(u_blackHolePositions[i * 2], u_blackHolePositions[i * 2 + 1]);
                    vec2 toBlackHole = blackHolePos - pixelCoords;
                    float dist = length(toBlackHole);
                    
                    // Check if pixel is within event horizon
                    if (dist < u_eventHorizonRadii[i]) {
                        inEventHorizon = true;
                        continue; // Skip lensing calculation for this black hole
                    }
                    
                    // Calculate gravitational lensing displacement
                    vec2 displacement = normalize(toBlackHole) * u_masses[i] / dist;
                    float falloff = 1.0 - smoothstep(u_eventHorizonRadii[i], u_eventHorizonRadii[i] * u_lensingRadiusMultipliers[i], dist);
                    displacement *= falloff;
                    
                    totalDisplacement += displacement;
                }
                
                // Apply total displacement
                vec2 sourceUv = vUv + totalDisplacement / u_resolution;
                vec4 finalColor = texture2D(tDiffuse, sourceUv);

                // Debug visualization
                if (u_debug) {
                    for (int i = 0; i < ${this.maxBlackHoles}; i++) {
                        if (i >= u_blackHoleCount) break;
                        
                        vec2 blackHolePos = vec2(u_blackHolePositions[i * 2], u_blackHolePositions[i * 2 + 1]);
                        float dist = length(blackHolePos - pixelCoords);
                        
                        // Get custom debug color from uniform array
                        vec3 debugColor = vec3(
                            u_debugColors[i * 3],
                            u_debugColors[i * 3 + 1],
                            u_debugColors[i * 3 + 2]
                        );
                        
                        float lensingRadius = u_eventHorizonRadii[i] * u_lensingRadiusMultipliers[i];
                        
                        // Show lensing radius boundary as a thin colored ring
                        float lensingEdge = abs(dist - lensingRadius);
                        finalColor.rgb = mix(debugColor, finalColor.rgb, smoothstep(0.0, 3.0, lensingEdge));
                        
                        // Show event horizon as white ring
                        float horizonEdge = abs(dist - u_eventHorizonRadii[i]);
                        finalColor.rgb = mix(vec3(1.0), finalColor.rgb, smoothstep(0.0, 2.0, horizonEdge));
                        
                        // Add numerical distance indicators at specific radii
                        float quarterRadius = lensingRadius * 0.25;
                        float halfRadius = lensingRadius * 0.5;
                        float threeQuarterRadius = lensingRadius * 0.75;
                        
                        // Show quarter markers as faint lines
                        if (abs(dist - quarterRadius) < 1.0) {
                            finalColor.rgb = mix(vec3(0.8, 0.8, 0.0), finalColor.rgb, 0.7);
                        }
                        if (abs(dist - halfRadius) < 1.0) {
                            finalColor.rgb = mix(vec3(0.0, 0.8, 0.8), finalColor.rgb, 0.7);
                        }
                        if (abs(dist - threeQuarterRadius) < 1.0) {
                            finalColor.rgb = mix(vec3(0.8, 0.0, 0.8), finalColor.rgb, 0.7);
                        }
                    }
                }

                // Render event horizon as black
                if (inEventHorizon) {
                    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
                } else {
                    gl_FragColor = finalColor;
                }
            }
        `;
    }

    updatePosition(x, y) {
        // Backward compatibility: update first black hole if it exists
        if (this.blackHoles.length > 0) {
            this.updateBlackHolePosition(0, x, y);
        }
    }

    updateResolution(width, height) {
        if (this.material) {
            this.material.uniforms.u_resolution.value.set(width, height);
        }
    }
}

class LensingEffect {
    constructor(options = {}) {
        this.container = options.container || document.body;
        this.config = {
            // Rendering settings
            verticalOverRenderMultiplier: 1.5, // Multiplier for vertical over-rendering to accommodate mobile address bar resizing
            
            // Starfield settings
            starDensity: 0.03,              // Stars per square pixel (controls star density based on viewport and document size)
            starBaseSize: 80.0,             // Base size of stars, adjusted by distance
            starfieldMinZ: -1500,           // The minimum z-position for a star (farthest)
            starfieldMaxZ: -70,            // The maximum z-position for a star (closest)
            starfieldMinBrightness: 0.8,    // Minimum brightness of the farthest star
            starfieldMaxBrightness: 1.0,    // Maximum brightness of the closest star
            starBrightnessMultiplierMin: 0.3, // Minimum individual star brightness multiplier
            starBrightnessMultiplierMax: 0.9, // Maximum individual star brightness multiplier
            cameraZ: 10,                    // Z-position of the camera
            parallaxFactor: 0.1,            // How much the starfield moves on scroll (higher is more)

            // Default black hole physics
            mass: 250.0,                    // Default gravitational mass (lensing strength)
            eventHorizonRadius: 5.0,        // Default radius of the black hole's center
            lensingRadiusMultiplier: 8.0,   // Default multiplier for the size of the lensing effect ring

            // Random black hole generation
            minBlackHoles: 2,              // Minimum number of black holes to generate randomly
            maxBlackHoles: 5,              // Maximum number of black holes the system can handle
            minBlackHolesMass: 500,         // Minimum mass for randomly generated black holes
            maxBlackHolesMass: 2000,        // Maximum mass for randomly generated black holes
            minEventHorizonRadius: 1,       // Minimum event horizon radius for random black holes
            maxEventHorizonRadius: 5,       // Maximum event horizon radius for random black holes
            minLensingRadiusMultiplier: 50,  // Minimum lensing radius multiplier for random black holes
            maxLensingRadiusMultiplier: 50,  // Maximum lensing radius multiplier for random black holes

            // Debugging
            debug: false,                    // Enables debug mode (shows overlays and lensing rings)
            debugBlackHolePosition: false,  // If true (and debug is true), uses fixed BH1-BH6 positions
            
            // Animation
            orbitalMovement: true,          // Enable/disable orbital animation for black holes
            minSpeedX: 0.0,                 // Min horizontal speed for orbital movement
            maxSpeedX: 0.1,                 // Max horizontal speed for orbital movement
            minSpeedY: 0.0,                 // Min vertical speed for orbital movement
            maxSpeedY: 0.1,                 // Max vertical speed for orbital movement
            minRadiusX: 20,                 // Min horizontal orbit radius
            maxRadiusX: 40,                 // Max horizontal orbit radius
            minRadiusY: 15,                 // Min vertical orbit radius
            maxRadiusY: 30,                 // Max vertical orbit radius

            ...options.config,
        };

        // Components
        this.starField = null;
        this.gravitationalLens = null;
        
        // Debug elements
        this.debugOverlays = [];
        
        // Initialize scroll position
        this.scrollY = window.pageYOffset || 0;

        // Bind methods to the instance
        this.animate = this.animate.bind(this);
        this.onScroll = this.onScroll.bind(this);
    }

    init() {
        this.setupBase();
        this.setupComponents();
        this.setupPostProcessing();
        this.setupDefaultBlackHoles();
        this.addEventListeners();
        this.animate();
        console.log("Lensing Effect Initialized.");
    }

    setupDefaultBlackHoles() {
        // Get the full document height to distribute black holes across entire content
        const getDocumentHeight = () => Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );
        
        const documentHeight = getDocumentHeight();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        console.log(`Document height: ${documentHeight}px`);
        console.log(`Viewport dimensions: ${viewportWidth}px × ${viewportHeight}px`);

        if (this.config.debug && this.config.debugBlackHolePosition) {
            // Define 6 specific black holes at strategic positions for debugging
            const blackHoles = [
                // 1) Top left of document
                { x: 100, y: viewportHeight - 200, documentY: 200, label: "BH1: Top Left (Document)", name: "BH1", debugColor: "#FF5555" },
                // 2) Top right of document
                { x: viewportWidth - 100, y: viewportHeight - 200, documentY: 200, label: "BH2: Top Right (Document)", name: "BH2", debugColor: "#55FF55" },
                // 3) Middle left of document
                { x: 100, y: viewportHeight - (documentHeight / 2), documentY: documentHeight / 2, label: "BH3: Middle Left (Document)", name: "BH3", debugColor: "#5555FF" },
                // 4) Middle right of document
                { x: viewportWidth - 100, y: viewportHeight - (documentHeight / 2), documentY: documentHeight / 2, label: "BH4: Middle Right (Document)", name: "BH4", debugColor: "#FFFF55" },
                // 5) Bottom left of document
                { x: 100, y: viewportHeight - (documentHeight - 200), documentY: documentHeight - 200, label: "BH5: Bottom Left (Document)", name: "BH5", debugColor: "#FF55FF" },
                // 6) Bottom right of document
                { x: viewportWidth - 100, y: viewportHeight - (documentHeight - 200), documentY: documentHeight - 200, label: "BH6: Bottom Right (Document)", name: "BH6", debugColor: "#55FFFF" }
            ];
            
            console.log(`Adding ${blackHoles.length} fixed position black holes for debugging:`);
            
            blackHoles.forEach((bh, i) => {
                const mass = 200;
                const eventHorizonRadius = 15;
                const lensingRadiusMultiplier = 5;
                
                this.addBlackHole(bh.x, bh.y, mass, eventHorizonRadius, lensingRadiusMultiplier, bh.debugColor);
                
                const addedBlackHole = this.gravitationalLens.blackHoles[this.gravitationalLens.blackHoles.length - 1];
                addedBlackHole.name = bh.name;
                addedBlackHole.documentY = bh.documentY;
                
                console.log(`Black hole ${bh.name} - ${bh.label} - pos(${Math.round(bh.x)}, ${Math.round(bh.y)}), document Y: ${Math.round(bh.documentY)}, mass: ${mass}, radius: ${eventHorizonRadius}, debug color: ${bh.debugColor || 'default'}`);
            });

        } else {
            // Generate a random number of black holes
            const numBlackHoles = this.config.minBlackHoles + Math.floor(Math.random() * (this.config.maxBlackHoles - this.config.minBlackHoles + 1));
            console.log(`Adding ${numBlackHoles} random black holes:`);

            for (let i = 0; i < numBlackHoles; i++) {
                const documentY = Math.random() * documentHeight;
                const x = Math.random() * viewportWidth;
                const y = viewportHeight - documentY; // Convert documentY to shader Y

                const mass = this.config.minBlackHolesMass + Math.random() * (this.config.maxBlackHolesMass - this.config.minBlackHolesMass);
                const eventHorizonRadius = this.config.minEventHorizonRadius + Math.random() * (this.config.maxEventHorizonRadius - this.config.minEventHorizonRadius);
                const lensingRadiusMultiplier = this.config.minLensingRadiusMultiplier + Math.random() * (this.config.maxLensingRadiusMultiplier - this.config.minLensingRadiusMultiplier);
                const randomColor = '#' + new THREE.Color(0xffffff).setHSL(Math.random(), 1.0, 0.5).getHexString();
                
                this.addBlackHole(x, y, mass, eventHorizonRadius, lensingRadiusMultiplier, randomColor);
                
                const addedBlackHole = this.gravitationalLens.blackHoles[i];
                addedBlackHole.name = `RBH${i}`;
                addedBlackHole.documentY = documentY;

                console.log(`Random Black hole ${i} - pos(${Math.round(x)}, ${Math.round(y)}), document Y: ${Math.round(documentY)}, mass: ${mass.toFixed(0)}, radius: ${eventHorizonRadius.toFixed(0)}, color: ${randomColor}`);
            }
        }
    }

    // Public API for managing black holes
    addBlackHole(x, y, mass = null, eventHorizonRadius = null, lensingRadiusMultiplier = null, debugColor = null) {
        return this.gravitationalLens.addBlackHole(x, y, mass, eventHorizonRadius, lensingRadiusMultiplier, debugColor);
    }

    removeBlackHole(index) {
        this.gravitationalLens.removeBlackHole(index);
    }

    updateBlackHolePosition(index, x, y) {
        this.gravitationalLens.updateBlackHolePosition(index, x, y);
    }

    getBlackHoleCount() {
        return this.gravitationalLens.blackHoles.length;
    }

    getBlackHole(index) {
        return this.gravitationalLens.blackHoles[index];
    }

    // Clear all black holes
    clearBlackHoles() {
        this.gravitationalLens.blackHoles = [];
        this.gravitationalLens.updateUniforms();
        this.clearDebugOverlays();
    }

    // Clear debug overlays
    clearDebugOverlays() {
        this.debugOverlays.forEach(overlay => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        });
        this.debugOverlays = [];
    }

    // Create debug overlay for a black hole
    createDebugOverlay(x, y, index) {
        if (!this.config.debug) return;
        
        const blackHole = this.gravitationalLens.blackHoles[index];
        const name = blackHole.name || `BH${index}`;
        const debugColor = blackHole.debugColor || '#FFFFFF';
        
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            pointer-events: none;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 10px;
            white-space: nowrap;
            z-index: 1000;
            transform: translate(-50%, -50%);
            border-left: 4px solid ${debugColor};
        `;
        
        overlay.textContent = `${name}: (${x.toFixed(2)}, ${y.toFixed(2)})`;
        overlay.style.left = x + 'px';
        overlay.style.top = y + 'px';
        
        document.body.appendChild(overlay);
        this.debugOverlays.push(overlay);
        
        return overlay;
    }

    // Update debug overlays
    updateDebugOverlays() {
        if (!this.config.debug) return;
        
        // Clear existing overlays
        this.clearDebugOverlays();

        // Use the same document height calculation as other methods
        const getDocumentHeight = () => Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );
        
        // Create new overlays for each black hole
        this.gravitationalLens.blackHoles.forEach((blackHole, index) => {
            const x = blackHole.position.x;
            
            // The position is already properly calculated in the animate method
            // and stored in the blackHole.position object
            const shaderY = blackHole.position.y;
            const screenY = window.innerHeight - shaderY;
            
            // Only show debug overlays for black holes that are currently visible on screen
            const isOnScreen = screenY >= 0 && screenY <= window.innerHeight && 
                               x >= 0 && x <= window.innerWidth;
            
            // Add some buffer around the viewport to show black holes that are just off-screen
            const isNearScreen = screenY >= -200 && screenY <= window.innerHeight + 200 && 
                                x >= -200 && x <= window.innerWidth + 200;
            
            if (isOnScreen || isNearScreen) {
                this.createDebugOverlay(x, screenY, index);
            }
        });
    }

    // Regenerate random black holes
    regenerateRandomBlackHoles() {
        this.clearBlackHoles();
        this.setupDefaultBlackHoles();
        console.log("Regenerated random black holes!");
    }

    setupBase() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 150%;
            z-index: -1;
            outline: none;
        `;
        this.container.appendChild(this.canvas);

        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas });
        this.renderer.setSize(window.innerWidth, window.innerHeight * this.config.verticalOverRenderMultiplier);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / (window.innerHeight * this.config.verticalOverRenderMultiplier), 0.1, 2000);
        this.camera.position.z = this.config.cameraZ;
    }

    setupComponents() {
        // Initialize StarField
        this.starField = new StarField(this.config, this.renderer);
        this.starField.init();

        // Initialize Gravitational Lens
        this.gravitationalLens = new GravitationalLens(this.config);
    }

    setupPostProcessing() {
        this.composer = new THREE.EffectComposer(this.renderer);

        // Pass 1: Render the starfield
        const renderPass = new THREE.RenderPass(this.starField.scene, this.camera);
        this.composer.addPass(renderPass);

        // Pass 2: Apply gravitational lensing
        const lensingPass = this.gravitationalLens.createMaterial();
        this.composer.addPass(lensingPass);

        // Pass 3: Apply FXAA anti-aliasing
        this.fxaaPass = new THREE.ShaderPass(THREE.FXAAShader);
        this.fxaaPass.material.uniforms['resolution'].value.x = 0.5 / (window.innerWidth * this.renderer.getPixelRatio());
        this.fxaaPass.material.uniforms['resolution'].value.y = 0.5 / (window.innerHeight * this.config.verticalOverRenderMultiplier * this.renderer.getPixelRatio());
        this.composer.addPass(this.fxaaPass);
    }
    
    addEventListeners() {
        window.addEventListener('scroll', this.onScroll);
        window.addEventListener('resize', this.onResize);
    }

    onScroll() {
        this.scrollY = window.pageYOffset;
    }

    animate() {
        requestAnimationFrame(this.animate);

        // Update camera for parallax effect
        this.camera.position.y = -this.scrollY * this.config.parallaxFactor;
        
        // Create dynamic movement for all black holes
        const time = Date.now() * 0.001; // Time in seconds
        
        this.gravitationalLens.blackHoles.forEach((blackHole, index) => {
            // Store original position and document position if not already stored
            if (!blackHole.originalX) {
                blackHole.originalX = blackHole.position.x;
                blackHole.originalY = blackHole.position.y;
                
                // Get document height
                const getDocumentHeight = () => Math.max(
                    document.body.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.clientHeight,
                    document.documentElement.scrollHeight,
                    document.documentElement.offsetHeight
                );
                const documentHeight = getDocumentHeight();
                
                // Calculate and store document position
                blackHole.documentX = blackHole.position.x; // X doesn't change with scroll
                blackHole.documentY = blackHole.position.y;
                
                // Store the original document Y to keep blackholes within their section
                blackHole.originalDocumentY = blackHole.documentY;
                
                // Store the original document Y to keep blackholes within their section
                blackHole.originalDocumentY = blackHole.documentY;
                
                
                // Give each black hole unique movement characteristics
                blackHole.speedX = this.config.minSpeedX + Math.random() * (this.config.maxSpeedX - this.config.minSpeedX);
                blackHole.speedY = this.config.minSpeedY + Math.random() * (this.config.maxSpeedY - this.config.minSpeedY);
                blackHole.radiusX = this.config.minRadiusX + Math.random() * (this.config.maxRadiusX - this.config.minRadiusX);
                blackHole.radiusY = this.config.minRadiusY + Math.random() * (this.config.maxRadiusY - this.config.minRadiusY);
                blackHole.phaseX = Math.random() * Math.PI * 2; // Random phase offset
                blackHole.phaseY = Math.random() * Math.PI * 2;
                
                console.log(`Black hole ${index} (${blackHole.name || ''}) original screen pos: (${blackHole.originalX}, ${blackHole.originalY}), document pos: (${blackHole.documentX}, ${blackHole.documentY})`);
            }
            
            if (this.config.orbitalMovement) {
                // Calculate new position with orbital movement relative to document position
                const newDocumentX = blackHole.documentX + 
                            Math.sin(time * blackHole.speedX + blackHole.phaseX) * blackHole.radiusX;
                
                // Limit vertical movement to stay relatively near original position
                const maxYDeviation = Math.min(100, window.innerHeight * this.config.verticalOverRenderMultiplier * 0.2); // Maximum 20% of viewport or 100px
                const yOffset = Math.cos(time * blackHole.speedY + blackHole.phaseY) * blackHole.radiusY;
                const newDocumentY = blackHole.originalDocumentY + yOffset * (maxYDeviation / blackHole.radiusY);
                
                // Convert document coordinates to screen coordinates
                const newX = newDocumentX; // X doesn't change with scroll
                const newY = newDocumentY + this.scrollY; // Apply scroll offset
                
                this.gravitationalLens.updateBlackHolePosition(index, newX, newY);
            } else {
                // Just update Y position for scroll without animation
                const newY = blackHole.documentY + this.scrollY;
                this.gravitationalLens.updateBlackHolePosition(index, blackHole.originalX, newY);
            }
        });

        // Update debug overlays if debug mode is enabled
        if (this.config.debug) {
            this.updateDebugOverlays();
        }

        // Render the scene using the composer
        this.composer.render();
    }

}
