# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 00:38:48 2013

@author: Dawid Huczyński
"""
import os

'''
This is just info for acad.exe functions:
/b           Script name (b stands for batch process)
/c           Configuration folder
/ld	        ARX or DBX application
/nohardware  Disables hardware acceleration
/nolisp	   Disables AutoLISP execution (2013 SP1.1)
/nologo	   No product logo screen
/nossm       No Sheet Set Manager window
/p	        User-defined registry profile for starting the program
/pl	        Background plotting/publishing prints off the drawings listed in a DSD file created with Publish
/r	        Default system pointing device
/s           Support folders
/set	        Sheet set
/t	        Template file name
/v	        View name
/w	        Default workspace
/automation – used with programming automation
/layout – loads a layout with the specified drawing

'''

# SCRIPT = '''FILEDIA
# 0
# PURGE
# A
# *
# N
# AUDIT
# Y
# SAVEAS
# 2004
# C:\test.dwg
# Y
# QUIT
#
# '''

ACAD_EXE_PATH = False
WDIR = '\\\\R2srv\\projekty\\DĄBKI\\PROJEKT\\PB\\WYDANIA\\170607-BUD HOTELOWE DLA PPOŻ'
SCRIPT = '''FILEDIA
0
-LAYER
OFF
A-WYBURZENIA

FIND
SAVEAS
2007

Y
QUIT

'''


def findACAD():
    for p, d, f in os.walk('c:\\'):
        if 'acad.exe' in f:
            print(p + '\\acad.exe')
            return (p + '\\acad.exe')
        if 'acadlt.exe' in f:
            print(p + '\\acadlt.exe')
            return (p + '\\acadlt.exe')


def createScript(SCRIPT, FILE_DWG):
    tmpDWG = open('SCRIPT.scr', 'w')
    tmpDWG.write(SCRIPT)
    tmpDWG.close()


def runDWG(FILE_DWG, ACAD_EXE_PATH, WDIR):
    path, cad = ACAD_EXE_PATH.rsplit('\\', 1)
    os.chdir(path)
    print(FILE_DWG)
    # print(cad + ' "' +
    #       os.path.join(WDIR, FILE_DWG) +
    #       '" /nologo /nossm /b "' +
    #       os.path.join(WDIR, 'SCRIPT.scr') + '"')
    os.system(cad + ' "' +
              os.path.join(WDIR, FILE_DWG) +
              '" /nologo /nossm /b "' +
              os.path.join(WDIR, 'SCRIPT.scr') + '"')
    os.chdir(WDIR)
    os.remove('SCRIPT.scr')


if __name__ == '__main__':
    if ACAD_EXE_PATH is False:
        ACAD_EXE_PATH = findACAD()
    os.chdir(WDIR)
    for f in os.listdir(WDIR):
        if f.endswith('.dwg') and not f.endswith('-P.dwg'):
            # print(f)
            createScript(SCRIPT, os.path.join(WDIR, f))
            runDWG(f, ACAD_EXE_PATH, WDIR)
