# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 22:37:22 2014

@author: Dawid Huczyński
"""
import os
import random
from math import sqrt

import matplotlib.pyplot as plt
# git@github.com:RickardSjogren/squarify.git updated for python3 compability
import squarify
import xlrd
from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER, MIDDLE
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Rectangle


class space(object):

    def __init__(self, nr, name):
        self.nr = nr
        self.name = name
        self.children = []
        self.area = 0.0

    def addChild(self, child):
        self.children.append(child)
        self.area += child.getArea()

    def getArea(self):
        return self.area

    def updateArea(self):
        self.area = 0
        for child in self.children:
            self.area += child.getArea()

    def __str__(self):
        return str(self.name) + ': ' + str(round(self.area, 2))

    def __repr__(self):
        return '(' + str(self.name) + ')'


class room(space):

    def __init__(self, nr, name, pplNr, area):
        self.nr = nr
        self.name = name
        self.pplNr = pplNr
        self.area = area


def addRow(sh, nrow=0, nr=0, root=None):
    if not root:
        root = space('0', 'data')
    while sh.nrows - 2 >= nrow:
        nrow += 1
        row = sh.row(nrow)
        print(sh.row(nrow))
        if sh.row(nrow)[0].ctype == 2:
            nr = 2
            row = sh.row(nrow)
            root.addChild(room(row[0].value, row[1].value, row[2].value,
                               row[4].value))
        elif str(sh.row(nrow)[0].value).count('.') >= nr:
            nr = str(sh.row(nrow)[0].value).count('.')
            temp, nrow, nr = addRow(sh, nrow, nr, space(sh.row(nrow)[0].value,
                                                        sh.row(nrow)[1].value))
            root.addChild(temp)
#        else:
#            nrow -=1
#            return root, nrow, nr
        if abs(str(sh.row(nrow)[0].value).count('.')) < nr:
            nrow -= 1
            nr -= 1
            return root, nrow, nr
    return root, nrow, nr


def importData(sh):
    first = []
    second = []
    rooms = []
    area = 0
    for nrow in range(sh.nrows)[1:]:
        #        print(sh.row(nrow))
        if sh.row(nrow)[0].ctype == 2:
            #            print('a', end='')
            if len(first) != 0:
                second[-1].children = rooms.copy()
                second[-1].area = area
                area = 0
                rooms = []
                first[-1].children = second.copy()
                first[-1].area = sum([x.area for x in second])
                second = []
            first.append(space(sh.row(nrow)[0].value, sh.row(nrow)[1].value))
        elif str(sh.row(nrow)[0].value).count('.') == 1:
            if len(second) != 0:
                second[-1].children = rooms.copy()
                second[-1].area = area
                area = 0
                rooms = []
            second.append(space(sh.row(nrow)[0].value, sh.row(nrow)[1].value))
        else:

            for n in range(int(sh.row(nrow)[3].value)):
                area += sh.row(nrow)[4].value
                if int(sh.row(nrow)[3].value) > 1:
                    roomNr = sh.row(nrow)[0].value + '.' + str(n)
                else:
                    roomNr = sh.row(nrow)[0].value
                rooms.append(room(roomNr, sh.row(nrow)[1].value,
                                  sh.row(nrow)[2].value, sh.row(nrow)[4].value))
    second[-1].children = rooms.copy()
    second[-1].area = area
    area = 0
    rooms = []
    first[-1].children = second.copy()
    first[-1].area = sum([x.area for x in second])
    second = []
    data = space('0', 'data')
    data.children = first.copy()
    data.area = sum([x.area for x in first])
    return data


def sortF(data):
    data.children = sorted(
        data.children, key=lambda space: space.area, reverse=True)
    for nr, n in enumerate(data.children):
        if type(n) == room:
            pass
        elif type(n) == space:
            n = sortF(n)
            data.children[nr] = n
    return data


def middle(rec):
    return (rec['dx'] / 2.0 + rec['x'], rec['dy'] / 2.0 + rec['y'])


def drawRec(nr, rec, data, ax):
    colr = hsv_to_rgb((random.random(), .7, .9))
    ax.add_patch(Rectangle((rec['x'], rec['y']),
                           rec['dx'], rec['dy'], color=colr))
    x, y = middle(rec)
    ax.text(x, y, data.children[nr].name, ha='center', va='center', size=10,
            color=colr)


def findAll(data, x, y, width, height, c=True):
    values = []
    names = []
    colors = []
    for child in data.children:
        values.append(child.getArea())
        names.append((str(child.nr).rstrip('.0'), child.name))
        if not c:
            colors.append('none')
    if c:
        c = False
    values = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(values, x, y, width, height)
    for nr, child in enumerate(data.children):
        if type(child) == space:
            print(child.name)
            tempRects, tempNames, tempCol = findAll(child,
                                                    rects[nr]['x'],
                                                    rects[nr]['y'],
                                                    rects[nr]['dx'],
                                                    rects[nr]['dy'],
                                                    c)
            rects += tempRects
            names += tempNames
            colors += tempCol
    return rects, names, colors


def printPlot(rects, names, colors, width, height, pltSize=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('equal')
    plt.axis('off')
    if pltSize:
        plt.xlim(pltSize[0])
        plt.ylim(pltSize[1])
    else:
        plt.xlim((-1, width))
        plt.ylim((-1, height))

    for nr, rec in enumerate(rects):
        ax.add_patch(Rectangle((rec['x'], rec['y']), rec['dx'], rec['dy'],
                               edgecolor=(.1, .1, .1),
                               linewidth=.2,
                               facecolor=colors[nr]))
        x, y = middle(rec)
        ax.text(x, y, names[nr][1], ha='center',
                va='center', size=2, alpha=.5, rotation=0)
#    plt.show()
    n = 0
    while True:
        if 'cad_areas2dxf-{:03d}.png'.format(n) in os.listdir():
            n += 1
        else:
            plt.savefig('cad_areas2dxf-{:03d}.png'.format(n),
                        dpi=600,
                        orienttion='landscape', papertype='a2')
            break
    plt.close()


def createDxf(rects, names, colors):
    n = 0
    while True:
        if 'cad_areas2dxf-{:03d}.dxf'.format(n) in os.listdir():
            n += 1
        else:
            dwg = dxf.drawing('cad_areas2dxf-{:03d}.dxf'.format(n))
            break
    dwg.add_layer('WYDZIALY', color=2)
    dwg.add_layer('PODWYDZIALY', color=3)
    dwg.add_layer('POMIESZCZENIA', color=16)
    dwg.add_layer('OPISY')
    print('cad open')
    roomCol = 0
    for nr, rec in enumerate(rects):
        flag = dxf.block(name='Area' + str(nr))
        flag.add(dxf.polyline([(0, 0),
                               (rec['dx'], 0),
                               (rec['dx'], rec['dy']),
                               (0, rec['dy']),
                               (0, 0)],
                              layer='0',
                              color=0))
        flag.add(dxf.attdef(insert=(rec['dx'] / 2, rec['dy'] / 2 + .1),
                            tag='NR',
                            height=.1,
                            layer='0',
                            halign=CENTER, valign=MIDDLE, color=0))
        flag.add(dxf.attdef(insert=(rec['dx'] / 2, rec['dy'] / 2),
                            tag='NAME',
                            height=.1,
                            layer='0',
                            halign=CENTER, valign=MIDDLE, color=0))
        flag.add(dxf.attdef(insert=(rec['dx'] / 2, rec['dy'] / 2 - .1),
                            tag='POW',
                            height=.1,
                            layer='0',
                            halign=CENTER, valign=MIDDLE, color=0))
        # flag.add(dxf.text(names[nr],
        #                   height=.1,
        #                   halign=CENTER,
        #                   valign=MIDDLE,
        #                   alignpoint=(rec['dx']/2, rec['dy']/2),
        #                   layer='0', color=0))
        dwg.blocks.add(flag)
        powierzchnia = str(round(rec['dx'] * rec['dy'], 2))
        if names[nr][0].count('.') == 0:
            lay = 'WYDZIALY'
            attNr = names[nr][0]
            roomCol += 10
        elif names[nr][0].count('.') == 1:
            lay = 'PODWYDZIALY'
            attNr = ''
        else:
            lay = 'POMIESZCZENIA'
            attNr = names[nr][0].split('.')
            attNr = '.'.join(attNr[::2])
        dwg.add(dxf.insert2(blockdef=flag, insert=(rec['x'], rec['y']),
                            attribs={'NR': attNr, 'NAME': names[
                                nr][1], 'POW': powierzchnia},
                            xscale=1,
                            yscale=1,
                            layer=lay,
                            rotation=0,
                            color=10))
    dwg.save()
    print('done')


def main(data, condition=True):
    #    goldenFix = 1.618
    area = sum([x.area for x in data.children])
    width = 4.60
    # height = sqrt(area)
    height = 21
    x, y = 0, 0
    colors = [hsv_to_rgb((random.random(), .7, .9))
              for col in range(len(data.children))]
    for n in range(15, int(sqrt(area))):
        # print(n, end=' | ')
        # height = n
        width = area / height
        rects, names, cols = findAll(data, x, y, width, height)
        colors += cols
        if condition:
            pltSize = [[-1, width + 1], [-1, int(sqrt(area)) + 1]]
            condition = False
        printPlot(rects, names, colors, width, height)
        plt.close()
        createDxf(rects, names, colors)
        break
    return rects, names, area, width, height


def printAll(rects, names):
    for nr, r in enumerate(rects):
        # print(round(r['dx'] * r['dy'], 0), end='   ')
        print(round(r['dx'] * r['dy'], 0))
        print(names[nr])


print('start.')
wb = xlrd.open_workbook(os.path.join('input_data', 'program.xls'))
sh = wb.sheet_by_index(0)
print('importing data...')
data = importData(sh)
print('sorting...')
data = sortF(data)
print('created data.')

rects, names, area, width, height = main(data)
print('all done')
# printAll(rects,names)
