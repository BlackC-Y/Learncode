import os
import re

def initrun():
    path = "C:/Program Files/Autodesk/Maya2018/devkit/other/pymel/extras/completion/py/maya/cmds/__init__.py"
    with open(path) as rfile:
        line = rfile.readline()
        allLine = []
        addLine = allLine.append
        while line:
            rers = re.findall('def \S*\\(', line)
            if not rers:
                line = rfile.readline()
                continue
            addLine(rers[0].split(' ')[1][:-1])
            line = rfile.readline()
    with open('D:/迅雷下载/line.txt', 'w') as of:
        for i in allLine:
            of.write('%s\n' %i)

def modulerun():
    path = "C:/Users/Black/.vscode/extensions/fxtd-odyssey.mayapy-1.0.4/mayaSDK/maya/cmds/"
    filelist = ['Animation.py', 'Effects.py', 'General.py', 'Language.py', 'Modeling.py', 'Rendering.py', 'System.py', 'Windows.py',]
    allLine = []
    addLine = allLine.append
    for i in filelist:
        with open(path + i) as rfile:
            line = rfile.readline()
            while line:
                rers = re.findall('def \S*\\(', line)
                if not rers:
                    line = rfile.readline()
                    continue
                addLine(rers[0].split(' ')[1][:-1])
                line = rfile.readline()
        print(i)
    with open('D:/迅雷下载/modline.txt', 'w') as of:
        for i in allLine:
            of.write('%s\n' % i)

def cmdsduibi():
    path1 = "D:/迅雷下载/line.txt"
    path2 = "D:/迅雷下载/modline.txt"
    allLine1 = []
    allLine2 = []
    with open(path1) as rfile:
        line = rfile.readline()
        while line:
            allLine1.append(line)
            line = rfile.readline()
    with open(path2) as rfile:
        line = rfile.readline()
        while line:
            allLine2.append(line)
            line = rfile.readline()
    with open('D:/迅雷下载/line2.txt', 'w') as of:
        for i in list(set(allLine1).difference(set(allLine2))):
            of.write('%s' % i)

cmdsduibi()