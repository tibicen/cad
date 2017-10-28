# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:21:23 2013

@author: Dawid Huczyński
"""
import os
import re

text = open(os.path.join('input_data', 'ACIdata.txt'), 'r')
lista = [x for x in text.readlines()]
ACItoRGB = {}
for n, v in enumerate(lista[1::2]):
    S = re.findall('\((\d+), (\d+), (\d+)\)', v)[0]
    T = (int(S[0]), int(S[1]), int(S[2]))
    ACItoRGB[T] = n


print(ACItoRGB)
s = 'data = ' + str(ACItoRGB)
f = open(os.path.join('input_data', 'dict_RGB.py'), 'w')
f.write(s)
f.close()
