# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from .pyside import QtWidgets, shiboken

from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om, OpenMayaAnim as omAni

import os
import json

try:
    import ngSkinTools2.api as ng2api
except:
    pass

from .Utils import BoxQtStyle
from .DisplayYes import DisplayYes


class ngSk2Weight_BbBB():

    def __init__(self):
        self.Ui = 'ngSk2Weight_Ui'

    def ToolUi(self, layout=0):
        if not ngUtils_BbBB.pluginCheck():
            om.MGlobal.displayError(u'这个Maya中缺少ng2插件, 无法使用!')
            return
        Ver = 0.8
        if cmds.window(self.Ui, q=1, ex=1):
            cmds.deleteUI(self.Ui)
        if not layout:
            cmds.window(self.Ui, t='ngSk2Weight', rtf=1, mb=1, tlb=1, bgc=BoxQtStyle.backgroundMayaColor)
        cmds.columnLayout('%s_MainCL' %self.Ui, cat=('both', 2), rs=1, cw=420)
        cmds.rowLayout(nc=2, h=28, cw2=(200, 150), co2=(5, 20), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        cmds.optionMenu('%s_TemplateMenu' %self.Ui, l=u'模板 ', mvi=6)
        self.DataLoc = '%s/data/ngSk2Weight/' %cmds.moduleInfo(p=1, mn='BbBBToolBox')
        if os.path.isdir(self.DataLoc):
            fileList = os.listdir(self.DataLoc)
            if fileList:
                for i in fileList:
                    fileSplit = i.rsplit('.')
                    if fileSplit[1] == 'json':
                        cmds.menuItem(l=fileSplit[0])
        cmds.rowLayout(nc=2, h=28)
        cmds.checkBox('%s_maxInfluencesCB' %self.Ui, l=u'最大影响值', v=1)
        cmds.intField('%s_maxInfluencesNum' %self.Ui, v=8, w=28)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowLayout(nc=2, h=28)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'临时身体模板', w=210, c=lambda *args: self.tempSelectJointUi()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'运行', w=210, c=lambda *args: self.doIt()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.popupMenu()
        cmds.menuItem('%s_objHaveSkin' %self.Ui, cb=0, l=u'模型已有蒙皮')
        cmds.menuItem('%s_smoothSkin' %self.Ui, cb=0, l=u'运行时Smooth权重')
        cmds.setParent('..')

        cmds.rowLayout(nc=2, cw2=(210, 210), co2=(2, 2), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'快速创建层', bgc=BoxQtStyle.accentMayaColor())
        cmds.columnLayout(cat=('both', 2), rs=2, adj=1)
        cmds.textFieldButtonGrp('%s_selectObj' %self.Ui, bl=u'选择', columnAlign=[1, 'center'], adj=2, cw3=[50, 110, 50], ed=0, bc=lambda *args: _selectObj(), l=u'选择模型')
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'创建', c=lambda *args: self.slJointCreateNgLayer(cmds.textFieldButtonGrp('%s_selectObj' %self.Ui, q=1, tx=1)))
            )), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'复制粘贴权重', bgc=BoxQtStyle.accentMayaColor())
        cmds.columnLayout(cat=('both', 2), rs=2, adj=1)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'复制点权重', c=lambda *args: self.copyVtxWeight()))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.rowLayout(nc=2)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'粘贴选择层', w=93, c=lambda *args: self.pasteVtxWeight(1)))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l=u'粘贴全部层', w=93, c=lambda *args: self.pasteVtxWeight(0)))), QtWidgets.QPushButton).setStyleSheet(BoxQtStyle.QButtonStyle(height=26))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        def _selectObj():
            sllist = cmds.ls(sl=1, typ='transform')
            if sllist:
                if not ng2api.target_info.get_related_skin_cluster(sllist[0]):
                    om.MGlobal.displayError(u'模型上没得蒙皮')
                    return
                cmds.textFieldButtonGrp('%s_selectObj' %self.Ui, e=1, tx=sllist[0])

        if not layout:
            #cmds.frameLayout('%s_smoothQuickL' %self.Ui, cll=1, cl=1, mw=5, l=u'Smooth', cc=lambda *args: foldSmoothPage(1), ec=lambda *args: foldSmoothPage(0))
            cmds.showWindow(self.Ui)
        

    """
        def foldSmoothPage(sate):
            if sate:
                cmds.window(self.Ui, e=1, rtf=1, wh=(240, 118))
            else:
                sllist = cmds.ls(sl=1)
                if not sllist:
                    om.MGlobal.displayError(u'什么都没选, 做咩啊')
                    return
                clusterName = ng2api.target_info.get_related_skin_cluster(sllist[0])
                if not clusterName:
                    om.MGlobal.displayError(u'模型上没得蒙皮, 做咩啊')
                    return
                if not cmds.listConnections('%s.message' %clusterName, d=1, t='ngst2SkinLayerData'):
                    om.MGlobal.displayError(u'模型上没有Ng数据, smooth功能不可用')
                    return
                objLayers = ng2api.Layers(clusterName)
                objAllLayer = objLayers.list()
                
                for i in objAllLayer:
                    if i.name == 'assignBase' or not ngUtils_BbBB.get_LayerWeights(i, 'mask'):
                        continue
                    cmds.radioButton(l=i.name, h=22)
                    if len(i.get_used_influences()) != 1:
                        cmds.radioButton(l=u'%s子骨骼' %i.name, h=22)
                cmds.button(l=u'< 反Smooth', h=25, c=lambda *args: self.floodLayerWeight(0, objAllLayer))
                cmds.button(l=u'Smooth >', h=25, c=lambda *args: self.floodLayerWeight(1, objAllLayer))
                #cmds.button(l=u'镜像权重', h=25, c=lambda *args: self.mirrorLayerWeight(clusterName, objAllLayer))
                cmds.button(l=u'删除NG节点', h=25, c=lambda *args: self.finishUseNg(clusterName))

    def floodLayerWeight(self, mode, objAllLayer):
        slLayer = cmds.radioButton(cmds.radioCollection('%s_smoothLayerRC' %self.Ui, q=1, sl=1), q=1, l=1)
        FloodSettings = ngUtils_BbBB.create_FloodSettings()
        FloodSettings.influences_limit = cmds.intField('%s_maxInfluencesNum' %self.Ui, q=1, v=1) if cmds.checkBox('%s_maxInfluencesCB' %self.Ui, q=1, v=1) else 0
        #FloodSettings.limit_to_component_selection = cmds.checkBox('%s_limitSelectComponentCB' %self.Ui, q=1, v=1)
        if mode:
            FloodSettings.mode = ng2api.PaintMode.smooth
            FloodSettings.intensity = 0.8
            FloodSettings.iterations = 2
        else:
            FloodSettings.mode = ng2api.PaintMode.sharpen
            FloodSettings.intensity = 0.1
        
        if u'子骨骼' in slLayer:
            for i in objAllLayer:
                if i.name == slLayer.rsplit(u'子骨骼')[0]:
                    break
            ng2api.flood_weights(i, settings=FloodSettings)
        else:
            for i in objAllLayer:
                if i.name == slLayer:
                    break
            ng2api.flood_weights(i, influence='mask', settings=FloodSettings)
    
    def mirrorLayerWeight(self, clusterName, objAllLayer):
        #for i in objAllLayer:
        cmds.ngst2Layers(clusterName, mirrorLayerWeights=1, mirrorLayerMask=1, mirrorLayerDq=0, mirrorDirection=1)

    def finishUseNg(self, clusterName):
        if cmds.confirmDialog(t='Confirm', m=u'确定不在需要使用Smooth了吗, 此操作将删除ng节点', b=['Yes', 'No'], db='Yes', cb='No', ds='No') == 'Yes':
            ng2api.export_json(clusterName, '%s/ngWeight_%s_%s.json' 
                                %(os.getenv('TEMP'), os.path.basename(cmds.file(q=1, sn=1)), cmds.listConnections('%s.outputGeometry' %clusterName, s=0)[0]))
            cmds.delete([i for i in cmds.listHistory(clusterName, future=1, levels=1) if cmds.nodeType(i) in ['ngst2MeshDisplay', 'ngst2SkinLayerData']])
    """

    def tempSelectJointUi(self):
        TUi = '%s_tempSelectJointdoIt_Ui' %self.Ui
        tempSelectDirt = {
            "Mirror": "_L/_R",
            "LayersOrder": ["Body", "Hip", "Knee", "Foot", "Scapula", "Shoulder", "Elbow", "Hand", "IndexFinger", "MiddleFinger", "RingFinger", "PinkyFinger", "ThumbFinger", "Neck", "Head"],
            "WeightOrder": [["Hip", "Knee", "Foot"], ["Scapula", "Shoulder", "Elbow", "Hand", {"Finger": ["IndexFinger", "MiddleFinger", "RingFinger", "PinkyFinger", "ThumbFinger"]}], ["Neck", "Head"]],
            "Layers": {}
        }
        if cmds.window(TUi, q=1, ex=1):
            cmds.deleteUI(TUi)
        cmds.window(TUi, t=u'临时选择骨骼处理权重', rtf=1, mb=1, tlb=1, wh=(240, 240))
        cmds.columnLayout('%s_MainCL' %TUi, cat=('both', 2), rs=1, cw=230, adj=1)
        
        def select(args):
            if type(args) == int:
                if args == 0:
                    tempSelectDirt['Mirror'] = cmds.textFieldGrp(LayerUi[0], q=1, tx=1)
                elif args == 1:
                    sllist = cmds.ls(sl=1, typ='joint')
                    if sllist:
                        tempSelectDirt["RootJoint"] = sllist[0]
                        cmds.textFieldButtonGrp(LayerUi[1], e=1, tx=sllist[0])
            else:
                sllist = cmds.ls(sl=1, typ='joint')
                tempSelectDirt['Layers'][args] = sllist
                cmds.textFieldButtonGrp('%s_Layer%s' %(TUi, args), e=1, tx=str(sllist))
        
        LayerUi = ['%s_LayerMirror' %TUi, '%s_LayerRootJoint' %TUi,
            '%s_LayerBody' %TUi, '%s_LayerHip' %TUi, '%s_LayerKnee' %TUi, '%s_LayerFoot' %TUi, 
            '%s_LayerScapula' %TUi, '%s_LayerShoulder' %TUi, '%s_LayerElbow' %TUi, '%s_LayerHand' %TUi, 
            '%s_LayerIndexFinger' %TUi, '%s_LayerMiddleFinger' %TUi, '%s_LayerRingFinger' %TUi, '%s_LayerPinkyFinger' %TUi, '%s_LayerThumbFinger' %TUi,
            '%s_LayerNeck' %TUi, '%s_LayerHead' %TUi
        ]
        cw3 = [75, 150, 70]
        cmds.textFieldGrp(LayerUi[0], columnAlign=[1, 'center'], cw2=cw3[:2], l=u'镜像标签', tx=u'_L/_R', tcc=lambda *args: select(0))
        cmds.textFieldButtonGrp(LayerUi[1],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select(1), l='RootJoint', pht=u'根骨骼')
        cmds.textFieldButtonGrp(LayerUi[2],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Body'), l='Body', pht=u'躯干')
        cmds.textFieldButtonGrp(LayerUi[3],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Hip'), l='Hip', pht=u'大腿')
        cmds.textFieldButtonGrp(LayerUi[4],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Knee'), l='Knee', pht=u'膝盖')
        cmds.textFieldButtonGrp(LayerUi[5],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Foot'), l='Foot', pht=u'脚')
        cmds.textFieldButtonGrp(LayerUi[6],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Scapula'), l='Scapula', pht=u'锁骨')
        cmds.textFieldButtonGrp(LayerUi[7],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Shoulder'), l='Shoulder', pht=u'手臂')
        cmds.textFieldButtonGrp(LayerUi[8],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Elbow'), l='Elbow', pht=u'手肘')
        cmds.textFieldButtonGrp(LayerUi[9],  bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Hand'), l='Hand', pht=u'手')
        cmds.textFieldButtonGrp(LayerUi[10], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('IndexFinger'), l='IndexFinger', pht=u'食指')
        cmds.textFieldButtonGrp(LayerUi[11], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('MiddleFinger'), l='MiddleFinger', pht=u'中指')
        cmds.textFieldButtonGrp(LayerUi[12], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('RingFinger'), l='RingFinger', pht=u'无名指')
        cmds.textFieldButtonGrp(LayerUi[13], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('PinkyFinger'), l='PinkyFinger', pht=u'小指')
        cmds.textFieldButtonGrp(LayerUi[14], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('ThumbFinger'), l='ThumbFinger', pht=u'拇指')
        cmds.textFieldButtonGrp(LayerUi[15], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Neck'), l='Neck', pht=u'脖子')
        cmds.textFieldButtonGrp(LayerUi[16], bl=u'选择', columnAlign=[1, 'center'], cw3=cw3, adj=2, ed=0, 
                                    bc=lambda *args: select('Head'), l='Head', pht=u'头')

        cmds.text(h=5, l='')
        cmds.button(l=u'运行', c=lambda *args: self.doIt(tempSelDirt=tempSelectDirt))
        cmds.showWindow(TUi)
        cmds.window(TUi, e=1, rtf=1, wh=(240, 240))

    def doIt(self, tempSelDirt=None):
        sllist = cmds.ls(sl=1, typ='transform')
        if not sllist:
            om.MGlobal.displayError(u'什么都没选, 做咩啊')
            return

        if tempSelDirt:   #tempui
            self.TemplateData = tempSelDirt
        else:
            filePath = os.path.normpath('%s%s.json' %(self.DataLoc, cmds.optionMenu('%s_TemplateMenu' %self.Ui, q=1, v=1)))
            if not os.path.isfile(filePath):
                om.MGlobal.displayError(u'选择的模板不存在')
                return
            with open(filePath, "r") as jsFile:
                self.TemplateData = json.loads(jsFile.read())
            #with open(, 'w') as jsFile:   #写入json
            #    json.dump(jsonDirt, jsFile, indent=4)   #sort_keys=1 排序
        jsRootJoint = self.TemplateData['RootJoint']
        if not cmds.ls(jsRootJoint, typ='joint'):
            om.MGlobal.displayError(u'没找到指定的根骨骼, 当前骨架跟选择模板不匹配')
            return
        objHaveSkin = cmds.menuItem('%s_objHaveSkin' %self.Ui, q=1, cb=1) if 'extractWeight' not in self.TemplateData else self.TemplateData['extractWeight']
        clusterName = ng2api.target_info.get_related_skin_cluster(sllist[0])
        if clusterName and not objHaveSkin:
            om.MGlobal.displayError(u'模型已经有蒙皮了, 请检查')
            return
        elif not clusterName and objHaveSkin:
            om.MGlobal.displayError(u'模型上没有蒙皮, 请检查')
            return

        cmds.select(jsRootJoint, hi=1)
        cmds.select(cmds.ls(sl=1, type='joint'), r=1)

        if tempSelDirt:   #tempui
            self.sortFirstJointList()
        self.stuffJointList()
        heatMapLayer = None
        if not objHaveSkin:
            heatMapLayer = self.bindSkin(sllist[0])
            clusterName = ng2api.target_info.get_related_skin_cluster(sllist[0])
        ngPath_Index = self.setJointWeight_createLayer(clusterName)
        self.replaceIssueJoint(heatMapLayer, ngPath_Index)
        self.setMaskWeight(heatMapLayer)
        if cmds.menuItem('%s_smoothSkin' %self.Ui, q=1, cb=1):
            self.layersFloodWeight()
        cmds.select(sllist, r=1)
        DisplayYes().showMessage(u'处理完成!')
    
    def sortFirstJointList(self):
        """
        骨骼列表排序
        """
        #入参
        dataLayers = self.TemplateData['Layers']

        for item in dataLayers:
            parentList = []
            for j in dataLayers[item]:
                if not cmds.listRelatives(j, p=1)[0] in dataLayers[item]:
                    parentList.append(j)
            for i1 in parentList:
                longName = cmds.ls(i1, l=1)[0].rsplit('|', 1)[0]
                for i2 in parentList:
                    if not i2 in longName:
                        parentJoint = i2
                        break
                else:   #break多个循环: 里循环未发生braek 则正常执行外else, 否则触发外break
                    continue
                break
            dataLayers[item].remove(parentJoint)
            dataLayers[item].insert(0, parentJoint)

    def stuffJointList(self):
        """
        骨骼列表补全(镜像、中间骨)
        """
        #入参
        dataLayers = self.TemplateData['Layers']
        mirror = self.TemplateData['Mirror']
        
        mirror = mirror.split('/') if '/' in mirror else 0
        stuffLayers = {}

        def multipleSplit(rangeName):
            if mirror and mirror[0] in joint:
                for i in cmds.ls(rangeName, sl=1):
                    stuffLayers[item][0].append(i)
                    stuffLayers[item][1].append(i.replace(mirror[0], mirror[1]))
            else:
                for i in cmds.ls(rangeName, sl=1):
                    stuffLayers[item][0].append(i)

        for item in dataLayers:
            stuffLayers[item] = [[], []]
            for joint in dataLayers[item]:
                split = joint.split('*')
                if len(split) == 1:
                    if cmds.ls(joint, sl=1):
                        stuffLayers[item][0].append(joint)
                        if mirror and mirror[0] in joint:
                            stuffLayers[item][1].append(joint.replace(mirror[0], mirror[1])) 
                elif len(split) == 2:
                    multipleSplit(['%s%s%s' %(split[0], n, split[1]) for n in range(40)])
                elif len(split) == 3:
                    multipleSplit(['%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2]) for n2 in range(40) for n1 in range(40)])
                elif len(split) == 4:
                    multipleSplit(['%s%s%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2], n3, split[3]) 
                                    for n3 in range(20) for n2 in range(20) for n1 in range(20)])
                elif len(split) == 5:
                    multipleSplit(['%s%s%s%s%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2], n3, split[3], n4, split[4]) 
                                    for n4 in range(20) for n3 in range(20) for n2 in range(20) for n1 in range(20)])
        #出参
        self.TemplateData['Layers'] = stuffLayers

    def bindSkin(self, slobj):
        """
        对指定物体蒙皮
        """
        #入参
        dataLayers = self.TemplateData['Layers']

        heatMapSkinMesh = cmds.duplicate(slobj, rr=1, n="__tempHeatMapSkin__Mesh")[0]
        assignJointList = []
        for key, value in dataLayers.items():
            assignJointList += value[0] + value[1]
        cmds.skinCluster(assignJointList, slobj, tsb=1, dr=4)
        try:
            cmds.skinCluster(assignJointList, heatMapSkinMesh, tsb=1, bm=2, hmf=0.8, mi=1, nw=1)
            clusterName = ng2api.target_info.get_related_skin_cluster(heatMapSkinMesh)
        except RuntimeError as Argument:
            if Argument.args[0] == 'Maya command error':   #报错信息
                cmds.confirmDialog(t=u'提醒', icn='warning', m=u'此模型不支持热度贴图蒙皮，将使用体素蒙皮。最终效果可能会降低', b='Ok', db='Ok', cb='Ok', ds='Ok')
                cmds.skinCluster(assignJointList, heatMapSkinMesh, tsb=1, bm=3, hmf=0.8, mi=1, nw=1)
                clusterName = ng2api.target_info.get_related_skin_cluster(heatMapSkinMesh)
                cmds.geomBind(clusterName, bm=3, fo=0.3, mi=1)
        else:
            layers = ng2api.init_layers(clusterName)
            return layers.add("heatMap")
        
    def setJointWeight_createLayer(self, skinCluster):
        """
        创建层 分权重
        """
        #入参
        dataLayers = self.TemplateData['Layers']
        dataLayersOrder = self.TemplateData['LayersOrder']
        extractWeight = self.TemplateData['extractWeight'] if 'extractWeight' in self.TemplateData else False

        layers = ng2api.init_layers(skinCluster)
        #layers = ng2api.Layers("")   #已存在数据层的skinCluster
        layerList = [layers.add("assignBase")]   #初始化后马上加层 才能继承maya权重
        layers.prune_weights_filter_threshold = 0.001
        layerJointPathIndex = ng2api.target_info.list_influences(skinCluster)   #获取骨骼在ng层内的信息
        ngPath_Index = []
        for i in layerJointPathIndex:
            ngPath_Index.extend([i.path.rsplit('|', 1)[1], i.logicalIndex])   #path 完整路径, logicalIndex 层内顺序
        for i in dataLayersOrder:
            _jointInLayerIndex = []
            layerList.append(layers.add(i))
            for joint in dataLayers[i][0]:   #dataLayers数据结构为'LayerName': [[Joint], [JointMirror]]
                _jointInLayerIndex.append(ngPath_Index[ngPath_Index.index(joint) + 1])   #查询层内骨骼的对应编号
            ng2api.assign_from_closest_joint(skinCluster, layerList[-1], _jointInLayerIndex)   #分权重
            if extractWeight:
                for joint in dataLayers[i][0]:
                    _jointIndex = ngPath_Index[ngPath_Index.index(joint) + 1]
                    _assignWeight = ngUtils_BbBB.get_LayerWeights(layerList[-1], _jointIndex)
                    _jointWeight = ngUtils_BbBB.get_LayerWeights(layerList[0], _jointIndex)
                    for w in range(len(_jointWeight)):
                        if not _jointWeight[w]:
                            _jointWeight[w] = _assignWeight[w]
                    layerList[-1].set_weights(_jointIndex, _jointWeight, undo_enabled=0)
                ng2api.fill_transparency(layerList[-1])
        if not extractWeight:
            ng2api.assign_from_closest_joint(skinCluster, layerList[0], ngPath_Index[1::2])   #Base层分权重
        ng2api.flood_weights(layerList[1], influence='mask')   #第二层Mask设为1权重
        #出参
        self.TemplateData['ngLayerList'] = layerList
        return ngPath_Index   #骨骼和对应编号

    def replaceIssueJoint(self, heatMapLayer, ngPath_Index):
        """
        替换有问题的骨骼权重
        """
        if 'Issue' not in self.TemplateData or 'JointWeight' not in self.TemplateData['Issue']:
            return
        #入参
        layerList = self.TemplateData['ngLayerList']
        dataLayers = self.TemplateData['Layers']
        dataIssueJoint = self.TemplateData['Issue']['JointWeight']
        dataLayersOrder = self.TemplateData['LayersOrder']
        
        for i in dataIssueJoint:
            for key, value in dataLayers.items():
                if i in value[0]:
                    layerIndex = dataLayersOrder.index(key) + 1
                    jointIndex = ngPath_Index[ngPath_Index.index(i) + 1]
                    if heatMapLayer:
                        layerList[layerIndex].set_weights(jointIndex, ngUtils_BbBB.get_LayerWeights(heatMapLayer, jointIndex), undo_enabled=0)
                    else:
                        layerList[layerIndex].set_weights(jointIndex, ngUtils_BbBB.get_LayerWeights(layerList[0], jointIndex), undo_enabled=0)
                    ng2api.fill_transparency(layerList[layerIndex])
                    break
        
    def setMaskWeight(self, heatMapLayer):
        """
        根据热度贴图权重设置层影响范围
        """
        #入参
        layerList = self.TemplateData['ngLayerList']
        dataLayersOrder = self.TemplateData['LayersOrder']
        dataWeightOrder = self.TemplateData['WeightOrder']

        #vertexNum = cmds.polyEvaluate(v=1) 获取模型点数
        def addListValue(inWeight):
            _addWeightList = []   #[0] *Num 创建指定数值列表
            for i in inWeight:
                _addWeightList = [v1 + v2 for v1, v2 in zip(_addWeightList, i)] if _addWeightList else i
            return _addWeightList

        def addLayerValue(layerIndex):   #累加指定层内所有骨骼权重
            _layerJointNum = layerList[layerIndex].get_used_influences()
            #热度贴图蒙皮问题，最后一节骨骼没有权重
            if heatMapLayer:   #如有热度蒙皮，则取热度蒙皮权重，最后一根骨骼用ng权重进行过滤
                _addHeatMapWeightList = []
                for indexList, index in enumerate(_layerJointNum):
                    if len(_layerJointNum) == 1: #如果本层只有一个骨骼 -> 且该骨骼没有权重，则返回Base层的权重
                        result = ngUtils_BbBB.get_LayerWeights(heatMapLayer, index)
                        return ngUtils_BbBB.get_LayerWeights(layerList[0], index) if not result else result
                    if indexList == len(_layerJointNum) - 1:   #最后一个骨骼 进行权重整理
                        # 如果v3(Base层)有权重 > 而且v1(此层已循环骨骼的热度贴图权重之和)或v2(此层当前骨骼的热度贴图权重)之中有一个是有权重的，则这个点在范围内
                        # 如果v3(Base层)没有权重, 但v1是有权重的, 则这个点在范围内
                        # 如果v3(Base层)没有权重, 而且v1也没有权重, 则这个点不在范围内
                        _addHeatMapWeightList = [1 if v3 and v1 or v2 else 1 if v1 else 0 for v1, v2, v3 in 
                                zip(_addHeatMapWeightList, ngUtils_BbBB.get_LayerWeights(heatMapLayer, index), ngUtils_BbBB.get_LayerWeights(layerList[0], index))]
                    else:
                        _addHeatMapWeightList = [v1 + v2 for v1, v2 in zip(_addHeatMapWeightList, ngUtils_BbBB.get_LayerWeights(heatMapLayer, index))] \
                                                                    if _addHeatMapWeightList else ngUtils_BbBB.get_LayerWeights(heatMapLayer, index)   #相同代码 减少占用
                return _addHeatMapWeightList
            else:
                _addngWeightList = []
                for indexList, index in enumerate(_layerJointNum):
                    _addngWeightList = [v1 + v2 for v1, v2 in zip(_addngWeightList, ngUtils_BbBB.get_LayerWeights(layerList[0], index))] \
                                                            if _addngWeightList else ngUtils_BbBB.get_LayerWeights(layerList[0], index)   #相同代码 减少占用
                return _addngWeightList

        for l1 in reversed(dataWeightOrder):   #肢体块
            saveLayerWeight = []
            for l2 in reversed(l1):   #层
                if type(l2) == {}.__class__:   #层里有字典(手指为平级)
                    saveChildLayerWeight = []
                    for l3 in l2[list(l2.keys())[0]]:
                        layerIndex = dataLayersOrder.index(l3) + 1   #获取当前循环层在ng层中的编号
                        saveWeight = addLayerValue(layerIndex)
                        layerList[layerIndex].set_weights('mask', saveWeight, undo_enabled=0)
                        saveChildLayerWeight.append(saveWeight)
                    saveLayerWeight.append(addListValue(saveChildLayerWeight))
                    continue
                layerIndex = dataLayersOrder.index(l2) + 1   #获取当前循环层在ng层中的编号
                saveWeight = addLayerValue(layerIndex)
                if not saveLayerWeight:
                    layerList[layerIndex].set_weights('mask', saveWeight, undo_enabled=0)
                    saveLayerWeight.append(saveWeight)
                else:
                    saveLayerWeight.append(saveWeight)
                    layerList[layerIndex].set_weights('mask', addListValue(saveLayerWeight), undo_enabled=0)

        if heatMapLayer:
            cmds.delete(cmds.listRelatives(cmds.skinCluster(heatMapLayer.mesh, q=1, g=1), p=1))

    def layersFloodWeight(self):
        """
        层内骨骼Smooth权重
        """
        #入参
        layerList = self.TemplateData['ngLayerList']
        dataLayers = self.TemplateData['Layers']

        omList = om.MGlobal.getSelectionListByName(layerList[0].mesh)   #skinCluster
        skinMObject = omList.getDependNode(0)
        skinNode = omAni.MFnSkinCluster(skinMObject)
        allJointDagPath = skinNode.influenceObjects()
        skCluInfo = []
        for i in allJointDagPath:
            pointList, weigthList = skinNode.getPointsAffectedByInfluence(i)
            if pointList.length():
                pointDagPath, pointObject = pointList.getComponent(0)
                vertex_MIt = om.MItMeshVertex(pointDagPath, pointObject)
                skCluInfo.extend([i.partialPathName(), vertex_MIt.count()])
                """
                while not vertex_MIt.isDone():
                    print(vertex_MIt.index())
                    vertex_MIt.next()
                """
            else:
                skCluInfo.extend([i.partialPathName(), 0])
        FloodSettings = ngUtils_BbBB.create_FloodSettings()
        FloodSettings.mode = ng2api.PaintMode.smooth
        FloodSettings.intensity = 1.0
        FloodSettings.influences_limit = cmds.intField('%s_maxInfluencesNum' %self.Ui, q=1, v=1) \
                                            if cmds.checkBox('%s_maxInfluencesCB' %self.Ui, q=1, v=1) else 0
        for i in layerList[1:]:
            Num = 0
            for joint in reversed(dataLayers[i.name][0]):   #dataLayers数据结构为'LayerName': [[Joint], [JointMirror]]
                Num += skCluInfo[skCluInfo.index(joint) + 1]
            FloodSettings.iterations = 1 if Num < 60 else int(Num / 60)
            ng2api.flood_weights(i, settings=FloodSettings)
            lastJoint = skCluInfo[skCluInfo.index(joint) + 1]   #最后一节骨骼的权重点数
            FloodSettings.iterations = 1 if lastJoint < 40 else int(lastJoint / 40)
            ng2api.flood_weights(i, influence='mask', settings=FloodSettings)

    ### Tool ###
    @staticmethod
    def slJointCreateNgLayer(slObj):
        slJoint = cmds.ls(sl=1, l=1, typ="joint")
        if not slJoint or not slObj:
            om.MGlobal.displayError(u'什么都没选, 做咩啊')
            return
        skinCluster = ng2api.target_info.get_related_skin_cluster(slObj)

        layers = ng2api.init_layers(skinCluster)
        if not layers.list():
            layers.add("Base")
        newLayer = layers.add('OneNewLayer')
        layerJointPathIndex = ng2api.target_info.list_influences(skinCluster)   #获取骨骼在数据层内的信息
        ngIndex = []
        for lj in slJoint:
            for i in layerJointPathIndex:
                if lj == i.path:
                    ngIndex.append(i.logicalIndex)
                    break
        ng2api.assign_from_closest_joint(skinCluster, newLayer, ngIndex)   #分权重
        DisplayYes().showMessage(u'处理完成!')

    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1)[0], sm=[31])
        if not selVtx:
            om.MGlobal.displayError(u'未选择点')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        objLayers = ng2api.Layers(clusterName)
        objAllLayer = objLayers.list()
        if not objAllLayer:
            om.MGlobal.displayError(u'不存在ng权重')
            return
        vtxIndex = int(selVtx[0].split('[')[-1][:-1])
        self.vtxWeightData = {'Info': [clusterName, selVtx[0]], 'weights':[]}
        vtxWeight = {}
        for layer in objAllLayer:
            if not layer.enabled:
                continue
            weights = ngUtils_BbBB.get_LayerWeights(layer, 'mask')
            if not weights:
                continue

            vtxWeight[str(layer)] = ['mask', weights[vtxIndex]]
            #for joint in layer.get_used_influences():
            #    vtxWeight.append([layer, joint, ngUtils_BbBB.get_LayerWeights(layer, joint)[vtxIndex]])
        self.vtxWeightData['weights'] = vtxWeight

    def pasteVtxWeight(self, oneLayer):
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[31])
        if not selVtx:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        vtxWeightData = self.vtxWeightData
        if vtxWeightData['Info'][0] != clusterName:
            om.MGlobal.displayError(u'复制数据不是同一模型')
            return
        if oneLayer:
            objLayers = ng2api.session.session.context.selected_layers(default=[])
            if not objLayers:
                om.MGlobal.displayError(u'未选择ng层')
                return
        else:
            Layers = ng2api.Layers(clusterName)
            objLayers = Layers.list()
            if not objLayers:
                om.MGlobal.displayError(u'不存在ng权重')
                return
        FloodSettings = ngUtils_BbBB.create_FloodSettings()
        for vtx in selVtx:
            for layer in objLayers:
                cmds.select(vtxWeightData['Info'][1], r=1)
                ng2api.copy_component_weights(layer)
                cmds.select(vtx, r=1)
                ng2api.paste_average_component_weights(layer)
                if str(layer) in vtxWeightData['weights']:
                    FloodSettings.intensity = vtxWeightData['weights'][str(layer)][1]
                    ng2api.flood_weights(layer, influence='mask', settings=FloodSettings)


class ngSmooth_BbBB():

    @classmethod
    def doIt(cls, value=3):
        mayaVer = int(cmds.about(v=1))
        if mayaVer >= 2021:
            if ngUtils_BbBB.pluginCheck():
                cls.doApi(value)
            else:
                om.MGlobal.displayError(u'缺少ng2插件, 无法使用!')
        elif mayaVer >= 2014:
            cls.doPlugin(value)

    @staticmethod
    def doPlugin(iterNum):
        if not cmds.ls(sl=1):
            return
        if not cmds.pluginInfo('ngSkinTools.mll', q=1, l=1):
            plugName = 'ngRelax%s.mll' %cmds.about(v=1)
            if not cmds.pluginInfo(plugName, q=1, l=1):
                cmds.loadPlugin(plugName, qt=1)
        cmds.ngSkinRelax(ns=iterNum, wl=8)

    @staticmethod
    def doApi(iterNum):
        sllist = cmds.ls(sl=1, o=1)
        if not sllist:
            return
        clusterName = ng2api.target_info.get_related_skin_cluster(sllist[0])
        if not clusterName:
            return
        layers = ng2api.init_layers(clusterName)
        if len(layers.list()):
            om.MGlobal.displayError(u'ng中已有数据 不适用此方式')
            return
        baseLayer = layers.add("assignBase")
        layers.prune_weights_filter_threshold = 0.001
        FloodSettings = ngUtils_BbBB.create_FloodSettings()
        FloodSettings.mode = ng2api.PaintMode.smooth
        FloodSettings.intensity = 0.8
        FloodSettings.iterations = iterNum
        FloodSettings.influences_limit = 8 if not cmds.skinCluster(clusterName, q=1, omi=1) else cmds.skinCluster(clusterName, q=1, mi=1)
        FloodSettings.limit_to_component_selection = True
        ng2api.flood_weights(baseLayer, settings=FloodSettings)
        cmds.delete([i for i in cmds.listHistory(clusterName, future=1, levels=1) if cmds.nodeType(i) in ['ngst2MeshDisplay', 'ngst2SkinLayerData']])


class ngUtils_BbBB():

    @staticmethod
    def pluginCheck():
        try:
            cmds.loadPlugin('ngSkinTools2', qt=1)
            import ngSkinTools2.api as ng2api
        except (RuntimeError, ImportError):
            return 0
        return 1

    @staticmethod
    def get_LayerWeights(Layer, influence):
        result = mel.eval("ngst2Layers -id {id} -paintTarget {index} -q -{arg} {mesh}".format(mesh=Layer.mesh, id=Layer.id, index=influence, arg='vertexWeights'))
        if result is None:
            return []
        return result
    
    @staticmethod
    def create_FloodSettings():
        if 'PaintModeSettings' in set(dir(ng2api)):
            return ng2api.PaintModeSettings()
        else:
            return ng2api.FloodSettings()
        '''
        mode = None                                         #工具模式 api.PaintMode.xxx(int 1-5)
        intensity = 1.0                                     #工具强度
        iterations = 1                                      #重复次数
        brush_shape = BrushShape.solid                      #笔刷形状
        brush_radius = 10                                   #笔刷半径
        mirror = False                                      #是否镜像
        distribute_to_other_influences = False              #削减的权重是否分配到其他骨骼
        influences_limit = 0                                #最大影响值限制
        brush_projection_mode = BrushProjectinMode.surface  #笔刷投影模式
        sample_joint_on_stroke_start = False
        tablet_mode = TabletMode.unused                     #压感模式
        use_volume_neighbours = False
        limit_to_component_selection = False                #只影响选中的组件
        fixed_influences_per_vertex = False                 #只影响当前点上的骨骼，不扩大影响
        '''

#ngSk2Weight_BbBB().ToolUi()
#ngSmooth_BbBB().doIt()
