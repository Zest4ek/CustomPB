import cuspb
import time
import random


def rgb_bar():
    pb = cuspb.init_bar()

    r,g,b = 255,0,0
    step = 15
    
    for i in range(101):
        pb.percent = i
        pb.fgtruecol(r,g,b)

        rand_ms = random.randint(0,100)/1000
        print(f"\r{pb.getsmoothbar()} {pb.percent}% ",end="",flush=True)

        if r == 255 and b == 0 and g < 255:
            g += step
            if g > 255: g = 255
        elif g == 255 and b == 0 and r > 0:
            r -= step
            if r < 0: r = 0
        elif g == 255 and r == 0 and b < 255:
            b += step
            if b > 255: b = 255
        elif b == 255 and r == 0 and g > 0:
            g -= step
            if g < 0: g = 0
        elif b == 255 and g == 0 and r < 255:
            r += step
            if r > 255: r = 255
        elif r == 255 and g == 0 and b > 0:
            b -= step
            if b < 0: b = 0

        time.sleep(rand_ms)

    print("\n")


def default_bar(col):  
    pb = cuspb.init_bar()
    pb.fgextdcol(col)

    for i in range(101):
        pb.percent = i

        rand_ms = random.randint(0,100)/1000
        print(f"\r{pb.getsmoothbar()} {pb.percent}% ",end="",flush=True)

        time.sleep(rand_ms)

    print("\n")


cuspb.init_console()
rgb_bar()