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

def get_diff_triple(l1, l2):
    return [l2[idx] - val  for idx, val in enumerate(l1)]

def get_diff(l1, l2):
    return abs(sum(get_diff_triple(l1, l2)))

def get_nearest_colours(colours):
    print colours

    for c in colours:
        print "{}: {}".format(c, get_diff([0,0,0], c))

    from_black = [(c, get_diff([0,0,0], c)) for c in colours]
    from_black.sort(key=lambda x: x[1])
    print from_black

    # black and white are at both ends of the spectrum, then we
    #  remove them so we can't possibly have them anywhere else
    black = from_black[0][0]
    white = from_black[-1][0]
    colours = colours[1:-1]

    # create a list so we can iterate through each individual list
    from_s = []
    
    from_red = [(c, get_diff([205,0,0], c)) for c in colours]
    from_grn = [(c, get_diff([0,205,0], c)) for c in colours]
    from_ylw = [(c, get_diff([205,205,0], c)) for c in colours]
    from_blu = [(c, get_diff([0,0,205], c)) for c in colours]
    from_prp = [(c, get_diff([205,0,205], c)) for c in colours]
    from_cyn = [(c, get_diff([0,205,205], c)) for c in colours]

    # TODO: handle minus - abs() ? 

    from_s = [from_red, from_grn, from_ylw, from_blu, from_prp, from_cyn]
    for fr in from_s:
        fr.sort(key=lambda x: x[1])
        print fr

    any_errors = False

    for fr1 in from_s:
        for fr2 in from_s:
            if fr1 == fr2:
                continue
            else:
                if fr1[0][0] == fr2[0][0]:
                    print "colour {} is in multiple".format(fr1[0][0])
                    any_errors = True
    
    if not any_errors:
        print "NOW TO PROCESS"
        red = from_red[0][0]
        grn = from_grn[0][0]
        ylw = from_ylw[0][0]
        blu = from_blu[0][0]
        prp = from_prp[0][0]
        cyn = from_cyn[0][0]
        return [black, red, grn, ylw, blu, prp, cyn, white]
    else:
        print "CANNOT CONTINUE: ELSE CASE NEEDED"
        exit(1)




def get_colours(path):
    _colours = colorz(path, 8)
    _colours.sort()
    colours = list(_colours)

    print "***********************************"
    print colours
    print "***********************************"
    
    colours = get_nearest_colours(colours)
    print "***********************************"
    print colours
    print "***********************************"

    
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
