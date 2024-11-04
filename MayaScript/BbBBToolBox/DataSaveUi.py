# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om

import json

from BbBBToolBox.deps import pyperclip


class DataSaveUi():

    def ToolUi(self):
        Ver = 1.4
        self.UiN = 'DataSave_BlackCUi'
        UiN = self.UiN
        if cmds.window(UiN, q=1, ex=1):
            cmds.deleteUI(UiN)
        cmds.window(UiN, t='DataSave %s' %Ver, rtf=1, mb=1, tlb=1, wh=(250, 150))
        cmds.columnLayout('%s_MaincL' %UiN, cat=('both', 2), rs=2, cw=250, adj=1)
        cmds.rowLayout(nc=2, adj=1)
        cmds.text(l='', w=225)
        cmds.iconTextButton(i='addClip.png', w=20, h=20, c=lambda *args: self.addUiComponent())
        cmds.popupMenu()
        cmds.menuItem(l=u'粘贴/提取数据', c=lambda *args: self.checkData(None, 'Paste'))
        cmds.setParent('..')
        cmds.showWindow(UiN)
        self.ComponentData = {}
        self.addUiComponent()

    def addUiComponent(self):
        UiN = self.UiN
        uiNum = len(cmds.columnLayout('%s_MaincL' %UiN, q=1, ca=1))
        cmds.columnLayout('%s_ComponentcL%s' %(UiN, uiNum), p='%s_MaincL' %UiN, cat=('both', 2), rs=2, cw=240, adj=1)
        cmds.rowLayout(nc=2)
        cmds.button(l='Save', w=120)
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'名称(用于再次选择)', c=lambda *args: self.saveData('Name', uiNum))
        cmds.menuItem(l=u'位移和旋转(用于选择物体对位)', c=lambda *args: self.saveData('Position', uiNum))
        cmds.menuItem(l=u'中心位置(用于选择物体对位)', c=lambda *args: self.saveData('CenterPosition', uiNum))
        cmds.menuItem(l=u'物体蒙皮骨骼(用于再次选择)', c=lambda *args: self.saveData('SkinJoint', uiNum))
        cmds.menuItem(l=u'物体颜色(用于给其他物体上色)', c=lambda *args: self.saveData('ShapeColor', uiNum))
        cmds.menuItem(l=u'Bs节点连接(用于重连Bs节点控制)', c=lambda *args: self.saveData('ConnectBlendShape', uiNum))
        cmds.menuItem(l=u'材质赋予信息(用于提取材质信息 重新上材质)', c=lambda *args: self.saveData('MatRelevancyMesh', uiNum))
        cmds.button(l='Get', w=120, c=lambda *args: self.checkData(uiNum))
        cmds.popupMenu()
        cmds.menuItem(l=u'打印数据', c=lambda *args: self.checkData(uiNum, 'Print'))
        cmds.menuItem(l=u'复制数据', c=lambda *args: self.checkData(uiNum, 'Copy'))
        cmds.menuItem(l=u'存储数据', c=lambda *args: self.checkData(uiNum, 'Save'))
        cmds.setParent('..')
        cmds.text('%s_ComponentText%s' %(UiN, uiNum), l='')
        cmds.popupMenu()
        cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.columnLayout('%s_ComponentcL%s' %(UiN, uiNum), e=1, vis=0))
        #cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.deleteUI('%s_ComponentcL%s' %(UiN, uiNum), lay=1))
        # 直接deleteUI时，导致数量和序号不匹配。再次添加时如果报错，Maya可能直接崩。

    def saveData(self, Type, uiNum):
        """
        保存数据
        """
        def _Name():
            slList = cmds.ls(sl=1)
            if not slList:
                return
            self.ComponentData['Data%s' %uiNum] = slList
            return 1

        def _Position():
            slList = cmds.ls(sl=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            _temploc_ = cmds.spaceLocator()
            cmds.matchTransform(_temploc_, slList[0], pos=1, rot=1)
            self.ComponentData['Data%s' %uiNum] = [cmds.xform(_temploc_, q=1, ws=1, t=1), cmds.xform(_temploc_, q=1, ws=1, ro=1)]
            cmds.delete(_temploc_)
            return 1

        def _CenterPosition():
            slList = cmds.ls(sl=1, fl=1)
            if not slList:
                return
            _tempobj_ = []
            if len(cmds.ls(slList, typ='transform')) == len(slList):   #簇点对Locator无效
                for i in slList:
                    _temp_ = cmds.polyCube(ch=0)[0]
                    _tempobj_.append(_temp_)
                    cmds.matchTransform(_temp_, i, pos=1, rot=1)
                _tempclu_ = cmds.cluster(_tempobj_)[1]
            else:
                _tempclu_ = cmds.cluster()[1]
            self.ComponentData['Data%s' %uiNum] = cmds.getAttr('%sShape.origin' %_tempclu_)[0]
            cmds.delete(_tempclu_, _tempobj_)
            return 1

        def _SkinJoint():
            slList = cmds.ls(sl=1, o=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            jointlist = cmds.skinCluster(slList, q=1, inf=1)
            self.ComponentData['Data%s' %uiNum] = jointlist
            return 1

        def _ShapeColor():
            slList = cmds.ls(sl=1, o=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            objShape = cmds.listRelatives(slList, c=1, s=1)
            if not objShape:
                if not cmds.ls(slList, typ='joint'):
                    return
                objShape = slList
            self.ComponentData['Data%s' %uiNum] = [cmds.getAttr("%s.overrideEnabled" %objShape[0]),
                                                    cmds.getAttr("%s.overrideRGBColors" %objShape[0]),
                                                    cmds.getAttr("%s.overrideColor" %objShape[0]),
                                                    cmds.getAttr("%s.overrideColorRGB" %objShape[0])[0]]
            return 1

        def _ConnectBlendShape():
            slbs = cmds.ls(sl=1, typ='blendShape')
            if not slbs:
                cmds.warning(u'没选blendShape鸭')
                return
            data = []
            for i in cmds.getAttr('%s.w' %slbs[0], mi=1):
                InInfo = cmds.listConnections('%s.w[%s]' %(slbs[0], i), c=1, d=0, p=1, scn=1, s=1)
                if InInfo:
                    data.append([InInfo[1], InInfo[0]])
                OutInfo = cmds.listConnections('%s.w[%s]' %(slbs[0], i), c=1, d=1, p=1, scn=1, s=0)
                if OutInfo:
                    for attr in OutInfo[1::2]:
                        data.append([OutInfo[0], attr])
            self.ComponentData['Data%s' %uiNum] = data
            return 1

        def _MatRelevancyMesh():
            data = []
            allMat = set(cmds.listConnections('defaultShaderList1'))
            for i in cmds.ls(sl=1):
                if i in allMat:
                    cmds.hyperShade(objects=i)
                    slmesh = cmds.polyListComponentConversion(ff=1, fv=1, fe=1, fuv=1, fvf=1, tf=1)
                    if slmesh:
                        data.append([i, slmesh])
                else:
                    cmds.warning(u'%s不是材质球' %i)
            self.ComponentData['Data%s' %uiNum] = data
            return 1

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        UiN = self.UiN
        if Type == 'Name':
            if _Name():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 名称')
        elif Type == 'Position':
            if _Position():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 位移和旋转')
        elif Type == 'CenterPosition':
            if _CenterPosition():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 中心位置')
        elif Type == 'SkinJoint':
            if _SkinJoint():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 蒙皮骨骼')
        elif Type == "ShapeColor":
            if _ShapeColor():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 物体颜色')
        elif Type == "ConnectBlendShape":
            if _ConnectBlendShape():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 BlendShape连接')
        elif Type == "MatRelevancyMesh":
            if _MatRelevancyMesh():
                cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 材质赋予信息')
        
    def checkData(self, uiNum, mode=None):
        """
        模式和数据判断 保存数据到剪切板
        """
        if mode == 'Paste':
            sl = cmds.ls(sl=1)
            if sl and cmds.ls('%s.SaveData_BbBB' %sl[0]):
                #从Maya提取
                _Data = cmds.getAttr('%s.SaveData_BbBB' %sl[0])
            else:
                #从剪切板粘贴
                _Data = pyperclip.paste()

            try:
                pasteData = json.loads(_Data)
                self.getData(pasteData['type'], pasteData['data'])
            except (json.decoder.JSONDecodeError, KeyError):
                om.MGlobal.displayError(u'没有复制临时数据')
        elif mode == 'Print':
            mel.eval("ScriptEditor;")
            print("#Data#:\n", self.ComponentData['Data%s' %uiNum])
        else:
            typString = cmds.text('%s_ComponentText%s' %(self.UiN, uiNum), q=1, l=1)
            if not 'Data%s' %uiNum in self.ComponentData:
                return
            data = self.ComponentData['Data%s' %uiNum]
            if not data or not typString:
                return

            if mode == 'Copy':
                pyperclip.copy(json.dumps({'type': typString, 'data': data}))
                print(u'复制成功')
            elif mode == 'Save':
                sl = cmds.ls(sl=1)
                if sl:
                    if not cmds.ls('%s.SaveData_BbBB' %sl[0]):
                        cmds.addAttr(sl[0], ln='SaveData_BbBB', dt='string')
                    cmds.setAttr('%s.SaveData_BbBB' %sl[0], json.dumps({'type': typString, 'data': data}), type='string')
                print(u'储存成功')
            else:
                self.getData(typString, data)
        

    def getData(self, typString, data):
        """
        获取数据
        """
        def _Name(data):
            cmds.select(data, add=1)

        def _Position(data):
            slList = cmds.ls(sl=1)
            if not slList:
                return
            _temploc_ = cmds.spaceLocator()[0]
            cmds.xform(_temploc_, ws=1, t=data[0], ro=data[1])
            for i in slList:
                cmds.matchTransform(i, _temploc_, pos=1, rot=1)
            cmds.delete(_temploc_)

        def _CenterPosition(data):
            slList = cmds.ls(sl=1)
            if not slList:
                return
            _temploc_ = cmds.spaceLocator()[0]
            cmds.setAttr('%s.t' %_temploc_, data[0], data[1], data[2])
            for i in slList:
                cmds.matchTransform(i, _temploc_, pos=1)
            cmds.delete(_temploc_)

        def _SkinJoint(data):
            cmds.select(data, r=1)

        def _ShapeColor(data):
            slList = cmds.ls(sl=1)
            for i in slList:
                objShape = cmds.listRelatives(i, c=1, s=1)
                if not objShape:
                    if not cmds.ls(i, typ='joint'):
                        continue
                    objShape = i
                for s in objShape:
                    cmds.setAttr("%s.overrideEnabled" %s, data[0])
                    cmds.setAttr("%s.overrideRGBColors" %s, data[1])
                    if data[1]:
                        cmds.setAttr("%s.overrideColorRGB" %s, data[3][0], data[3][1], data[3][2])
                    else:
                        cmds.setAttr("%s.overrideColor" %s, data[2])

        def _ConnectBlendShape(data):
            slbs = cmds.ls(sl=1, type='blendShape')
            if slbs:
                for i in data:
                    try:
                        cmds.connectAttr(i[0], '%s.%s' %(slbs[0], i[1].split('.')[-1]), f=1)
                    except Exception as e:
                        print(e)
            else:
                cmds.warning(u'未选择Bs节点 将使用储存的Bs名称')
                for i in data:
                    try:
                        cmds.connectAttr(i[0], i[1], f=1)
                    except Exception as e:
                        print(e)

        def _MatRelevancyMesh(data):
            for i in data:
                if cmds.ls(i[0]) and cmds.ls(i[1]):
                    cmds.select(i[1], r=1)
                    cmds.hyperShade(assign=i[0])
                else:
                    cmds.warning(u'材质%s或模型%s不存在 已跳过' %(i[0], i[1]))

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++
        if typString == u'已储存 名称':
            _Name(data)
        elif typString == u'已储存 位移和旋转':
            _Position(data)
        elif typString == u'已储存 中心位置':
            _CenterPosition(data)
        elif typString == u'已储存 蒙皮骨骼':
            _SkinJoint(data)
        elif typString == u'已储存 物体颜色':
            _ShapeColor(data)
        elif typString == u'已储存 BlendShape连接':
            _ConnectBlendShape(data)
        elif typString == u'已储存 材质赋予信息':
            _MatRelevancyMesh(data)
        
#DataSaveUi().ToolUi()
