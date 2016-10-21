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


ACAD_EXE_PATH = 'c:\Program Files\Autodesk\AutoCAD LT 2012 - English\acadlt.exe'
ACAD_EXE_PATH = False
FILE_DWG = ''
SCRIPT_PATH = ''
SCRIPT = '''FILEDIA
0
PURGE
A
*
N
AUDIT
Y
SAVEAS
2004
C:\test.dwg
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
    os.chdir(FILE_DWG.rsplit('\\', 1)[0])
    tmpDWG = open('SCRIPT.scr', 'w')
    tmpDWG.write(SCRIPT)
    tmpDWG.close()


def runDWG(FILE_DWG, ACAD_EXE_PATH):
    os.system(ACAD_EXE_PATH.rsplit('\\', 1)[1] + ' ' +
              FILE_DWG.rsplit('\\', 1)[1] +
              '/nologo /nossm /b "' +
              FILE_DWG.rsplit('\\', 1)[0] + '\\SCRIPT.scr"')
    os.chdir(ACAD_EXE_PATH.rsplit('\\', 1)[0])
    os.remove('SCRIPT.scr')


if __name__ == '__main__':
    if ACAD_EXE_PATH == False:
        ACAD_EXE_PATH = findACAD()
        a = open('AutoACAD.py', 'r+')
        b = open('test.py', 'w')
        newtext = ''
        lines = a.readlines()
        for n in lines:
            if n.startswith('ACAD_EXE_PATH'):
                n = "ACAD_EXE_PATH = '" + ACAD_EXE_PATH + "'\n"
            newtext += n

        b.write(newtext)
        b.close()
        a.close()
