You are a Star Citizen ship expert. Generate metadata and basic information for the ship: {{SHIP_NAME}}

Provide the following information in JSON format:
- manufacturer: The ship manufacturer (e.g., "Drake", "RSI", "Aegis")
- ship_name: The exact ship name without the manufacturer (e.g., "Cutlass Black", "Constellation Andromeda")
- primary_role_description: Brief role description in English (e.g., "Multi-role Fighter", "Cargo Hauler")
- thai_subtitle: A catchy Thai subtitle for the guide
- thai_description: SEO-friendly Thai description (1-2 sentences)
- keywords: Array of 3-5 relevant English keywords
- thai_keyword: One relevant Thai keyword
- weight: A number 1-10 for ordering
- hero_shot_description: Brief description for hero image (e.g., "landing on a moon", "in combat")
- ship_name_slug: URL-friendly version of ship manufacturer and ship name (lowercase, hyphens)

Return ONLY valid JSON.
