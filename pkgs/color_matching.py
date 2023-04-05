import numpy as np
import pandas
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def load_colorpairs(path_to_excel="colormatch.xlsx"):
    pd_excel_handler = pandas.read_excel(path_to_excel, sheet_name="used")
    colorpairs = np.array(pd_excel_handler)
    return colorpairs


def matcher(pixel, colorpairs):
    """
    color_matching
    Args:
        pixel (an array of 3): RGB
        colorpairs (data): 2darray

    Returns:
        matched pixel: 
    """
    pixel_c = np.array(np.copy(pixel))
    pair_idx = np.argmin(np.sum((colorpairs[:, :3]-pixel_c)**2, axis=1))
    return np.copy(colorpairs[pair_idx][4:7])


def choose_representative_pixel(imgobj):  # using clustering
    imgarr = np.array(imgobj)
    if not np.issubdtype(imgarr.dtype, np.integer):
        imgarr = (imgarr*255).astype(np.uint8)
    kmeansmodel = KMeans(n_clusters=3)
    flatten = imgarr[imgarr[..., -1] > 125].reshape(-1, 4)
    flatten = flatten[..., :3]
    pred = kmeansmodel.fit(flatten)
    color0 = pred.cluster_centers_[0]
    color1 = pred.cluster_centers_[1]
    color2 = pred.cluster_centers_[2]
    print(color0, color1, color2)

    representative = color0[:3]
    return (representative//1).astype(np.uint8)


def color_matching(imgobj):
    representative = choose_representative_pixel(imgobj)
    colorpairs = load_colorpairs()
    matchcolor = matcher(representative, colorpairs)
    return matchcolor


def main():
    representative = choose_representative_pixel("cleared_imgs/macaron.png")
    colorpairs = load_colorpairs()
    matchcolor = matcher(representative, colorpairs)
    # figure, ax = plt.subplots(2)
    # # you should comment out this
    # print(representative, matchcolor)
    # ax[0].imshow([[representative]]*3)
    # ax[1].imshow([[matchcolor]]*3)
    # # figure.show()
    # figure.savefig("color_matching.jpg")
    return


if __name__ == "__main__":
    main()
