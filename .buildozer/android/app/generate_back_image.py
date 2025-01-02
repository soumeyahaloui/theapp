from PIL import Image, ImageDraw, ImageFont

# Define image properties for a bigger image
image_width = 800  # Larger width
image_height = 300  # Larger height
background_color = (255, 255, 255, 0)  # Fully transparent background (RGBA)
text_color = (0, 0, 0, 255)  # Black text with full opacity
font_path = "assets/fonts/NotoNaskhArabic-Regular.ttf"  # Ensure this path is correct
font_size = 300  # Larger font size for much bigger text

# Create an empty image with a transparent background
image = Image.new("RGBA", (image_width, image_height), background_color)

# Load the font
font = ImageFont.truetype(font_path, font_size)

# Draw the text
text = "رجوع"  # Arabic word for "Back"
draw = ImageDraw.Draw(image)

# Calculate the text size and center position
bbox = font.getbbox(text)  # Returns (left, top, right, bottom)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (image_width - text_width) // 2
y = (image_height - text_height) // 2 - 170

# Render the text
draw.text((x, y), text, font=font, fill=text_color)

# Save the image
output_path = "assets/images/icon/back.png"
image.save(output_path, format="PNG")
print(f"Bigger back.png image saved at {output_path}.")
