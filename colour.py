from colorz import colorz, rtoh
from math   import sqrt
import colorsys


from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie1976
from colormath.color_conversions import convert_color


from array import array
from generic import output

def limit(n, lim):
    if n > lim:
        return lim
    else:
        return n

def tint(r,g,b):
    rt = r + (0.25 * (255 - r))
    gt = g + (0.25 * (255 - g))
    bt = b + (0.25 * (255 - b))

    # rt = limit((r * 1.25), 255) #  + (0.25 * (255 - r))
    # gt = limit((g * 1.25), 255) # + (0.25 * (255 - g))
    # bt = limit((b * 1.25), 255) # + (0.25 * (255 - b))

    return rt, gt, bt

def shade(r,g,b):
    rs = r * 0.25
    gs = g * 0.25
    bs = b * 0.25
    return rs, gs, bs

def lighter_colour(colour):
    # http://stackoverflow.com/questions/6615002/given-an-rgb-value-how-do-i-create-a-tint-or-shade
    ret = colour + (0.45 * (255 - colour))
    # ONLY if high enough ?? 

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
    trip = get_diff_triple(l1, l2)
    return abs(trip[0] * 2 + trip[1] * 3 + trip[2] * 4)

def rgb_to_lab_color(rgb):
    return convert_color(sRGBColor(rgb[0], rgb[1], rgb[2]), LabColor)

def rgb_compare_delta_e(rgb_1, rgb_2):
    return delta_e_cie1976(rgb_to_lab_color(rgb_1), rgb_to_lab_color(rgb_2))

def get_nearest_colours(colours):

    from_black = [(c, rgb_compare_delta_e([0,0,0], c)) for c in colours]
    print from_black
    from_black.sort(key=lambda x: x[1])
    print from_black

    from_white = [(c, rgb_compare_delta_e([255, 255, 255], c)) for c in colours]
    print from_white
    from_white.sort(key=lambda x: x[1])
    print from_white
    

    black = from_black[0][0]
    white = from_white[0][0]   
   
    from_s = []
    
    from_red = [(c, rgb_compare_delta_e([205,0,0], c)) for c in colours]
    from_grn = [(c, rgb_compare_delta_e([0,205,0], c)) for c in colours]
    from_ylw = [(c, rgb_compare_delta_e([205,205,0], c)) for c in colours]
    from_blu = [(c, rgb_compare_delta_e([0,0,205], c)) for c in colours]
    from_prp = [(c, rgb_compare_delta_e([205,0,205], c)) for c in colours]
    from_cyn = [(c, rgb_compare_delta_e([0,205,205], c)) for c in colours]

    from_s = [from_red, from_grn, from_ylw, from_blu, from_prp, from_cyn]
  
    from_s = [from_red, from_grn, from_ylw, from_blu, from_prp, from_cyn]
    print "?////////////////////////???"
    for idx, fr in enumerate(from_s):
        fr.sort(key=lambda x: x[1])
        print "{}:".format(idx)
        for f in fr:
            print "  " + str(f)
    print "?////////////////////////???"

    any_errors = False
    num_errors = 0

    for idx1, fr1 in enumerate(from_s):
        for idx2, fr2 in enumerate(from_s):
            if idx1 == idx2:
                continue
            else:
                if fr1[0][0] == fr2[0][0]:
                    print "colour {} is in multiple ({}, {})".format(fr1[0][0], idx1, idx2)
                    # any_errors = True
                    # num_errors += 1
                    print "fr1: {}".format(len(fr1))
                    from_s[idx1] = fr1[1:]
                    print "fr1[1:]: {}".format(len(from_s[idx1]))

                    # fr2[0] = fr2[0][1:]
                    
    print "?////////////////////////???"
    for idx, fr in enumerate(from_s):
        fr.sort(key=lambda x: x[1])
        print "{}:".format(idx)
        for f in fr:
            print "  " + str(f)
    print "?////////////////////////???"


    if not any_errors:
        print "NOW TO PROCESS"

        for idx, f in enumerate(from_s):
            print "{}: {}".format(idx, f[0][0])
        print "==========="

        red = from_s[0][0][0]
        grn = from_s[1][0][0]
        ylw = from_s[2][0][0]
        blu = from_s[3][0][0]
        prp = from_s[4][0][0]
        cyn = from_s[5][0][0]
        ret = [black, red, grn, ylw, blu, prp, cyn, white]
        for idx, r in enumerate(ret):
            print "{}: {}".format(idx, r)
        return ret
    else:
        print "CANNOT CONTINUE: ELSE CASE NEEDED"
        exit(1)

## TODO: order in get is not what I'm setting

# #000000000000
# #CDCD00000000
# #0000CDCD0000
# #CDCDCDCD0000
# #00000000CDCD
# #CDCD0000CDCD
# #0000CDCDCDCD

## TODO: FFFFFFF should be the bold one - make sure we know that the white we're returned takes this into account
# #FFFFFFFFFFFF
 
# #000000000000
# #00000000cdcd
# #00000000cdcd
# #0000cdcdcdcd
# #00000000cdcd
# #0000cdcdcdcd
# #0000cdcdcdcd
# #ffffffffffff

def get_colours(path): 
    _colours = colorz(path, 8)
    _colours.sort()

    print "***********************************"
    print _colours
    print "***********************************"
    
    colours = get_nearest_colours(_colours)
    print "***********************************"
    print colours
    print "***********************************"
    
    # print "+++++++++++++++++++++++++++++++++++++++++++++"
    # for idx,c in enumerate(colours):
    #     print "{}:\t{}\t{}".format(idx, c, [lighter_colour(x) for x in c])
    # print "+++++++++++++++++++++++++++++++++++++++++++++"

    ret = list(colours)

    print "????????????????????????????????????????????????"
    for c in colours:
        print "{}:\tt({})\ts({})".format(c, tint(c[0], c[1], c[2]), shade(c[0], c[1], c[2]))
        # colours.append( [lighter_colour(x) for x in c] )
        ret.append(tint(c[0], c[1], c[2]))
    print "????????????????????????????????????????????????"

    ret = map(rtoh, ret)

    for idx, c in enumerate(ret):
        print "{}: {}".format(idx, c)
    
    return ret
