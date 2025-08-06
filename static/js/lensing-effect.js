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
 * - CopyShader.js
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
        this.scene = new THREE.Scene();
        const starGeometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];

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

        for (let i = 0; i < this.config.starCount; i++) {
            positions.push(
                (Math.random() - 0.5) * 2000,
                (Math.random() - 0.5) * 2000,
                (Math.random() - 0.5) * 2000
            );
            const randomColor = allStarColors[Math.floor(Math.random() * allStarColors.length)];
            colors.push(randomColor.r, randomColor.g, randomColor.b);
        }
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        starGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        this.material = new THREE.ShaderMaterial({
            uniforms: {
                size: { value: this.config.starBaseSize * this.renderer.getPixelRatio() }
            },
            vertexShader: `
                varying vec3 vColor;
                uniform float size;
                void main() {
                    vColor = color;
                    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                    float pointSize = size * (10.0 / -mvPosition.z);
                    // Limit the maximum star size to prevent overly large stars
                    gl_PointSize = clamp(pointSize, 1.6, 4.0);
                    gl_Position = projectionMatrix * mvPosition;
                }
            `,
            fragmentShader: `
                varying vec3 vColor;
                void main() {
                    if (length(gl_PointCoord - vec2(0.5, 0.5)) > 0.48) discard;
                    gl_FragColor = vec4(vColor, 1.0);
                }
            `,
            blending: THREE.AdditiveBlending,
            depthTest: false,
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
                u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
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
                    displacement *= falloff * falloff;
                    
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
                        float lensingEdge = abs(dist - lensingRadius);
                        finalColor.rgb = mix(debugColor, finalColor.rgb, smoothstep(0.0, 2.0, lensingEdge));
                        
                        float horizonEdge = abs(dist - u_eventHorizonRadii[i]);
                        finalColor.rgb = mix(vec3(1.0), finalColor.rgb, smoothstep(0.0, 2.0, horizonEdge));
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
            starCount: 50000,
            starBaseSize: 40.0,        // Increased from 15.0 for larger stars
            cameraZ: 10,
            parallaxFactor: 0.15,      // Increased from 0.02 for stronger parallax
            mass: 250.0,
            eventHorizonRadius: 25.0,
            lensingRadiusMultiplier: 8.0,
            minBlackHoles: 5,          // Minimum number of black holes to generate
            maxBlackHoles: 100,        // Maximum number of black holes the system can handle
            minBlackHolesMass: 100,    // Minimum mass for randomly generated black holes
            maxBlackHolesMass: 1000,   // Maximum mass for randomly generated black holes
            debug: true,
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
        this.onResize = this.onResize.bind(this);
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
        
        // Define 6 specific black holes at strategic positions
        // Since we can access the document height, we should convert the viewport positions 
        // to document positions to THREE positions here.
        const blackHoles = [
            // 1) Top left of document
            {
                x: 100,
                y: viewportHeight - 200,
                documentY: 200,
                label: "BH1: Top Left (Document)",
                name: "BH1",
                debugColor: "#FF5555"
            },

            // 2) Top right of document
            {
                x: viewportWidth - 100,
                y: viewportHeight - 200,
                documentY: 200,
                label: "BH2: Top Right (Document)",
                name: "BH2",
                debugColor: "#55FF55"
            },

            // 3) Middle left of document
            {
                x: 100,
                y: viewportHeight - (documentHeight / 2),
                documentY: documentHeight / 2,
                label: "BH3: Middle Left (Document)",
                name: "BH3",
                debugColor: "#5555FF"
            },

            // 4) Middle right of document
            {
                x: viewportWidth - 100,
                y: viewportHeight - (documentHeight / 2),
                documentY: documentHeight / 2,
                label: "BH4: Middle Right (Document)",
                name: "BH4",
                debugColor: "#FFFF55"
            },

            // 5) Bottom left of document
            {
                x: 100,
                y: viewportHeight - (documentHeight - 200),
                documentY: documentHeight - 200,
                label: "BH5: Bottom Left (Document)",
                name: "BH5",
                debugColor: "#FF55FF"
            },

            // 6) Bottom right of document
            {
                x: viewportWidth - 100,
                y: viewportHeight - (documentHeight - 200),
                documentY: documentHeight - 200,
                label: "BH6: Bottom Right (Document)",
                name: "BH6",
                debugColor: "#55FFFF"
            }
        ];
        
        console.log(`Adding ${blackHoles.length} fixed position black holes:`);
        
        // Create each black hole with unique properties
        blackHoles.forEach((bh, i) => {
            // Vary the properties slightly for each black hole
            const mass = 200 + (i * 50); // Range from 200-450
            const eventHorizonRadius = 15 + (i * 3); // Range from 15-30
            const lensingRadiusMultiplier = 5 + (i * 0.5); // Range from 5-7.5
            
            // Add the black hole
            this.addBlackHole(bh.x, bh.y, mass, eventHorizonRadius, lensingRadiusMultiplier, bh.debugColor);
            
            // Add name property to the black hole
            const addedBlackHole = this.gravitationalLens.blackHoles[this.gravitationalLens.blackHoles.length - 1];
            addedBlackHole.name = bh.name;
            addedBlackHole.documentY = bh.documentY;
            
            console.log(`Black hole ${bh.name} - ${bh.label} - pos(${Math.round(bh.x)}, ${Math.round(bh.y)}), document Y: ${Math.round(bh.documentY)}, mass: ${mass}, radius: ${eventHorizonRadius}, debug color: ${bh.debugColor || 'default'}`);
        });
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
        
        const documentHeight = getDocumentHeight();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
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
                
                if (isOnScreen) {
                    console.log(`Black hole ${index} (${blackHole.name || ''}) visible on screen at (${Math.round(x)}, ${Math.round(screenY)})`);
                }
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
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            outline: none;
        `;
        this.container.appendChild(this.canvas);

        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
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
        this.fxaaPass.material.uniforms['resolution'].value.y = 0.5 / (window.innerHeight * this.renderer.getPixelRatio());
        this.composer.addPass(this.fxaaPass);
    }
    
    addEventListeners() {
        window.addEventListener('scroll', this.onScroll);
        window.addEventListener('resize', this.onResize);
    }

    onScroll() {
        this.scrollY = window.pageYOffset;
        // Immediately update black hole positions on scroll
        this.gravitationalLens.blackHoles.forEach((blackHole, index) => {
            if (blackHole.documentY !== undefined) {
                const screenY = blackHole.documentY - this.scrollY;
                const shaderY = window.innerHeight - screenY;
                this.gravitationalLens.updateBlackHolePosition(index, blackHole.originalX || blackHole.position.x, shaderY);
            }
        });
    }

    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        this.composer.setSize(window.innerWidth, window.innerHeight);
        
        // Update gravitational lens resolution
        this.gravitationalLens.updateResolution(window.innerWidth, window.innerHeight);
        
        // Update FXAA resolution
        this.fxaaPass.material.uniforms['resolution'].value.x = 1 / (window.innerWidth * this.renderer.getPixelRatio());
        this.fxaaPass.material.uniforms['resolution'].value.y = 1 / (window.innerHeight * this.renderer.getPixelRatio());

        // Update star field size
        this.starField.updateSize();
    }

    animate() {
        requestAnimationFrame(this.animate);

        // Update camera for parallax effect
        this.camera.position.y = -this.scrollY * 0.02;
        
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
                blackHole.speedX = (Math.random() - 0.5) * 0.3; // Random speed multiplier
                blackHole.speedY = (Math.random() - 0.5) * 0.2;
                blackHole.radiusX = 20 + Math.random() * 40; // Random orbit radius
                blackHole.radiusY = 15 + Math.random() * 30; // Limit vertical movement to stay in section
                blackHole.phaseX = Math.random() * Math.PI * 2; // Random phase offset
                blackHole.phaseY = Math.random() * Math.PI * 2;
                
                console.log(`Black hole ${index} (${blackHole.name || ''}) original screen pos: (${blackHole.originalX}, ${blackHole.originalY}), document pos: (${blackHole.documentX}, ${blackHole.documentY})`);
            }
            
            /* 
            // ANIMATION COMMENTED OUT
            // Calculate new position with orbital movement relative to document position
            // Ensure the black hole stays close to its original section by limiting Y movement
            const newDocumentX = blackHole.documentX + 
                        Math.sin(time * blackHole.speedX + blackHole.phaseX) * blackHole.radiusX;
            
            // Limit vertical movement to stay relatively near original position
            const maxYDeviation = Math.min(100, window.innerHeight * 0.2); // Maximum 20% of viewport or 100px
            const yOffset = Math.cos(time * blackHole.speedY + blackHole.phaseY) * blackHole.radiusY;
            const newDocumentY = blackHole.originalDocumentY + yOffset * (maxYDeviation / blackHole.radiusY);
            
            // Convert document coordinates to screen coordinates
            // With our simplified approach, we can just use the coordinates directly
            // Just make sure to adjust for scroll position for Y coordinate
            const newX = newDocumentX; // X doesn't change with scroll
            const newY = newDocumentY + this.scrollY; // Apply scroll offset
            
            this.gravitationalLens.updateBlackHolePosition(index, newX, newY);
            */
            
            // Just update Y position for scroll without animation
            // When scrolling down, document moves up, black holes should also move up (negative offset)
            // Black hole Y position = original document position - scroll position
            const newY = blackHole.documentY + this.scrollY;
            this.gravitationalLens.updateBlackHolePosition(index, blackHole.originalX, newY);
        });

        // Update debug overlays if debug mode is enabled
        if (this.config.debug) {
            this.updateDebugOverlays();
        }

        // Render the scene using the composer
        this.composer.render();
    }

}
