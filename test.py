import matplotlib.pyplot as plt
import cv2
import webcolors
import numpy as np
import glob
from PIL import Image



def _reversedict(d: dict) -> dict:
    """
    Internal helper for generating reverse mappings; given a
    dictionary, returns a new dictionary with keys and values swapped.

    """
    return {value: key for key, value in d.items()}


HAIRCOLOR_NAMES_TO_HEX = {
    "black": "#000000",
    "blond": "#d2b48c",
    "brown": "#352118",
    "darkbrown": "#1d130e",
    "lightbrown": "#4a3014",
    "red": "#4a1414",
    "grey": "#606060",
    "snow": "#fffafa"
}

HAIRCOLOR_HEX_TO_NAMES = _reversedict(HAIRCOLOR_NAMES_TO_HEX)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in HAIRCOLOR_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    closest_name = closest_colour(requested_colour)

    return closest_name




def rgb_to_hsv(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d / high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h*360, s*100, v/2.55


def print_list(a):
    string = ''
    for i in a:
        string += str(i) + '/'
    return string[:-1]


debug = False
path = 'example/Pictures2020/300_morph_Asiaten_dunkle/'
for filename in glob.glob(path + '/*_hair.jpg'):
    # for row in range(1788, 1791):

    img = cv2.imread(filename)
    Z = img.reshape((-1, 3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(img.shape)
    res2 = cv2.resize(res2, (200, 200))

    h0, s0, v0 = rgb_to_hsv(center[0][2], center[0][1], center[0][0])
    h1, s1, v1 = rgb_to_hsv(center[1][2], center[1][1], center[1][0])
    if debug:
        print("HSV 0: " + str(h0) + " " + str(s0) + " " + str(v0))
        print("HSV 1: " + str(h1) + " " + str(s1) + " " + str(v1))

    if (h0 > 65 and (s0 > 20 or v0 > 16)) or (h1 > 65 and (s1 > 20 or v1 > 16)):
        if s0 + v0 > s1 + v1:
            color = print_list(center[1])
        else:
            color = print_list(center[0])
    else:
        if v0 > v1:
            color = print_list(center[1])
        else:
            color = print_list(center[0])
    print(color)

    img = cv2.resize(img, (200, 200))
    size = 100
    a = 2
    pattern = round(size/a)
    fname = filename.replace('_hair.jpg', 'k_means.jpg')
    cv2.imwrite(fname, res2)
    '''for x in range(a):
        for y in range(a):
            max_values = []
            for i, col in enumerate(['b', 'g', 'r']):
                crop_img = img[y*pattern:(1+y)*pattern, x*pattern:(1+x)*pattern]
                hist = cv2.calcHist([crop_img], [i], None, [256], [0, 256])
                minmax = cv2.minMaxLoc(hist)
                max_values.append(minmax[3][1])
                plt.plot(hist, color=col)
                plt.xlim([0, 256])

            print(max_values)
            h,s,v = rgb_to_hsv(max_values[2], max_values[1], max_values[0])
            print(str(int(h)) + " " + str(int(s)) + " " + str(int(v)))
            plt.show()

            plt.close()
'''
quit()
