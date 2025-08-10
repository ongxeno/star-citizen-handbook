# คู่มือการสร้างหน้าใหม่ (Manual Page Creation Guide)

คู่มือนี้สรุปขั้นตอนการสร้างหน้าใหม่ใน Star Citizen Handbook ทั้งแบบหน้าเดี่ยวและหน้า Collection (รวมบทความ)

---

## 1. โครงสร้างโฟลเดอร์และไฟล์
ทุกหน้าใหม่ควรอยู่ในโฟลเดอร์ของตัวเอง เช่น หน้า content ที่เป็น `category` ชื่อบทความ `my-new-guide` ควรอยู่ในโฟลเดอร์ `content/guides/my-new-guide/` โดยเก็บไฟล์เนื้อหาและรูปภาพไว้ในโฟลเดอร์เดียวกัน

**ตัวอย่าง:**
```
content/
  guides/
    annual-events/
      index.md           # ตัวบทความ
      cover.jpg          # รูปปก
      some-image1.png    # รูปอื่น ๆ
      some-image2.png    # รูปอื่น ๆ
      event-preview-image/  # โฟลเดอร์เก็บรูปสำหรับ carousel
        Screenshot2025-07-30095735.jpg
        Screenshot2025-07-30095759.png
        # ... รูปอื่น ๆ
```

---

## การเขียนเนื้อหา แทรกรูป และใช้งาน shortcode

### 1. สร้างโฟลเดอร์และไฟล์
- ตั้งชื่อโฟลเดอร์/ไฟล์เป็นภาษาอังกฤษ ใช้ขีดกลาง เช่น `my-new-guide.md`
- หลีกเลี่ยงชื่อซ้ำกับไฟล์อื่น

### 2. ใส่ front matter
ทุกไฟล์ Markdown ต้องมี front matter (YAML) คร่อมด้วย `---` เช่น:
ตัวอย่าง front matter:
```
---
title: "ชื่อบทความภาษาไทย"
subtitle: "คำอธิบายสั้น ๆ (ถ้ามี)"
date: 2025-08-10
lastmod: 2025-08-10
draft: false
tags: ["tag1", "tag2"]
categories: ["guides"]
author: "ชื่อผู้เขียน"
image: "cover.jpg" # (ถ้ามี)
description: "สรุปเนื้อหาแบบสั้น ๆ"
---
```

### 3. เขียนเนื้อหา
- ใช้ Markdown ในการเขียนเนื้อหา
- ใช้หัวข้อ `##` และ `###` สำหรับแต่ละส่วน
- ใส่ลิงก์ภายในด้วย `[ชื่อเรื่อง](/path/to/page/)`
- ทำ **ตัวหน้า** ด้วย `**ตัวอย่าง**`
- ทำ *ตัวเอียง* ด้วย `*ตัวอย่าง*`
- รองรับการใช้ HTML code เช่น `<br>` เพื่อบังคับการขึ้นบรรทัดใหม่
- ใส่ blockquote ได้โดยการ `> ตัวอย่าง`
- อ่านวิธีเขียน markdown เพิ่มเติมได้ที่ [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

### 4. จัดการรูปภาพ
- วางภาพประกอบไว้ในโฟลเดอร์เดียวกับไฟล์ .md
- สำหรับรูปจำนวนมาก ให้สร้างโฟลเดอร์ย่อย เช่น `event-preview-image/`
- แทรกรูปใน Markdown เช่น:
  ```markdown
  ![cover](cover.jpg)
  ![แผนที่](some-image.png)
  ```
- สำหรับรูปใน subfolder ให้ระบุ path:
  ```markdown
  ![ภาพตัวอย่าง](event-preview-image/Screenshot2025-07-30095735.jpg)
  ```

---

### 5. การใช้งาน Shortcode

#### 5.1 การใช้ carousel shortcode
สามารถแทรก carousel สำหรับแสดงภาพหมุนจากโฟลเดอร์ย่อยได้ดังนี้:

**แสดงภาพจากโฟลเดอร์ย่อย:**
สร้างโฟลเดอร์เก็บรูปภาพภายในโฟลเดอร์เนื้อหา และใช้ `path` parameter

ตัวอย่างนี้ใช้ในไฟล์ `content/guides/annual-events/index.md` ที่แสดงภาพทั้งหมดจากโฟลเดอร์ `event-preview-image/`

```markdown
{{< carousel path="event-preview-image/" height="400px" interval="5000" >}}
```
**โครงสร้างโฟลเดอร์:**
```
content/
  guides/
    annual-events/
      index.md               # ไฟล์เนื้อหา
      event-preview-image/   # โฟลเดอร์เก็บรูปภาพสำหรับ carousel
        Screenshot2025-07-30095735.jpg
        Screenshot2025-07-30095759.png
        Screenshot2025-07-30095845.png
        ...
```

#### 5.2 การใช้ youtube shortcode
สามารถฝังวิดีโอ YouTube พร้อมระบุเวลาเริ่ม/จบ และใส่ชื่อคลิปได้ด้วย shortcode `youtube` เช่น:

```markdown
{{< youtube id="wYvPpQ25XGc" starttime="21:20" endtime="22:39" title="CitizenCon 2954: Brave New Worlds - Swamp Biome Demo" >}}
```

**อธิบาย parameter:**
- `id` (จำเป็น): รหัสวิดีโอ YouTube เช่น `wYvPpQ25XGc`
- `starttime` (ไม่บังคับ): เวลาเริ่ม
- `endtime` (ไม่บังคับ): เวลาสิ้นสุด
- `title` (ไม่บังคับ): ชื่อวิดีโอที่จะแสดงใต้คลิป

**หมายเหตุ:**
- รูปแบบเวลาที่รองรับสำหรับ `starttime` และ `endtime`:
  - `วินาที` (ตัวเลขล้วน เช่น `1280`)
  - `ชั่วโมง.นาที.วินาที` หรือ `นาที.วินาที` เช่น `1.23.45`, `21.20`
  - `ชั่วโมง:นาที:วินาที` หรือ `นาที:วินาที` เช่น `1:23:45`, `21:20`
- หากไม่ระบุ `starttime` จะเริ่มเล่นตั้งแต่ต้นคลิป
- หากไม่ระบุ `endtime` จะเล่นไปเรื่อยๆ จนจบคลิป
- สามารถดูตัวอย่างการใช้งานได้ในไฟล์ `content/concepts/citizencon-2954-brave-new-worlds.md`
- โค้ดของ shortcode อยู่ที่ `layouts/shortcodes/youtube.html`

---

## ข้อควรระวัง
- หลีกเลี่ยง slug หรือชื่อไฟล์ซ้ำ
- ตรวจสอบวันที่และ metadata ให้ถูกต้อง
- ใช้ภาษาไทยเป็นหลัก (หรืออังกฤษถ้าจำเป็น)
- ตรวจสอบตัวอย่าง (preview) ก่อน publish

## การเชื่อมโยงกับเมนู/ลิงก์ภายใน
- เพิ่มลิงก์ไปยังหน้าใหม่ในบทความอื่นหรือเมนู (ถ้าต้องการ)
- ใช้ลิงก์สัมพัทธ์ เช่น `[กลับสู่หน้าหลัก](/)`

---

*ดูตัวอย่างไฟล์ใน `content/` หรือสอบถามใน GitHub/Discord หากมีข้อสงสัยเพิ่มเติม*
