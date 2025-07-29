# **Star Citizen Ship Guide Formatting Template**

**Objective:** Using the raw data provided below, generate a complete, polished ship guide for the Star Citizen vessel **\[SHIP NAME\]**. The guide must be formatted in a single Markdown file, following the exact structure provided.

**Tone & Language:**

* The guide must be written primarily in **Thai**.  
* It is acceptable and encouraged to use English for direct, common, or technical game-related vocabulary (e.g., 'SCU', 'Quantum Drive', 'decoupled', 'Vehicle Loadout Manager').  
* The tone must be informative, practical, and authoritative, as if an expert player is guiding a new player. Write engaging prose that connects the data points into a readable guide.

**Context:** The guide is for **Star Citizen Alpha 4.2.1**.

**BEGIN PROMPT**

**\[PASTE THE GATHERED DATA FROM THE RESEARCH PROMPT HERE\]**

**TASK:** Using the data provided above, generate a complete Markdown file for the **\[SHIP NAME\]** ship guide. Follow this exact structure:

### **Part 1: Markdown Front Matter (YAML)**

Create a YAML front matter block using the gathered data.

\---  
title: "\[MANUFACTURER\] \[SHIP NAME\] \- \[PRIMARY ROLE DESCRIPTION\]"  
subtitle: "\[THAI TRANSLATION OF THE GUIDE'S PURPOSE, e.g., คู่มือสำหรับยาน...\]"  
date: 2025-07-29  
lastmod: 2025-07-29  
draft: false  
game\_version: "Alpha 4.2.1"  
tags: \["\[MANUFACTURER\]", "\[SHIP NAME\]", "\[KEYWORD 1\]", "\[KEYWORD 2\]", "\[THAI KEYWORD\]"\]  
categories: \["ยานอวกาศ"\]  
author: "Star Citizen Handbook Team"  
weight: \[A NUMBER, e.g., 4\]  
image: "img/ships/\[lowercase\_ship\_name\]/\[ship\_name\]\_hero.jpg"  
description: "\[A SHORT THAI DESCRIPTION OF THE SHIP AND ITS ROLE\]"  
\---

### **Part 2: Introductory Content**

1. Include this exact "Work in Progress" blockquote: \> \*\*🚧 Work in Progress\*\* \- คู่มือนี้อยู่ระหว่างการพัฒนา เนื้อหาอาจยังไม่สมบูรณ์  
2. Include a commented-out photo placeholder: \<\!-- Photo: Hero shot of the \[SHIP NAME\] \[describe an ideal scene for the hero shot, e.g., landing on a moon, in combat, etc.\] \--\>

### **Part 3: Main Guide Content (Structured Sections)**

Generate the rest of the guide, using the provided data to write descriptive paragraphs for each section.

**1\. Table of Contents (สารบัญ)**

\#\# สารบัญ

1\. \[ภาพรวมและบทบาท\](\#overview)  
2\. \[การออกแบบภายนอกและระบบขนส่ง\](\#exterior-and-cargo)  
3\. \[การจัดวางภายใน\](\#interior-layout)  
4\. \[ลักษณะการบิน\](\#flight-characteristics)  
5\. \[การจัดการส่วนประกอบ\](\#components)  
6\. \[ระบบป้องกันตัว\](\#defenses)  
7\. \[การเปรียบเทียบกับยานอื่น\](\#comparisons)  
8\. \[กลยุทธ์การเผชิญหน้า\](\#tactics)  
9\. \[ยานลำนี้เหมาะกับใคร?\](\#who-is-this-for)

**2\. Overview and Role (\#\# ภาพรวมและบทบาท {\#overview})**

* Write an introductory paragraph based on the "General Description."  
* Create a \#\#\# จุดเด่นหลัก (Key Features) section using the "Key Strengths / Pros" data.  
* Create a \#\#\# ข้อควรระวังที่สำคัญ (Important Cautions) or \#\#\# ปรัชญาการออกแบบ (Design Philosophy) section using the "Key Weaknesses / Cons" and "Design Philosophy" data.

**3\. Exterior Design and Cargo System (\#\# การออกแบบภายนอกและระบบขนส่ง {\#exterior-and-cargo})**

* Create a \#\#\# จุดเข้า-ออกยาน (Entry/Exit Points) section from the data.  
* Create a \#\#\# ระบบขนส่งสินค้า (Cargo System) section. State the **SCU** and describe the loading mechanism.

**4\. Interior Layout (\#\# การจัดวางภายใน {\#interior-layout})**

* Describe the interior, detailing the cockpit, living amenities, and component access based on the provided data.

**5\. Flight Characteristics (\#\# ลักษณะการบิน {\#flight-characteristics})**

* Write a descriptive paragraph using the "Flight Analogy" and performance data for space and atmosphere.

**6\. Component Management (\#\# การจัดการส่วนประกอบ {\#components})**

* List the default components (Power Plants, Coolers, Shield Generators, Quantum Drive) using the data.

**7\. Defenses (\#\# ระบบป้องกันตัว {\#defenses})**

* List the defensive capabilities (Weapons, Turrets, Missiles) from the data.

**8\. Comparisons (\#\# การเปรียบเทียบกับยานอื่น {\#comparisons})**

* For each competitor listed in the data, create a \#\#\# vs. \[Competitor Ship Name\] section and write a comparison based on the provided points.

**9\. Encounter Strategy (\#\# กลยุทธ์การเผชิญหน้า {\#tactics})**

* Using the "Encounter Strategy / Tactics" data, write a section advising players on how to handle different threats.

**10\. Who is this ship for? (\#\# ยานลำนี้เหมาะกับใคร? {\#who-is-this-for})**

* Create a \#\#\# เหมาะสำหรับ: (Suitable for:) list using the "Ideal Player Type" data.  
* Create a \#\#\# ไม่เหมาะสำหรับ: (Not suitable for:) list using the "Player Type to Avoid" data.  
* Write a concluding paragraph summarizing the ship's value.

### **Part 4: Footer**

End the document with this exact footer:

\---

\*คู่มือนี้อัปเดตสำหรับ Star Citizen Alpha 4.2.1\*  
