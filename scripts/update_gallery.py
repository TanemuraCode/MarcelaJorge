import os

html_file = "main.html"
image_dir = "images"

# Build gallery HTML
# files = sorted(f for f in os.listdir(image_dir) if os.path.splitext(f)[-1].lower() == 'enc')
files = sorted(f for f in os.listdir(image_dir) if f.split('.')[-1] == 'enc')
gallery_html = '<div class="gallery">\n'
for f in files:
    gallery_html += f'    <img data-enc="{image_dir}/{f}" alt="">\n'
gallery_html += '</div>\n'

# Read HTML
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Replace between markers
start = html.index("<!-- GALLERY-START -->") + len("<!-- GALLERY-START -->")
end = html.index("<!-- GALLERY-END -->")

new_html = html[:start] + "\n" + gallery_html + html[end:]

# Write back
with open(html_file, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Gallery updated!")
