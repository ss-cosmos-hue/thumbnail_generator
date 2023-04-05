import os
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from color_matching import color_matching
from add_image_to_canvas import add_image_to_canvas
from add_txt_to_canvas import add_txt_to_canvas
from add_shadow_effect import preprocess_image, shadow_adder
from helpers import shift_contrast, remove, crop, bottom_value_decider, upscale_image
# from configuration import config

INTERMEDIATE_FRAME_PATH = "output/frame.png"


def thumbnail_generator(input_txt, input_path, output_path):
    try:
        os.makedirs('input')
        os.makedirs('output')
        os.makedirs('thumbnails')
    except OSError:
        pass

    # remove background
    input = Image.open(input_path).convert('RGBA')
    intermediate, color = shift_contrast(input)
    intermediate = intermediate.filter(ImageFilter.FIND_EDGES)
    ImageDraw.floodfill(intermediate, xy=(0, 0), value=color)
    intermediate.paste(input, (0, 0), input)
    output = remove(intermediate)
    output, _ = shift_contrast(output, color)
    output.save(INTERMEDIATE_FRAME_PATH)

    # crop above shoulders
    image_path = "output/frame.png"
    crop(bottom_value_decider(image_path), image_path)

    # crop extra space
    image_path = 'output/cropped.png'
    cropped_img = preprocess_image(image_path)

    # calculate ratio
    thumbnail_image = Image.new('RGB', (1280, 720), (255, 255, 255))
    centerpiece_image = Image.open(image_path).convert('RGBA')
    width, height = centerpiece_image.size
    ratio = thumbnail_image.height / height

    # more focus (upscaling)
    centerpiece_image.save('shadow.png')
    os.system('mv shadow.png Real-ESRGAN/inputs')

    if ratio > 1.5:  # Only if image needs to be upscaled
        upscale_image(str(ratio))
    os.system('rm -r Real-ESRGAN/inputs/*') # empty the folder

    # Add shadow
    shadow_out = Image.open('Real-ESRGAN/results/shadow_out.png')if os.path.exists('Real-ESRGAN/results/shadow_out.png') else cropped_img
    
    centerpiece_image = shadow_adder(shadow_out).convert('RGBA')
    os.system('rm -r Real-ESRGAN/results/*') # empty the folder
    
    
    
    # figure out color
    # cleared_imgs/macaron.png" # can be an img object
    matchcolor = color_matching(centerpiece_image)

    # add images
    numrow_txt = len(input_txt.split())
    canvasobj, placed_left, limits, filled_img_w = add_image_to_canvas(centerpiece_image,
                                                                       numrow_txt,
                                                                       matchcolor)
    # add text
    add_txt_to_canvas(canvasobj, output_path, filled_img_w,
                      input_txt, limits, object_placed_left=True)


def main():
    cwd = os.getcwd()
    thumbnail_generator("Sprite!", cwd+"/images/strawberry.png", cwd+"/images/cleared.png",cwd+"/images/canvas_without.png", cwd+"/images/out.png")
    return


if __name__ == "__main__":
    main()
