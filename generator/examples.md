# AI Blog Generator - Example Output Format

This file shows examples of the expected output format for different types of content.

## Example 1: Ship Guide (Drake Cutlass Black)

### Generated Front Matter (YAML):
```yaml
---
title: "🚀 Drake Cutlass Black - คู่มือยานอเนกประสงค์สุดคลาสสิก"
subtitle: "เรียนรู้ทุกสิ่งเกี่ยวกับยานที่ทำได้ทุกอย่าง - ขนส่ง ต่อสู้ และสำรวจ"
date: "2025-08-01"
lastmod: "2025-08-01"
draft: false
game_version: "Alpha 4.2.1"
tags: ["Drake", "Cutlass Black", "Multi-Role", "ยานขนส่ง", "ยานต่อสู้", "เริ่มต้น"]
categories: ["ยานอวกาศ"]
author: "Star Citizen Handbook Team"
weight: 5
image: "img/ships/cutlass-black/cutlass_black_hero.jpg"
description: "คู่มือสมบูรณ์สำหรับ Drake Cutlass Black ยานอเนกประสงค์ที่เป็นที่นิยมที่สุด เรียนรู้การใช้งาน การอัพเกรด และเทคนิคการบินสำหรับผู้เล่นทุกระดับ"
---
```

### Generated Content Structure:
```markdown
> **🚧 Work in Progress** - คู่มือนี้อยู่ระหว่างการพัฒนา เนื้อหาอาจยังไม่สมบูรณ์

<!-- Photo: Hero shot ของ Cutlass Black บินในอวกาศ เห็นรูปทรงและขนาดของยาน -->

## สารบัญ {#table-of-contents}

- [ภาพรวมของ Cutlass Black](#overview)
- [ข้อมูลเทคนิค](#specifications)
- [การใช้งานและบทบาท](#roles-and-usage)
- [การอัพเกรดและปรับแต่ง](#upgrades)
- [เทคนิคการบิน](#flying-techniques)
- [ข้อดีและข้อเสีย](#pros-and-cons)
- [สรุปและคำแนะนำ](#conclusion)

## 🚀 ภาพรวมของ Cutlass Black {#overview}

Drake Cutlass Black เป็นยานอเนกประสงค์ที่ได้รับความนิยมมากที่สุดใน Star Citizen...

<!-- Content continues with proper Thai language, emoji, and anchor links -->
```

## Example 2: Concept Guide (Insurance System)

### Generated Front Matter:
```yaml
---
title: "🛡️ ระบบประกันใน Star Citizen - คู่มือสมบูรณ์"
subtitle: "เข้าใจระบบประกันยานอวกาศและการปกป้องทรัพย์สินของคุณ"
date: "2025-08-01"
lastmod: "2025-08-01"
draft: false
game_version: "Alpha 4.2.1"
tags: ["Insurance", "ประกัน", "Game Mechanics", "ระบบเกม", "LTI"]
categories: ["แนวคิดและระบบเกม"]
author: "Star Citizen Handbook Team"
weight: 3
image: "img/concepts/insurance/insurance_system_hero.jpg"
description: "เรียนรู้ระบบประกันในเกม Star Citizen ตั้งแต่ประกันพื้นฐานไปจนถึง LTI (Lifetime Insurance) พร้อมเทคนิคการจัดการความเสี่ยง"
---
```

## Example 3: Tutorial Guide (Mining)

### Generated Front Matter:
```yaml
---
title: "⛏️ การขุดแร่ Quantanium - คู่มือเริ่มต้นสู่ความร่ำรวย"
subtitle: "เรียนรู้เทคนิคการขุดแร่ที่มีกำไรสูงที่สุดในจักรวาล"
date: "2025-08-01"
lastmod: "2025-08-01"
draft: false
game_version: "Alpha 4.2.1"
tags: ["Mining", "การขุดแร่", "Quantanium", "Tutorial", "เริ่มต้น", "หาเงิน"]
categories: ["คู่มือการเล่น"]
author: "Star Citizen Handbook Team"
weight: 6
image: "img/guides/mining/quantanium_mining_hero.jpg"
description: "คู่มือการขุดแร่ Quantanium ตั้งแต่เริ่มต้นจนเก่งกาจ เรียนรู้เทคนิค อุปกรณ์ และสถานที่ขุดที่ดีที่สุด พร้อมเคล็ดลับหาเงินจากการขุดแร่"
---
```

## Key Features of Generated Content

### 1. Thai Language Requirements
- All headers, descriptions, and content in Thai
- Technical terms remain in English where appropriate
- Gaming terminology uses both Thai and English
- Clear, helpful tone for Thai gamers

### 2. Hugo Integration
- Proper YAML front matter format
- Category-specific content organization
- SEO-optimized metadata
- Image placeholders with descriptive comments

### 3. Navigation Structure
- Manual anchor IDs in English: `{#english-id}`
- Table of contents with proper links
- Hierarchical heading structure (H2, H3)
- Internal linking to related content

### 4. Content Quality
- Emoji integration for visual appeal
- Work-in-progress notices where appropriate
- Practical examples and tips
- Code blocks for key bindings
- Blockquotes for important information
- Tables for comparative data

### 5. File Organization
- URL-friendly slugs as filenames
- Automatic placement in correct categories
- Updates to category index files
- Consistent file naming conventions

## Category Mapping

The generator automatically determines the correct category:

- **ships** → ยานอวกาศ (Spacecraft guides and reviews)
- **concepts** → แนวคิดและระบบเกม (Game mechanics and systems)
- **guides** → คู่มือการเล่น (Tutorials and how-to content)

## Quality Assurance

Each generated post includes:
- ✅ Proper Thai language and grammar
- ✅ Star Citizen game accuracy
- ✅ Hugo/Markdown formatting compliance
- ✅ SEO optimization
- ✅ Navigation functionality
- ✅ Mobile-friendly structure
- ✅ Theme compatibility (beautifulhugo)
