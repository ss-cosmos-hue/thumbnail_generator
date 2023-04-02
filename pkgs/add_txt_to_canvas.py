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
    # font = ImageFont.truetype('/System/Library/Fonts/Supplemental/arial.ttf', size=36)
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", canvas.size, (255, 255, 255, 120))

    # get a font
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    word = words[narrow_row]
    # fontsize initialization
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

    height_unit = np.abs(t-b)
    heights = (np.linspace(canvas_h//2 - numrow*height_unit//2-height_unit//2, canvas_h//2 -
               numrow*height_unit//2 + numrow*height_unit-height_unit, num=numrow)).astype(np.int16)

    for i in range(numrow):
        word = words[i]
        filling_ratio = 0.8
        font = ImageFont.truetype("Arial.ttf", fontsize)
        l, t, r, b = font.getbbox(word)

        if not object_placed_left:  # no meaaning
            d.text((10, heights[i]), word, font=font,
                   fill=(255, 255, 255, 200))

        else:
            d.text(((canvas_w+size_limits[i]-5*(r-l)//4)//2, heights[i]),
                   word, font=font, fill=(255, 255, 255, 200))
            # offset from left, offset from top
    out = Image.alpha_composite(canvas, txt)
    out.save(output_path)


def main():
    add_txt_to_canvas()
    return


if __name__ == "__main__":
    main()
