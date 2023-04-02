import matplotlib.pyplot as plt
import cv2
from rembg import remove
from PIL import Image
import numpy as np


def blacken_image(org_image):
    shade_image = np.copy(org_image)
    shade_image[..., 0:3] = 0
    # plt.imshow(shade_image)
    return shade_image


def add_shade(org_image, shade, stride=(2, 2)):
    h_str, w_str = stride
    h_org, w_org = np.shape(org_image)[:2]
    expanded = np.zeros((h_org+h_str, w_org+w_str, 4))
    org_image_copy = np.copy(org_image)
    expanded[-h_org:, -w_org:] = np.copy(shade)
    expanded[:h_org, :w_org][org_image_copy[..., -1] > 0.8] = org_image_copy[org_image_copy[..., -1] > 0.8]

    return expanded


def preprocess_image(imgpath):
    # so far only png file is tested
    image = Image.open(imgpath)
    # cutout outline
    image_cutout = remove(image)
    # cutout transparent part
    cropped_image = image_cutout.crop(image_cutout.getbbox())
    # plt.imshow(cropped_image)
    return cropped_image


def shadow_adder(scaled_image):
    # make sure that (0...1) scale is used
    image_array = np.array(scaled_image)
    if np.issubdtype(image_array.dtype, np.integer):
        image_array = image_array/255.0
    original_image = image_array

    shade_sharp = blacken_image(original_image)
    shade = cv2.GaussianBlur(shade_sharp, (11, 11), 2, 2)  # blurring process
    # choose number close to half of the (n,n) above.
    image_with_shade = add_shade(original_image, shade, stride=(6, 6))
    # img_obj = Image.fromarray((image_with_shade*255)//1, "RGB")
    # img_obj.save(outputpath)
    img_obj = Image.fromarray(
        (image_with_shade*255).astype(np.uint8), mode="RGBA")

    return img_obj


def main():
    preprocess_image()


if __name__ == "__main__":
    main()
