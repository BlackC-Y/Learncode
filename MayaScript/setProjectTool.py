# -*- coding: UTF-8 -*-
from maya import cmds, mel
import maya.OpenMaya as Om
import os
import re


class setProjectTool():

    #Ver = 1.2  # 在maya文件夹中创建一个ProjectList文件

    def __init__(self):
        self.filePath = os.path.expanduser("~") + '/maya/ProjectList'

    def setProjectUi(self):
        Ui = 'setProject'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        cmds.window(Ui, t=Ui, rtf=1, mb=1, mxb=0, wh=(350, 50))
        cmds.columnLayout(cat=('both', 2), rs=3, cw=350)
        cmds.text('ProjectText', h=18, l=cmds.workspace(q=1, dir=1, rd=1))
        cmds.optionMenu('ProjectList', l='ProjectPath')
        cmds.button(h=24, l='Set', c=lambda *args: self.setPath())
        cmds.popupMenu()
        cmds.menuItem(l='Add Project', c=lambda *args: self.refreshList('add'))
        cmds.menuItem(l='Delete Path', c=lambda *args: self.refreshList('delete'))
        cmds.showWindow(Ui)
        self.refreshList(None)

    def setPath(self):
        Path = cmds.optionMenu('ProjectList', q=1, v=1).strip()
        if Path == '----------':
            return
        mel.eval('setProject \"%s\";print "Finish!"' % Path)
        cmds.text('ProjectText', e=1, l=Path)

    def refreshList(self, mode):
        if mode == 'add':
            if cmds.promptDialog(t='PojectPath', m='eg: C:/xxx/xxx', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
                newPath = cmds.promptDialog(q=1, t=1).replace('\\', '/')
                if not newPath:
                    return
                if newPath == '----------':
                    pass
                elif not os.path.exists(newPath):
                    Om.MGlobal.displayError(u'路径不存在! - Path not exist!')
                    return
                elif not re.match('.:/\S', newPath) and not re.match('//\S', newPath):
                    Om.MGlobal.displayError('Path is wrong!')
                    return
                with open(self.filePath, 'a') as listFile:
                    listFile.write(newPath + ';')
            self.refreshList(None)
        elif mode == 'delete':
            dPath = cmds.optionMenu('ProjectList', q=1, v=1)
            with open(self.filePath, 'r') as listFile:
                allPath = listFile.readline().split(';')
            with open(self.filePath, 'w') as listFile:
                for i in allPath:
                    if i and i != dPath:
                        listFile.write(i + ';')
            self.refreshList(None)
        else:
            oldList = cmds.optionMenu('ProjectList', q=1, ill=1)
            if oldList:
                for i in oldList:
                    cmds.deleteUI(i)
            with open(self.filePath, 'r') as listFile:
                allPath = listFile.readline().split(';')
                for i in allPath[:-1]:
                    if os.path.exists(i) or i == '----------':
                        cmds.menuItem(p='ProjectList', l=i)
                    else:
                        cmds.menuItem(p='ProjectList', l='%s - not exist' % i)


setProjectTool().setProjectUi()
