# **How to Create a Hugo Image Carousel Shortcode**

Hugo doesn't have a built-in image carousel shortcode, but you can easily create one. The most common approach is to use a front-end framework like Bootstrap and create a custom shortcode that generates the necessary HTML.

This guide will walk you through creating a responsive image carousel using Bootstrap 5 that automatically finds images in your content's folder (a Page Bundle).

### **Step 1: Add Bootstrap to Your Site**

First, you need to ensure your Hugo site includes the Bootstrap CSS and JavaScript files. If you haven't already, add the CDN links to your site's template files.

1. **Add the CSS link** in your site's \<head\> section. This is typically located in layouts/\_default/baseof.html or layouts/partials/head.html.  
   \<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous"\>

2. **Add the JS link** just before the closing \</body\> tag. This is often in layouts/\_default/baseof.html or layouts/partials/footer.html.  
   \<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"\>\</script\>

### **Step 2: Create the Shortcode File**

Next, create the shortcode file that will generate the carousel. This code is designed to find all images within the same folder as your content file.

1. Create a new file at this location: layouts/shortcodes/carousel.html.  
2. Paste the following code into the file. This code finds all image resources in the current Page Bundle and generates the Bootstrap 5 carousel markup.  
   {{/\*  
   layouts/shortcodes/carousel.html  
   Finds all images in the current page bundle and displays them in a Bootstrap 5 carousel.  
   \*/}}

   {{ $page := .Page }}  
   {{/\* Find all image resources within the current page's bundle \*/}}  
   {{ $images := $page.Resources.ByType "image" }}

   {{ if $images }}  
   {{/\* Create a unique ID for the carousel to avoid conflicts \*/}}  
   {{ $carouselID := printf "carousel-%d" .Ordinal }}  
   \<div id="{{ $carouselID }}" class="carousel slide" data-bs-ride="carousel"\>

     {{/\* Carousel Indicators (the little dots at the bottom) \*/}}  
     \<div class="carousel-indicators"\>  
       {{ range $index, $image := $images }}  
       \<button type="button" data-bs-target="\#{{ $carouselID }}" data-bs-slide-to="{{ $index }}" {{ if eq $index 0 }}class="active" aria-current="true"{{ end }} aria-label="Slide {{ add $index 1 }}"\>\</button\>  
       {{ end }}  
     \</div\>

     {{/\* Carousel Inner Content (the images and captions) \*/}}  
     \<div class="carousel-inner"\>  
       {{ range $index, $image := $images }}  
       \<div class="carousel-item {{ if eq $index 0 }}active{{ end }}"\>  
         \<img src="{{ $image.RelPermalink }}" class="d-block w-100" alt="{{ $image.Title | default "Carousel image" }}"\>  
         {{/\* Add a caption if specified in image front matter \*/}}  
         {{ with $image.Params.caption }}  
         \<div class="carousel-caption d-none d-md-block"\>  
           \<p\>{{ . | markdownify }}\</p\>  
         \</div\>  
         {{ end }}  
       \</div\>  
       {{ end }}  
     \</div\>

     {{/\* Carousel Controls (the previous/next arrows) \*/}}  
     \<button class="carousel-control-prev" type="button" data-bs-target="\#{{ $carouselID }}" data-bs-slide="prev"\>  
       \<span class="carousel-control-prev-icon" aria-hidden="true"\>\</span\>  
       \<span class="visually-hidden"\>Previous\</span\>  
     \</button\>  
     \<button class="carousel-control-next" type="button" data-bs-target="\#{{ $carouselID }}" data-bs-slide="next"\>  
       \<span class="carousel-control-next-icon" aria-hidden="true"\>\</span\>  
       \<span class="visually-hidden"\>Next\</span\>  
     \</button\>  
   \</div\>  
   {{ else }}  
   \<p class="text-center fst-italic"\>No images found for carousel.\</p\>  
   {{ end }}

### **Step 3: Use the Shortcode in Your Content**

To use the carousel, you must structure your content as a **Page Bundle**. This simply means putting your Markdown file and its associated images together in the same folder.

1. Create a folder for your content post, for example: content/posts/my-cool-trip/.  
2. Inside that folder, place your content file and name it index.md (or \_index.md for a section).  
3. Place all the images you want in the carousel inside that same folder (content/posts/my-cool-trip/).  
   Your folder structure should look like this:  
   .  
   └── content/  
       └── posts/  
           └── my-cool-trip/  
               ├── image1.jpg  
               ├── image2.png  
               ├── image3.gif  
               └── index.md

4. Finally, call the shortcode in your index.md file wherever you want the carousel to appear.  
   \---  
   title: "My Cool Trip"  
   date: 2025-07-30  
   \---

   Here are some pictures from my trip\! They show the beautiful landscapes we encountered.

   {{\< carousel \>}}

   The trip was amazing. We saw mountains, rivers, and ancient ruins. I would definitely recommend it to anyone looking for an adventure.

When you build your site, Hugo will find the carousel shortcode, locate all the images in the my-cool-trip folder, and generate a fully functional and responsive Bootstrap carousel right in your post.