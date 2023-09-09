from logging import debug
from pyautogui import screenshot, locate, locateOnScreen, locateCenterOnScreen
from pydirectinput import position
from numpy import array, ndarray, pi
from cv2 import cvtColor, COLOR_BGR2HSV, inRange, Canny, HoughLinesP, imwrite
from PIL import ImageGrab


def get_pixel_color_at_cursor():
    """Get rgb color at per mouse cursor selected pixel"""
    x, y = position()
    r, g, b = screenshot().getpixel((x, y))

    return x, y, r, g, b


def get_image_at_cursor(name='default', path='.\\assets\\skills\\', w=25, h=25):
    """Save an image with given format from the mouse cursor position"""
    x, y = position()
    img = screenshot(region=(x, y, w, h))
    img.save(path + name + ".png")

    return x, y


def get_image_at_position(name='default', region=(1018, 887, 393, 107)):
    """Save an image with given format from a given position"""
    img = screenshot(region=region)
    img.save('.\\assets\\test\\' + name + ".png")


def pixel_matches_color(x,y, exR,exG,exB, tolerance=25):
    """Get rgb color at a given coordinate and compare with given rgb color"""
    r, g, b = screenshot().getpixel((x, y))

    if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
        return True
    return False


def pixel_matches_color_region(r,g,b, start=(1018,887), end=(393,107)):
    x = int(end[0]-start[0] + 1)
    y = int(end[1]-start[1] + 1)
    
    for x in range(start[0], end[0] + 1, 1):
        for y in range(start[1], end[1] + 1, 1):
            if pixel_matches_color(x,y, r,g,b):
                debug("found position and color:\nx,y, r,g,b=%d,%d, %d,%d,%d" % (x,y, r,g,b))
                return True

            y = y + 1
        x = x + 1
    
    return False


def target_lines(max_dist, pos_x, pos_y):
    """Recognition of a line by a given color in the given screen region,
    returning distance to player"""
    array_min = array([108, 219, 97])
    array_max = array([188, 229, 157])
    screen_box = (200, 105, 1660, 920)
    
    image_grab = ImageGrab.grab(bbox=screen_box)
    np_array = array(image_grab)
    hsv = cvtColor(np_array, COLOR_BGR2HSV)
    #imwrite('.\\assets\\target-hsv.png', hsv)
    mask = inRange(hsv, array_min, array_max)
    edges = Canny(mask, 50, 150, apertureSize=3, L2gradient=True)
    lines = HoughLinesP(image=edges, rho=1, theta=pi/180, threshold=15, lines=array([]), minLineLength=5, maxLineGap=0)

    if type(lines) is ndarray:
        for points in lines:
            x,y, w,h=points[0]
            dist = ((pos_x - x)**2 + (pos_y - y)**2)**0.5
            if dist < max_dist:
                #imwrite('.\\assets\\target-hsv-match.png', hsv)
                debug('found target at ' + str(x) + ', ' + str(y))
                return dist
    return -1


def locate_needle(needle, haystack=0, conf=0.8, loctype='l', grayscale=True, region=(575,900,1337,1066)):
    """Searches the haystack image for the needle image, returning a tuple
    of the needle's coordinates within the haystack. If a haystack image is
    not provided, searches the client window or the overview window,
    as specified by the loctype parameter."""
    
    # with haystack image, return coordinates
    if haystack != 0:
        locate_var = locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            debug('found needle ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)))
            return locate_var
        else:
            debug('cant find needle ' + (str(needle)) + ' in haystack' + (str(haystack)) + ', ' + (str(locate_var)) + ', conf=' + (str(conf)))
            return -1, -1
        
    # without haystack image, return 1 or 0
    elif loctype == 'l':  # 'l' for regular 'locate'
        locate_var = locateOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            debug('found l image ' + (str(needle)) + ', ' + (str(locate_var)))
            # If the center of the image is not needed, don't return any coordinates.
            return True
        elif locate_var is None:
            debug('cannot find l image ' + (str(needle)) + ' conf=' + (str(conf)))
            return False
        
    # without haystack image, return coordinates
    elif loctype == 'c':  # 'c' for 'center'
        locate_var = locateCenterOnScreen(needle, confidence=conf, region=region, grayscale=grayscale)
        if locate_var is not None:
            debug('found c image ' + (str(needle)) + ', ' + (str(locate_var)))
            # Return the xy coordinates for the center of the image, relative to the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            debug('cannot find c image ' + (str(needle)) + ', conf=' + (str(conf)))
            return -1, -1

