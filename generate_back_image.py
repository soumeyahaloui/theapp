from PIL import Image, ImageDraw, ImageFont
import os

# Define constants
final_width = 380  
final_height = 200  
scale_factor = 4  
large_width = final_width * scale_factor
large_height = final_height * scale_factor

background_color = (255, 255, 255, 0)  
text_color = (255, 255, 255, 255)  
font_path = "assets/fonts/NotoNaskhArabic-Regular.ttf"  
font_size = 80 * scale_factor  

# Arabic category names
animal_categories = [
            "حيوانات أليفة", "حيوانات برية", "حيوانات المزرعة", "طيور", "كائنات بحرية", "حشرات"
        ]

# Output directory
output_dir = "assets/images/text/animalcategories"
os.makedirs(output_dir, exist_ok=True)

# Load font
font = ImageFont.truetype(font_path, font_size)

for text in animal_categories:
    # Create a large blank image
    large_image = Image.new("RGBA", (large_width, large_height), background_color)

    # Draw text
    draw = ImageDraw.Draw(large_image)
    bbox = font.getbbox(text)  
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (large_width - text_width) // 2
    y = ((large_height - text_height) // 2) - (40 * scale_factor)  

    # Add shadow effect
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for offset in offsets:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=text_color)

    # Add main text
    draw.text((x, y), text, font=font, fill=text_color)

    # Resize image to final dimensions
    final_image = large_image.resize((final_width, final_height), Image.Resampling.LANCZOS)

    # Save the image
    output_path = os.path.join(output_dir, f"{text}.png")
    final_image.save(output_path, format="PNG")
    print(f"Saved: {output_path}")
