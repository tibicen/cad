# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:37:27 2013

@author: Dawid Huczyński
"""
import os

from dxfwrite import DXFEngine as dxf
from PIL import Image

from RGBdict import data


def getImage():
    folder = os.listdir()
    for f in folder:
        if f.endswith(('.png', '.jpg', '.jpeg')):
            im = Image.open(f, 'r')
            return im


def findCOL(px, keys):
    cols = keys
    tolerance = 255 * 3
    found = None
    for col in cols:
        tol = sum([x for x in map(lambda a, b: abs(a - b), px, col)])
        if tol <= tolerance:
            tolerance = tol
            found = col
    return found


def lolipop():
    drawning = dxf.drawing()
    k = 0
    for w in range(100):
        if w % 255 == 0:
            k += 1
        drawning.add(dxf.text('R2', insert=(
            w % 16 * 1.6, k), height=1.0, color=w % 255))
    return drawning


def kolory(im, data):
    drawning = dxf.drawing()
    k = 0
    awesome = 'AWESOME'
    keys = list(data.keys())
    keys.sort()
    h, w = im.size
    for l in range(h * w - 255):
        if l % 2000 == 0:
            print('{:6.2}/100'.format(l * 100 / (h * w - 255)), end='\r')
        if l % w == 0:
            k += 1
        if l % w == 1:
            c = -0.27
        else:
            c = 0
        x = l % w
        y = k
        px = im.getpixel((x, y))[:3]
        drawning.add(dxf.text(awesome[l % 7], insert=(
            float(x) + c, -y), height=1.0, color=data[findCOL(px, keys)]))
    return drawning

if __name__ == "__main__":
    print("Ruszylo...")
    im = getImage()
    drawning = kolory(im, data)
    drawning.saveas('cad_img2text.dxf')
    print("koniec.")
