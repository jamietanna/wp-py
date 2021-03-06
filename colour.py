"""
Helper code to generate the correct colours from a given file,
 interfacing with Caleb Everett (everett1992)'s code in colorz.py. 
"""
from colorz import colorz, rtoh
import config

from colormath.color_objects     import sRGBColor, LabColor
from colormath.color_diff        import delta_e_cie1976
from colormath.color_conversions import convert_color

def tint(red, green, blue):
    """
    Generate a tint (calculated from Config.TINT_MULT) given an RGB colour. 
    """
    red_tint   = red   + (config.TINT_MULT * (255 - red))
    green_tint = green + (config.TINT_MULT * (255 - green))
    blue_tint  = blue  + (config.TINT_MULT * (255 - blue))
    return  red_tint, green_tint, blue_tint

def rgb_to_lab_color(rgb):
    """
    Given an rgb list, generate a colormath.color_objects.LabColor
    """
    return convert_color(sRGBColor(rgb[0], rgb[1], rgb[2]), LabColor)

def rgb_compare_delta_e(rgb_1, rgb_2):
    """
    Compare two rgb colours, and return the DeltaE value as per 
     the colormath library
    """
    return delta_e_cie1976(rgb_to_lab_color(rgb_1), rgb_to_lab_color(rgb_2))

def get_nearest_colours(colours):
    """
    Given a list of colours from a file, return the colours which are 
     most like the [BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE]
     as per the terminal (and /probably/ other) standards
    """
    from_s = [
        [(c, rgb_compare_delta_e([0,   0,   0],   c)) for c in colours],
        [(c, rgb_compare_delta_e([205, 0,   0],   c)) for c in colours],
        [(c, rgb_compare_delta_e([0,   205, 0],   c)) for c in colours],
        [(c, rgb_compare_delta_e([205, 205, 0],   c)) for c in colours],
        [(c, rgb_compare_delta_e([0,   0,   205], c)) for c in colours],
        [(c, rgb_compare_delta_e([205, 0,   205], c)) for c in colours],
        [(c, rgb_compare_delta_e([0,   205, 205], c)) for c in colours],
        [(c, rgb_compare_delta_e([255, 255, 255], c)) for c in colours]
    ]
    
    for idx, colour_list in enumerate(from_s):
        colour_list.sort(key=lambda x: x[1])
  
    for idx1, fr1 in enumerate(from_s):
        for idx2, fr2 in enumerate(from_s):
            if idx1 != idx2 and fr1[0][0] == fr2[0][0]:
                from_s[idx1] = fr1[1:]


    return [ from_s[idx][0][0] for idx in list(xrange(len(from_s))) ]
## TODO: FFFFFFF should be the bold one - make sure we know that the
#    white we're returned takes this into account

def get_colours(path): 
    """
    Given a file, extract the 8 most prominent colours, and 
     generate the corresponding tints. Provides an interface 
     between Caleb Everett (everett1992)'s code which extracts
     the colours from an image, and returns the hex values
     for the generated colours. 
    """
    _colours = colorz(path, 8)
    _colours.sort()

    colours = get_nearest_colours(_colours)
    ret = list(colours)

    for colour in colours:
        ret.append(tint(colour[0], colour[1], colour[2]))
    return [rtoh(colour) for colour in ret]

