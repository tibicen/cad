import os
import sys
from multiprocessing import Pool

import ezdxf

FILES_DWG = ['BSH-LAB_QMT-PW-A.dwg']
FILES_DWG = sys.argv[1:] if len(sys.argv) > 1 else FILES_DWG


def find():
    for p, d, f in os.walk('c:\\'):
        if 'acad.exe' in f:
            print(p + '\\acad.exe')
            return (p + '\\acad.exe')
        if 'acadlt.exe' in f:
            print(p + '\\acadlt.exe')
            return (p + '\\acadlt.exe')


def createScript(FILE_DWG):
    if FILE_DWG.rstrip('dwg') + 'dxf' in os.listdir():
        QUIT = '\nY\nQUIT\nY\n'
    else:
        QUIT = '\nQUIT\nY\n'
    SCRIPT = 'FILEDIA\n0\nPURGE\nA\n*\nN\nAUDIT\nY\nSAVEAS\nDXF\n16\n' + \
        os.path.join(os.getcwd(), FILE_DWG.rstrip('dwg') + 'dxf') + QUIT
    SCRIPT = 'FILEDIA\n0\nSAVEAS\nDXF\n16\n' + \
        os.path.join(os.getcwd(), FILE_DWG.rstrip('dwg') + 'dxf') + QUIT
    tmpDWG = open('SCRIPT.scr', 'w')
    tmpDWG.write(SCRIPT)
    tmpDWG.close()


def runDWG(FILE_DWG, AcadExePath):
    tmpDir = os.getcwd()
    os.chdir(os.path.split(AcadExePath)[0])
    os.system(os.path.split(AcadExePath)[1] + ' "' + os.path.join(
        tmpDir, FILE_DWG) + '" /nologo /nossm /b "' + os.path.join(
        tmpDir, 'SCRIPT.scr') + '"')
    os.chdir(tmpDir)
    os.remove('SCRIPT.scr')


def createDXF(FILE_DWG, SCRIPT):
    print('creating dxf for ', FILE_DWG)
    AcadExePath = find()
    createScript(FILE_DWG)
    runDWG(FILE_DWG, AcadExePath)


def job(z):
    nr, FILE_DWG, RYSUNKI = z
    createDXF(FILE_DWG)
    print('opening ', FILE_DWG.rstrip('dwg') + 'dxf')
    dxf = ezdxf.readfile(FILE_DWG.rstrip('dwg') + 'dxf')
    tabelki = dxf.entities.query('INSERT[name=="TABELKA"]')
    for tab in tabelki:
        NR = tab.get_attrib_text('NR_RYSUNKI')
        SKALA = tab.get_attrib_text('SKALA')
        NAZWA = ''
        for attr in tab.attribs():
            if attr.dxf.tag.startswith('NAZWA_RYSUNKU'):
                NAZWA += attr.dxf.text + ' '
        RYSUNKI.append((NR, SKALA, NAZWA.rstrip(' ')))
        print("'{}','{}','{}'".format((NR, SKALA, NAZWA.rstrip(' '))))
    os.remove(FILE_DWG.rstrip('dwg') + 'dxf')


def main():
    RYSUNKI = []
    pool = Pool()
    z = zip(range(len(FILES_DWG)), FILES_DWG, [
            RYSUNKI for x in range(len(FILES_DWG))])
    for t in pool.imap(job, z):
        pass
    for rys in RYSUNKI:
        print("'{}','{}','{}'".format(*rys))
    return RYSUNKI

if __name__ == '__main__':
    RYSUNKI = main()
