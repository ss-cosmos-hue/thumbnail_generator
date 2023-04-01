from add_image_to_canvas import add_image_to_canvas
from PIL import Image,ImageDraw, ImageFont
import numpy as np
#place_images
def place_txt(canvas=Image.open("canvas/canvas.png"),filled_img_width=1800,inputtxt="Macaron Go Go",size_limits=[2432, 2369, 2352,],object_placed_left = True):
    #size_limits = [width_limit for each row]

    canvas_w,canvas_h = canvas.size 
    print(canvas_h)
    words = inputtxt.split()
    numrow = len(words)
    
    breakpoint_h = canvas_h//numrow 
    breakpoint_ws = [0]*3
    if object_placed_left:
        for i in range(numrow):
            breakpoint_ws[i] = canvas_w- size_limits[i]
    else:
        for i in range(numrow):
            breakpoint_ws[i] = canvas_w-filled_img_width+size_limits[i]
 
    assert 1<=numrow<=3
    assert len(size_limits) == numrow
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

    for i in range(numrow):
        word = words[i]
        fontsize = 1
        # jumpsize = 75
        filling_ratio = 0.9
        font = ImageFont.truetype("Arial.ttf", fontsize)
        l,t,r,b = font.getbbox(word)
        while np.abs(l-r) < breakpoint_ws[i]*filling_ratio and np.abs(t-b) < breakpoint_h*filling_ratio:
            # iterate until the text size is just larger than the criteria
            fontsize += 2
            font = ImageFont.truetype("Arial.ttf", fontsize)
            l,t,r,b = font.getbbox(word)
            # print(l,r,t,b)

        font = ImageFont.truetype("Arial.ttf", fontsize-2)
        print(l,r,t,b)
        if not object_placed_left:
            d.text((10,breakpoint_h*i), word, font=font, fill=(255, 255, 255, 128))
            # d.text((0,0), word, font=font, fill=(255, 255, 255, 128))
            
        else:
            d.text((canvas_w-breakpoint_ws[i],breakpoint_h*i), word, font=font, fill=(255, 255, 255, 128))
            # d.text((0,breakpoint_h*i), word, font=font, fill=(255, 255, 255, 128))
            #offset from left, offset from top
        print(breakpoint_ws,breakpoint_h)
    
    out = Image.alpha_composite(canvas, txt)
    out.save("canvas/canvas_with_txt.png")
    #bold and defo  


def main():
    place_txt()
    return
    
if __name__ == "__main__":
    main()