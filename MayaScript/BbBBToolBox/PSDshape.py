# -*- coding: UTF-8 -*-
from .pyside import QtWidgets, shiboken

from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om


class PSD_PoseUi():

    def ToolUi(self):
        Ver = 0.87
        self.Ui = 'PSD_Pose_Ui'
        if cmds.window(self.Ui, q=1, ex=1):
            cmds.deleteUI(self.Ui)
        cmds.window(self.Ui, t='PSD_Pose %s' %Ver, rtf=1, mb=1, tlb=1, wh=(250, 250))
        cmds.menu(l=u'Twist轴')
        cmds.radioMenuItemCollection()
        cmds.menuItem('%s_AxisItemX' %self.Ui, l='X', rb=1),
        cmds.menuItem('%s_AxisItemY' %self.Ui, l='Y', rb=0),
        cmds.menuItem('%s_AxisItemZ' %self.Ui, l='Z', rb=0),
        cmds.menu(l=u'设置')
        cmds.menuItem(divider=True, dividerLabel=u'创建模式')
        cmds.radioMenuItemCollection()
        cmds.menuItem('%s_CtrlMode' %self.Ui, l=u'控制器模式', rb=1)
        cmds.menuItem(l=u'纯骨骼模式', rb=0)
        cmds.menuItem(l=u'镜像名称', c=lambda *args: cmds.columnLayout('%sMirrorName_Ly' %self.Ui, e=1, vis=1))
        cmds.menu(l=u'帮助')
        cmds.menuItem(l=u'文档', c=lambda *args: self.helpDoc())

        cmds.columnLayout(cat=('both', 2), rs=1, cw=230)
        cmds.text(l='', h=5)
        styleButton1 = cmds.button('%s_loadobj' %self.Ui, l=u'|  加载模型  |', h=28, c=lambda *args: _loadObj())
        def _loadObj():
            lslist = cmds.ls(sl=1, o=1, typ='transform')
            if lslist:
                if cmds.listRelatives(lslist[0], s=1, typ='mesh'):
                    cmds.button('%s_loadobj' %self.Ui, e=1, l=lslist[0])
            else:
                cmds.button('%s_loadobj' %self.Ui, e=1, l=u'|  加载模型  |')
                if cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, q=1, v=1):
                    cmds.iconTextButton('%s_addPoseButton' %self.Ui, e=1, en=1)
                    cmds.iconTextButton('%s_subPoseButton' %self.Ui, e=1, en=1)
                    cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, e=1, v=0)
        cmds.rowLayout(nc=3)
        _iconwh = 70
        cmds.iconTextButton('%s_addPoseButton' %self.Ui, st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh, l=u'添加', 
                                c=lambda *args: self.AddCallBack())
        cmds.popupMenu()
        cmds.menuItem(l=u'整体镜像', c=lambda *args: self.mirrorPose())
        import tempfile
        with tempfile.NamedTemporaryFile('w+t', suffix='.xpm', delete=False) as tempfileA:
            tempfileA.write('/* XPM */\n  \
                static char *[] = {"20 20 68 1 ","  c None",". c #3A3A3A","X c #3A3A3B","o c #3E3D3F","O c #3E3D40","+ c #3E3E40","@ c #3F3E41","# c #414044", \
                "$ c #424146","% c #434247","& c #444248","* c #444349","= c #46444A","- c #46444B","; c #49474F",": c #4A4750","> c #4B4952",", c #4C4952", \
                "< c #595566","1 c #5A5567","2 c #5B5667","3 c #5B5668","4 c #5C5669","5 c #5C5769","6 c #5D576A","7 c #5D586B","8 c #5E596D","9 c #5F5A6E", \
                "0 c #625C72","q c #635C73","w c #635D73","e c #645D74","r c #645E74","t c #676078","y c #676079","u c #69627C","i c #746B8B","p c #756C8B", \
                "a c #756C8C","s c #776E8F","d c #786F90","f c #8B7EAA","g c #8B7FAB","h c #8F81AF","j c #8F82B0","k c #9083B2","l c #9385B5","z c gray74", \
                "x c #9B8CC1","c c #9C8DC2","v c #9D8DC3","b c #9F8FC6","n c #9F90C7","m c #A090C7","M c #A090C8","N c #A191C9","B c #A292CA","V c #A292CB", \
                "C c #A392CB","Z c #A493CC","A c #A494CD","S c #A695D0","D c #A796D2","F c #A998D3","G c #A998D4","H c #AA99D5","J c #AA99D6","K c #AE9CDB", \
                "                    ","   ..               ","  3CC<              "," .ZKKC.   .........."," .CKKm$.  .zzzzzzzz.", \
                "  <CC<s5  .zzzzzzzz.","   .$sKbo ..........","    .7nKi,lJJk5.    ","      oiS;3$#8cp.   ","       ,:u....#x3   ","      .l<.5AC3.8k.  ", \
                "      .J+.mKKC.+S.  ","      .JX$MKKm.+S.  ","      .rrd3ZC<.7h.  ","      .-DKa#..#x5   ","      .fKGr.#9ca.   ","      eKg-wDJk5.    ", \
                "     -cw......      ","     w-             ","                    "};')
            self.tempIco = tempfileA.name
        cmds.iconTextButton('%s_subPoseButton' %self.Ui, st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh, l=u'删除',
                            c=lambda *args: self.DeleteProc())
        cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh, l=u'编辑',
                              cc=lambda *args: self.EditCallBack())
        cmds.popupMenu()
        cmds.menuItem(l=u'转到Pose', c=lambda *args: self.goToPose())
        cmds.setParent('..')

        cmds.rowLayout(nc=3)
        cmds.columnLayout(cat=('both', 0), rs=1, cw=_iconwh)
        styleButton2 = cmds.button(l=u'拷贝', h=34, c=lambda *args: self.BakePoseCallBack())
        styleButton3 = cmds.button(l=u'重建', h=34, c=lambda *args: self.RemakeBs())
        cmds.popupMenu()
        cmds.menuItem(l=u'传输属性', c=lambda *args: self.PoseAttr_trans())
        cmds.setParent('..')
        cmds.iconTextButton(st='iconAndTextVertical', i='kinMirrorJoint_S.png', l=u'翻转', w=_iconwh, h=_iconwh, c=lambda *args: self.FilpTarget())
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('%s_FlipAxisItemX' %self.Ui, l='X', rb=1)
        cmds.menuItem('%s_FlipAxisItemY' %self.Ui, l='Y', rb=0)
        cmds.menuItem('%s_FlipAxisItemZ' %self.Ui, l='Z', rb=0)
        cmds.iconTextButton(st='iconAndTextVertical', i='substGeometry.png', l=u'*', w=_iconwh, h=_iconwh, c='')
        cmds.setParent('..')
        cmds.text('%s_editTarget' %self.Ui, vis=0)
        cmds.text('%s_saveLMirrortextField' %self.Ui, l='_L', vis=0)
        
        cmds.columnLayout('%sMirrorName_Ly' %self.Ui, cat=('both', 2), rs=2, cw=120, vis=0)
        cmds.textFieldGrp('%s_saveLMirrortextField' %self.Ui, l='L', tx='_L', cw2=(15, 95))
        cmds.textFieldGrp('%s_saveRMirrortextField' %self.Ui, l='R', tx='_R', cw2=(15, 95))
        cmds.button(l='Save', c=lambda *args: cmds.columnLayout('%sMirrorName_Ly' %self.Ui, e=1, vis=0))
        cmds.setParent('..')

        style = '''
        QPushButton {
            border: none;
            padding-left: 10px;
            padding-right: 5px;
        }
        QPushButton:hover {
            background-color: rgb(76, 76, 76);
        }
        QPushButton:pressed {
            background-color: #1d1d1d;
        }
        '''
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(styleButton1)), QtWidgets.QPushButton).setStyleSheet(style)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(styleButton2)), QtWidgets.QPushButton).setStyleSheet(style)
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(styleButton3)), QtWidgets.QPushButton).setStyleSheet(style)
        cmds.showWindow(self.Ui)
        
        try:
            cmds.loadPlugin('invertShape.mll', qt=1)
            cmds.loadPlugin('poseInterpolator.mll', qt=1)
        except RuntimeError:
            om.MGlobal.displayWarning(u'这个Maya中缺少必要插件, 修型功能将无法使用!')

    def helpDoc(self):
        if cmds.window('%s_HelpDoc' %self.Ui, q=1, ex=1):
            cmds.deleteUI('%s_HelpDoc' %self.Ui)
        cmds.window('%s_HelpDoc' %self.Ui, t='Help Doc', rtf=1, s=1, tlb=1, wh=(600, 550))
        _iconwh = 60
        cmds.columnLayout(cat=('both', 2), rs=10, cw=600)
        cmds.text(l=u'带 * 表示需要在 |  加载模型  | 的前提下操作', h=50, fn='fixedWidthFont')
        fn = 'fixedWidthFont'
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'添加', st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh)
        cmds.popupMenu()
        cmds.menuItem(l=u'整体镜像')
        cmds.text(l=u'*初始化(每根骨骼首次添加): 选择骨骼 + 控制器 \n*添加Pose: 选择骨骼/控制器 \n*在已有Pose下添加其他模型: 1.加载其他模型 - 2.选择要使用的Pose - 3.点添加\n*右键菜单: 整体镜像, 可以镜像单个Pose或整个PSD节点', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'删除', st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh)
        cmds.text(l=u'选择一个PSD节点或多个Pose, 进行删除操作', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextCheckBox(l=u'编辑', st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh)
        cmds.popupMenu()
        cmds.menuItem(l=u'转到Pose')
        cmds.text(l=u'*选择单个Pose, 调出当前修型开始编辑 \n*按钮点亮时: 将当前的修型模型, 塞回指定的BS \n右键菜单: 转到选择的Pose', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'拷贝', st="textOnly", h=50, w=_iconwh)
        cmds.text(l=u'*选择一个PSD节点或多个Pose, 提取出修型目标体', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'重建', st="textOnly", h=50, w=_iconwh)
        cmds.popupMenu()
        cmds.menuItem(l=u'传输属性')
        cmds.text(l=u'*选择一个或多个修型目标体, 根据模型信息新增或修改指定Pose \n右键菜单: 将脚本模型(a)的属性传递到修好的普通模型(b)上, 让模型(b)可以通过重建功能使用 \n\
            先选拷贝出的模型, 加选要重建的模型', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'翻转', st='iconAndTextVertical', i='kinMirrorJoint_S.png',w=_iconwh, h=_iconwh)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem(l='X', rb=1)
        cmds.menuItem(l='Y', rb=0)
        cmds.menuItem(l='Z', rb=0)
        cmds.text(l=u'*一般模型: 将选择的模型翻转, 得到一个对称的模型 \n*PSD模型: 将选择的修型目标体翻转, 得到一个对称的-可通过(重建)按钮添加Pose的修型目标体\n右键菜单: 修改翻转对称轴', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(l=u'*', st='iconAndTextVertical', i='substGeometry.png', w=_iconwh, h=_iconwh)
        cmds.text(l=u'*暂未实现', al='left', fn=fn)
        cmds.setParent('..')
        
        cmds.showWindow('%s_HelpDoc' %self.Ui)

    def AddCallBack(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return
        if cmds.nodeType(sllist[0]) == 'joint':
            _Joint = sllist[0]
        elif cmds.listConnections(sllist[0], d=0, t='joint') and cmds.ls('%s.ctrlJnt_Psd' %sllist[0]):
            #如果有链接信息 和 .ctrlJnt_Psd属性 说明选择的是个控制器
            _Joint = cmds.listConnections('%s.ctrlJnt_Psd' %sllist[0], d=0, t='joint')[0]
        elif cmds.ls('%s.isPose' %sllist[0]):
            _Joint = cmds.listConnections('%s.message' %cmds.listRelatives(sllist[0], p=1)[0], t='joint')[0]
            PoseName = sllist[0]
            self.goToPose(PoseName)
            _Ctrl = cmds.getAttr('%s.CtrlName' %sllist[0])
            _jntRotate = cmds.getAttr('%s.JointRotate' %sllist[0])[0]
            self.AddPoseProc(_Joint, [_Joint, PoseName, _Ctrl, _jntRotate, ''], 1)
            return
        else:
            return
        
        if not cmds.listConnections(_Joint, s=0, sh=1, t='poseInterpolator'):
            if cmds.menuItem('%s_CtrlMode' %self.Ui, q=1, rb=1):
                if len(sllist) < 2:
                    om.MGlobal.displayError(u'请确认选择了骨骼和控制器')
                    return
                self.AddPoseIProc(_Joint, sllist[1])
                return
            else:
                self.AddPoseIProc(_Joint, None)
                return
        self.AddPoseProc(_Joint)

    def EditCallBack(self, stEd=0, fhEd=0):
        if stEd:
            cmds.iconTextButton('%s_addPoseButton' %self.Ui, e=1, en=0)
            cmds.iconTextButton('%s_subPoseButton' %self.Ui, e=1, en=0)
            cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, e=1, v=1)
            return
        if fhEd:
            cmds.iconTextButton('%s_addPoseButton' %self.Ui, e=1, en=1)
            cmds.iconTextButton('%s_subPoseButton' %self.Ui, e=1, en=1)
            cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, e=1, v=0)
            return
        if not cmds.iconTextCheckBox('%s_editPoseButton' %self.Ui, q=1, v=1):
            # 按钮为点亮状态
            self.EditCallBack(0, 1)
            self.transfer2Bs(cmds.text('%s_editTarget' %self.Ui, q=1, l=1))
        else:
            if not cmds.button('%s_loadobj' %self.Ui, q=1, l=1) == u'|  加载模型  |':
                if self.EditProc():   #调出bs, 开始编辑
                    self.EditCallBack(1)
                else:
                    self.EditCallBack(0, 1)

    def AddPoseIProc(self, _Joint, _Ctrl):
        _poseI = cmds.poseInterpolator(_Joint, n='%s_poseInterpolator' %_Joint)[0]
        _poseIShape = cmds.listRelatives(_poseI, s=1, typ="poseInterpolator")[0]
        cmds.addAttr(_Joint, ln='Associated_Psd', at="message")
        cmds.connectAttr('%s.message' %_poseI, '%s.Associated_Psd' %_Joint, f=1)
        cmds.poseInterpolator(_poseIShape, e=1, ap="neutral")
        cmds.setAttr("%s.pose[%s].poseType" %(_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralSwing")), 1)
        cmds.setAttr("%s.pose[%s].poseType" %(_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralTwist")), 2)
        if not _Ctrl:
            cmds.connectAttr('%s.rotate' %_Joint, '%s.driver[0].driverController[0]' %_poseIShape, f=1)
            _Ctrl = _Joint
        else:
            cmds.connectAttr('%s.rotate' %_Ctrl, '%s.driver[0].driverController[0]' %_poseIShape, f=1)
            cmds.addAttr(_Ctrl, ln='ctrlJnt_Psd', at="message")
            cmds.connectAttr('%s.message' %_Joint, '%s.ctrlJnt_Psd' %_Ctrl, f=1)

        self.PoseAttr_add(cmds.group(n="%s_neutralPose" %_Joint, p=_poseI, em=1), 0, [_Joint, _Ctrl, 'neutralPose', cmds.getAttr('%s.r' %_Joint)[0]])
        _AxisItem = ['%s_AxisItemX' %self.Ui, '%s_AxisItemY' %self.Ui, '%s_AxisItemZ' %self.Ui]
        for n in range(3):
            if cmds.menuItem(_AxisItem[n], q=1, rb=1):
                break
        cmds.setAttr('%s.driver[0].driverTwistAxis' %_poseIShape, n)
        cmds.setAttr('%s.outputSmoothing' %_poseIShape, 1)
        om.MGlobal.displayInfo(u'已完成首次创建!')
    
    def AddPoseProc(self, _Joint, Remake_Data=[], useAgain=0):
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if Remake_Data:
            _Joint = Remake_Data[0]
            PoseName = Remake_Data[1]
            _Ctrl = Remake_Data[2]
            _jntRotate = Remake_Data[3]
            dupObj = Remake_Data[4]
            if not dupObj:
                dupObj = self.extractPose(PoseName)
        else:
            _rotateData = []
            _jntRotate = cmds.getAttr('%s.r' %_Joint)[0]
            for i in _jntRotate:
                i = round(i)
                if int('%d' %i) < 0:
                    _rotateData.append('n%d' %abs(i))
                else:
                    _rotateData.append('%d' %i)
            PoseName = '%s_%s_%s_%s' %(_Joint, _rotateData[0], _rotateData[1], _rotateData[2])
            if cmds.ls(PoseName):
                om.MGlobal.displayError(u'这个Pose已经存在')
                return
            if not cmds.menuItem('%s_CtrlMode' %self.Ui, q=1, rb=1):
                _Ctrl = _Joint
            else:
                for _Ctrl in cmds.listConnections('%s.message' %_Joint, t='transform'):
                    if cmds.ls('%s.ctrlJnt_Psd' %_Ctrl):
                        break
            dupObj = cmds.duplicate(loadobj, n='%s_%s' %(loadobj, PoseName), rr=1)[0]
            _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
            cmds.setAttr('%s.overrideEnabled' %_dupObjShape, 1)
            cmds.setAttr('%s.overrideColor' %_dupObjShape, 20)
        
        _BsName = ''
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' %i):
                _BsName = i
                break
        if not _BsName:
            _BsName = cmds.blendShape(loadobj, frontOfChain=1, n='Psd_BlendShape%s' %(len(cmds.ls('Psd_BlendShape*', typ='blendShape')) + 1))[0]
            cmds.addAttr(_BsName, ln='Use2Psd', at='bool')
        
        if not useAgain:
            lsCposeI = cmds.listConnections('%s.Associated_Psd' %_Joint, d=0, t='transform')[0]
            _lsCposeIShape = cmds.listRelatives(lsCposeI, s=1)[0]
            self.PoseAttr_add(cmds.group(n=PoseName, p=lsCposeI, em=1), 0, [_Joint, _Ctrl, PoseName, _jntRotate])
            cmds.addAttr(lsCposeI, ln=PoseName, at='double', min=0, max=1, dv=0)
            poseAttr = '%s.%s' %(lsCposeI, PoseName)
            _poseId = cmds.poseInterpolator(_lsCposeIShape, e=1, ap=PoseName)
            cmds.setAttr('%s.pose[%s].poseType' %(_lsCposeIShape, _poseId), 1) #Type默认Swing
            cmds.connectAttr('%s.output[%s]' %(_lsCposeIShape, _poseId), poseAttr, f=1)
        else:
            poseAttr = '%s.%s' %(cmds.listConnections('%s.Associated_Psd' %_Joint, d=0, t='transform')[0], PoseName)
        
        _newBsId = cmds.getAttr('%s.w' %_BsName, mi=1)
        _newBsId = 0 if not _newBsId else _newBsId[-1] + 1
        cmds.blendShape(_BsName, e=1, tc=1, t=(loadobj, _newBsId, dupObj, 1), w=[_newBsId, 0]) #初始bs开关
        cmds.disconnectAttr('%s.worldMesh[0]' %dupObj, cmds.listConnections('%s.worldMesh[0]' %dupObj, p=1)[0])
        _newBsAttr = '%s.w[%s]' %(_BsName, _newBsId)
        cmds.aliasAttr(PoseName, _newBsAttr)
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=0, v=0, itt='linear', ott='linear')
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=1, v=1, itt='linear', ott='linear')

        cmds.setAttr(poseAttr, e=1, cb=1)
        if not Remake_Data or useAgain:
            if not useAgain:
                self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
            cmds.select(dupObj, r=1)
            cmds.text('%s_editTarget' %self.Ui, e=1, l=dupObj)
            cmds.setAttr('%s.v' %loadobj, 0)
            self.EditCallBack(1)
    
    def DeleteProc(self):
        sllist = cmds.ls(sl=1)
        if not sllist:
            return
        for a in sllist:
            if cmds.listRelatives(a, s=1, typ='poseInterpolator'):
                for b in cmds.listRelatives(a, c=1):
                    if cmds.ls('%s.isPose' %b):
                        self._deletePose(b)
                for j in cmds.listConnections('%s.message' %a, t='joint'):
                    if cmds.ls('%s.Associated_Psd' %j):
                        for c in cmds.listConnections('%s.message' %j):
                            if cmds.ls('%s.ctrlJnt_Psd' %c):
                                cmds.deleteAttr('%s.ctrlJnt_Psd' %c)
                                break
                        cmds.deleteAttr('%s.Associated_Psd' %j)
                        break
                cmds.delete(a)
            elif cmds.ls('%s.isPose' %a):
                self._deletePose(a)
                
    def _deletePose(self, name):
        PoseName = cmds.getAttr('%s.PoseName' %name)
        if PoseName == 'neutralPose':
            cmds.delete(name)
            return
        a = cmds.listRelatives(name, p=1)[0]
        for c in cmds.listConnections('%s.%s' %(a, PoseName))[:-1]:
            if cmds.ls(c, typ='animCurveUU'):
                for d in cmds.listConnections('%s.output' %c):
                    if cmds.ls(d, typ='blendShape'):
                        for e in cmds.getAttr('%s.w' %d, mi=1):
                            if PoseName == cmds.aliasAttr('%s.w[%s]' %(d, e), q=1):
                                break
                        #_targetId = cmds.ls('%s.inputTarget[0].inputTargetGroup[*]' %d)[e].split('%s.inputTarget[0].inputTargetGroup[' %d)[1][:-1]
                        mel.eval('blendShapeDeleteTargetGroup %s %s' %(d, e))
        cmds.setAttr('%s.%s' %(a, PoseName), e=1, cb=1, l=0)
        cmds.deleteAttr(a, at=PoseName)
        cmds.poseInterpolator(cmds.listRelatives(a, s=1, typ='poseInterpolator')[0], e=1, dp=PoseName)
        cmds.delete(name)

    def EditProc(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return 0
        if cmds.ls('%s.isPose' %sllist[0]):
            self.goToPose(sllist[0])
            dupObj = self.extractPose(sllist[0])
            cmds.text('%s_editTarget' %self.Ui, e=1, l=dupObj)
            cmds.select(dupObj, r=1)
            cmds.setAttr('%s.v' %loadobj, 0)
            return 1
        elif cmds.ls('%s.isEditMesh' %sllist[0]):
            cmds.text('%s_editTarget' %self.Ui, e=1, l=sllist[0])
            return 1
        else:
            return 0
        
    def PoseAttr_add(self, transName, _type, _Data_):
        #if not cmds.ls('{}.PoseName'.format(transName)): 导致错误
        #    return
        cmds.addAttr(transName, ln='JointName', dt="string")
        cmds.setAttr('%s.JointName' %transName, _Data_[0], typ='string')
        cmds.addAttr(transName, ln='CtrlName', dt="string")
        cmds.setAttr('%s.CtrlName' %transName, _Data_[1], typ='string')
        cmds.addAttr(transName, ln='PoseName', dt="string")
        cmds.setAttr('%s.PoseName' %transName, _Data_[2], typ='string')
        cmds.addAttr(transName, ln="JointRotate", at='double3')
        cmds.addAttr(transName, ln="JointRotateX", at='double', dv=_Data_[3][0], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateY", at='double', dv=_Data_[3][1], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateZ", at='double', dv=_Data_[3][2], p="JointRotate")
        if not _type:
            cmds.addAttr(transName, ln='isPose', at="bool")
        elif _type == 1:
            cmds.addAttr(transName, ln='isEditMesh', at="bool")
            for i in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
                cmds.setAttr('%s%s' %(transName, i), l=0)
    
    def PoseAttr_trans(self):
        sl = cmds.ls(sl=1)
        if not cmds.ls('%s.JointName' %sl[0]) and not cmds.ls('%s.PoseName' %sl[0]):
            return
        if not cmds.ls('%s.JointName' %sl[1]) and not cmds.ls('%s.CtrlName' %sl[1]) and not cmds.ls('%s.PoseName' %sl[1]):
            cmds.addAttr(sl[1], ln='JointName', dt="string")
            cmds.addAttr(sl[1], ln='CtrlName', dt="string")
            cmds.addAttr(sl[1], ln='PoseName', dt="string")
            cmds.addAttr(sl[1], ln="JointRotate", at='double3')
            cmds.addAttr(sl[1], ln="JointRotateX", at='double', dv=0, p="JointRotate")
            cmds.addAttr(sl[1], ln="JointRotateY", at='double', dv=0, p="JointRotate")
            cmds.addAttr(sl[1], ln="JointRotateZ", at='double', dv=0, p="JointRotate")
            if cmds.ls('%s.isPose' %sl[0]):
                cmds.addAttr(sl[1], ln='isPose', at="bool")
            elif cmds.ls('%s.isEditMesh' %sl[0]):
                cmds.addAttr(sl[1], ln='isEditMesh', at="bool")
        cmds.setAttr('%s.JointName' %sl[1], cmds.getAttr('%s.JointName' %sl[0]), typ='string')
        cmds.setAttr('%s.CtrlName' %sl[1], cmds.getAttr('%s.CtrlName' %sl[0]), typ='string')
        cmds.setAttr('%s.PoseName' %sl[1], cmds.getAttr('%s.PoseName' %sl[0]), typ='string')
        r = cmds.getAttr('%s.JointRotate' %sl[0])[0]
        cmds.setAttr('%s.JointRotate' %sl[0], r[0], r[1], r[2])

    def transfer2Bs(self, name):
        if not cmds.ls('%s.isEditMesh' %name):
            om.MGlobal.displayError('Object not exists.')
            return
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' %i):
                _BsName = i
        PoseName = cmds.getAttr('%s.PoseName' %name)
        _bsList = cmds.listAttr('%s.w[*]' %_BsName)
        for i in cmds.getAttr('%s.w' %_BsName, mi=1):
            if PoseName == cmds.aliasAttr('%s.w[%s]' %(_BsName, i), q=1):
                break
        self.goToPose(PoseName)
        cmds.setAttr('%s.w[%s]' %(_BsName, i), 0)
        objInBS = cmds.blendShape(_BsName, q=1, g=1)[0]   #[0]目前没见到多Shape的情况
        IndexInBS = cmds.blendShape(_BsName, q=1, gi=1)[0]   #[0]目前没见到多Index的情况
        invertedobj = cmds.invertShape(objInBS, name)
        cmds.connectAttr('%s.outMesh' %invertedobj, 
                            '%s.inputTarget[%s].inputTargetGroup[%s].inputTargetItem[6000].inputGeomTarget' %(_BsName, IndexInBS, i), f=1)
        cmds.refresh()
        cmds.disconnectAttr('%s.outMesh' %invertedobj, 
                                '%s.inputTarget[%s].inputTargetGroup[%s].inputTargetItem[6000].inputGeomTarget' %(_BsName, IndexInBS, i))
        #cmds.blendShape(_BsName, e=1, t=(loadobj, i, name, 1.0), w=[i, 1])    #塞回去的时候有顺序问题
        #cmds.aliasAttr(PoseName, '%s.w[%s]' %(_BsName, i))
        cmds.delete(name, invertedobj)
        cmds.setAttr('%s.v' %loadobj, 1)
    
    def goToPose(self, name=''):
        sllist = cmds.ls(sl=1)
        if sllist or name:
            if not name:
                name = sllist[0]
            _Ctrl = '%s.CtrlName' %name
            if not cmds.ls(_Ctrl):
                _Ctrl = '%s.JointName' %name
            _jntRotate = '%s.JointRotate' %name
            if cmds.ls(_Ctrl) and cmds.ls(_jntRotate):
                _rotate = cmds.getAttr(_jntRotate)[0]
                cmds.setAttr('%s.r' %cmds.getAttr(_Ctrl), _rotate[0], _rotate[1], _rotate[2])
    
    def extractPose(self, name):
        #需要提前判断 loadobj 和 '%s.isPose'
        #rebuildSelectedTargetShape     cmds.sculptTarget(_BsName, e=1, r=1, t=0)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        _Joint = cmds.getAttr('%s.JointName' %name) 
        _Ctrl = cmds.getAttr('%s.CtrlName' %name)
        _jntRotate = cmds.getAttr('%s.JointRotate' %name)[0]
        PoseName = cmds.getAttr('%s.PoseName' %name)
        dupObj = cmds.duplicate(loadobj, n='%s_%s' %(loadobj, PoseName), rr=1)[0]
        _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
        cmds.setAttr('%s.overrideEnabled' %_dupObjShape, 1)
        cmds.setAttr('%s.overrideColor' %_dupObjShape, 20)
        self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
        return dupObj
    
    def BakePoseCallBack(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return
        self.BakePose(sllist)
    
    def BakePose(self, data):
        _exPose = []
        if cmds.listRelatives(data, s=1, typ='poseInterpolator'):
            _childItem = cmds.listRelatives(data, c=1, typ='transform')
            for i in _childItem[1:]:
                if cmds.ls('%s.isPose' %i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
            self.goToPose(_childItem[0])
        else:
            for i in data:
                if cmds.ls('%s.isPose' %i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
                self.goToPose(cmds.listRelatives(cmds.listRelatives(i, p=1)[0], c=1, typ='transform')[0])
        if _exPose:
            cmds.select(_exPose, r=1)
            return _exPose
        else:
            om.MGlobal.displayError(u"没有可以提取的Pose")

    def RemakeBs(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return
        for i in sllist:
            if not cmds.ls('%s.isEditMesh' %i):
                continue
            _Joint = cmds.getAttr('%s.JointName' %i)
            _Ctrl = cmds.getAttr('%s.CtrlName' %i)
            _jntRotate = cmds.getAttr('%s.JointRotate' %i)[0]
            PoseName = cmds.getAttr('%s.PoseName' %i)
            if not cmds.ls('%s.Associated_Psd' %_Joint):
                self.AddPoseIProc(_Joint, _Ctrl)
            elif cmds.ls(PoseName):
                self.goToPose(i)
                self.transfer2Bs(i)
                continue
            cmds.setAttr('%s.r' %_Ctrl, _jntRotate[0], _jntRotate[1], _jntRotate[2])
            cmds.select(_Joint, r=1)
            self.AddPoseProc(_Joint, [_Joint, PoseName, _Ctrl, _jntRotate, i])
            self.goToPose(cmds.listRelatives(cmds.listRelatives(PoseName, p=1)[0], c=1, typ='transform')[0])
    
    def FilpTarget(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return
        _filpPose = []
        for i in sllist:
            sourceObj = cmds.duplicate(loadobj, n='_TempSourceMesh_')
            dupObj = cmds.duplicate(i, n='_TempFilpMesh_')
            bs = cmds.blendShape(dupObj[0], sourceObj[0], w=(0,1), tc=0)[0]
            cmds.refresh()
            _AxisItem = ['%s_FlipAxisItemX' %self.Ui, '%s_FlipAxisItemY' %self.Ui, '%s_FlipAxisItemZ' %self.Ui]
            for n in range(3):
                if cmds.menuItem(_AxisItem[n], q=1, rb=1):
                    break
            mel.eval('doBlendShapeFlipTarget %s 0 {"%s.0"}' %(n + 1, bs))
            
            if cmds.ls('%s.isEditMesh' %i):
                _Joint = cmds.getAttr('%s.JointName' %i)
                _Ctrl = cmds.getAttr('%s.CtrlName' %i)
                _jntRotate = cmds.getAttr('%s.JointRotate' %i)[0]
                PoseName = cmds.getAttr('%s.PoseName' %i)
                _old = cmds.textFieldGrp('%s_saveLMirrortextField' %self.Ui, q=1, tx=1)
                _new = cmds.textFieldGrp('%s_saveRMirrortextField' %self.Ui, q=1, tx=1)
                filpObj = cmds.duplicate(sourceObj[0], n=i.replace(_old, _new))[0]
                _filpObjShape = cmds.listRelatives(filpObj, s=1)[0]
                cmds.setAttr('%s.overrideEnabled' %_filpObjShape, 1)
                cmds.setAttr('%s.overrideColor' %_filpObjShape, 20)
                self.PoseAttr_add(filpObj, 1, [_Joint.replace(_old, _new), _Ctrl.replace(_old, _new), PoseName.replace(_old, _new), _jntRotate])
                _filpPose.append(filpObj)
            else:
                cmds.duplicate(sourceObj[0], n='%s_Filp' %i)
            cmds.delete(sourceObj, dupObj)
        cmds.select(_filpPose, r=1)
        return _filpPose

    def mirrorPose(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.button('%s_loadobj' %self.Ui, q=1, l=1)
        if not sllist or loadobj == u'|  加载模型  |':
            return
        exPose = self.BakePose(sllist)
        filpPose = self.FilpTarget()
        self.RemakeBs()
        cmds.delete(exPose, filpPose)
        
#PSD_PoseUi().ToolUi()
