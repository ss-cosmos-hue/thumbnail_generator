# configuration
from PIL import Image
import numpy as np
from configuration import config

# def set_configs(numrow,canvas_size,processed_img_size,processed_img_obj):
#     numrow = numrow
#     canvas_size = canvas_size
#     processed_img_size = processed_img_size
#     processed_img_obj = processed_img_obj
#     canvas_ = np.ones((canvas_size+[4]))
#     return


def calc_rightcorners(imgarr):
    h, w = np.shape(imgarr)[:2]
    a = [0]*h
    for i in range(h):
        nontransindices = np.where(imgarr[i][..., 3] != 0)[0]
        if len(nontransindices) != 0:
            a[i] = nontransindices[-1]+1  # the size of margin wouldn't hurt
    return a


def calc_leftcorners(imgarr):
    h, w = np.shape(imgarr)[:2]
    a = [0]*h
    for i in range(h):
        nontransindices = np.where(imgarr[i][..., 3] != 0)[0]
        if len(nontransindices) != 0:
            a[i] = nontransindices[-1]+1  # the size of margin wouldn't hurt
    return a


def calc_maxspace_for_text(numrow, canvas_size, corners):
    canvas_h, canvas_w = canvas_size[:2]
    res = np.zeros((numrow))
    for i in range(numrow):
        res[i] = np.max(corners[(canvas_h//numrow)
                        * i:(canvas_h//numrow)*(i+1)])
    return res


def place_image(canvas, processed_img, numrow, margin_h=1, margin_w=1):
    canvas_size = canvas.shape
    processed_img_size = np.array((np.array(processed_img)).shape)
    prop = min(canvas_size[0]//processed_img_size[0],
               canvas_size[1]//processed_img_size[1])
    filled_img_size = processed_img_size[:2]*prop
    # print(tuple(filled_img_size),canvas_size[0],)
    filled_img = processed_img.resize(tuple(filled_img_size[::-1]))
    filled_img_arr = np.array(filled_img)
    placed_left = True  # we need to update according to the orientation
    placed_right = not(placed_left)
    assert placed_left != placed_right
    filled_img_h, filled_img_w = filled_img_size

    if placed_left == True:
        canvas[-filled_img_h-margin_h:-margin_h, margin_w:filled_img_w +
               margin_w][filled_img_arr[..., -1] > 125] = filled_img_arr[filled_img_arr[..., -1] > 125]
        right_corners = calc_rightcorners(filled_img_arr)
        right_limits = calc_maxspace_for_text(
            numrow, canvas_size, right_corners)
        for _ in right_limits:
            _ += margin_w
        return canvas, placed_left, right_limits, filled_img_h
    else:
        canvas[-filled_img_h-margin_h:-margin_h, -filled_img_w-margin_w:-
               margin_w][filled_img_arr[..., -1] > 125] = filled_img_arr[filled_img_arr[..., -1] > 125]
        left_corners = calc_leftcorners(filled_img_arr)
        left_limits = calc_maxspace_for_text(numrow, canvas_size, left_corners)
        for _ in left_limits:
            _ += margin_h

        return canvas, placed_left, left_limits, filled_img_w

# main part of this file


def add_image_to_canvas(img_obj, numrow_txt, backgroundcolor=[0, 0, 0]):
    numrow = numrow_txt
    canvas_size = config.canvas_size  # height and width
    # image object of pillow#if you are to add edge, edge is already added
    processed_img = img_obj
    processed_img_arr = np.array(processed_img)

    canvas = np.ones(canvas_size+[4]).astype(np.uint8)
    # backgroundcolor =  [227,180,72]#can be obtained from color_matcher.py
    canvas[..., 0] = backgroundcolor[0]  # R
    canvas[..., 1] = backgroundcolor[1]  # G
    canvas[..., 2] = backgroundcolor[2]  # B of the images
    canvas[..., 3] = 255  # not transparent
    if not np.issubdtype(processed_img_arr.dtype, np.integer):
        print("converted type of array")
        processed_img_arr = (processed_img_arr*255.0).astype(np.uint8)
    canvas, placed_left, limits, filled_img_w = place_image(canvas, processed_img, numrow)
    canvasobj = Image.fromarray(canvas.astype(np.uint8), mode="RGBA")
    return canvasobj, placed_left, limits, filled_img_w


def main():
    # # print(type(processed_img_arr[0][0][0]))
    # if not np.issubdtype(processed_img.dtype, np.integer):
    #     print("converted type of array")
    #     processed_img_arr=(processed_img_arr*255.0).astype(np.uint8)
    # canvas,placed_left,limits = place_image(canvas_,processed_img)
    # # print(type(canvas[0][0][0]*))
    # canvasobj = Image.fromarray(canvas.astype(np.uint8),mode="RGBA")
    # canvasobj.save("canvas/canvas.png")
    # print(placed_left)
    canvas, placed_left, limits, filled_img_w = add_image_to_canvas()
    # print(limits)
    return canvas, placed_left, limits, filled_img_w


if __name__ == "__main__":
    main()
