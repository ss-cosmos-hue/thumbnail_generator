from PIL import Image, ImageDraw, ImageFont
from rembg import remove
from FaceDetectionInfo import bottom_value_decider
from FaceCropper import crop

# Remove background
input_path = 'penguin.png'
output_path = 'removed_bg.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)

image_path = output_path

# Crop filler
crop(bottom_value_decider(image_path), image_path)
image_path = 'cropped.png'

# Load saved image
centerpiece_image = Image.open(image_path).convert('RGBA')

# Create new thumbnail image
thumbnail_image = Image.new('RGB', (1280, 720), (255, 255, 255))

# Determine centerpiece size and position
centerpiece_width = int(thumbnail_image.width / 2)
#centerpiece_height = int((centerpiece_image.height / centerpiece_image.width) * centerpiece_width)
centerpiece_height = int(thumbnail_image.height)
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

text_lines = "Hi I'm Mario".split('\n')

# Determine maximum font size for text
max_font_size = int(text_width / max([len(line) for line in text_lines]))

# Set font size to maximum font size or 36 (whichever is smaller)
font_size = min(max_font_size, 36)

# Set font and text color
draw.text((text_x, text_y), '\n'.join(text_lines), fill=(0, 0, 0), font=font)

# Save thumbnail image
thumbnail_image.save('thumbnail.png')
