#potential main code
#includes everything
from color_matching import color_matching
from add_image_to_canvas import add_image_to_canvas
from add_txt_to_canvas import add_txt_to_canvas

def thumbnail_generator(inputtxt,inputpath,path_to_clearedimg,path_to_canvas_without_img, outputpath):
    #cutout
    #crop
    #detection
    #more focus
    #size fit
    #figure out color 
    matchcolor = color_matching(path_to_clearedimg)#cleared_imgs/macaron.png"#can be an img object
    #add images
    numrow_txt = len(inputtxt)
    canvasobj,placed_left,limits,filled_img_w = add_image_to_canvas(numrow_txt,backgroundcolor=matchcolor, inputpath=path_to_clearedimg,outputpath=path_to_canvas_without_img)
    #add text
    add_txt_to_canvas(canvasobj,filled_img_width=filled_img_w,inputtxt=inputtxt,size_limits=limits,object_placed_left = True)

    return

def main():
    return

if __name__ == "__main__":
    main()