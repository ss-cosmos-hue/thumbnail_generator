from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rembg import remove
from FaceDetectionInfo import bottom_value_decider
from FaceCropper import crop
import numpy as np
import os

try:
    os.makedirs('input')
    os.makedirs('output')
    os.makedirs('thumbnails')
except OSError:
    pass


def shift_contrast(im: Image, color=None):
    data = np.array(im)
    print(data.shape)
    if color is None:
        r1, g1, b1 = 0, 0, 0  # Original value
        pixels = set([i for i in im.getdata()])
        all_colors = list(np.ndindex((200, 200, 200)))
        non_colors = []
        i = len(all_colors)-1
        while len(non_colors) < 10 and i > 0:
            if all_colors[i] not in pixels:
                non_colors.append(all_colors[i])
            i -= 1
        color = non_colors[0]  # find brightest color that is not in the image
        r2, g2, b2 = color
    else:
        r1, g1, b1 = color
        r2, g2, b2 = 0, 0, 0

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = (r2, g2, b2)

    return Image.fromarray(data), color


def upscale_image(scale_factor):
    cmd = ("cd Real-ESRGAN; wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P weights; "
           "python3 inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i inputs --outscale", scale_factor, "--fp32")
    os.system(cmd)


def start(input_path, text):
    input = Image.open(input_path).convert('RGBA')
    intermediate, color = shift_contrast(input)
    # intermediate.save("output/shifted.png")
    intermediate = intermediate.filter(ImageFilter.FIND_EDGES)
    # intermediate.save("output/outline.png")
    ImageDraw.floodfill(intermediate, xy=(0, 0), value=color)
    intermediate.paste(input, (0, 0), input)
    output = remove(intermediate)
    output, _ = shift_contrast(output, color)
    output.save("output/frame.png")

    image_path = "output/frame.png"

    # Crop filler
    crop(bottom_value_decider(image_path), image_path)
    image_path = 'output/cropped.png'

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
    centerpiece_image = centerpiece_image.resize(
        (centerpiece_width, centerpiece_height))
    thumbnail_image.paste(centerpiece_image, (centerpiece_x,
                                              centerpiece_y), centerpiece_image)

    # Determine text box size and position
    text_x = int(thumbnail_image.width / 2)
    text_y = 0
    text_width = int(thumbnail_image.width / 2)
    text_height = thumbnail_image.height

    # Create new draw object and set font
    draw = ImageDraw.Draw(thumbnail_image)
    font = ImageFont.truetype(
        '/System/Library/Fonts/Supplemental/arial.ttf', size=36)

    text_lines = text.split('\n')

    # Determine maximum font size for text
    max_font_size = int(text_width / max([len(line) for line in text_lines]))

    # Set font size to maximum font size or 36 (whichever is smaller)
    font_size = min(max_font_size, 36)

    # Set font and text color
    draw.text((text_x, text_y), '\n'.join(
        text_lines), fill=(0, 0, 0), font=font)

    # Save thumbnail image
    thumbnail_image.save('thumbnails/thumbnail.png')
