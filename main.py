from PIL import Image, ImageDraw, ImageFont

# Load centerpiece image
centerpiece_image = Image.open('mario.png').convert('RGBA')

# Convert image to alpha channel
alpha = Image.new('RGBA', centerpiece_image.size, (0, 0, 0, 0))
alpha_draw = ImageDraw.Draw(alpha)
alpha_draw.rectangle((0, 0, centerpiece_image.size[0], centerpiece_image.size[1]), fill=(255, 255, 255, 255))
alpha.paste(centerpiece_image, mask=centerpiece_image)

# Save new centerpiece image with alpha channel
centerpiece_image = alpha.convert('RGBA')
centerpiece_image.save('mario_alpha.png')

# Load saved image
centerpiece_image = Image.open('mario_alpha.png').convert('RGBA')

# Create new thumbnail image
thumbnail_image = Image.new('RGB', (1280, 720), (255, 255, 255))

# Determine centerpiece size and position
centerpiece_width = int(thumbnail_image.width / 2)
centerpiece_height = int((centerpiece_image.height / centerpiece_image.width) * centerpiece_width)
centerpiece_x = 0
centerpiece_y = 0

# Resize and paste centerpiece image onto thumbnail image
centerpiece_image = centerpiece_image.resize((centerpiece_width, centerpiece_height))
thumbnail_image.paste(centerpiece_image, (centerpiece_x, centerpiece_y), centerpiece_image)

# Determine text box size and position
text_x = int(thumbnail_image.width / 2)
text_y = 0
text_width = int(thumbnail_image.width / 2)
text_height = thumbnail_image.height

# Create new draw object and set font
draw = ImageDraw.Draw(thumbnail_image)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/arial.ttf', size=36)

# Split text into lines based on newline character
text_lines = "Hi I'm Mario".split('\n')

# Determine maximum font size for text
max_font_size = int(text_width / max([len(line) for line in text_lines]))

# Set font size to maximum font size or 36 (whichever is smaller)
font_size = min(max_font_size, 36)

# Set font and text color
draw.text((text_x, text_y), '\n'.join(text_lines), fill=(0, 0, 0), font=font)

# Save thumbnail image
thumbnail_image.save('thumbnail.png')
