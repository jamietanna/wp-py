from colorz import colorz, rtoh
from math   import sqrt
import colorsys

from array import array
from generic import output

def lighter_colour(colour):
    ret = colour + 20
    if ret > 255:
        return 255
    else:
        return ret

def torgb(hexv):
    hexv = hexv[1:]
    r, g, b = (
        int(hexv[0:2], 16) / 256.0,
        int(hexv[2:4], 16) / 256.0,
        int(hexv[4:6], 16) / 256.0,
    )
    return r, g, b

def normalize(hexv, minv=128, maxv=256):
    r, g, b = torgb(hexv)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    minv = minv / 256.0
    maxv = maxv / 256.0
    if v < minv:
        v = minv
    if v > maxv:
        v = maxv
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))

def darkness(hexv):
  r, g, b = torgb(hexv)
  darkness = sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
  return darkness

def to_hsv(c):
    r, g, b = torgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

def get_diff(l1, l2):
    return sum([l2[idx] - val  for idx, val in enumerate(l1)] )


def get_colours(path):
    
    # print torgb("#000000000000")
    # print torgb("#CDCD00000000")
    # print torgb("#0000CDCD0000")
    # print torgb("#CDCDCDCD0000")
    # print torgb("#00000000CDCD")
    # print torgb("#CDCD0000CDCD")
    # print torgb("#0000CDCDCDCD")
    # print torgb("#FAFAEBEBD7D7")
    # print torgb("#404040404040")
    # print torgb("#FFFF00000000")
    # print torgb("#0000FFFF0000")
    # print torgb("#FFFFFFFF0000")
    # print torgb("#00000000FFFF")
    # print torgb("#FFFF0000FFFF")
    # print torgb("#0000FFFFFFFF")
    # print torgb("#FFFFFFFFFFFF")
    

    # 000000  (0, 0, 0)
    # CD0000  (205, 0, 0)
    # 00CD00  (0, 205, 0)
    # CDCD00  (205, 205, 0)
    # 0000CD  (0, 0, 205)
    # CD00CD  (205, 0, 205)
    # 00CDCD  (0, 205, 205)
    # FAEBD7  (250, 235, 215)
   
    # 404040  (64, 64, 64)
    # FF0000  (255, 0, 0)
    # 00FF00  (0, 255, 0)
    # FFFF00  (255, 255, 0)
    # 0000FF  (0, 0, 255)
    # FF00FF  (255, 0, 255)
    # 00FFFF  (0, 255, 255)
    # FFFFFF  (255, 255, 255)
    

    _colours = colorz(path, 8)
    _colours.sort()
    colours = list(_colours)
    
    for c in _colours:
        colours.append( [lighter_colour(x) for x in c] )

    colours = map(rtoh, colours)
    colours_normalised = []
    ret = []

    for i, c in enumerate(colours):
        if i == 0:
            c = normalize(c, minv=0, maxv=32)
        elif i == 8:
            c = normalize(c, minv=128, maxv=192)
        elif i < 8:
            c = normalize(c, minv=160, maxv=224)
        else:
            c = normalize(c, minv=200, maxv=256)
        c = normalize(c, minv=32, maxv=224)
        ret.append(c)
    
    return ret
