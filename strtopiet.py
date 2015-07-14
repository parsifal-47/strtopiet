#!/usr/bin/env python
"""strtopiet

Usage:
    strtopiet <string> <pngname>
    strtopiet -h | --help

Options:
    -h, --help       Show this help
"""

from __future__ import print_function

import docopt
import random
import sys
from PIL import Image

height = 20

operations = {"add": (1, 0), "push": (0, 1), "mult": (1, 2), "out": (5, 2)}
colors = [["#FFC0C0", "#FF0000", "#C00000"],\
          ["#FFFFC0", "#FFFF00", "#C0C000"],\
          ["#C0FFC0", "#00FF00", "#00C000"],\
          ["#C0FFFF", "#00FFFF", "#00C0C0"],\
          ["#C0C0FF", "#0000FF", "#0000C0"],\
          ["#FFC0FF", "#FF00FF", "#C000C0"]]
    
white = "#FFFFFF"
black = "#000000"

def hex_to_rgb(hex):
    return (int(hex[1:3],16),int(hex[3:5],16),int(hex[5:7],16))

def divide(mult, num):
    return ((divide(mult, num/mult) + [("push", mult), ("mult", random.randint(1, height))] + \
        ([("push", num % mult), ("add", random.randint(1, height))] if num % mult > 0 else [])) if num/mult > 0 else [("push", num % mult)])

def encode(num):
    mult = random.randint(5, height)
    return divide(mult, num) + [("out", random.randint(1, height))]


def main():
    args = docopt.docopt(__doc__, version='0.1.0')
    numbers = map(ord, args['<string>'])
    commands = sum(map(encode, numbers), []) + [("push", 1)] # last operation is ignored
    program = Image.new("RGB", (len(commands)+4, height), "white")
    colorX = 0
    colorY = 0
    X = 0
    for (Action, Value) in commands:
        for Y in range(0, Value):
            program.im.putpixel((X, Y), hex_to_rgb(colors[colorX][colorY]))
        (dX, dY) = operations[Action]
        colorX = (colorX + dX) % 6
        colorY = (colorY + dY) % 3
        X = X + 1

    # stop program
    l = len(commands)
    b = hex_to_rgb(black)
    s = hex_to_rgb(colors[0][0])
    [program.im.putpixel(p, c) for (p, c) in [((l+3, 0), b), ((l+3, 1), b), ((l+3, 3), b), ((l+2, 3), b),
        ((l+1, 3), b), ((l, 3), b), ((l, 2), b), ((l, 1), b), ((l+1, 1), b), 
        ((l+1, 2), s), ((l+2, 2), s), ((l+3, 2), s)]]

    program.save(args['<pngname>'])
    sys.exit(1)

if __name__ == '__main__':
    main()
