from PIL import Image, ImageDraw, ImageFont

# Define image properties for high-resolution rendering
final_width = 800  # Final image width
final_height = 300  # Final image height
scale_factor = 4  # Scale up for better text rendering
large_width = final_width * scale_factor
large_height = final_height * scale_factor

background_color = (255, 255, 255, 0)  # Fully transparent background (RGBA)
text_color = (0, 0, 0, 255)  # Black text with full opacity
font_path = "assets/fonts/NotoNaskhArabic-Bold.ttf"  # Ensure this path is correct
font_size = 300 * scale_factor  # Scale font size for high-resolution rendering

# Create a high-resolution image with a transparent background
large_image = Image.new("RGBA", (large_width, large_height), background_color)

# Load the font
font = ImageFont.truetype(font_path, font_size)

# Draw the text
text = "رجوع"  # Arabic word for "Back"
draw = ImageDraw.Draw(large_image)

# Calculate the text size and center position
bbox = font.getbbox(text)  # Returns (left, top, right, bottom)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (large_width - text_width) // 2
y = ((large_height - text_height) // 2) - (170 * scale_factor)  # Adjust vertically if needed

# Render the text multiple times for a bold effect
offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Offsets for bold effect
for offset in offsets:
    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=text_color)

# Render the original text again to enhance the boldness
draw.text((x, y), text, font=font, fill=text_color)

# Downscale to the final size for smooth rendering
final_image = large_image.resize((final_width, final_height), Image.Resampling.LANCZOS)

# Save the image
output_path = "assets/images/icon/back.png"
final_image.save(output_path, format="PNG")
print(f"Bolder and smoother back.png image saved at {output_path}.")
