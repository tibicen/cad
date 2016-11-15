# -*- coding: utf-8 -*-
import datetime
import os
import sys
from multiprocessing import Pool

import ezdxf

WORK_DIR = 'C:\\test'
FILES_DWG = ['BSH-LAB_QMT-PW-A.dwg']
FILES_DWG = sys.argv[1:] if len(sys.argv) > 1 else FILES_DWG
ACAD_PATH = None


def find_acad():
    global ACAD_PATH
    if ACAD_PATH:
        return ACAD_PATH
    for p, d, f in os.walk('c:\\'):
        if 'acad.exe' in f:
            ACAD_PATH = p + '\\acad.exe'
            return (p + '\\acad.exe')
        if 'acadlt.exe' in f:
            ACAD_PATH = p + '\\acadlt.exe'
            return (p + '\\acadlt.exe')


def openDrawning(FILE):
    if FILE.endswith('dwg'):
        if FILE.rstrip('dwg') + 'dxf' not in os.listdir():
            createDXF(FILE)
        return ezdxf.readfile(FILE.rstrip('dwg') + 'dxf')
    elif FILE.endswith('dxf'):
        return ezdxf.readfile(FILE)


def createScript(FILE):
    # SCRIPT = 'FILEDIA\n0\nPURGE\nA\n*\nN\nAUDIT\nY\nSAVEAS\nDXF\n16\n' + \
    #     os.path.join(os.getcwd(), FILE.rstrip('dwg') + 'dxf') + "\nQUIT"
    SCRIPT = 'FILEDIA\n0\nSAVEAS\nDXF\n16\n' + \
        os.path.join(os.getcwd(), FILE.rstrip('dwg') + 'dxf') + "\nQUIT\n\n"
    tmpDWG = open('SCRIPT.scr', 'w')
    tmpDWG.write(SCRIPT)
    tmpDWG.close()


def runDWG(FILE, AcadExePath):
    tmpDir = os.getcwd()
    os.chdir(os.path.split(AcadExePath)[0])
    os.system(os.path.split(AcadExePath)[1] + ' "' + os.path.join(
        tmpDir, FILE) + '" /nologo /nossm /b "' + os.path.join(
        tmpDir, 'SCRIPT.scr') + '"')
    os.chdir(tmpDir)
    os.remove('SCRIPT.scr')


def createDXF(FILE):
    print('creating dxf for ', FILE)
    AcadExePath = find_acad()
    createScript(FILE)
    if FILE.rstrip('dwg') + 'dxf' in os.listdir():
        os.remove(FILE.rstrip('dwg') + 'dxf')
    runDWG(FILE, AcadExePath)
    os.remove(FILE.rstrip('dwg') + 'bak')


def job(z):
    nr, FILE, RYSUNKI = z
    createDXF(FILE)
    print('opening ', FILE.rstrip('dwg') + 'dxf')
    dxf = ezdxf.readfile(FILE.rstrip('dwg') + 'dxf')
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
    os.remove(FILE.rstrip('dwg') + 'dxf')


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


def sum_all_areas():
    dxf = ezdxf.readfile('C:\\test\\bb.dxf')
    texts = dxf.entities.query('MTEXT')
    texts = [x for x in texts if x.dxf.layer == 'R2_POWIERZCHNIE']
    l4 = [x for x in texts if x.dxf.insert[0] > 40000]


def areas2xls4dabki():
    files = []
    l = len(os.listdir())
    for nr, f in enumerate(os.listdir()):
        if f.endswith('.dwg'):
            files.append(openDrawning(f))
            print('\rOpening files... remains {:>2}'.format(l - nr), end='')
    print('\r')
    metki = []
    for dxf in files:
        tmp_metki = dxf.entities.query('INSERT[name=="METKA2"]')
        metki += list(tmp_metki)
    metki = sorted(metki, key=lambda x: x.get_attrib_text('NR'))
    today = datetime.date.today().isoformat()
    f = open('DĄBKI ZESTAWIENIE POWIERZCHNI {}.csv'.format(today),
             'w', encoding='utf-8')
    for nr, m in enumerate(metki):
        float_error = False
        NR = m.get_attrib_text('NR')
        try:
            POW = float(m.get_attrib_text('POW').replace(',', '.'))
        except(ValueError):
            POW = m.get_attrib_text('POW').replace(',', '.')
            float_error = True
        NAZWA = m.get_attrib_text('NAZWA_POM')
        if not float_error:
            print('{},\t{:>6.2f}m2,\t{}'.format(NR, POW, NAZWA))
            f.write("{},{:.2f},{}\n".format(NR, POW, NAZWA))
        else:
            print('{},\t{}m2,\t{}'.format(NR, POW, NAZWA))
            f.write("{},{},{}\n".format(NR, POW, NAZWA))
    f.close()


if __name__ == '__main__':
    os.chdir(WORK_DIR)
    # areas2xls4dabki()
