
def crop(percent_bottom, image_path):
    # Importing Image class from PIL module
    from PIL import Image
    
    # Opens a image in RGB mode
    im = Image.open(image_path)
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    
    # Check if the FaceDetector detected no info. If it detected no info, percent_bottom will be -3249429594509234095243095, since that's what I set the default to in FaceDetectionInfo.bottom_value_decider()
    if (percent_bottom == -3249429594509234095243095):
        im.save('cropped.png')
        return 

    # Setting the points for cropped image
    left = 0
    top = 0 
    right = width 
    bottom = (height * percent_bottom) + ((percent_bottom/10) * height) # The first part of this equation (before the plus sign) takes the relative y_max (percent_bottom) and multiplies it by the height to get the exact bottom. The second half of the equation (after the paranthesis) adds some room below the face, relative to the size of 1) image and 2) the bottom of the face
    #y_max = 0.38673246
    #y_min = 0.13302855
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    
    # Shows the image in image viewer
    #im1.show()

    im1.save('cropped.png')

#crop(0.38673246)


