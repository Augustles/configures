# coding=utf-8

from PIL import Image
import sys
BACKGROUND = 255



def floodfillfilter(im, way=4, mincount=8):
    frame = im.load()
    (w, h) = im.size
    points = []
    processedpoints = []
    global goodpoints
    goodpoints = []
    for x in xrange(w):
        for y in xrange(h):
            color = frame[x, y]
            if color == BACKGROUND or ((x, y) in processedpoints):
                continue
            processedpoints.append((x, y))

            points.append((x, y))

            # points.remove((x,y))
            for (x, y) in points:

                try:
                    if frame[x, y - 1] == color and (x, y - 1) not in points:
                        points.append((x, y - 1))
                except:
                    pass
                try:
                    if frame[x, y + 1] == color and (x, y + 1) not in points:
                        points.append((x, y + 1))
                except:
                    pass
                try:
                    if frame[x - 1, y] == color and (x - 1, y) not in points:
                        points.append((x - 1, y))
                except:
                    pass
                try:
                    if frame[x + 1, y] == color and (x + 1, y) not in points:
                        points.append((x + 1, y))
                except:
                    pass
                if way == 8:
                    try:
                        if frame[x - 1, y - 1] == color and (x - 1, y - 1) not in points:
                            points.append((x - 1, y - 1))
                    except:
                        pass
                    try:
                        if frame[x + 1, y - 1] == color and (x + 1, y - 1) not in points:
                            points.append((x + 1, y - 1))
                    except:
                        pass
                    try:
                        if frame[x - 1, y + 1] == color and (x - 1, y + 1) not in points:
                            points.append((x - 1, y + 1))
                    except:
                        pass
                    try:
                        if frame[x + 1, y + 1] == color and (x + 1, y + 1) not in points:
                            points.append((x + 1, y + 1))
                    except:
                        pass
            processedpoints.extend(points)
            # print color,len(points)
            # print points
            if 1 < len(points) < mincount:
                for (x, y) in points:
                    # print x,y
                    frame[x, y] = BACKGROUND
            if len(points) > 16:
                goodpoints.extend(points)

            points = []

    return im

# 去除噪点
def removedot(im):
    #global goodpoints
    frame = im.load()
    (w, h) = im.size
    for i in xrange(w):
        for j in xrange(h):
            if frame[i, j] != 255:
                count = 0
                try:
                    if frame[i, j - 1] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i, j + 1] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i - 1, j - 1] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i - 1, j] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i - 1, j + 1] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i + 1, j - 1] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i + 1, j] == 255:
                        count += 1
                except IndexError:
                    pass
                try:
                    if frame[i + 1, j + 1] == 255:
                        count += 1
                except IndexError:
                    pass

                if count >= 6:
                    frame[i, j] = BACKGROUND

    return im


def get_code(im):
    from pytesseract import image_to_string
    code = image_to_string(im)
    return code

# main主程序
def getframe(fname, strict=1):
    '''return w*h key frame without noise'''
    # open image
    try:
        im = Image.open(fname)
    except:
        return "File error!"
    frame = im.load()
    (w, h) = im.size
    print(w, h)
    for i in xrange(w):
        frame[i, 0] = (255, 255, 255)
        frame[i, h - 1] = (255, 255, 255)

    for i in xrange(h):
        frame[0, i] = (255, 255, 255)
        frame[w - 1, i] = (255, 255, 255)

    for i in xrange(w):
        for j in xrange(h):
            if frame[i, j] > (200, 200, 200):
                frame[i, j] = (255, 255, 255)
            if frame[i, j] != (255, 255, 255):
                frame[i, j] = (0, 0, 0)
    im = im.convert('L')
    im.show()
    im = removedot(im)
    im = floodfillfilter(im, 4, 20)
    im.show()
    return im


if __name__ == '__main__':
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        im = getframe(fn)
        # im.show()
        print get_code(im)
