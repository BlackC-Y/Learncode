# -*- coding: UTF-8 -*-
from .pyside import QtWidgets, shiboken

from maya import cmds, mel
#from maya import OpenMaya as Om, OpenMayaAnim as OmAni
from maya.api import OpenMaya as om, OpenMayaAnim as omAni

import json
import time
import decimal

from BbBBToolBox.deps import pyperclip

from .DisplayYes import *
from .Utils import BoxQtStyle, Functions


class PointWeightTool_BbBB():

    def ToolUi(self):
        Ver = '1.08'
        self.ToolUi = 'PointWeightTool_BbBB'
        if cmds.window(self.ToolUi, q=1, ex=1):
            cmds.deleteUI(self.ToolUi)
        cmds.window(self.ToolUi, t='PointWeightTool %s' %Ver, rtf=1, mb=1, tlb=1, wh=(230, 500))
        cmds.columnLayout('FiristcL_BbBB', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.text('spJobchangeVtx_BbBB', p='FiristcL_BbBB', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', lambda *args: self.refreshBoxChange(None)], p='spJobchangeVtx_BbBB')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh_BbBB', i='refresh.png', w=20, h=20, onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.popupMenu()
        cmds.menuItem('OFFmeunItem_BbBB', l='OFF', cb=0)
        cmds.textField('searchText_BbBB', h=22, tcc=lambda *args: self.refreshJointList(1, cmds.textField('searchText_BbBB', q=1, tx=1)))
        # cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_BbBB', e=1, h=cmds.treeView('JointTV_BbBB', q=1, h=1) + 20))
        # cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_BbBB', e=1, h=cmds.treeView('JointTV_BbBB', q=1, h=1) - 20))
        # invertSelection.png
        cmds.iconTextButton(i='invertSelection.png', w=20, h=20, c=self.reSelect)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout('JointTVLayout_BbBB')
        cmds.treeView('JointTV_BbBB', nb=1, adr=0, h=100, idc=lambda text:pyperclip.copy(text), scc=self._weightView, pc=(1, self.lock_unLock))
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem_BbBB', l='Hierarchy', rb=1, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('AImeunItem_BbBB', l='Alphabetically', rb=0, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('FImeunItem_BbBB', l='Filter Zero', cb=0, c=lambda *args: self.refreshJointList(1))
        #cmds.menuItem(l='Select Vtx', c=lambda *args: self.slVtx())
        cmds.formLayout('JointTVLayout_BbBB', e=1, af=[('JointTV_BbBB', 'top', 0), ('JointTV_BbBB', 'bottom', 0),
                                                            ('JointTV_BbBB', 'left', 3), ('JointTV_BbBB', 'right', 3)])
        cmds.setParent('..')
        cmds.columnLayout(cat=('both', 2), rs=2, cw=225)
        cmds.rowLayout(nc=4, cw4=(50, 50, 50, 65))
        cmds.floatField('weighrfloat_BbBB', w=52, h=26, pre=4, min=0, max=1,
                        ec=lambda *args: self.editVtxWeight(cmds.floatField('weighrfloat_BbBB', q=1, v=1)))
        cmds.button(w=50, h=26, l='Copy', c=lambda *args: self.copyVtxWeight())
        cmds.button(w=50, h=26, l='Paste', c=lambda *args: self.pasteVtxWeight())
        cmds.popupMenu()
        cmds.menuItem(l='PasteAll', c=lambda *args: mel.eval("polyConvertToShell;artAttrSkinWeightPaste;"))
        cmds.button(w=65, h=26, l='Hammer', c=lambda *args: (mel.eval('weightHammerVerts'), self.refreshJointList(0)))
        cmds.setParent('..')
        cmds.rowLayout(nc=5, cw5=(43, 43, 43, 43, 43))
        cmds.button(w=43, h=26, l='Loop', c=lambda *args: cmds.polySelectSp(loop=1))
        cmds.button(w=43, h=26, l='Ring', c=lambda *args: mel.eval("PolySelectConvert 2;PolySelectTraverse 2;polySelectEdges edgeRing;PolySelectConvert 3;"))
        cmds.button(w=43, h=26, l='Shell', c=lambda *args: mel.eval("polyConvertToShell"))
        cmds.button(w=43, h=26, l='Shrink', c=lambda *args: cmds.polySelectConstraint(pp=2))
        cmds.button(w=43, h=26, l='Grow', c=lambda *args: cmds.polySelectConstraint(pp=1))
        cmds.setParent('..')
        cmds.rowLayout(nc=7, cw=[(1, 30), (2, 30), (3, 30), (4, 30), (5, 30), (6, 30), (7, 30)])
        cmds.button(w=30, h=26, l='0', c=lambda *args: self.editVtxWeight(0))
        cmds.button(w=30, h=26, l='.1', c=lambda *args: self.editVtxWeight(.1))
        cmds.button(w=30, h=26, l='.25', c=lambda *args: self.editVtxWeight(.25))
        cmds.button(w=30, h=26, l='.5', c=lambda *args: self.editVtxWeight(.5))
        cmds.button(w=30, h=26, l='.75', c=lambda *args: self.editVtxWeight(.75))
        cmds.button(w=30, h=26, l='.9', c=lambda *args: self.editVtxWeight(.9))
        cmds.button(w=30, h=26, l='1', c=lambda *args: self.editVtxWeight(1))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='A/S Weight', w=80)
        cmds.floatField('ASFloat_BbBB', v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c=lambda *args: self.editVtxWeight('+'))
        cmds.button(w=38, h=26, l='-', c=lambda *args: self.editVtxWeight('-'))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='M/D Weight', w=80)
        cmds.floatField('MDFloat_BbBB', v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c=lambda *args: self.editVtxWeight('*'))
        cmds.button(w=38, h=26, l='/', c=lambda *args: self.editVtxWeight('/'))
        cmds.setParent('..')

        cmds.showWindow(self.ToolUi)
        self.saveData = ['', []]

    def spJobStart(self):
        if cmds.text('spJobVtxParent_BbBB', q=1, ex=1):
            return
        cmds.text('spJobVtxParent_BbBB', p='FiristcL_BbBB', vis=0)
        cmds.scriptJob(e=['Undo', lambda *args: self.refreshJointList(0)], p='spJobVtxParent_BbBB')
        cmds.scriptJob(e=['SelectionChanged', lambda *args: self.refreshJointList(0)], p='spJobVtxParent_BbBB')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent_BbBB')
        cmds.scriptJob(uid=['PointWeightTool_BbBB', lambda *args: self.refreshBoxChange(9)])

        PaintSkinCmd = '"ArtPaintSkinWeightsToolOptions;"'
        if int(cmds.about(v=1)) > 2017:
            edgeCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"edge\\\", 0);")'
            vertexCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"vertex\\\", 0);")'
            faceCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"facet\\\", 0);")'
            objModeCmd = '"maintainActiveChangeSelectMode time1 0;"'  # python (\\\"PointWeightTool_BbBB().refreshBoxChange(9)\\\");
        else:
            #2017以下兼容
            edgeCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"edge\\\");")'
            vertexCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"vertex\\\");")'
            faceCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"facet\\\");")'
            objModeCmd = '"changeSelectMode -component;changeSelectMode -object;"'
        #string $selCmd + PointWeightTool_BbBB()._weightView()
        mel.eval(
            'global proc dagMenuProc(string $parent, string $object){ \
            if(!size($object)){ \
            string $lsList[] = `ls -sl -o`; if(!size($lsList)){return;} else{$object = $lsList[0];}} \
            if(objectType($object) == "joint"){ \
            string $selCmd = "python(\\\"cmds.treeView(\'JointTV_BbBB\', e=1, cs=1);cmds.treeView(\'JointTV_BbBB\', e=1, si=(\'" + $object + "\', 1));\\\")"; \
            menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
            }else{ \
            menuItem -l "Paint Skin Weights Tool" -ec true -c %s -rp "NW" -p $parent; \
            menuItem -l "Vertex" -ec true -c %s -rp "W" -p $parent; \
            menuItem -l "Edge" -ec true -c %s -rp "N" -p $parent; \
            menuItem -l "Face" -ec true -c %s -rp "S" -p $parent; \
            menuItem -l "Object Mode" -ec true -c %s -rp "NE" -p $parent;}}'
            %(PaintSkinCmd, vertexCmd, edgeCmd, faceCmd, objModeCmd)
        )

    def refreshBoxChange(self, force):
        if force == 9 or cmds.menuItem('OFFmeunItem_BbBB', q=1, cb=1):
            if cmds.text('spJobVtxParent_BbBB', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent_BbBB', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            if cmds.window('PointWeightTool_BbBB', q=1, ex=1):
                cmds.iconTextCheckBox('refresh_BbBB', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh_BbBB', e=1, v=1)
            self.refreshJointList(0)
        #PointWeightTool_BbBB().refreshBoxChange(9)   #报绿脚本兼容

    def refreshJointList(self, refresh, search=''):
        seltyp = 0 if cmds.selectType(q=1, ocm=1, pv=1) or cmds.selectType(q=1, ocm=1, lp=1) or cmds.selectType(q=1, ocm=1, cv=1) else 1
        if seltyp:
            self.refreshBoxChange(9)
            return
        sel = cmds.ls(sl=1, fl=1)
        # ▽ copy权重后会触发刷新, 列表中的第一个可能是shape节点, 所以过滤一下mesh, 但是感觉可能会出现一些问题?
        #    点的Type也是mesh, 如果出问题可能在这.
        errorsel = cmds.ls(sl=1, typ=('transform', 'mesh'))
        if not sel or errorsel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            self.refreshBoxChange(9)
            return
        self.tempcluster = clusterName
        jointList = cmds.skinCluster(selobj, q=1, inf=1)  # cmds.skinCluster(selobj, q=1, wi=1)
        siItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        _zero = cmds.menuItem('FImeunItem_BbBB', q=1, cb=1)
        if refresh or _zero or self.saveData[0] != clusterName or self.saveData[1] != jointList or not cmds.treeView('JointTV_BbBB', q=1, ch=''):
            cmds.treeView('JointTV_BbBB', e=1, ra=1)
            if search:
                text = cmds.textField('searchText_BbBB', q=1, tx=1)
                getList = [i for i in jointList if text in i]
                if getList:
                    jointList = getList
            jointList.sort()
            _jointList = []
            _valueList = []
            for i in jointList:
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=10**-15, q=1, t=i)
                if _zero:
                    if float(Value):
                        _jointList.append(i)
                        _valueList.append(Value)
                else:
                    _jointList.append(i)
                    _valueList.append(Value)
            for j, v in zip(_jointList, _valueList):
                if cmds.menuItem('HImeunItem_BbBB', q=1, rb=1):
                    self.addHItoList(j, _jointList)
                else:
                    cmds.treeView('JointTV_BbBB', e=1, ai=[j, ''])
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                if not cmds.treeView('JointTV_BbBB', q=1, dls=1):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, ''))
                if float(v):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, '   |   %s' % v))
            if siItem:
                allItem = cmds.treeView('JointTV_BbBB', q=1, ch='')
                _Temp_ = list(set(siItem).intersection(set(allItem)))  # 求并集
                for i in _Temp_:
                    cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))
        else:
            allItem = cmds.treeView('JointTV_BbBB', q=1, ch='')
            for j in allItem:
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=10**-15, q=1, t=j)
                if not cmds.treeView('JointTV_BbBB', q=1, dls=1):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, ''))
                if not float(Value):
                    continue
                cmds.treeView('JointTV_BbBB', e=1, dls=(j, '   |   %s' % Value))
        self.saveData = [clusterName, jointList]

    def addHItoList(self, i, jointList):
        jointP = cmds.listRelatives(i, p=1)
        if not jointP:
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, ''])
        elif cmds.treeView('JointTV_BbBB', q=1, iex=jointP[0]):
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, jointP[0]])
        elif jointP[0] in jointList:
            self.addHItoList(jointP[0], jointList)
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, jointP[0]])
        else:
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, ''])

    def lock_unLock(self, jnt, but):
        slItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not slItem or len(slItem) == 1:
            slItem = [jnt]
        if cmds.getAttr(jnt + '.liw'):
            for i in slItem:
                cmds.setAttr(i + '.liw', 0)
                cmds.treeView('JointTV_BbBB', e=1, i=(i, 1, 'Lock_OFF_grey.png'))
        else:
            for i in slItem:
                cmds.setAttr(i + '.liw', 1)
                cmds.treeView('JointTV_BbBB', e=1, i=(i, 1, 'Lock_ON.png'))

    def reSelect(self):
        allItem = cmds.treeView('JointTV_BbBB', q=1, iv=1)
        slItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not allItem or not slItem:
            return
        cmds.treeView('JointTV_BbBB', e=1, cs=1)
        _Temp_ = list(set(allItem).difference(set(slItem)))  # 求差集 a有b没有
        for i in _Temp_:
            cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))

    def editVtxWeight(self, mode):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        if not selVtx:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            return
        sljntList = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not sljntList:
            om.MGlobal.displayError(u'未选择骨骼')
            return
        if mode == '+' or mode == '-':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=10**-15, q=1, t=j)
                    Value = Value + cmds.floatField('ASFloat_BbBB', q=1, v=1)   \
                        if mode == '+' else Value - cmds.floatField('ASFloat_BbBB', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        elif mode == '*' or mode == '/':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=10**-15, q=1, t=j)
                    Value = Value * cmds.floatField('MDFloat_BbBB', q=1, v=1)   \
                        if mode == '*' else Value / cmds.floatField('MDFloat_BbBB', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        else:
            for v in selVtx:
                tvList = [(j, float(mode)) for j in sljntList]
                cmds.skinPercent(clusterName, v, tv=tvList)
        siItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        self.refreshJointList(0)
        for i in siItem:
            cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))

    def slVtx(self):
        slJnt = cmds.treeView('JointTV_BbBB', q=1, si=1)
        vtxList = []
        for i in slJnt:
            cmds.skinCluster(self.tempcluster, e=1, siv=i)
            vtxList.append(cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46]))
        cmds.select(vtxList, r=1)

    def _weightView(self):
        if cmds.iconTextCheckBox('refresh_BbBB', q=1, v=1):
            treesl = cmds.treeView('JointTV_BbBB', q=1, si=1)
            if treesl:
                #cmds.hilite(treesl[0], r=1)
                if cmds.currentCtx() == 'artAttrSkinContext':
                    mel.eval('setSmoothSkinInfluence "%s";' %treesl[0])
                sel = cmds.ls(sl=1, fl=1)
                if sel:
                    selobj = cmds.ls(sl=1, o=1)[0]
                    clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
                    cmds.floatField('weighrfloat_BbBB', e=1, v=cmds.skinPercent(clusterName, sel[0], ib=0.0001, q=1, t=treesl[0]))

    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError(u'未选择点')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return
        mel.eval('artAttrSkinWeightCopy;')
        ValueList = cmds.skinPercent(clusterName, selVtx, q=1, ib=10**-15, v=1)
        TransList = cmds.skinPercent(clusterName, selVtx, q=1, ib=10**-15, t=None)
        '''   #倒序循环
        for i in range(len(ValueList)-1, -1, -1):
            if ValueList[i] < .0001:
                del ValueList[i], TransList[i]
        '''
        self.vtxWeightInfo = [clusterName, TransList, ValueList]
        # print(self.vtxWeightInfo)

    def pasteVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError(u'未选择点')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selObj)
        if not clusterName:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return
        if clusterName != self.vtxWeightInfo[0]:
            jointList = cmds.skinCluster(selObj, q=1, inf=1)
            for j in self.vtxWeightInfo[1]:
                if not j in jointList:
                    om.MGlobal.displayError(u'两个物体的蒙皮骨骼不一样！')
                    return
        tvList = [(self.vtxWeightInfo[1][i], self.vtxWeightInfo[2][i]) for i in range(len(self.vtxWeightInfo[1]))]
        # print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=1, tv=%s)' % (clusterName, i, tvList))
        self.refreshJointList(0)


class WeightSL_BbBB():

    def SLcheck(self, mode):   #单独调用时filePath为列表
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError(u'什么都没选诶 这我很难办啊')
            return
        selobj = cmds.ls(sl=1, o=1)
        if mode == 'Load' and len(selobj) > 1:
            om.MGlobal.displayError(u'只能选择一个物体')
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        skCluster = mel.eval('findRelatedSkinCluster("%s")' %selobj[0])
        if not skCluster:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return
        if not selVtx:   #选的是整个物体
            seltyp = cmds.objectType(cmds.listRelatives(selobj[0], s=1, f=1)[0])
            if seltyp == 'mesh':                                                                                    #整个mesh
                if mode == 'Save':
                    filePath = cmds.fileDialog2(ff='Xml (*.xml)', ds=2) #['%s/%s.xml' %(allInPath, selobj[0])]
                    if filePath:
                        self.vtxSave_dW(filePath)
                else:
                    filePath = cmds.fileDialog2(ff='File (*.xml *.Weight)', ds=2, fm=1)
                    if filePath:
                        if filePath[0].rsplit('.', 1)[1] == 'xml':
                            self.vtxLoad_dW(filePath)
                        elif filePath[0].rsplit('.', 1)[1] == 'Weight':
                            self.vtxLoad_api(filePath)
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface' or seltyp == 'subdiv' or seltyp == 'lattice':   #整个其他
                if mode == 'Save':
                    filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                    if filePath:
                        self.vtxSave_Mel(filePath)
                else:
                    filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                    if filePath:
                        self.vtxLoad_Mel(filePath)
            else:
                om.MGlobal.displayError(u'选择的物体不支持')
                return
        elif cmds.filterExpand(sel, sm=[31]):                                                                        #mesh点
            if mode == 'Save':
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                if filePath:
                    self.vtxSave_api(filePath)
            else:
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                if filePath:
                    self.vtxLoad_api(filePath)
        elif cmds.filterExpand(sel, sm=[28, 36, 40, 46]):                                                            #其他点
            if mode == 'Save':
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                if filePath:
                    self.vtxSave_Mel(filePath)
            else:
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                if filePath:
                    self.vtxLoad_Mel(filePath)
        else:
            om.MGlobal.displayError(u'选择的点不支持')
            return

    def vtxSave_Mel(self, filePath=''):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46])
        if not selVtx:
            seltyp = cmds.objectType(cmds.listRelatives(selobj, s=1, f=1)[0])
            if seltyp == 'mesh':
                suf = '.vtx'
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface':
                suf = '.cv'
            elif seltyp == 'subdiv':
                suf = '.smp'
            elif seltyp == 'lattice':
                suf = '.pt'
            selVtx = cmds.ls('%s%s[*]' % (selobj, suf), fl=1)
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        
        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
        with open(filePath[0], 'w') as vwfile:
            jsonData = {'Data':[]}
            for i in selVtx:
                valueList = cmds.skinPercent(skCluster, i, ib=10**-15, q=1, v=1)
                transList = cmds.skinPercent(skCluster, i, ib=10**-15, q=1, t=None)
                allWeight = 0
                for w in range(len(valueList)):
                    valueList[w] = round(valueList[w], 4)
                    allWeight += valueList[w]
                valueList[-1] += (1.0 - allWeight)
                jsonData['Data'].append([i.split('.')[-1], [[transList[u], valueList[u]] for u in range(len(valueList))]])
            json.dump(jsonData, vwfile)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    def vtxLoad_Mel(self, filePath='', selectpoint=0):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)

        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
        with open(filePath[0], 'r') as vwfile:
            readData = json.load(vwfile)
            if selectpoint:
                selVtx = [i.split('.', 1)[-1] for i in cmds.ls(sl=1, fl=1)]
            num = 0
            for i in readData['Data']:
                if selectpoint:
                    if i[0] != selVtx[num]:
                        continue
                    num += 1
                exec('cmds.skinPercent("%s", "%s.%s", tv=%s, nrm=1)' %(skCluster, selobj, i[0], i[1]))
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    ''' 有报错 仅参考
    def vtxSave_Oapi(self, filePath=''):
        st = time.time()
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        #_prselList = []
        #selList.getSelectionStrings(_prselList)   #获取 MSelectionList 内容
        #print _prselList
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容
        slMIt = Om.MItSelectionList(selList)
        MItDagPath = Om.MDagPath()
        MItcomponent = Om.MObject()
        slMIt.getDagPath(MItDagPath, MItcomponent)

        #_selType = MDagPath.apiType()
        MDagPath.extendToShape()  # 获取当前物体的shape节点
        _selShapeType = MDagPath.apiType()
        if _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294:
            suf = 'cv'
        elif _selShapeType == 279:
            suf = 'pt'

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        #connectNode = cmds.listHistory(MDagPath.partialPathName(), il=1, pdo=1)
        # if not connectNode:
        #    Om.MGlobal.displayError('Select No Skin')
        #    return
        # for skCluster in connectNode:
        #    if cmds.nodeType(skCluster) == 'skinCluster':
        #        break
        #    if skCluster == connectNode[-1]:
        #        return
        Om.MGlobal.getSelectionListByName(skCluster, selList)
        skinObj = Om.MObject()
        selList.getDependNode(1, skinObj)
        skinNode = OmAni.MFnSkinCluster(skinObj)
        infs = Om.MDagPathArray()
        numInfs = skinNode.influenceObjects(infs)
        infNameList = []  # 骨骼列表
        for i in range(numInfs):
            infName = infs[i].partialPathName()
            infNameList.append(infName)
        # fn = Om.MFnDependencyNode(MDagPath.node())   #获取MDagPath的内容?
        # print fn.name()   #获取 MFnDependencyNode 内容

        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
        # component组件不为空（点）,线和面会强制转为点
        if MItcomponent.isNull():   #有报错
            vertIter = om.MItMeshVertex(MObject)
        else:
            vertIter = om.MItMeshVertex(MItDagPath, MItcomponent)

        with open(filePath[0], 'w') as vwfile:
            jsonData = {'Data':[]}
            while not vertIter.isDone():
                infCount = Om.MScriptUtil()
                infCountPtr = infCount.asUintPtr()
                Om.MScriptUtil.setUint(infCountPtr, 0)
                weights = Om.MDoubleArray()
                skinNode.getWeights(MDagPath, vertIter.currentItem(), weights, infCountPtr)

                tvList = self.zeroWeightData_Save(weights, infNameList)
                jsonData['Data'].append(['%s[%s]' %(suf, vertIter.index()), tvList])
                vertIter.next()
            json.dump(jsonData, vwfile)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))
    '''
    '''
    def vtxLoad_Oapi(self, filePath=''):
        st = time.time()
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        Om.MGlobal.getSelectionListByName(skCluster, selList)
        skinObj = Om.MObject()
        selList.getDependNode(1, skinObj)
        skinNode = OmAni.MFnSkinCluster(skinObj)
        infs = Om.MDagPathArray()
        numInfs = skinNode.influenceObjects(infs)
        infNameList = []  # 骨骼列表
        for i in range(numInfs):
            infName = infs[i].partialPathName()
            infNameList.append(infName)
        # fn = Om.MFnDependencyNode(MDagPath.node())   #获取MDagPath的内容?
        # print fn.name()   #获取 MFnDependencyNode 内容
        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)

        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
        readData = self.readWeightData_Load(filePath[0])
        _Num = 0
        vertIter = Om.MItGeometry(MObject)
        while not vertIter.isDone():
            if vertIter.index() != readData[_Num][0]:
                vertIter.next()
                continue
            jntindex = Om.MIntArray()
            weights = Om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i, w in zip(readData[_Num][1], readData[_Num][2]):
                jntindexapp(infNameList.index(i))
                weightsapp(w)
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, True)
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))
    '''

    def vtxSave_api(self, filePath=''):
        st = time.time()
        selList = om.MGlobal.getActiveSelectionList()
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表
        slMIt = om.MItSelectionList(selList)
        MItDagPath, MItcomponent = slMIt.getComponent()

        #_selType = MDagPath.apiType()
        #_selShapeType = MDagPath.extendToShape().apiType()
        #if not _selType in set([110, 296, 267, 294, 279, ]):
        #    return
        
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
        # component组件不为空（点）,线和面会强制转为点
        vertIter = om.MItMeshVertex(MObject) if MItcomponent.isNull() else om.MItMeshVertex(MItDagPath, MItcomponent)
        Aobject = True if MItcomponent.isNull() else False
        with open(filePath[0], 'w') as vwfile:
            jsonData = {'Data':[]}
            while not vertIter.isDone():
                weights = skinNode.getWeights(MDagPath, vertIter.currentItem())[0]

                tvList = self.zeroWeightData_Save(weights, infNameList, source=Aobject)
                jsonData['Data'].append(['vtx[%s]' %vertIter.index(), tvList])
                vertIter.next()
            json.dump(jsonData, vwfile)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    def vtxLoad_api(self, filePath=''):
        st = time.time()
        selList = om.MGlobal.getActiveSelectionList()
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表

        #_selType = MDagPath.apiType()
        #_selShapeType = MDagPath.extendToShape().apiType()
        
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表
        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        
        if not filePath:
            filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
        readData = self.readWeightData_Load(filePath[0])
        _Num = 0
        vertIter = om.MItMeshVertex(MObject)
        while not vertIter.isDone():
            if vertIter.index() != readData[_Num][0]:
                vertIter.next()
                continue
            jntindex = om.MIntArray()
            weights = om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i, w in zip(readData[_Num][1], readData[_Num][2]):
                jntindexapp(infNameList.index(i))
                weightsapp(w)
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, True)
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    def vtxSave_dW(self, filePath=''):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        
        if not filePath:
            filePath = cmds.fileDialog2(ff='Xml (*.xml)', ds=2)
        fileANDPath = filePath[0].rsplit('\\', 1) if '\\' in filePath else filePath[0].rsplit('/', 1)
        #attribute = ['envelope', 'skinningMethod', 'normalizeWeights', 'deformUserNormals', 'useComponents']
        cmds.deformerWeights(fileANDPath[1], path=fileANDPath[0], deformer=[skCluster], ex=1, vc=1, wp=6, dv=-1.0)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    def vtxLoad_dW(self, filePath=''):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)

        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        
        if not filePath:
            filePath = cmds.fileDialog2(ff='Xml (*.xml)', ds=2, fm=1)
        fileANDPath = filePath[0].rsplit('\\', 1) if '\\' in filePath else filePath[0].rsplit('/', 1)
        cmds.deformerWeights(fileANDPath[1], path=fileANDPath[0], deformer=[skCluster], im=1, method='index', ws=1)   #"index", "nearest", "barycentric", "bilinear", "over"
        cmds.skinCluster([skCluster], e=1, forceNormalizeWeights=1)

        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage(u'处理完成! 用时: %s秒' %(time.time()-st))

    def zeroWeightData_Save(self, weights, infNameList, source=False):
        #去除0权重数据, source为True则输出源数据
        if source:
            return [[i, w] for i, w in zip(infNameList, weights)]
        allWeight = 0
        transList = []
        valueList = []
        _jLappend = transList.append
        _wLappend = valueList.append
        for i, w in zip(infNameList, weights):
            _tempweight = round(w, 4)
            if _tempweight:
                _jLappend(i)
                _wLappend(_tempweight)
            allWeight += _tempweight
        valueList[0] += (1.0 - allWeight)
        return [[i, w] for i, w in zip(transList, valueList)]

    def readWeightData_Load(self, path):
        with open(path, 'r') as vwfile:
            readData = json.load(vwfile)
            for i in readData:
                i[0] = int(i[0].split('[', 1)[-1][:1])
            readData.append([-1, None, None])
        return readData


class WeightCheckTool_BbBB():

    def ToolUi(self, layout=0):
        self.UiName = 'WeightCheckTool_Ui'

        Setting_CheckDefaultMode = Functions.readSetting(self.UiName, "CheckDefaultMode")
        if not Setting_CheckDefaultMode:
            Setting_CheckDefaultMode = 1
        
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        if not layout:
            cmds.window(self.UiName, t='WeightCheckTool', rtf=1, tlb=1, wh=(165, 350), bgc=BoxQtStyle.backgroundMayaColor, cc=lambda *args: self.saveSettings())
            cmds.columnLayout(cat=('left', 3), h=300, w=140, rs=2)
        else:
            cmds.rowColumnLayout(nr=4, cs=((1, 2), (2, 2)), rs=((2, 2), (3, 2)))

        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'加载', w=80, c=lambda *args: self.Load()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'清理', w=80, c=lambda *args: self.Clean()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'选择', w=80, c=lambda *args: self.selectVtx()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.text(l='', h=1)
        cmds.radioCollection()
        cmds.radioButton('%s_DecimalText' %self.UiName, l=u'小数点精度', h=22)
        cmds.intField('%s_DecimalInt' %self.UiName, w=80, h=24, v=3)
        cmds.radioButton('%s_InfluenceText' %self.UiName, l=u'骨骼影响值', h=22)
        cmds.intField('%s_InfluenceInt' %self.UiName, w=80, h=24, v=4)
        if Setting_CheckDefaultMode == 0:
            cmds.radioButton('%s_DecimalText' %self.UiName, e=1, sl=1)
        else:
            cmds.radioButton('%s_InfluenceText' %self.UiName, e=1, sl=1)
        #cmds.radioCollection(e=1, sl=_intField[Setting_CheckDefaultMode])
        cmds.text(l='', h=20)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'列出结果', w=80, c=lambda *args: showCheckResult()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.progressBar('%s_progressBar' %self.UiName, h=26, w=150, vis=0)
        self.saveObj = ''

        def showCheckResult():
            resultUiName = '%s_Result' %self.UiName
            if cmds.window(resultUiName, q=1, ex=1):
                cmds.deleteUI(resultUiName)
            if not self.saveObj or not self.BadList:
                om.MGlobal.displayWarning(u'没有问题点')
                return
            cmds.window(resultUiName, t='result', rtf=1, tlb=1)
            cmds.rowLayout(nc=2, adj=2, rat=((1, 'both', 2), (2, 'both', 2)))
            cmds.textScrollList('%s_vtxList' %self.UiName, ams=1, w=100, 
                                sc=lambda *args: cmds.textScrollList('%s_weightList' %self.UiName, e=1, da=1, sii=cmds.textScrollList('%s_vtxList' %self.UiName, q=1, sii=1)))
            cmds.textScrollList('%s_weightList' %self.UiName, ams=1, 
                                sc=lambda *args: cmds.textScrollList('%s_vtxList' %self.UiName, e=1, da=1, sii=cmds.textScrollList('%s_weightList' %self.UiName, q=1, sii=1)))
            if self.BadList:
                clusterName = mel.eval('findRelatedSkinCluster("%s")' % self.saveObj)
                for i in self.BadList:
                    valueList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, v=1)
                    transList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, t=None)
                    tvStr = ''
                    for w, j in zip(valueList, transList):
                        tvStr += '%s ~ %s @ ' % (j, w)
                    cmds.textScrollList('%s_vtxList' %self.UiName, e=1, a=i.split('.')[1])
                    cmds.textScrollList('%s_weightList' %self.UiName, e=1, a=tvStr)
                cmds.textScrollList('%s_vtxList' %self.UiName, e=1, si=[i.split('.')[1] for i in self.BadList])
                cmds.textScrollList('%s_weightList' %self.UiName, e=1, sii=cmds.textScrollList('%s_vtxList' %self.UiName, q=1, sii=1))
            cmds.showWindow(resultUiName)
        
        if not layout:
            cmds.showWindow(self.UiName)
        
    def saveSettings(self):
        data = 0 if cmds.radioButton('%s_DecimalText' %self.UiName, q=1, sl=1) else 1
        Functions.editSetting(self.UiName, "CheckDefaultMode", data)

    def getSel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError(u'什么都没选')
            return None, None
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        selobj = cmds.ls(sl=1, o=1)[0]
        self.saveObj = selobj
        if not selVtx:
            if not selobj:
                return None, None
            seltyp = cmds.objectType(cmds.listRelatives(selobj, s=1, f=1)[0])
            if seltyp == 'mesh':
                suf = '.vtx'
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface':
                suf = '.cv'
            elif seltyp == 'subdiv':
                suf = '.smp'
            elif seltyp == 'lattice':
                suf = '.pt'
            selVtx = cmds.ls('%s%s[*]' % (selobj, suf), fl=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return None, None
        return selVtx, clusterName

    def Load(self, mode=0):
        cmds.radioButton('%s_DecimalText' %self.UiName, e=1, l=u'小数点精度')
        cmds.radioButton('%s_InfluenceText' %self.UiName, e=1, l=u'骨骼影响值')
        cmds.progressBar('%s_progressBar' %self.UiName, e=1, vis=0)
        #listVis = 0 if cmds.button('%s_unfold' %self.UiName, q=1, l=1) == '>' else 1
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        
        self.BadList = []
        self.LoadInfo = 0
        if cmds.radioButton('%s_InfluenceText' %self.UiName, q=1, sl=1):
            self.LoadInfo = 1   #Influence
            maxValue = cmds.intField('%s_InfluenceInt' %self.UiName, q=1, v=1)
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, v=1)
                #transList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, t=None)
                if len(valueList) > maxValue:
                    self.BadList.append(i)
                    continue
            if self.BadList:
                cmds.radioButton('%s_InfluenceText' %self.UiName, e=1, l=u'超影响值的数量: %s' %len(self.BadList))
        else:
            self.LoadInfo = 2   #Decimal
            maxValue = cmds.intField('%s_DecimalInt' %self.UiName, q=1, v=1) + 2   #加上0.两位
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, v=1)
                #transList = cmds.skinPercent(clusterName, i, ib=10**-15, q=1, t=None)
                for w in valueList:
                    _num = '%.15f' %w
                    if len(_num.rstrip('0')) > maxValue:
                        self.BadList.append(i)
                        break
            if self.BadList:
                cmds.radioButton('%s_DecimalText' %self.UiName, e=1, l=u'超小数点的数量: %s' %len(self.BadList))

    def Clean(self):
        if cmds.radioButton('%s_InfluenceText' %self.UiName, q=1, sl=1):
            if cmds.ls(sl=1, o=1)[0] == self.saveObj and self.LoadInfo == 1:
                self.RemoveInfluence()
            else:
                self.Load(1)   #不刷新界面
                self.RemoveInfluence()
        else:
            if cmds.ls(sl=1, o=1)[0] == self.saveObj and self.LoadInfo == 2:
                self.CleanDecimal()
            else:
                self.Load(1)   #不刷新界面
                self.CleanDecimal()

    def selectVtx(self):
        if not self.BadList:
            return
        _shapeN = self.saveObj
        cmds.hilite(_shapeN)
        cmds.select(self.BadList, r=1)

    def CleanDecimal(self):
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % self.saveObj)
        if not self.BadList:
            om.MGlobal.displayInfo(u'没有需要清理的顶点')
            return
        if not clusterName:
            return
        cmds.progressBar('%s_progressBar' %self.UiName, e=1, pr=0, vis=1)
        jntList = cmds.skinCluster(self.saveObj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        
        _decimalInt = cmds.intField('%s_DecimalInt' %self.UiName, q=1, v=1)
        cmds.skinPercent(clusterName, prw=10**-_decimalInt)   #生成小数点后10**-n位
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        _decimalStr = "{:.%sf}" %_decimalInt
        _decimal = decimal.Decimal(_decimalStr.format(1))
        _decimal1 = decimal.Decimal('1.0')
        oneinAll = len(self.BadList)/100.0
        progressNum = 0
        for index, item in enumerate(self.BadList):
            transList = cmds.skinPercent(clusterName, item, ib=10**-15, q=1, t=None)
            _tv = []
            allValue = 0
            for j in transList:
                # mel.eval('global proc float _rounding(float $f, int $n){float $N = pow(10, ($n));float $a = $f%(1/$N)*$N;float $B;     \
                #            if($a>0.5)$B = ceil($f*$N)/$N;else$B = floor($f*$N/$N);return $B;}')     #精度问题?
                #Value = mel.eval('_rounding(%s, %s)' %(cmds.skinPercent(clusterName, i, ib=10**-15, q=1, t=j), cmds.intField('DecimalInt', q=1, v=1)))
                Value = decimal.Decimal(str(cmds.skinPercent(clusterName, item, ib=10**-15, q=1, t=j))).quantize(_decimal)
                if Value == 1:
                    _tv.append([j, 1])
                    break
                if Value == 0:
                    continue
                allValue += Value
                _tv.append([j, round(float(Value), _decimalInt)])
            _tv[-1][1] = round(float(decimal.Decimal(str(_tv[-1][1])) + _decimal1 - allValue), _decimalInt)
            cmds.skinPercent(clusterName, item, tv=_tv, nrm=1)
            if index/oneinAll > progressNum:
                cmds.progressBar('%s_progressBar' %self.UiName, e=1, s=1)
                progressNum += 1
        cmds.progressBar('%s_progressBar' %self.UiName, e=1, vis=0)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveInfluence(self):
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % self.saveObj)
        if not self.BadList:
            om.MGlobal.displayInfo(u'没有需要清理的顶点')
            return
        if not clusterName:
            return
        cmds.progressBar('%s_progressBar' %self.UiName, e=1, pr=0, vis=1)
        jntList = cmds.skinCluster(self.saveObj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)

        Influence = cmds.intField('%s_InfluenceInt' %self.UiName, q=1, v=1)
        oneinAll = len(self.BadList)/100.0
        progressNum = 0
        for index, item in enumerate(self.BadList):
            transList = cmds.skinPercent(clusterName, item, ib=10**-15, q=1, t=None)
            while len(transList) > Influence:
                valueList = cmds.skinPercent(clusterName, item, ib=10**-15, q=1, v=1)
                tvdic = {}
                for w, j in zip(valueList, transList):
                    tvdic[j] = w
                tvList = sorted(tvdic.items(), key=lambda item: item[1])
                cmds.skinPercent(clusterName, item, tv=(tvList[0][0], 0), nrm=1)
                transList = cmds.skinPercent(clusterName, item, ib=10**-15, q=1, t=None)
            if index/oneinAll > progressNum:
                cmds.progressBar('%s_progressBar' %self.UiName, e=1, s=1)
                progressNum += 1
        cmds.progressBar('%s_progressBar' %self.UiName, e=1, vis=0)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()


class CopyWeightTool_BbBB():

    def ToolUi(self, layout=0):
        self.ComponentData = {'source':'', 'targe':''}
        Ver = 1.43
        self.UiName = 'CopyWeightTool_Ui'
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        if not layout:
            cmds.window(self.UiName, t='%s %s' %(self.UiName, Ver), rtf=1, mb=1, tlb=1, wh=(300, 85), bgc=BoxQtStyle.backgroundMayaColor)
        cmds.columnLayout(cat=('both', 5), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('%s_sourceText' %self.UiName, l=u'源', bl='Select', h=26, adj=2, ed=0, cw3=[30, 200, 60], bc=lambda *args: select(1))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.ComponentData['source'], r=1))
        cmds.textFieldButtonGrp('%s_targeText' %self.UiName, l=u'目标', bl='Select', h=26, adj=2, ed=0, cw3=[30, 200, 60], bc=lambda *args: select(0))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.ComponentData['targe'], r=1))
        cmds.checkBox('%s_oneToOneAttr' %self.UiName, l=u'使用一对一标签 (源和目标的蒙皮骨骼基本一致时)', h=25, v=1)
        cmds.rowLayout(nc=3)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(cmds.button(l='Help', w=50, c=lambda *args: showHelp()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=24))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(cmds.button(l='Run', w=255, c=lambda *args: self.checkProc()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=24))
        cmds.setParent('..')
        
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl('%s_sourceText' %self.UiName)), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=24))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl('%s_targeText' %self.UiName)), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=24))
        

        def showHelp():
            helpUiName = '%s_Help' %self.UiName
            if cmds.window(helpUiName, q=1, ex=1):
                cmds.deleteUI(helpUiName)
            cmds.window(helpUiName, t='Help', rtf=1, tlb=1)
            cmds.columnLayout(cat=('both', 2), rs=2, adj=1)
            cmds.text(l=u'源：整个模型 - 模型的点/线/面\n\n目标: 源模型的点/线/面\n     单个有蒙皮模型的点/线/面\n     多个无蒙皮模型\n     单个无蒙皮Surface曲面模型\n', 
                        al='left', fn='fixedWidthFont')
            cmds.showWindow(helpUiName)

        def select(type):
            if type:
                self.ComponentData['source'] = lsList = cmds.ls(sl=1)
                cmds.textFieldButtonGrp('%s_sourceText' %self.UiName, e=1, tx=str(lsList))
            else:
                self.ComponentData['targe'] = lsList = cmds.ls(sl=1)
                cmds.textFieldButtonGrp('%s_targeText' %self.UiName, e=1, tx=str(lsList))
        if not layout:
            cmds.showWindow(self.UiName)
    
    def checkProc(self):
        if not self.ComponentData['source'] or not self.ComponentData['targe']:
            if len(cmds.ls(sl=1)) == 2:
                self.selectProc()
            else:
                return
        else:
            self.runProc()

    def selectProc(self):
        sllist = cmds.ls(sl=1)
        copyAttr = ('oneToOne', 'closestJoint') if cmds.checkBox('%s_oneToOneAttr' %self.UiName, q=1, v=1) else 'closestJoint'
        soureSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %sllist[0])
        if not soureSkinCluster:
            cmds.error(u'源模型没得蒙皮呀')
        infJointList = cmds.skinCluster(sllist[0], q=1, inf=1)
        jntLock = [cmds.getAttr('%s.liw' %j) for j in infJointList]
        targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' % sllist[1])
        if not targeSkinCluster:
            targeSkinCluster = cmds.skinCluster(infJointList, sllist[1], tsb=1, mi=cmds.getAttr('%s.maxInfluences' % soureSkinCluster), dr=4)[0]
        cmds.copySkinWeights(ss=soureSkinCluster, ds=targeSkinCluster, nm=1, sa='closestPoint', ia=copyAttr, nr=1, sm=1)
        for j, l in zip(infJointList, jntLock):
            cmds.setAttr('%s.liw' %j, l)

    def runProc(self):
        sourelist = cmds.ls(self.ComponentData['source'], fl=1)
        targelist = cmds.ls(self.ComponentData['targe'], fl=1)
        soureObj = cmds.ls(sourelist, o=1)[0]
        targeObj = cmds.ls(targelist, o=1)
        isExtract = 0
        isComponent = 0
        copyAttr = ('oneToOne', 'closestJoint') if cmds.checkBox('%s_oneToOneAttr' %self.UiName, q=1, v=1) else 'closestJoint'
        #源
        if not cmds.objectType(soureObj, i='transform'):   #是点线面
            isExtract = 1   #为点线面时提取
            soureObj = cmds.listRelatives(soureObj, p=1)[0]
        elif sourelist[0] == soureObj:   #是整个模型
            isExtract = 0
        #目标
        if not cmds.objectType(targeObj[0], i='transform'):   #目标选的是点线面
            isComponent = 1
            targeObj = cmds.listRelatives(targeObj[0], p=1)

        isExtract = 1 if soureObj == targeObj[0] else 0   #目标和源为相同模型 需要提取
        
        soureSkinCluster = mel.eval('findRelatedSkinCluster("%s")' % soureObj)
        if not soureSkinCluster:
            cmds.error(u'源模型没得蒙皮呀')
        sourelist = cmds.ls(cmds.polyListComponentConversion(sourelist, ff=1, fv=1, fe=1, fuv=1, fvf=1, tf=1), fl=1)
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)   #所有骨骼
        jntLock = [cmds.getAttr('%s.liw' %j) for j in infJointList]

        if isExtract:   #需要提取
            _TempObj_ = cmds.duplicate(soureObj, rr=1)[0]
            #allList = ['%s.f[%s]' % (soureObj, i) for i in range(cmds.polyEvaluate(_TempObj_, f=1))]
            _difflist_ = set(cmds.ls('%s.f[*]' %soureObj, fl=1)).difference(set(sourelist))
            _list_ = [i.replace(soureObj, _TempObj_) for i in _difflist_]
            if cmds.ls(_list_):
                cmds.delete(_list_)
            cmds.skinCluster(infJointList, _TempObj_, tsb=1, dr=4)
            cmds.copySkinWeights(soureObj, _TempObj_, nm=1, sa='closestPoint', ia='oneToOne', nr=1)
            soureObj = _TempObj_

        if cmds.listRelatives(targeObj, c=1, s=1, typ='nurbsSurface'):
            self.SurfaceCWeight(soureObj, targeObj[0], copyAttr)
        else:
            if isComponent:
                targelist = cmds.ls(cmds.polyListComponentConversion(targelist, ff=1, fv=1, fe=1, fuv=1, fvf=1, tv=1), fl=1)
                cmds.copySkinWeights(soureObj, targelist, nm=1, sa='closestPoint', ia=copyAttr, nr=1, sm=1)
            else:
                for i in targeObj:
                    targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' % i)
                    if not targeSkinCluster:
                        targeSkinCluster = cmds.skinCluster(infJointList, i, tsb=1, mi=cmds.getAttr('%s.maxInfluences' % soureSkinCluster), dr=4)[0]
                    cmds.copySkinWeights(ss=soureSkinCluster, ds=targeSkinCluster, nm=1, sa='closestPoint', ia=copyAttr, nr=1, sm=1)
        if isExtract:
            cmds.delete(_TempObj_)
        for j, l in zip(infJointList, jntLock):
            cmds.setAttr('%s.liw' %j, l)
        DisplayYes().showMessage(u'处理完成!')

    def SurfaceCWeight(self, soureObj, targeObj, copyAttr):
        _StPObj = cmds.nurbsToPoly(targeObj, mnd=1, ch=0, f=3, n='__TempStP_Obj')[0]
        targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %targeObj)
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)
        cmds.skinCluster(infJointList, _StPObj, tsb=1, dr=4)
        cmds.copySkinWeights(soureObj, _StPObj, nm=1, sa='closestPoint', ia=copyAttr, nr=1)
        StpSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %_StPObj)
        if not targeSkinCluster:
            cmds.skinCluster(infJointList, targeObj, tsb=1, dr=4)
            targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %targeObj)
        
        _cPOMNode = cmds.createNode('closestPointOnMesh', n='__TempcPOM_Node')
        cmds.connectAttr('%s.worldMesh[0]' %cmds.listRelatives(_StPObj, s=1, c=1)[0], '%s.inMesh' %_cPOMNode, f=1)
        for i in cmds.ls('%s.cv[*][*]' %targeObj, fl=1):
            cvTrans = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr('%s.inPosition' %_cPOMNode, cvTrans[0], cvTrans[1], cvTrans[2])
            vtxIndex = cmds.getAttr('%s.vt' %_cPOMNode)
            valueList = cmds.skinPercent(StpSkinCluster, '%s.vtx[%s]' %(_StPObj, vtxIndex), q=1, ib=.000000001, v=1)
            transList = cmds.skinPercent(StpSkinCluster, '%s.vtx[%s]' %(_StPObj, vtxIndex), q=1, ib=.000000001, t=None)
            exec('cmds.skinPercent("%s", "%s", tv=%s)' % (targeSkinCluster, i, [[t, v] for t, v in zip(transList, valueList)]))
        cmds.delete(_StPObj, _cPOMNode)


class softSelectWeightTool_BbBB():

    def ToolUi(self):
        self.Ui = 'TestT_Ui'
        if cmds.window(self.Ui, q=1, ex=1):
            cmds.deleteUI(self.Ui)
        cmds.window(self.Ui, t='%s' %(self.Ui), rtf=1, mb=1, tlb=1, wh=(290, 85))
        cmds.columnLayout(cat=('both', 2), rs=2, cw=290)

        cmds.text(l=u'软选择创建次级骨骼')
        cmds.rowLayout(nc=3)
        cmds.button(l=u'软选择创建新骨骼', w=100, c=lambda *args: self.softSelectCreateJoint())
        cmds.button(l=u'软选择加选现有骨骼', w=115, c=lambda *args: self.softSelectCreateJoint('selJoint'))
        cmds.button(l=u'+0.05权重', w=70, c=lambda *args: self.softSelectCreateJoint('add'))
        cmds.setParent('..')
        cmds.text(l=u'记录一个骨骼权重规律 在新骨骼和范围中重现')
        cmds.rowLayout(nc=2)
        cmds.button(l=u'选择现有模型骨骼', w=135, c=lambda *args: self.getWeightToEquation())
        cmds.button(l=u'软选择加选现有骨骼', w=150, c=lambda *args: self.setWeightFromEquation())
        cmds.showWindow(self.Ui)

    def check_numpyPackge(self):
        _ver = int(cmds.about(v=1))
        if _ver < 2022:
            try:
                from BbBBToolBox.deps import numpy27 as np
                return 27
            except ImportError as e:
                raise ImportError(u'没找到适用于py2的numpy包')
        else:   #22 3.7.7 | 23 3.9.7
            try:
                import numpy as np
            except ImportError as e:
                raise ImportError(u'没找到适用于Maya%s的numpy包' %_ver)
    
    def getWeightToEquation(self):
        """
        选取模型和骨骼 获取权重公式
        """
        index = self.check_numpyPackge()
        if index == 27:
            from BbBBToolBox.deps import numpy27 as np
        else:
            import numpy as np
        selApiList = om.MGlobal.getActiveSelectionList()
        if selApiList.length() != 2:
            om.MGlobal.displayError(u'需要先选模型再选骨骼')
            return
        objDagPath = selApiList.getDagPath(0)
        #objObject = selApiList.getDependNode(0)
        jointDagPath = selApiList.getDagPath(1)

        skCluster = mel.eval('findRelatedSkinCluster("%s")' %objDagPath.partialPathName())
        selApiList.add(skCluster)
        skinObj = selApiList.getDependNode(2)
        skinNode = omAni.MFnSkinCluster(skinObj)
        vtxSelList, weightList = skinNode.getPointsAffectedByInfluence(jointDagPath)

        #列表排序方法
        #weightList, vtxSelList = zip(*sorted(zip(weightList, cmds.ls(vtxSelList.getSelectionStrings(), fl=1)), reverse=True))
        dataRange = WeightUtils_BbBB.reRange(weightList, 0, 1, 0, max(weightList))
        
        xAxis = np.array(dataRange)
        yAxis = np.array(weightList)
        self.weightEquation = np.polynomial.polynomial.Polynomial.fit(xAxis, yAxis, 3)
        #print(self.weightEquation(1), self.weightEquation(.5), self.weightEquation(.3333)) 

    def setWeightFromEquation(self):
        """
        软选择点加选骨骼 根据权重公式赋予权重
        """
        if self.weightEquation:
            selList = cmds.ls(sl=1, fl=1)
            selobj = cmds.ls(sl=1, o=1)[0]
            clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
            if not clusterName:
                return
            
            IndexList, weightList = WeightUtils_BbBB.getSoftSelectData()
            newJoint = selList[1]
            for index, weight in zip(IndexList, weightList):
                cmds.skinPercent(clusterName, '%s.vtx[%s]'%(selobj, index), tv=[newJoint, self.weightEquation(weight)])

    def softSelectCreateJoint(self, mode=None):
        """
        软选择点创建新骨骼分权重
        - mode: None创建新的骨骼分权重 | selJoint记录选择的骨骼 | add在之前记录的骨骼上添加权重
        """
        selList = cmds.ls(sl=1, fl=1)
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            return
        
        IndexList, weightList = WeightUtils_BbBB.getSoftSelectData()
        if mode == 'add':
            newJoint = self.creatNewData[0]
            if not newJoint:
                om.MGlobal.displayError(u'没有记录骨骼')
                return
            scaleValue = 0.05
            for index, weight in zip(IndexList, weightList):
                cmds.skinPercent(clusterName, '%s.vtx[%s]'%(selobj, index), tv=
                    [newJoint, weight * scaleValue + cmds.skinPercent(clusterName, '%s.vtx[%s]'%(selobj, index), q=1, t=newJoint)])
            return
        elif mode == 'selJoint':
            newJoint = selList[1]
        else:
            cmds.select(cl=1)
            newJoint = cmds.joint(p=cmds.xform(selList[0], q=1, ws=1, t=1), n='oneNewJoint')
            cmds.skinCluster(clusterName, e=1, dr=4, lw=1, wt=0, ai=newJoint)
        scaleValue = 0.1
        for index, weight in zip(IndexList, weightList):
            cmds.skinPercent(clusterName, '%s.vtx[%s]'%(selobj, index), tv=[newJoint, weight * scaleValue])
        self.creatNewData = [newJoint]


class WeightUtils_BbBB():

    @staticmethod
    def reRange(dataList, to_min, to_max, minNow, maxNow):
        """
        重映射范围
        - dataList: 需要映射的列表
        - to_min: 要映射到的最小值
        - to_max: 要映射到的最大值
        - minNow: 现有数据最小值
        - maxNow: 现有数据最大值
        """
        return [to_min + ((to_max - to_min) / (maxNow - minNow)) * i - minNow for i in dataList]

    @staticmethod
    def getSoftSelectData():
        """
        获取软选择的组件和权重值
        """
        softSel = om.MGlobal.getRichSelection()
        selApiList = softSel.getSelection()
        MDagPth, MComponent = selApiList.getComponent(0)
        fnComp = om.MFnSingleIndexedComponent(MComponent)
        return list(fnComp.getElements()), [fnComp.weight(i).influence for i in range(fnComp.elementCount)]
               #IndexList, weightList
        '''
        selection = Om.MSelectionList()
        softSelection = Om.MRichSelection()
        Om.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)
        pathDag = Om.MDagPath()
        oComp = Om.MObject()
        selection.getDagPath(0, pathDag, oComp)
        fnComp = Om.MFnSingleIndexedComponent(oComp)
        for i in range(fnComp.elementCount()):
            print(fnComp.element(i), fnComp.weight(i).influence())
        '''

    @staticmethod
    def resetSkinPose():
        for obj in cmds.ls(sl=1):
            clusterName = mel.eval('findRelatedSkinCluster("%s")' % obj)
            if not clusterName:
                continue
            sk_matrix = '%s.matrix' %clusterName
            mx_num = cmds.getAttr(sk_matrix, mi=1)
            infs = cmds.listConnections(sk_matrix, s=1, d=0, scn=1)
            if not infs:
                continue
            for n in mx_num:
                inf = cmds.listConnections('%s[%d]' % (sk_matrix, n), s=1, d=0, scn=1)
                if not inf:
                    continue
                matrix = cmds.getAttr('%s.worldInverseMatrix[0]' %inf[0])
                cmds.setAttr('%s.pm[%d]' %(clusterName, n), matrix, typ='matrix')
                cmds.dagPose(inf[0], rs=1, n=cmds.listConnections('%s.bp' %clusterName, s=1, d=0, scn=1)[0])


#PointWeightTool_BbBB().ToolUi()
#WeightCheckTool_BbBB().ToolUi()
#CopyWeightTool_BbBB().ToolUi()
