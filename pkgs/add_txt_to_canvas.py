from PIL import Image, ImageDraw, ImageFont
import numpy as np


# place_images
def add_txt_to_canvas(canvas, output_path,
              filled_img_width, input_txt,
              size_limits,
              object_placed_left
              ):
    # size_limits = [width_limit for each row]

    canvas_w, canvas_h = canvas.size
    print(canvas_h)
    words = input_txt.split()
    numrow = len(words)

    breakpoint_h = canvas_h//numrow
    breakpoint_ws = [0]*numrow

    if object_placed_left:
        for i in range(numrow):
            breakpoint_ws[i] = canvas_w - size_limits[i]
    else:
        for i in range(numrow):
            breakpoint_ws[i] = canvas_w-filled_img_width+size_limits[i]

    # will be replaced with the lengths considering font
    word_lens = [len(word) for word in words]
    margin_lens = np.copy(breakpoint_ws)
    props = [margin_lens[i]/word_lens[i] for i in range(numrow)]
    narrow_row = np.argmin(props)

    assert 1 <= numrow <= 3
    # assert len(size_limits) == numrow
    # place_image()
    # thumbnail_image = Image.new('RGB', (1280, 720), (255, 255, 255))
    # draw = ImageDraw.Draw(thumbnail_image)
    # font = ImageFont.truetype('/System/Library/Fonts/Supplemental/arial.ttf', size=36)
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", canvas.size, (255, 255, 255, 40))

    # get a font
    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    # fnt = ImageFont.load_default()
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    # draw text, full opacity
    # d.text((100, 200), "World", font=fnt, fill=(255, 255, 255, 255))
    word = words[narrow_row]
    fontsize = 1
    filling_ratio = 0.95
    font = ImageFont.truetype("Arial.ttf", fontsize)
    l, t, r, b = font.getbbox(word)

    # font size determination
    while np.abs(l-r) < breakpoint_ws[i]*filling_ratio and np.abs(t-b) < breakpoint_h*filling_ratio:
        # iterate until the text size is just larger than the criteria
        fontsize += 2
        font = ImageFont.truetype("Arial.ttf", fontsize)
        l, t, r, b = font.getbbox(word)
        font = ImageFont.truetype("Arial.ttf", fontsize-2)

    # heights =None
    # if numrow == 1:

    height_unit = np.abs(t-b)
    heights = (np.linspace(canvas_h//2-numrow*height_unit//2, canvas_h//2 -
               numrow*height_unit//2+numrow*height_unit, num=numrow)).astype(np.int16)
    print(heights, t-b)

    for i in range(numrow):
        word = words[i]
        filling_ratio = 0.9
        font = ImageFont.truetype("Arial.ttf", fontsize)
        l, t, r, b = font.getbbox(word)

        print(l, r, t, b)
        if not object_placed_left:  # no meaaning
            d.text((10, heights[i]), word, font=font,
                   fill=(255, 255, 255, 200))
            # d.text((0,0), word, font=font, fill=(255, 255, 255, 128))

        else:
            d.text(((canvas_w+size_limits[i]-(r-l))//2, heights[i]),
                   word, font=font, fill=(255, 255, 255, 200))
            # d.text((0,breakpoint_h*i), word, font=font, fill=(255, 255, 255, 128))
            # offset from left, offset from top
        # print(breakpoint_ws,breakpoint_h)

    out = Image.alpha_composite(canvas, txt)
    out.save(output_path)
    #bold and defo


def main():
    place_txt()
    return


if __name__ == "__main__":
    main()
