_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def rgb(triplet):
    return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]

def triplet(rgb, lettercase=LOWERCASE):
    return format(rgb[0]<<16 | rgb[1]<<8 | rgb[2], '06'+lettercase)


def get_diff_triple(l1, l2):
    return [l2[idx] - val  for idx, val in enumerate(l1)]

def get_diff(l1, l2):
    return abs(sum(get_diff_triple(l1, l2)))

def get_nearest_colours(colours):
    
    # 404040  (64, 64, 64)
    # FF0000  (255, 0, 0)
    # 00FF00  (0, 255, 0)
    # FFFF00  (255, 255, 0)
    # 0000FF  (0, 0, 255)
    # FF00FF  (255, 0, 255)
    # 00FFFF  (0, 255, 255)
    # FFFFFF  (255, 255, 255)

    print colours

    for c in colours:
        print "{}: {}".format(c, get_diff([0,0,0], c))

    from_black = [(c, get_diff([0,0,0], c)) for c in colours]
    from_black.sort(key=lambda x: x[1])
    print from_black
    # black and white are at both ends of the spectrum, then we
    #  remove them so we can't possibly have them anywhere else
    black = from_black[0][0]
    white = from_black[0][-1]
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

if __name__ == '__main__':
    
    get_nearest_colours([[2, 4, 15], [6, 11, 48], [18, 30, 85], [28, 49, 130], [31, 79, 188], [47, 145, 232], [139, 155, 197], [209, 219, 241]])

    print "==================================\n\n\n"

    print ("#000000" + rgb("#000000"))
    print ("#CD0000" + rgb("#CD0000"))
    print ("#00CD00" + rgb("#00CD00"))
    print ("#CDCD00" + rgb("#CDCD00"))
    print ("#0000CD" + rgb("#0000CD"))
    print ("#CD00CD" + rgb("#CD00CD"))
    print ("#00CDCD" + rgb("#00CDCD"))
    print ("#FAEBD7" + rgb("#FAEBD7"))
    print ("#404040" + rgb("#404040"))
    print ("#FF0000" + rgb("#FF0000"))
    print ("#00FF00" + rgb("#00FF00"))
    print ("#FFFF00" + rgb("#FFFF00"))
    print ("#0000FF" + rgb("#0000FF"))
    print ("#FF00FF" + rgb("#FF00FF"))
    print ("#00FFFF" + rgb("#00FFFF"))
    print ("#FFFFFF" + rgb("#FFFFFF"))
