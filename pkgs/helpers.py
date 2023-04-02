from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rembg import remove
from FaceDetectionInfo import bottom_value_decider
from FaceCropper import crop
import numpy as np
import os


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
           f"python3 inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i inputs --outscale {scale_factor} --fp32")
    os.system(cmd)
