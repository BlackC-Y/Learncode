# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om

import os
import math
import shutil
import hashlib
import threading
import subprocess
from typing import NamedTuple   #py3.6
#from collections import namedtuple
from dataclasses import dataclass, field  #py3.7

import dna
import dnacalib
from BbBBToolBox.deps import dnaviewer
from BbBBToolBox.deps import pyperclip

import time
from BbBBToolBox.Utils import timeStatistics


class DNAVector():
    
    @classmethod
    def creatByVectorList(cls, vector: list):
        xyzList=[list(i) for i in zip(*vector)]
        return cls(xyzList, vector)
    
    @classmethod
    def creatByXYZList(cls, xyz: list):
        vectorList=[list(i) for i in zip(*xyz)]
        return cls(xyz, vectorList)
    
    def __init__(self, xyz: list, vector: list):
        self.vectorList = vector
        self.xList = xyz[0]
        self.yList = xyz[1]
        self.zList = xyz[2]
    
    def __getitem__(self, index: int):
        return self.vectorList[index]
    
    def __setitem__(self, index: int, value):
        self.vectorList[index] = value
        self.xList[index] = value[0]
        self.yList[index] = value[1]
        self.zList[index] = value[2]
    
    def __len__(self) -> int:
        return len(self.vectorList)

    def __str__(self):
        return str(self.vectorList)


@dataclass
class JointChain:
    index: int = None
    name: str = None
    parentIndex: int = None
    #childChainList: list = field(default_factory=list)   #list[JointChain]
    #childIndexList: list = field(default_factory=list)   #list[int]
    matrix: om.MMatrix = None
    parentMatrix: om.MMatrix = None
    worldMatrix: om.MMatrix = None


@dataclass
class jointDataStruct:
    index: int = None
    name: str = None
    parentName: str = None
    neutralTranslation: list = field(default_factory=list)
    neutralOrientation: list = field(default_factory=list)
    effect: bool = None
    allDriver: list = field(default_factory=list)


class guiAnimStruct(NamedTuple):
    name: str
    attr: str
    minValue: int
    maxValue: int
    direction: int


class groupDataStruct(NamedTuple):
    controlList: list
    jointAxisList: list
    valueList: list


class jointDriverStruct(NamedTuple):
    groupIndex: int
    controlIndex: int
    jointIndex: int
    offset: list


class MetaHumanDnaTool():

    def __init__(self):
        self.modulePath = cmds.moduleInfo(p=1, mn='BbBBToolBox')
        self.uiVariable = {}

    def ToolUi(self):
        Ver = 0.01
        self.UiName = "MetaHumanDNATool"
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        cmds.window(self.UiName, t=f"MetaHumanDNATool v{Ver}", mb=0, tlb=1) #bgc=[.266, .266, .266]
        form = cmds.formLayout()
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, e=1, af=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

        child1 = cmds.columnLayout(cat=('both', 2), rs=3, cw=250, adj=1)
        self.createUi_CreatePage()
        cmds.setParent('..')

        child2 = cmds.formLayout()
        self.createUi_EditPage(child2)
        cmds.setParent('..')

        child3 = cmds.columnLayout(cat=('both', 2), rs=3, cw=250, adj=1)
        self.createUi_ToolPage()
        cmds.setParent('..')

        cmds.tabLayout(tabs, e=True, tl=((child1, '创建'), (child2, '编辑'), (child3, '工具')), 
                        cc=lambda *args: self.checkUi_TabPage(cmds.tabLayout(tabs, q=1, sti=1)))
        cmds.showWindow()
    
    def createUi_CreatePage(self):
        _cl3_ = ('left', 'center', 'center')
        _cw3_ = (90, 200, 10)
        _cat_ = (2, 'right', 5)
        self.uiVariable['Create_loadModel'] = [
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(0), l='头 Head'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(1), l='牙 Teeth'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(2), l='唾液 Saliva'), #牙龈湿润层
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(3), l='左眼球 eyeLeft'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(4), l='右眼球 eyeRight'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(5), l='眼膜 eyeShell'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(6), l='睫毛 eyeLashes'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(7), l='眼睑 eyeEdge'), 
            cmds.textFieldButtonGrp(bl='加载', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _LoadModelName_(8), l='眼眶 Cartilage'), #材质为透明?
        ]
        cmds.separator(height=5) 
        self.uiVariable['Create_dnaPath'] = cmds.textFieldButtonGrp(bl='选择', ed=0, adj=2, h=24, cl3=_cl3_, cw3=_cw3_, cat=_cat_, bc=lambda *args: _selectDNAWindow_(), l='DNA模板')
        self.uiVariable['Create_mirrorJoint'] = cmds.checkBox(l='使左右骨骼对称')

        form = cmds.formLayout()
        editLayout= cmds.rowLayout(nc=1, adj=1)
        self.uiVariable['Create_FitJointButton'] = cmds.button(l='手动调整骨骼位置', h=24, c=lambda *args: self.createJointInMaya(self.getUi_DnaPath()))
        cmds.setParent('..')
        saveLayout= cmds.rowLayout(nc=2, adj=1)
        cmds.button(l='生成新DNA文件并创建绑定', h=24, c=lambda *args: self.saveCreateToDnaFile(self.getUi_DnaPath(), rig=True))
        cmds.button(l='>', h=24)
        cmds.popupMenu(b=1)
        cmds.menuItem(l='生成新DNA文件', c=lambda *args: self.saveCreateToDnaFile(self.getUi_DnaPath(), rig=False))
        cmds.menuItem(l='从选择的DNA创建绑定', c=lambda *args: self.generateDnaRigInMaya(self.getUi_DnaPath()))
        cmds.menuItem(divider=True, dividerLabel='生成选项')
        self.uiVariable['Create_generateOptions'] = [
            cmds.menuItem(l='添加控制属性到头部骨骼', cb=0),
            cmds.menuItem(l='添加贴图切换属性到头部骨骼', cb=0),
            cmds.menuItem(l='添加模型名称到BS形状', cb=0),
        ]
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout(form, e=1, af=((editLayout, 'top', 0), (editLayout, 'left', 0), (editLayout, 'bottom', 0), 
                                        (saveLayout, 'top', 0), (saveLayout, 'right', 0), (saveLayout, 'bottom', 0),),
                                    ap=((editLayout, 'right', 0, 50), (saveLayout, 'left', 0, 50),))
        
        toPoMap = [['Head', 'e71f39f41a0a6ea0897dfb1ddbc9425a'], 
                ['Teeth', '4f9f379b80a6b9b159d871d07ef251de'], 
                ['Saliva', 'df7913b5c2cfd43321ce80bc9f878db1'], 
                ['eyeLeft', 'ea67c74689741571cc3525cfa2d23c11'], 
                ['eyeRight', 'ea67c74689741571cc3525cfa2d23c11'], 
                ['eyeShell', '9dd5b054a890a4dc8109c9d53259cc60'], 
                ['eyeLashes', '44eee5c1e54b2994c14c3b59bf5b865e'], 
                ['eyeEdge', '6e752f7bca8848b6d4f9f1aada61adc3'], 
                ['Cartilage', '0294d0178f2ad3d6f57eb368e39e32d2']]
        def _LoadModelName_(loadui: int):
            slList = cmds.ls(sl=1, typ="transform")
            if slList:
                slMD5 = self.checkModelTopology(om.MGlobal.getSelectionListByName(slList[0]))
                if slMD5 == toPoMap[loadui][1]:
                    cmds.textFieldButtonGrp(self.uiVariable['Create_loadModel'][loadui], e=1, tx=slList[0])
                else:
                    om.MGlobal.displayError('选择的模型不符合MetaHuman拓扑结构')
            else:
                cmds.textFieldButtonGrp(self.uiVariable['Create_loadModel'][loadui], e=1, tx='')

        def _selectDNAWindow_():
            DnaUi = f'selectDna_{self.UiName}'
            if cmds.window(DnaUi, q=1, ex=1):
                cmds.deleteUI(DnaUi)
            cmds.window(DnaUi, t="Select DNA", s=0, mb=0, tlb=1, wh=(1032, 290)) #bgc=[.266, .266, .266]
            cmds.columnLayout(cat=('both', 2), rs=2)
            cmds.rowLayout(nc=4, w=1024)
            dnaDir = f'{self.modulePath}/data/Dna'
            _DNAiconSelectCollect = cmds.iconTextRadioCollection()
            cmds.iconTextRadioButton(st='iconOnly', w=256 , h=256, i=f"{dnaDir}/Myles.png")
            cmds.iconTextRadioButton(st='iconOnly', w=256 , h=256, i=f"{dnaDir}/Stephane.png")
            cmds.iconTextRadioButton(st='iconOnly', w=256 , h=256, i=f"{dnaDir}/Vivian.png")
            cmds.iconTextRadioButton(st='iconOnly', w=256 , h=256, i=f"{dnaDir}/Sookja.png")
            cmds.setParent('..')
            cmds.rowLayout(nc=2, w=1024)
            cmds.button(l='确认选择', w=512, c=lambda *args: _selectDNAFile_(0))
            cmds.button(l='选择自定义DNA', w=512, c=lambda *args: _selectDNAFile_(1))
            cmds.setParent('..')
            def _selectDNAFile_(mode):
                if mode == 0:
                    sl = cmds.iconTextRadioCollection(_DNAiconSelectCollect, q=1, sl=1)
                    if sl != "NONE" and os.path.isfile(cmds.iconTextRadioButton(sl, q=1, i=1).replace('.png', '.dna')):
                        cmds.textFieldButtonGrp(self.uiVariable['Create_dnaPath'], e=1, tx=cmds.iconTextRadioButton(sl, q=1, i=1).replace('.png', '.dna'))
                        cmds.deleteUI(DnaUi)
                else:
                    filePath = cmds.fileDialog2(ff='MetaHumanDNA (*.dna)', ds=2, fm=1)
                    if filePath:
                        cmds.textFieldButtonGrp(self.uiVariable['Create_dnaPath'], e=1, tx=filePath[0])
                        cmds.deleteUI(DnaUi)
                        self.checkDnaPreset(self.loadDna(filePath[0]))
            cmds.showWindow()

    def getUi_loadModel(self, onlyHead=False):   # -> list[list[int, om.MDagPath]]:
        headModel = cmds.textFieldButtonGrp(self.uiVariable['Create_loadModel'][0], q=1, tx=1)
        if not headModel:
            cmds.error('没加载头部Head模型')
        if onlyHead:
            return [om.MGlobal.getSelectionListByName(headModel).getDagPath(0)]
    
        modelDagPath = []
        for i in self.uiVariable['Create_loadModel']:
            modelName = cmds.textFieldButtonGrp(i, q=1, tx=1)
            if modelName:
                modelDagPath.append(om.MGlobal.getSelectionListByName(modelName).getDagPath(0))
        return modelDagPath
    
    def getUi_DnaPath(self) -> str:
        path = cmds.textFieldButtonGrp(self.uiVariable['Create_dnaPath'], q=1, tx=1)
        if not path:
            cmds.error('没选择DNA文件')
        return os.path.normpath(path)

    def getUi_mirrorJoint(self) -> bool:
        return cmds.checkBox(self.uiVariable['Create_mirrorJoint'], q=1, v=1)
    
    def getUi_FitJointButton(self) -> bool:
        return cmds.button(self.uiVariable['Create_FitJointButton'], q=1, en=1)
    
    def editUi_FitJointButton(self, enable: bool):
        if enable:
            cmds.button(self.uiVariable['Create_FitJointButton'], e=1, en=1, l='手动调整骨骼位置')
        else:
            cmds.button(self.uiVariable['Create_FitJointButton'], e=1, en=0, l='可以进行调整')
    
    def createUi_EditPage(self, mainForm):
        pane = cmds.paneLayout(cn='right3')
        copyFunc = lambda lable: self.checkUi_copyTreeViewItem(lable)

        form = self.uiVariable['Edit_controlLayout'] = cmds.formLayout()
        searchControl = cmds.textField(h=24, pht='搜索...', tcc=lambda text: self.editUi_searchControlTreeView(text))
        ctv = self.uiVariable['Edit_controlTreeView'] = cmds.treeView(
            nb=2, adr=0, fb=1, idc=copyFunc, ams=0, 
            scc=lambda *args: self.checkUi_selectControlTreeView())
        aniSlider = self.uiVariable['Edit_aniSlider'] = cmds.floatSlider(
            min=0, max=1, v=1, step=0.001, dc=lambda value: self.setGuiValue(value))
        resetGui = cmds.button(l='回到默认表情', h=24, c=lambda *args: self.resetAllGui())
        mirrorJoint = cmds.button(l='镜像表情骨骼', h=24, c=lambda *args: self.checkUi_mirrorControl('joint'))
        mirrorBs = cmds.button(l='镜像表情BS', h=24, c=lambda *args: self.checkUi_mirrorControl('bs'))
        cmds.setParent('..')   #formLayout
        cmds.formLayout(form, e=1, af=((searchControl, 'top', 3), (searchControl, 'left', 0), (searchControl, 'right', 0), 
                                        (ctv, 'left', 0), (ctv, 'right', 0), 
                                        (aniSlider, 'left', 0), (aniSlider, 'right', 0), 
                                        (resetGui, 'left', 0), (resetGui, 'bottom', 0), 
                                        (mirrorJoint, 'left', 0), (mirrorJoint, 'bottom', 0), 
                                        (mirrorBs, 'right', 0), (mirrorBs, 'bottom', 0)),
                                    ac=((ctv, 'top', 3, searchControl), (ctv, 'bottom', 3, aniSlider), 
                                        (aniSlider, 'bottom', 3, mirrorJoint)),
                                    ap=((resetGui, 'right', 1, 33), 
                                        (mirrorJoint, 'left', 1, 33), (mirrorJoint, 'right', 1, 66), 
                                        (mirrorBs, 'left', 1, 66)))

        form = cmds.formLayout()
        bstv = self.uiVariable['Edit_bsTreeView'] = cmds.treeView(nb=2, adr=0, fb=1, idc=copyFunc, h=20)
        editLayout = cmds.columnLayout(adj=1)
        self.uiVariable['Edit_startEditBs'] = cmds.button(l='开始编辑', h=24, c=lambda *args: self.startEditBs())
        self.uiVariable['Edit_endEditBs'] = cmds.rowLayout(adj=2, nc=2, vis=0)
        cmds.button(l='取消编辑', h=24, w=100, c=lambda *args: self.endEditBs('cancel'))
        cmds.button(l='保存编辑', h=24, bgc=(1, .3, .3), c=lambda *args: self.endEditBs('apply'))
        cmds.setParent('..')   #rowLayout
        cmds.setParent('..')   #columnLayout
        cmds.setParent('..')   #formLayout
        cmds.formLayout(form, e=1, af=((bstv, 'top', 0), (bstv, 'left', 0), (bstv, 'right', 0), 
                                        (editLayout, 'left', 0), (editLayout, 'right', 0), (editLayout, 'bottom', 0)),
                                    ac=((bstv, 'bottom', 3, editLayout)))
        
        form = cmds.formLayout()
        searchJoint = self.uiVariable['Edit_searchJoint'] = cmds.textField(
            h=24, pht='搜索...', tcc=lambda text: self.editUi_filterJointTreeView(search=text))
        filterJointCB = self.uiVariable['Edit_filterJointCB'] = cmds.iconTextCheckBox(
            i='RS_filter_list.png', w=22, h=22, v=1, cc=lambda driver: self.editUi_filterJointTreeView(driver=driver))
        jtv = self.uiVariable['Edit_jointTreeView'] = cmds.treeView(
            nb=2, adr=0, fb=1, idc=copyFunc, enk=1, 
            scc=lambda *args: cmds.select(cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, si=1), r=1))
        editLayout = cmds.columnLayout(adj=1)
        self.uiVariable['Edit_startEditJoint'] = cmds.button(l='开始编辑', h=24, c=lambda *args: self.startEditJoint())
        self.uiVariable['Edit_endEditJoint'] = cmds.rowLayout(adj=2, nc=2, vis=0)
        cmds.button(l='取消编辑', h=24, w=100, c=lambda *args: self.endEditJoint('cancel'))
        cmds.button(l='保存编辑', h=24, bgc=(1, .3, .3), c=lambda *args: self.endEditJoint('apply'))
        cmds.setParent('..')   #rowLayout
        cmds.setParent('..')   #columnLayout
        cmds.setParent('..')   #formLayout
        cmds.formLayout(form, e=1, af=((searchJoint, 'top', 0), (searchJoint, 'left', 0), 
                                        (filterJointCB, 'top', 0), (filterJointCB, 'right', 3), 
                                        (jtv, 'left', 0), (jtv, 'right', 0), 
                                        (editLayout, 'left', 0), (editLayout, 'right', 0), (editLayout, 'bottom', 0)),
                                    ac=((searchJoint, 'right', 3, filterJointCB),
                                        (jtv, 'top', 3, searchJoint), (jtv, 'bottom', 3, editLayout)))
        
        cmds.setParent('..')   #paneLayout
        cmds.formLayout(mainForm, e=1, af=((pane, 'top', 0), (pane, 'left', 0), (pane, 'right', 0), (pane, 'bottom', 0)))

        self.DataSave_channleColorScriptJobId = -1
        self.DataSave_controlTreeViewSelectItem = {'itemName': None, 'animInfo': []}
        self.DataSave_DNAData = {'nodeName': None, 'filePath': None, 'dnaReader': None} 
        self.DataSave_jointConnectInfo = {}
    
    def editUi_AddItemToTreeView(self, treeView, lable, index, psd: str='', joint: bool=False):
        widgetName = f'Edit_{treeView}TreeView'
        cmds.treeView(self.uiVariable[widgetName], e=1, ai=(lable, ''))
        if treeView == "control":
            if psd:
                icon = "HIKCharacterToolFullBody.png"
                cmds.treeView(self.uiVariable[widgetName], e=1, ia=(lable, psd))
            else:
                icon = 'HIKCharacterToolStancePose.png'
        elif treeView == "bs":
            icon = 'ts-head3.png'
        elif treeView == "joint":
            icon = 'out_joint.png'
            cmds.treeView(self.uiVariable[widgetName], e=1, ia=(lable, joint))
        cmds.treeView(self.uiVariable[widgetName], e=1, eb=((lable, 1, 1), (lable, 2, 0)), 
                                                        i=(lable, 1, icon),
                                                        bti=(lable, 2, index))
        
    def editUi_refreshControlTreeView(self):
        dnaReader = self.DataSave_DNAData['dnaReader']
        cmds.treeView(self.uiVariable['Edit_controlTreeView'], e=1, ra=1)
        #获取控制名称
        controlNameList = []
        for i1 in range(dnaReader.getRawControlCount()):
            controlName = dnaReader.getRawControlName(i1).replace('CTRL_expressions.', '')
            self.editUi_AddItemToTreeView("control", controlName, i1)
            controlNameList.append(controlName)
        #获取PSD叠加关系名称
        psdDataList = [None] * (i1 + dnaReader.getPSDCount() + 1)
        for psdIndex, controlIndex in zip(dnaReader.getPSDRowIndices(), dnaReader.getPSDColumnIndices()):
            if not psdDataList[psdIndex]:
                psdDataList[psdIndex] = [controlIndex]
            else:
                psdDataList[psdIndex].append(controlIndex)
        for i2 in range(dnaReader.getPSDCount()):
            nowPsd = psdDataList[i1+i2+1]
            nowPsd.sort()
            self.editUi_AddItemToTreeView("control", ' + '.join(map(str, nowPsd)), i1+i2+1, 
                                            psd=' + '.join([controlNameList[i] for i in nowPsd]))
    @timeStatistics
    def editUi_refreshBlendShapeTreeView(self, bsIndexList):
        cmds.treeView(self.uiVariable['Edit_bsTreeView'], e=1, ra=1)
        if bsIndexList:
            self.editUi_AddItemToTreeView("bs", bsIndexList[1], bsIndexList[0])

    @timeStatistics
    def editUi_refreshJointTreeView(self, jointIndexList):
        jointIndexList: list[jointDataStruct] = jointIndexList
        cmds.treeView(self.uiVariable['Edit_jointTreeView'], e=1, ra=1)
        cmds.textField(self.uiVariable['Edit_searchJoint'], e=1, tx='')
        if jointIndexList:
            jointIndexList.sort(key=lambda i:i.index)
            for i in jointIndexList:
                self.editUi_AddItemToTreeView("joint", i.name, i.index, joint=i.effect)
            if cmds.iconTextCheckBox(self.uiVariable['Edit_filterJointCB'], q=1, v=1):
                self.editUi_filterJointTreeView(driver=True)
    
    def editUi_searchControlTreeView(self, text):
        tv = 'Edit_controlTreeView'
        if not text:
            for i in cmds.treeView(self.uiVariable[tv], q=1, children=1):
                cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 1))
            return
        for i in cmds.treeView(self.uiVariable[tv], q=1, children=1):
            if '+' in i:
                if text in cmds.treeView(self.uiVariable[tv], q=1, itemAnnotation=1, it=i):
                    cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 1))
                    continue
            if text in i:
                cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 1))
                continue
            cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 0))
    
    @timeStatistics
    def editUi_filterJointTreeView(self, search='', driver=False):
        tv = 'Edit_jointTreeView'
        if not cmds.treeView(self.uiVariable[tv], q=1, children=1):
            return
        if driver:
            for i in cmds.treeView(self.uiVariable[tv], q=1, children=1):
                if cmds.treeView(self.uiVariable[tv], q=1, itemAnnotation=1, it=i) == 'False':
                    cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 0))
        elif search:
            for i in cmds.treeView(self.uiVariable[tv], q=1, children=1):
                if search in i:
                    cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 1))
                    continue
                cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 0))
        else:
            for i in cmds.treeView(self.uiVariable[tv], q=1, children=1):
                cmds.treeView(self.uiVariable[tv], e=1, iv=(i, 1))
            searchText = cmds.textField(self.uiVariable['Edit_searchJoint'], q=1, tx=1)
            if searchText:
                self.editUi_filterJointTreeView(search=searchText)
            driverBool = cmds.iconTextCheckBox(self.uiVariable['Edit_filterJointCB'], q=1, v=1)
            if driverBool:
                self.editUi_filterJointTreeView(driver=driverBool)

    def editUi_switchEditVisible(self, ui: str, edit: bool):
        if edit:
            cmds.button(self.uiVariable[f'Edit_startEdit{ui}'], e=1, vis=0)
            cmds.rowLayout(self.uiVariable[f'Edit_endEdit{ui}'], e=1, vis=1)
            cmds.formLayout(self.uiVariable['Edit_controlLayout'], e=1, en=0)
        else:
            cmds.button(self.uiVariable[f'Edit_startEdit{ui}'], e=1, vis=1)
            cmds.rowLayout(self.uiVariable[f'Edit_endEdit{ui}'], e=1, vis=0)
            cmds.formLayout(self.uiVariable['Edit_controlLayout'], e=1, en=1)

    def editUi_switchSaveButtonEnable(self, save: bool):
        for i in ('Joint', 'Bs'):
            saveButton = cmds.rowLayout(self.uiVariable[f'Edit_endEdit{i}'], q=1, ca=1)[1]
            if save:
                cmds.button(saveButton, e=1, en=0, l='上次编辑保存中...')
            else:
                cmds.button(saveButton, e=1, en=1, l='保存编辑')

    def checkUi_copyTreeViewItem(self, text):
        if '+' in text:
            text = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemAnnotation=1, it=text)
        pyperclip.copy(text)
        print(text)

    @timeStatistics
    def checkUi_selectControlTreeView(self):
        slText = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, si=1)[0]
        if self.DataSave_controlTreeViewSelectItem['itemName'] == slText:
            return
        self.DataSave_controlTreeViewSelectItem['itemName'] = slText
        self.setGuiValue(0)
        cmds.floatSlider(self.uiVariable['Edit_aniSlider'], e=1, v=1)

        slIndex = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=slText)
        dnaReader = self.DataSave_DNAData['dnaReader']
        self.editUi_refreshBlendShapeTreeView(self.getBlendShapeFromControl(dnaReader, slIndex))
        self.editUi_refreshJointTreeView(self.getJointFromControl(dnaReader, slIndex))
        if '+' in slText:
            resultAnimInfo = self.getGuiAnimRangeFromControl(dnaReader, self.getControlFromPSD(dnaReader, slIndex))
        else:
            resultAnimInfo = self.getGuiAnimRangeFromControl(dnaReader, [slIndex])
        self.DataSave_controlTreeViewSelectItem['animInfo'] = resultAnimInfo
        self.setGuiValue(1)
        cmds.select([i.name for i in resultAnimInfo], r=1)
    
    def checkUi_mirrorControl(self, mode):
        haveOtherSide = None
        controlName = self.DataSave_controlTreeViewSelectItem['itemName']
        if '+' in controlName:
            sidePsdList = []
            for i in cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemAnnotation=1, it=controlName).split(' + '):
                if i[-1] == 'L':
                    sideControl = f'{i[:-1]}R'
                elif i[-1] == 'R':
                    sideControl = f'{i[:-1]}L'
                else:
                    sidePsdList.append(cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=i))
                    continue
                haveOtherSide = True
                sidePsdList.append(cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=sideControl))
            sideControlName = ' + '.join(sidePsdList)
        else:
            if controlName[-1] == 'L':
                sideControlName = f'{controlName[:-1]}R'
                haveOtherSide = True
            elif controlName[-1] == 'R':
                sideControlName = f'{controlName[:-1]}L'
                haveOtherSide = True
        if not haveOtherSide:
            om.MGlobal.displayWarning('没找到对应的表情')
            return
        
        if mode == 'joint':
            self.mirrorControlJoint(controlName, sideControlName)
        elif mode == 'bs':
            pass
        
    def createUi_ToolPage(self):
        cmds.button(l='DnaViewer面板', c=lambda *args: dnaviewer.show())
        cmds.button(l='测试按钮', c=lambda *args: print())

    def checkUi_TabPage(self, page):
        if page == 2:   #编辑页
            dnaNode = self.checkSceneDnaNode()
            if dnaNode:
                self.editUi_refreshControlTreeView()
        
    #####   Utils   #####
    def indexGenerator(n=0):
        while True:
            yield n
            n += 1

    def reRange(self, num, to_min, to_max, minNow, maxNow) -> float:
        """
        重映射范围
        - num: 需要映射数值
        - to_min: 要映射到的最小值
        - to_max: 要映射到的最大值
        - minNow: 现有数据最小值
        - maxNow: 现有数据最大值
        """
        return (to_min + ((to_max - to_min) / (maxNow - minNow)) * num - minNow)

    def omMatrixCompose(self, T, R, S, space=om.MSpace.kWorld, RotOrder=om.MTransformationMatrix.kXYZ) -> om.MMatrix:
        MTMatrix = om.MTransformationMatrix()
        MTMatrix.setTranslation(om.MVector(T), space)
        MTMatrix.setRotationComponents([math.radians(i) for i in R] + [RotOrder])
        MTMatrix.setScale(S, space)
        return MTMatrix.asMatrix()

    def list3Add(self, list1, list2):
        return [list1[0]+list2[0], list1[1]+list2[1], list1[2]+list2[2]]
    
    def list3Subtract(self, list1, list2):
        return [list1[0]-list2[0], list1[1]-list2[1], list1[2]-list2[2]]

    def getDnaSavePath(self, dnaName):
        return f'{os.path.dirname(cmds.file(q=1, sn=1))}/{dnaName}'

    def setNewDnaPath(self, dnaPath):
        cmds.setAttr(f"{self.DataSave_DNAData['nodeName']}.dnaFilePath", dnaPath, type="string")
        self.DataSave_DNAData['filePath'] = dnaPath
        self.DataSave_DNAData['dnaReader'] = self.loadDna(dnaPath)
    
    def loadDna(self, path) -> dna.BinaryStreamReader:
        stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
        reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
        reader.read()
        if not dna.Status.isOk():
            status = dna.Status.get()
            raise RuntimeError(f"Error loading DNA: {status.message}")
        return reader

    def createDnaWriter(self, reader, path, mode=False) -> dna.BinaryStreamWriter:
        stream = dna.FileStream(path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
        writer = dna.BinaryStreamWriter(stream)
        #writer = dna.JSONStreamWriter(stream)
        if mode:
            writer.setFrom(reader, dna.DataLayer_Behavior)
        else:
            writer.setFrom(reader)
        # DataLayer_Descriptor - ~ 3 KB
        # DataLayer_Definition - includes Descriptor, ~ 131 KB
        # DataLayer_Behavior - includes Descriptor and Definition, ~ 10 MB
        # DataLayer_Geometry - includes Descriptor and Definition, ~ 191 MB
        # DataLayer_GeometryWithoutBlendShapes - includes Descriptor and Definition, ~ 22 MB
        # DataLayer_AllWithoutBlendShapes - includes everything except blend shapes from Geometry, ~ 32 MB
        # DataLayer_All - ~ 201 MB
        return writer

    def saveDna(self, writer: dna.BinaryStreamWriter):
        writer.write()
        if not dna.Status.isOk():
            status = dna.Status.get()
            raise RuntimeError(f"Error saving DNA: {status.message}")
    
    def saveFullDna(self, tempDnaPath):
        self.editUi_switchSaveButtonEnable(True)
        self.setNewDnaPath(tempDnaPath)
        pyargs = [f'{os.environ["MAYA_LOCATION"]}/bin/mayapy.exe',                      #python解释器
                    f'{self.modulePath}/scripts/BbBBToolBox/assist/mayapySaveDna.py',   #要执行的Py
                    f'{self.modulePath}/python/{cmds.about(q=1, v=1)}',                 #要添加的环境变量
                    self.DataSave_DNAData['filePath'],                                  #完整Dna路径
                    tempDnaPath]                                                        #小号Dna路径
        #index = self.indexGenerator(1)
        if os.path.exists(f'{self.DataSave_DNAData['filePath']}BAK{index}'):
            shutil.copyfile(self.DataSave_DNAData['filePath'], )
        saveDnaThread = threading.Thread(target=self.assistSaveFullDna, args=(pyargs, ))
        saveDnaThread.start()

    def assistSaveFullDna(self, pyargs):
        p = subprocess.run(pyargs, shell=True, capture_output=True, timeout=120)
        if p.returncode != 0:
            om.MGlobal.displayError(f'Save FullDNA Error: {p.stderr.decode()}')
        self.setNewDnaPath(pyargs[3])
        self.editUi_switchSaveButtonEnable(False)

    #####   Create   #####
    def checkModelTopology(self, MslList: om.MSelectionList) -> str:
        #objDagPath = MslList.getDagPath(0)
        objObject = MslList.getDependNode(0)
        ToPoData = []
        ToPoDataApp = ToPoData.append
        polyIter = om.MItMeshPolygon(objObject)
        while not polyIter.isDone():
            ToPoDataApp([polyIter.index(), polyIter.getVertices()[0]])
            polyIter.next()
        return hashlib.md5(str(ToPoData).encode("utf-8")).hexdigest()

    def checkDnaPreset(self, dnaReader) -> str:
        preset = dnaReader.getDBName()
        if preset == "DHI":
            cmds.framelessDialog(title='注意', message='选择的Dna文件为旧版本——对比新版会缺少部分骨骼和控制器', button=['已阅'], primary=['已阅'])
        return preset
    
    def checkScenceState(self):
        result = cmds.framelessDialog(title='注意', message='从Dna生成需要新建maya场景', button=['另存为', '不保存'], primary=['另存为'])
        if result == '另存为':
            cmds.SaveSceneAs()

    def getModelPoints(self, model: om.MDagPath) -> DNAVector:
        return DNAVector.creatByVectorList(om.MFnMesh(model).getPoints())

    def getDnaModelPoints(self, dnaReader: dna.BinaryStreamReader, ModelIndex: int) -> DNAVector:
        return DNAVector.creatByXYZList([dnaReader.getVertexPositionXs(ModelIndex), 
                                         dnaReader.getVertexPositionYs(ModelIndex), 
                                         dnaReader.getVertexPositionZs(ModelIndex)])
    
    def getSceneJointTrans(self, dnaReader: dna.BinaryStreamReader):
        jointNames = [dnaReader.getJointName(i) for i in range(dnaReader.getJointCount())]
        cmds.makeIdentity(jointNames[0], apply=1, t=0, r=1, s=0, n=0, pn=1)
        newJointPos = DNAVector.creatByVectorList(cmds.getAttr([f'{i}.t' for i in jointNames]))
        newJointRot = DNAVector.creatByVectorList(cmds.getAttr([f'{i}.jointOrient' for i in jointNames]))
        return newJointPos, newJointRot

    def calculateDnaJointTrans(self, dnaReader: dna.BinaryStreamReader, objDagPath):
        newModelPos = self.getModelPoints(objDagPath)
        dnaModelPos = self.getDnaModelPoints(dnaReader, 0)
        jointChain, jointWorldPos = self.bulidJointChain(dnaReader)
        newJointOffset = self.getJointOffset(jointWorldPos, dnaModelPos, newModelPos)
        newJointPos, newJointRot = self.getJointTrans(dnaReader, jointChain, newJointOffset)
        return newJointPos, newJointRot
    
    def bulidJointChain(self, dnaReader: dna.BinaryStreamReader):
        jointCount = dnaReader.getJointCount()
        jointChainList: list[JointChain] = []
        _jointWorldPos = []
        _parentIndexList = [dnaReader.getJointParentIndex(i) for i in range(jointCount)]

        def _buildChain_(index, parentMatrix) -> JointChain:
            joint = JointChain(index=index, name=dnaReader.getJointName(index), parentIndex=_parentIndexList[index])
            joint.matrix = self.omMatrixCompose(dnaReader.getNeutralJointTranslation(index), 
                                               dnaReader.getNeutralJointRotation(index), 
                                               [1.0, 1.0, 1.0])
            joint.parentMatrix = parentMatrix
            joint.worldMatrix = joint.matrix * parentMatrix

            _jointWorldPos.append(om.MTransformationMatrix(joint.worldMatrix).translation(om.MSpace.kWorld))
            return joint

        jointChainList.append(_buildChain_(0, om.MMatrix.kIdentity))
        for i in range(1, jointCount):
            jointChainList.append(_buildChain_(i, jointChainList[_parentIndexList[i]].worldMatrix))
        return jointChainList, DNAVector.creatByVectorList(_jointWorldPos)

    def getJointOffset(self, jointWorldPos: DNAVector, dnaModelPos: DNAVector, newModelPos: DNAVector) -> DNAVector:
        jointOffset=[]

        _dnaModelMPoint = om.MPointArray(dnaModelPos)
        def _getNearModelIndex_(onePos: om.MPoint):
            distances = [onePos.distanceTo(p) for p in _dnaModelMPoint]
            return distances.index(min(distances))

        for jPos in jointWorldPos:
            index = _getNearModelIndex_(om.MPoint(jPos))
            jointOffset.append(om.MVector(newModelPos[index]) - om.MVector(dnaModelPos[index]))
        return DNAVector.creatByVectorList(jointOffset)

    def getJointTrans(self, dnaReader: dna.BinaryStreamReader, jointChain, jointOffset: DNAVector):
        jointChain: list[JointChain] = jointChain
        _newJointPos: list[om.MVector] = [None] * len(jointOffset)
        _newJointRot: list[om.MVector] = _newJointPos[:]
        mirrorFlag = self.getUi_mirrorJoint()
        #centerJointList = set()
        if mirrorFlag:
            mirrorMatrix = om.MMatrix().setElement(0, 0, -1)   #(-1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)
            jointNames = [dnaReader.getJointName(i) for i in range(dnaReader.getJointCount())]
            #centerJointList = ('spine_04', 'spine_05', 'neck_01', 'neck_02', 'head')

        def _getMatrix_(joint: JointChain, parentMatrix, lMatrix, translateXToCenter=False):
            joint.parentMatrix = parentMatrix
            if not lMatrix:
                offsetMatrix = self.omMatrixCompose(jointOffset[joint.index], [0, 0, 0], [1.0, 1.0, 1.0])
                joint.worldMatrix = joint.worldMatrix * offsetMatrix
            else:
                joint.worldMatrix = mirrorMatrix * lMatrix * mirrorMatrix
            #if translateXToCenter:
            #    joint.worldMatrix = joint.worldMatrix.setElement(3, 0, 0)
            joint.matrix = joint.worldMatrix * joint.parentMatrix.inverse()
            return joint.matrix

        oneoff = True
        for i in jointChain:
            jointLMatrix = None
            parentMatrix = jointChain[i.parentIndex].worldMatrix
            if oneoff:
                parentMatrix = om.MMatrix.kIdentity
                oneoff = False
            elif mirrorFlag:
                if 'FACIAL_R_' in i.name:
                    lIndex = jointNames.index(i.name.replace('FACIAL_R_', 'FACIAL_L_'))
                    jointLMatrix = jointChain[lIndex].worldMatrix
            jointTrans = om.MTransformationMatrix(_getMatrix_(i, parentMatrix, jointLMatrix)) 
            _newJointPos[i.index] = jointTrans.translation(om.MSpace.kWorld)
            _newJointRot[i.index] = [math.degrees(r) for r in jointTrans.rotation()]
        _newJointPos[0].x = 0
        return DNAVector.creatByVectorList(_newJointPos), DNAVector.creatByVectorList(_newJointRot)

    def createJointInMaya(self, dnaPath):
        dnaReader = self.loadDna(dnaPath)
        headInfo: list[int, om.MDagPath] = self.getUi_loadModel(onlyHead=True)
        newJointPos, newJointRot = self.calculateDnaJointTrans(dnaReader, headInfo[0])

        #jointDataStruct = namedtuple("joint", "name parentName translation orientation")
        _joints: list[jointDataStruct] = []
        _joint_flags: dict[str, bool] = {}
        for i in range(dnaReader.getJointCount()):
            name = dnaReader.getJointName(i)
            _joints.append(jointDataStruct(name = name, 
                                           parentName = dnaReader.getJointName(dnaReader.getJointParentIndex(i)), 
                                           neutralTranslation = newJointPos[i], 
                                           neutralOrientation = newJointRot[i]))
            _joint_flags[name] = False

        def _createJoint_(joint: jointDataStruct):
            in_parent_space = True
            if cmds.objExists(joint.parentName):
                cmds.select(joint.parentName)
            else:
                if joint.name != joint.parentName:
                    parent_joint = next(j for j in _joints if j.name == joint.parentName)
                    _createJoint_(parent_joint)
                else:
                    cmds.select(d=True)
                    in_parent_space = False
            cmds.joint(p=joint.neutralTranslation, o=joint.neutralOrientation, 
                       n=joint.name, r=in_parent_space, a=not in_parent_space, sc=False)
            _joint_flags[joint.name] = True

        for i in _joints:
            if not _joint_flags[i.name]:
                _createJoint_(i)
        self.editUi_FitJointButton(False)

    def saveCreateToDnaFile(self, dnaPath, rig: bool):
        dnaReader = self.loadDna(dnaPath)
        calibRader = dnacalib.DNACalibDNAReader(dnaReader)
        commands = dnacalib.CommandSequence()
        modelInfo: list[om.MDagPath] = self.getUi_loadModel()
        for index, item in enumerate(modelInfo):
            modelPos = self.getModelPoints(item)
            commands.add(
                dnacalib.SetVertexPositionsCommand(index, modelPos.xList, modelPos.yList, modelPos.zList, dnacalib.VectorOperation_Interpolate))
        if self.getUi_FitJointButton():   #按钮为开，没进行过手动调整骨骼
            jointPos, jointRot = self.calculateDnaJointTrans(dnaReader, modelInfo[0])
        else:   #按钮为关，重新获取场景中的骨骼位置
            jointPos, jointRot = self.getSceneJointTrans(dnaReader)
        commands.add(dnacalib.SetNeutralJointTranslationsCommand(jointPos.xList, jointPos.yList, jointPos.zList))
        commands.add(dnacalib.SetNeutralJointRotationsCommand(jointRot.xList, jointRot.yList, jointRot.zList))
        commands.run(calibRader)
        for i in dnaReader.getMeshIndicesForLOD(0):
            dnacalib.CalculateMeshLowerLODsCommand(i).run(calibRader)

        outDnaPath = self.getDnaSavePath(os.path.basename(dnaPath))
        self.saveDna(self.createDnaWriter(calibRader, outDnaPath))
        if rig:
            self.generateDnaRigInMaya(outDnaPath)
    
    def generateDnaRigInMaya(self, dnaPath):
        self.checkScenceState()
        viewDnaReader = dnaviewer.DNA(dnaPath)
        generateOptions = [cmds.menuItem(i, q=1, cb=1) for i in self.uiVariable['Create_generateOptions']]
        extraPath = '' if viewDnaReader.reader.getDBName() == "MH.4" else 'DHI/'
        utilsPath = f'{self.modulePath}/data/Dna/Utils'
        utilsFiles = (f'{utilsPath}/{extraPath}gui.ma', f'{utilsPath}/analog_gui.ma', f'{utilsPath}/{extraPath}additional_assemble_script.py')

        config = dnaviewer.builder.config.RigConfig(
            meshes=[i for i in range(viewDnaReader.reader.getMeshCount())],
            gui_path=utilsFiles[0],
            analog_gui_path=utilsFiles[1],
            aas_path=utilsFiles[2],
            add_rig_logic=True,
            add_joints=True,
            add_blend_shapes=True,
            add_skin_cluster=True,
            add_ctrl_attributes_on_root_joint=generateOptions[0],
            add_animated_map_attributes_on_root_joint=generateOptions[1],
            add_mesh_name_to_blend_shape_channel_name=generateOptions[2],
            add_key_frames=False,
        )
        dnaviewer.build_rig(dna=viewDnaReader, config=config)
        self.setDefaultMaterial(viewDnaReader.reader)

    def setDefaultMaterial(self, dnaReader: dna.BinaryStreamReader):
        modelList = [dnaReader.getMeshName(i) for i in range(dnaReader.getMeshCount())]
        texPath = f'{self.modulePath}/data/Dna/Tex'
        newMat = cmds.shadingNode('blinn', asShader=1, n='M_eyeTransparenctDna_blinn')
        cmds.setAttr(f'{newMat}.transparency', .8, .8, .8, type='double3')
        cmds.select([mod for mod in modelList if 'eyeshell' in mod or 'eyeEdge' in mod], r=1)
        cmds.hyperShade(assign=newMat)
        for i in ['teeth', 'eye', 'head']:
            newMat = cmds.shadingNode('lambert', asShader=1, n=f'M_{i}Dna_lambert')
            newTex = cmds.shadingNode('file', asTexture=1, isColorManaged=1)
            cmds.setAttr(f'{newTex}.fileTextureName', f'{texPath}/T_{i}_D.PNG', type="string")
            cmds.connectAttr(f'{newTex}.outColor', f'{newMat}.color', f=1)
            matMod = [mod for mod in modelList if i in mod] if i != 'eye' \
                else [mod for mod in modelList if 'eyeLeft' in mod or 'eyeRight' in mod]
            cmds.select(matMod, r=1)
            cmds.hyperShade(assign=newMat)
    
    #####   Edit   #####
    def cleanScriptJob(self):
        self.highLightJointInChannleBox(False)
        if cmds.scriptJob(ex=self.DataSave_channleColorScriptJobId):
            cmds.scriptJob(kill=self.DataSave_channleColorScriptJobId)
            self.DataSave_channleColorScriptJobId = -1

    def resetAllGui(self):
        dnaReader = self.DataSave_DNAData['dnaReader']
        for i in range(dnaReader.getGUIControlCount()):
            cmds.setAttr(dnaReader.getGUIControlName(i), 0)
        cmds.setAttr('CTRL_L_nose_wrinkleUpper.ty', 1)
        cmds.setAttr('CTRL_R_nose_wrinkleUpper.ty', 1)
        cmds.treeView(self.uiVariable['Edit_controlTreeView'], e=1, cs=1)
        self.DataSave_controlTreeViewSelectItem['itemName'] = ''
        self.editUi_refreshBlendShapeTreeView([])
        self.editUi_refreshJointTreeView([])

    @timeStatistics
    def setGuiValue(self, multiplier):
        cmds.undoInfo(swf=0)
        try:
            animInfoList: list[guiAnimStruct] = self.DataSave_controlTreeViewSelectItem['animInfo']
            for i in animInfoList:
                if i.maxValue in (0.0, 1.0, -1.0) and i.minValue in (0.0, 1.0, -1.0):
                    onValue = i.maxValue if i.direction == 1 else i.minValue
                    value = onValue * multiplier
                else:
                    minValue = i.minValue
                    maxValue = i.maxValue
                    if i.direction == -1:
                        minValue, maxValue = maxValue, minValue
                    value = self.reRange(multiplier, minValue, maxValue, 0, 1)

                cmds.setAttr(f'{i.name}.{i.attr}', value)
        except Exception as e:
            om.MGlobal.displayError(f'SetGuiValue Error: {str(e)}')
        finally:
            cmds.undoInfo(swf=1)

    def checkSceneDnaNode(self) -> bool:
        lsNode = cmds.ls(typ="embeddedNodeRL4")
        if not lsNode:
            return False
        elif len(lsNode) > 1:
            cmds.framelessDialog(title='注意', message='场景中有多个Dna节点 请先清理', button=['已阅'], primary=['已阅'])
            return False
        if self.DataSave_DNAData['nodeName'] != lsNode[0]:   #dna节点有变化
            dnaPath = cmds.getAttr(f'{lsNode[0]}.dnaFilePath')
            self.DataSave_DNAData = {'nodeName': lsNode[0], 'filePath': dnaPath, 'dnaReader': self.loadDna(dnaPath)}
            return True
        return False

    def getGuiFromControl(self, dnaReader: dna.BinaryStreamReader, inControlIndexList):
        """
        return: [(index, guiName.Attr), ]
        """
        guiIndexList = []
        for gui, control in zip(dnaReader.getGUIToRawInputIndices(), dnaReader.getGUIToRawOutputIndices()):
            if control in inControlIndexList:
                guiIndexList.append((gui, dnaReader.getGUIControlName(gui)))
        return guiIndexList

    def getControlFromPSD(self, dnaReader: dna.BinaryStreamReader, inPsdIndex):
        """
        return: [controlIndex, ]
        """
        controlIndexList = []
        for psd, control in zip(dnaReader.getPSDRowIndices(), dnaReader.getPSDColumnIndices()):
            if psd == inPsdIndex:
                controlIndexList.append(control)
        return controlIndexList

    @timeStatistics
    def getJointFromControl(self, dnaReader: dna.BinaryStreamReader, inControlIndex, outDriver= False) -> list[jointDataStruct]:
        """
        return: jointDataStruct(index, jointName, effect, @outDriver)
        """
        jointList = []
        for i in range(1, dnaReader.getJointGroupCount()):
            if inControlIndex in dnaReader.getJointGroupInputIndices(i):
                for j in dnaReader.getJointGroupJointIndices(i):
                    jointDriver = self.getJointDriverFromControl(dnaReader, i, inControlIndex, j)
                    isEffect = True if jointDriver.count(0.0) != len(jointDriver) else False
                    if not outDriver:
                        jointList.append(jointDataStruct(index= j, name= dnaReader.getJointName(j), effect= isEffect))
                    else:
                        jointList.append(jointDataStruct(index= j, name= dnaReader.getJointName(j), effect= isEffect, allDriver= jointDriver))
        return jointList

    def getJointDriverFromControl(self, dnaReader: dna.BinaryStreamReader, inGroupIndex, inControlIndex, inJointIndex):
        """
        return: [tx, ty, tz, rx, ry, rz, sx, sy, sz]
        """
        controlList = dnaReader.getJointGroupInputIndices(inGroupIndex)
        controlNum = len(controlList)
        cListIndex = controlList.index(inControlIndex)
        jointAxisList = dnaReader.getJointGroupOutputIndices(inGroupIndex)
        valueList = dnaReader.getJointGroupValues(inGroupIndex)

        jointDriver = []
        for axisIndex in (inJointIndex*9+i for i in range(9)):
            if axisIndex in jointAxisList:
                driverValue = valueList[jointAxisList.index(axisIndex) * controlNum + cListIndex]
                jointDriver.append(round(driverValue, 8))
            else:
                jointDriver.append(0.0)
        return jointDriver
    
    @timeStatistics
    def getBlendShapeFromControl(self, dnaReader: dna.BinaryStreamReader, inControlIndex):   #[index, bsName]
        controlList = dnaReader.getBlendShapeChannelInputIndices()
        if inControlIndex in controlList:
            listIndex = controlList.index(inControlIndex)
            bsIndex = dnaReader.getBlendShapeChannelOutputIndices()[listIndex]
            return (bsIndex, dnaReader.getBlendShapeChannelName(bsIndex))

    @timeStatistics
    def getGuiAnimRangeFromControl(self, dnaReader: dna.BinaryStreamReader, inControlList):
        #guiAnimStruct = namedtuple("guiAnim", "name attr min max direction")
        animInfoList = []
        for i in zip(dnaReader.getGUIToRawInputIndices(), dnaReader.getGUIToRawOutputIndices(), 
                     dnaReader.getGUIToRawFromValues(), dnaReader.getGUIToRawToValues(), 
                     dnaReader.getGUIToRawSlopeValues()):   #dnaReader.getGUIToRawCutValues()
            if i[1] in inControlList:
                gui = dnaReader.getGUIControlName(i[0]).split('.')
                animInfoList.append(guiAnimStruct(gui[0], gui[1], i[2], i[3], 1 if i[4] >= 0 else -1))
        return animInfoList
    
    @timeStatistics
    def setJointDriver(self, dnaReader: dna.BinaryStreamReader, dnaWriter: dna.BinaryStreamWriter, jointDriverList):
        jointDriver: list[jointDriverStruct] = jointDriverList
        #groupDataStruct = namedtuple("groupData", "controlList jointAxisList valueList")
        groupDataList: list[groupDataStruct] = [None] * dnaReader.getJointGroupCount()

        for i in jointDriver:
            if not groupDataList[i.groupIndex]:
                groupDataList[i.groupIndex] = groupDataStruct(dnaReader.getJointGroupInputIndices(i.groupIndex), 
                                                              dnaReader.getJointGroupOutputIndices(i.groupIndex), 
                                                              dnaReader.getJointGroupValues(i.groupIndex))
            data: groupDataStruct = groupDataList[i.groupIndex]
            controlNum = len(data.controlList)
            cListIndex = data.controlList.index(i.controlIndex)

            for index, axisIndex in enumerate(i.jointIndex*9+n for n in range(9)):
                if axisIndex in data.jointAxisList:
                    valueIndex = data.jointAxisList.index(axisIndex) * controlNum + cListIndex
                    data.valueList[valueIndex] = i.offset[index]
        for index, data in enumerate(groupDataList):
            if data:
                dnaWriter.setJointGroupValues(index, data.valueList)

    def highLightJointInChannleBox(self, reset=True):
        slList = cmds.ls(sl=1, type='joint')
        axisList = ('TranslateX', 'TranslateY', 'TranslateZ', 'RotateX', 'RotateY', 'RotateZ', 'ScaleX', 'ScaleY', 'ScaleZ')
        if not slList or not reset:
            for i in axisList:
                cmds.channelBox('mainChannelBox', e=1, attrRegex=i, attrColor=(.696, .696, .696))
            return
        if slList[0] in self.DataSave_jointConnectInfo:
            for i in self.DataSave_jointConnectInfo[slList[0]]:
                cmds.channelBox('mainChannelBox', e=1, attrRegex=axisList[i], attrColor=(1.0, 0, 1.0))

    def reConnectDriver(self):
        for c in self.DataSave_jointConnectInfo['command']:
            cmds.connectAttr(c[0], c[1], f=1)

    def highLightJointInScence(self, mode):
        jointList = cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, children=1)
        activePanel = cmds.paneLayout('viewPanes', q=True, pane1=True)
        if mode:
            cmds.select(jointList + ['head_lod0_grp'], r=1)
            cmds.editor(activePanel, e=1, lockMainConnection=1, mainListConnection='activeList')
            cmds.isolateSelect(activePanel, s=1)
            cmds.select(cl=1)
            for i in jointList:
                if cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, itemAnnotation=1, it=i) == 'True':
                    cmds.setAttr(f'{i}.overrideEnabled', 1)
                    cmds.setAttr(f'{i}.overrideColor', 17)
        else:
            cmds.isolateSelect(activePanel, s=0)
            for i in jointList:
                if cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, itemAnnotation=1, it=i) == 'True':
                    cmds.setAttr(f'{i}.overrideEnabled', 0)

    def startEditJoint(self):
        jointList = cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, children=1)
        driverInfo = []
        if not jointList:
            om.MGlobal.displayError('没选择表情')
            return
        for j in jointList:
            self.DataSave_jointConnectInfo[j] = []
            for index, axis in enumerate(('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz')):
                getName = f'{j}.{axis}'
                connectInfo = cmds.listConnections(getName, c=0, d=0, p=1, t='embeddedNodeRL4')
                if connectInfo:
                    cmds.disconnectAttr(connectInfo[0], getName)
                    driverInfo.append((connectInfo[0], getName))
                    self.DataSave_jointConnectInfo[j].append(index)
        self.DataSave_jointConnectInfo['command'] = set(driverInfo)

        self.uiVariable['Edit_editScriptJobId'] = cmds.scriptJob(e=['SelectionChanged', lambda: self.highLightJointInChannleBox()], p=self.UiName)
        self.highLightJointInScence(True)
        self.editUi_switchEditVisible('Joint', True)

    def endEditJoint(self, mode):
        self.cleanScriptJob()
        if mode == 'apply':
            jointList = cmds.treeView(self.uiVariable['Edit_jointTreeView'], q=1, children=1)
            controlIndex = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=self.DataSave_controlTreeViewSelectItem['itemName'])
            dnaReader: dna.BinaryStreamReader = self.DataSave_DNAData['dnaReader']
            tempDnaPath = f'{os.getenv("TEMP")}/tempDnaFile.dna'
            dnaWriter: dna.BinaryStreamWriter = self.createDnaWriter(dnaReader, tempDnaPath, True)
            dnaJointNameList = [dnaReader.getJointName(i) for i in range(dnaReader.getJointCount())]

            jointDriverInfo = []
            #jointDriverStruct = namedtuple("jointDriver", "groupIndex controlIndex jointIndex offset")
            for i in jointList:
                jointIndex = dnaJointNameList.index(i)
                jointTOffset = self.list3Subtract(cmds.getAttr(f'{i}.t')[0], dnaReader.getNeutralJointTranslation(jointIndex))
                jointROffset = self.list3Subtract(self.list3Add(cmds.getAttr(f'{i}.r')[0], cmds.getAttr(f'{i}.jo')[0]), dnaReader.getNeutralJointRotation(jointIndex))
                jointSOffset = self.list3Subtract(cmds.getAttr(f'{i}.s')[0], (1.0, 1.0, 1.0))
                jointOffset = jointTOffset + jointROffset + jointSOffset
                for groupIndex in range(1, dnaReader.getJointGroupCount()):
                    if jointIndex in dnaReader.getJointGroupJointIndices(groupIndex):
                        break
                jointDriverInfo.append(jointDriverStruct(groupIndex, controlIndex, jointIndex, jointOffset))
            self.setJointDriver(dnaReader, dnaWriter, jointDriverInfo)
            self.saveDna(dnaWriter)
            self.saveFullDna(tempDnaPath)

        self.reConnectDriver()
        self.highLightJointInScence(False)
        self.highLightJointInChannleBox(False)
        self.editUi_switchEditVisible('Joint', False)

    def mirrorControlJoint(self, controlName, sideControlName):
        dnaReader = self.DataSave_DNAData['dnaReader']

        controlIndex = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=controlName)
        jointDict = {i.name: i for i in self.getJointFromControl(dnaReader, controlIndex, outDriver=True)}
        


        sideControlIndex = cmds.treeView(self.uiVariable['Edit_controlTreeView'], q=1, itemIndex=sideControlName)
        sideJointList = self.getJointFromControl(dnaReader, sideControlIndex)
        jointDriverInfo = []
        for j in sideJointList:
            if 'FACIAL_L' in j.name:
                sideName = j.name.replace('FACIAL_L', 'FACIAL_R')
            elif 'FACIAL_R' in j.name:
                sideName = j.name.replace('FACIAL_R', 'FACIAL_L')
            elif 'FACIAL_C' in j.name:
                sideName = j.name
            if sideName in jointDict:
                jointOffset = jointDict[sideName].allDriver
            for groupIndex in range(1, dnaReader.getJointGroupCount()):
                    if j.index in dnaReader.getJointGroupJointIndices(groupIndex):
                        break
            jointDriverInfo.append(jointDriverStruct(groupIndex, controlIndex, j.index, jointOffset))
        self.setJointDriver(dnaReader, dnaWriter, jointDriverInfo)


MetaHumanDnaTool().ToolUi()
