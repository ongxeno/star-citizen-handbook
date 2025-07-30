---
title: "คู่มือ: ปฏิทินอีเวนต์ประจำปีใน Star Citizen"
subtitle: "รู้จักอีเวนต์สำคัญตลอดทั้งปี เผื่อวางแผนการเล่นและการช็อปปิ้งอย่างมืออาชีพ"
date: 2025-07-30
lastmod: 2025-07-30
tags: ["Event", "Guide", "IAE", "Invictus", "CitizenCon", "Sales", "Red Festival", "Pirate Week"]
categories: ["Guides", "คู่มือการเล่น"]
image: "img/guides/events/event-calendar.jpg"
---

**สารบัญ**
- [บทนำ: ทำไมต้องรู้จักอีเวนต์ประจำปี?](#introduction)
- [ปฏิทินอีเวนต์หลัก (เรียงตามช่วงเวลา)](#event-calendar)
  - [Red Festival (มกราคม/กุมภาพันธ์)](#red-festival)
  - [Coramor (กุมภาพันธ์)](#coramor)
  - [Stella Fortuna (มีนาคม)](#stella-fortuna)
  - [Invictus Launch Week (พฤษภาคม)](#invictus)
  - [Alien Week (มิถุนายน)](#alien-week)
  - [Foundation Festival (กรกฎาคม)](#foundation-festival)
  - [Ship Showdown (สิงหาคม - กันยายน)](#ship-showdown)
  - [Pirate Week (กันยายน)](#pirate-week)
  - [Day of the Vara (ตุลาคม)](#day-of-the-vara)
  - [CitizenCon (ตุลาคม/พฤศจิกายน)](#citizencon)
  - [Intergalactic Aerospace Expo (IAE) (พฤศจิกายน)](#iae)
  - [Luminalia (ธันวาคม)](#luminalia)
  - [โปรโมชั่นอื่นๆ ที่น่าสนใจ](#other-promotions)
- [สรุป: อีเวนต์ไหนสำคัญที่สุดสำหรับนักล่าดีล?](#summary)

---

<div id="eventCarousel" class="carousel slide" style="margin-bottom: 30px;">
  <ol class="carousel-indicators">
    <li data-target="#eventCarousel" data-slide-to="0" class="active" onclick="currentSlide(1)"></li>
    <li data-target="#eventCarousel" data-slide-to="1" onclick="currentSlide(2)"></li>
    <li data-target="#eventCarousel" data-slide-to="2" onclick="currentSlide(3)"></li>
    <li data-target="#eventCarousel" data-slide-to="3" onclick="currentSlide(4)"></li>
    <li data-target="#eventCarousel" data-slide-to="4" onclick="currentSlide(5)"></li>
    <li data-target="#eventCarousel" data-slide-to="5" onclick="currentSlide(6)"></li>
  </ol>
  <div class="carousel-inner" role="listbox">
    <div class="item active">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 095735.png" alt="Star Citizen Event 1" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
    <div class="item">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 095759.png" alt="Star Citizen Event 2" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
    <div class="item">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 095845.png" alt="Star Citizen Event 3" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
    <div class="item">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 100055.png" alt="Star Citizen Event 4" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
    <div class="item">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 100146.png" alt="Star Citizen Event 5" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
    <div class="item">
      <img src="/star-citizen-handbook/img/guides/events/carousel/Screenshot 2025-07-30 100209.png" alt="Star Citizen Event 6" style="width: 100%; height: 400px; object-fit: cover;">
    </div>
  </div>
  <a class="left carousel-control" href="javascript:void(0)" role="button" onclick="plusSlides(-1)">
    <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="right carousel-control" href="javascript:void(0)" role="button" onclick="plusSlides(1)">
    <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>

<script>
let slideIndex = 1;
let slideInterval;

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let slides = document.querySelectorAll('#eventCarousel .item');
  let dots = document.querySelectorAll('#eventCarousel .carousel-indicators li');
  
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  
  for (let i = 0; i < slides.length; i++) {
    slides[i].classList.remove('active');
  }
  
  for (let i = 0; i < dots.length; i++) {
    dots[i].classList.remove('active');
  }
  
  if (slides[slideIndex-1]) {
    slides[slideIndex-1].classList.add('active');
  }
  if (dots[slideIndex-1]) {
    dots[slideIndex-1].classList.add('active');
  }
}

function autoSlides() {
  slideIndex++;
  showSlides(slideIndex);
}

// Initialize carousel
document.addEventListener('DOMContentLoaded', function() {
  showSlides(slideIndex);
  // Auto-advance every 5 seconds
  slideInterval = setInterval(autoSlides, 5000);
  
  // Pause on hover
  const carousel = document.getElementById('eventCarousel');
  if (carousel) {
    carousel.addEventListener('mouseenter', function() {
      clearInterval(slideInterval);
    });
    
    carousel.addEventListener('mouseleave', function() {
      slideInterval = setInterval(autoSlides, 5000);
    });
  }
});
</script>

## **บทนำ: ทำไมต้องรู้จักอีเวนต์ประจำปี?** {#introduction}

Star Citizen ไม่ได้มีแค่การอัปเดตแพตช์เกมเท่านั้น แต่ในแต่ละปีจะมีอีเวนต์พิเศษมากมายที่จัดขึ้นในจักรวาล ซึ่งอีเวนต์เหล่านี้ไม่ได้มีแค่กิจกรรมให้ทำในเกม แต่ยังเป็นช่วงเวลาสำคัญที่ CIG จะเปิดขายยานพิเศษ, นำเสนอโปรโมชั่น Warbond CCU, และแจกไอเทมต่างๆ อีกด้วย

การรู้จักปฏิทินอีเวนต์จะช่วยให้คุณ:
- **วางแผนการซื้อ:** รู้ว่าควรเก็บเงินไว้รอซื้อยานหรือ CCU ในช่วงไหน
- **ไม่พลาดของดี:** เตรียมพร้อมสำหรับ Warbond CCU ที่มีส่วนลดสูงซึ่งมักจะมาในช่วงอีเวนต์ใหญ่
- **สัมผัสประสบการณ์ใหม่ๆ:** เข้าร่วมกิจกรรมในเกมและทดลองขับยานที่ปกติไม่มีให้ขับฟรี

---

## **ปฏิทินอีเวนต์หลัก (เรียงตามช่วงเวลา)** {#event-calendar}

### **Red Festival (มกราคม/กุมภาพันธ์)** {#red-festival}
อีเวนต์เฉลิมฉลองปีใหม่ทางจันทรคติ (ตรุษจีน) มักจะมาพร้อมกับซองแดงและไอเทมสีแดง-ทองเพื่อความเป็นสิริมงคล โดยทั่วไปจะมีการเปิดขายยานและไอเทมในธีมสีแดง-ทอง และอาจมีโปรโมชั่นเล็กๆ น้อยๆ
- **เว็บไซต์อ้างอิง:**
  - [Lunar New Year 2025](https://robertsspaceindustries.com/comm-link/transmission/20373-Lunar-New-Year-2025)

### **Coramor (กุมภาพันธ์)** {#coramor}
เฉลิมฉลองความรักและความสัมพันธ์ในจักรวาล (วันแห่งความรัก) มักจะเน้นไปที่ยานสำหรับสองคนและกิจกรรมคู่รัก โดยจะมีการเปิดขายยาน 2 ที่นั่งในธีมสีชมพูหรือสีพิเศษ
- **เว็บไซต์อ้างอิง:** 
  - [Coramor 2024](https://robertsspaceindustries.com/comm-link/transmission/19743-Valentines-Day-2024)
  - [Galactapedia](https://robertsspaceindustries.com/galactapedia/article/RWozkYYxla-coramor)

### **Stella Fortuna (มีนาคม)** {#stella-fortuna}
เทศกาลแห่งโชคลาภ (คล้ายวัน St. Patrick) ที่มาในธีมสีเขียว-ทอง เฉลิมฉลองให้กับความกล้าเสี่ยงโชคและการผจญภัย ในช่วงนี้จะมีการเปิดขายยานในธีมสีเขียวและสีทอง โดยเฉพาะยานจากค่าย Origin และ CNOU
- **เว็บไซต์อ้างอิง:**
  - [St. Patrick's Day 2025](https://robertsspaceindustries.com/en/comm-link/transmission/20427-St-Patricks-Day-2025)
  - [Galactapedia](https://robertsspaceindustries.com/galactapedia/article/0qn8vv3Aw1-stella-fortuna)

### **Invictus Launch Week (พฤษภาคม)** {#invictus}
งานแสดงเทคโนโลยีและยานรบของกองทัพ UEE Navy ซึ่งเป็นโอกาสดีที่จะได้ทดลองขับยานทหารและชมการสวนสนามของยานเรือธงอย่าง Javelin และ Idris ถือเป็น **อีเวนต์ใหญ่ที่สุดช่วงครึ่งปีแรก** ที่ผู้เล่นจะได้สัมผัสประสบการณ์ Free Fly, ทดลองขับยานทหารฟรี, รับดีล Warbond CCU ประจำวัน, และซื้อยานทหารที่ปกติไม่มีขาย
- **เว็บไซต์อ้างอิง:**
  - [Invictus Launch Week 2955](https://robertsspaceindustries.com/comm-link/transmission/20489-Invictus-Launch-Week-2955-Countdown)

### **Alien Week (มิถุนายน)** {#alien-week}
สัปดาห์แห่งยานจากเผ่าพันธุ์ต่างดาว เป็นอีเวนต์ที่เปิดโอกาสให้สัมผัสเทคโนโลยีและยานอวกาศจากเผ่าพันธุ์อื่นๆ เช่น Banu, Xi'an, และ Tevarin โดยจะมีการเปิดขายยานจากผู้ผลิตต่างดาวทั้งหมด (Aopoa, Banu, Esperia, Gatac)
- **เว็บไซต์อ้างอิง:**
  - [Alien Week 2954](https://robertsspaceindustries.com/en/comm-link/transmission/19937-Alien-Week-2024)

### **Foundation Festival (กรกฎาคม)** {#foundation-festival}
อีเวนต์เฉลิมฉลองคอมมูนิตี้และผู้เล่นใหม่ ที่เน้นการช่วยเหลือและต้อนรับผู้เล่นใหม่เข้าสู่จักรวาล มีกิจกรรมส่งเสริมการทำงานร่วมกันและแจกรางวัล ผู้เล่นสามารถคาดหวัง Free Fly, ส่วนลด Starter Pack, และกิจกรรมในเกมสำหรับผู้เล่นใหม่ได้
- **เว็บไซต์อ้างอิง:**
  - [Foundation Festival 2954](https://robertsspaceindustries.com/en/comm-link/transmission/20015-Foundation-Festival-2024)
  - [Foundation Festival 2955](https://robertsspaceindustries.com/en/comm-link/transmission/20622-Foundation-Festival-2025)

### **Ship Showdown (สิงหาคม - กันยายน)** {#ship-showdown}
การแข่งขันโหวตยานยอดนิยมประจำปี ที่ให้ผู้เล่นโหวตยานที่ชื่นชอบที่สุดในแต่ละรอบจนเหลือผู้ชนะเพียงหนึ่งเดียว เป็นอีเวนต์ที่ขับเคลื่อนโดยคอมมูนิตี้อย่างแท้จริง จะมี Free Fly สำหรับยานที่เข้ารอบ, โปรโมชั่น Warbond CCU สำหรับยาน 4 ลำสุดท้าย, และสกินพิเศษสำหรับยานที่ชนะ
- **เว็บไซต์อ้างอิง:**
  - [Ship Showdown 2955](https://robertsspaceindustries.com/en/ship-showdown2025/community-call)

### **Pirate Week (กันยายน)** {#pirate-week}
สัปดาห์แห่งโจรสลัด เป็นอีเวนต์สำหรับผู้ที่ชื่นชอบชีวิตนอกกฎหมาย เฉลิมฉลองวัฒนธรรมโจรสลัดและเปิดขายยานที่เกี่ยวข้อง โดยจะเน้นการขายยานจากค่าย Drake และยานที่เกี่ยวกับวิถีชีวิตนอกกฎหมาย
- **เว็บไซต์อ้างอิง:**
  - [Pirate Week 2024](https://robertsspaceindustries.com/en/comm-link/transmission/20075-Pirate-Week-2024)

### **Day of the Vara (ตุลาคม)** {#day-of-the-vara}
เทศกาลแห่งความตายและความทรงจำที่มาในบรรยากาศสยองขวัญ (วันฮาโลวีน) ผู้เล่นมักจะสวมหน้ากากและตามหาไอเทมพิเศษ รวมถึงมีไอเทมและสกินในธีมสยองขวัญวางขาย
- **เว็บไซต์อ้างอิง:**
  - [Day of the Vara 2022](https://robertsspaceindustries.com/comm-link/transmission/18870-Halloween-2022)
  - [Galactapedia](https://robertsspaceindustries.com/galactapedia/article/RkGQqpJwGp-day-of-the-vara)

### **CitizenCon (ตุลาคม/พฤศจิกายน)** {#citizencon}
งานประชุมใหญ่ประจำปีของ CIG ที่จะเปิดเผยข้อมูลล่าสุดเกี่ยวกับการพัฒนาเกม, เทคโนโลยีใหม่ๆ และแผนในอนาคต เป็นวันที่ผู้เล่นจะได้เห็นภาพใหญ่ของโปรเจกต์ โดยจะมีการ **ประกาศข่าวใหญ่และเทคโนโลยีใหม่**, ประกาศยานคอนเซ็ปต์ใหม่, และมีโปรโมชั่นพิเศษ
- **เว็บไซต์อ้างอิง:**
  - [CitizenCon 2954](https://robertsspaceindustries.com/en/citizencon)

### **Intergalactic Aerospace Expo (IAE) (พฤศจิกายน)** {#iae}
งานแสดงยานที่ใหญ่ที่สุดแห่งปี (Expo) ที่เปิดโอกาสให้ผู้เล่นได้เช่าและทดลองขับยานเกือบทุกรุ่นที่มีในเกม โดยจะจัดแสดงยานตามผู้ผลิตในแต่ละวัน ถือเป็น **อีเวนต์ใหญ่และสำคัญที่สุดของปีสำหรับนักช็อป** ที่จะมี Free Fly, ทดลองขับยานฟรี, Warbond CCU ที่ดีที่สุดและเยอะที่สุด, และเปิดขายยานเกือบทุกรุ่น
- **เว็บไซต์อ้างอิง:**
  - [IAE 2954](https://robertsspaceindustries.com/en/iae2954#/schedule/welcome)

### **Luminalia (ธันวาคม)** {#luminalia}
เทศกาลแห่งแสงไฟและของขวัญ (คล้ายวันคริสต์มาส) ซึ่งเป็นเทศกาลส่งท้ายปีที่เน้นการให้และการเฉลิมฉลอง ผู้เล่นจะได้รับของขวัญฟรีทุกวันตลอดช่วงอีเวนต์ และอาจมีโปรโมชั่นเล็กๆ หรือยาน Starter Pack ราคาพิเศษ
- **เว็บไซต์อ้างอิง:**
  - [Luminalia 2954](https://robertsspaceindustries.com/comm-link/transmission/20280-Luminalia-2954)
  - [Luminalia 2953](https://robertsspaceindustries.com/comm-link/transmission/19605-Luminalia-2953)

### **โปรโมชั่นอื่นๆ ที่น่าสนใจ** {#other-promotions}
- **ICYMI (In Case You Missed It):** ไม่ใช่อีเวนต์ประจำ แต่เป็น "รอบเก็บตก" ที่มักจะเกิดขึ้นหลังอีเวนต์ใหญ่อย่าง IAE หรือ Invictus จบลง โดยจะนำดีล Warbond ที่ดีที่สุดบางส่วนกลับมาขายอีกครั้งในเวลาจำกัด เป็นโอกาสสุดท้ายสำหรับคนที่พลาดไป

---

## **สรุป: อีเวนต์ไหนสำคัญที่สุดสำหรับนักล่าดีล?** {#summary}

สำหรับผู้ที่ต้องการสร้าง CCU Chain ให้คุ้มค่าที่สุด สองอีเวนต์ที่คุณ **ห้ามพลาดเด็ดขาด** คือ:
1.  **IAE (พฤศจิกายน):** เป็นแหล่งรวม Warbond CCU ที่ดีที่สุดและมีตัวเลือกเยอะที่สุด
2.  **Invictus Launch Week (พฤษภาคม):** เป็นอีเวนต์ใหญ่รองลงมา มี Warbond CCU ที่น่าสนใจมากมาย โดยเฉพาะสายยานรบ

การวางแผนและเก็บสะสม CCU จากสองอีเวนต์นี้ คือกุญแจสำคัญสู่การสร้างยานในฝันด้วยราคาที่ประหยัดที่สุดครับ
