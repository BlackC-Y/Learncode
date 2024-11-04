# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om

import math

from .DisplayYes import DisplayYes
import epic_pose_wrangler.v2.main as UERbf


class CreateModifyJoint():

    def ToolUi(self, layout=0):
        self.UiName = 'CreateModifyJoint_BbBB'
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        cmds.window(self.UiName, t='CreateModifyJoint', rtf=1, mb=1, tlb=1, wh=(300, 85))
        form = cmds.formLayout()
        meshText = cmds.textFieldButtonGrp('%s_MeshTarget' %self.UiName, l=u'检测模型', bl=u'选择', h=24, adj=2, ed=0, cw3=[60, 180, 60], bc=lambda *args: _select())
        halfJointCB = cmds.checkBox('%s_halfJointCB' %self.UiName, l=u'添加半转骨骼', h=25)
        createJointLayout = cmds.rowLayout(nc=2, adj=1, h=24)
        cmds.button(l=u'创建骨骼',  c=lambda *args: self.doCreateJoint(cmds.textFieldButtonGrp('%s_MeshTarget' %self.UiName, q=1, tx=1)), ann=u'选择身体骨骼，会在4个方向创建辅助骨骼\n右键-Adv模板')
        cmds.button(l='>')
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'使用Adv模版', c=lambda *args: self.doAdvTemplateCreateJoint(cmds.textFieldButtonGrp('%s_MeshTarget' %self.UiName, q=1, tx=1)), ann=u'基于Adv的身体骨架，创建出全身的辅助骨骼')
        cmds.setParent('..')
        mirrorJointButton = cmds.button(l=u'镜像骨骼', h=24, c=lambda *args: self.doMirrorJoint(), ann=u'从左至右镜像全部骨骼/选择的骨骼 (调整时不要冻结)')
        
        createCtrlButton = cmds.button(l=u'创建控制器', h=24, c=lambda *args: self.doCreateCtrl(), ann=u'创建全部辅助骨骼的控制器/选择的辅助骨骼的控制器')
        mirrorCtrlButton = cmds.button(l=u'镜像控制器', h=24, c=lambda *args: self.doMirrorCtrl(), ann=u'从左至右镜像全部控制器/选择的控制器')
        separator = cmds.separator(height=5, style='in')
        
        SimpleDriverLayout = cmds.rowLayout(nc=2, adj=1, h=24)
        cmds.button(l=u'创建简易驱动', w=255, c=lambda *args: self.doCreateSimpleDriver(), ann=u'选择要驱动的辅助骨骼对应的身体骨骼 (只建议用在手指)')
        cmds.button(l='>')
        cmds.popupMenu(b=1)
        cmds.menuItem(divider=True, dividerLabel=u'轴向')
        cmds.radioMenuItemCollection()
        cmds.menuItem('SimpleDriverAxis_RB0%s' %self.UiName, label=u'X', radioButton=0)
        cmds.menuItem('SimpleDriverAxis_RB1%s' %self.UiName, label=u'Y', radioButton=1)
        cmds.menuItem('SimpleDriverAxis_RB2%s' %self.UiName, label=u'Z', radioButton=0)
        cmds.menuItem(divider=True, dividerLabel=u'旋转方向')
        cmds.radioMenuItemCollection()
        cmds.menuItem('SimpleDriverPos_RB%s' %self.UiName, label=u'正', radioButton=1)
        cmds.menuItem(label=u'负', radioButton=0)
        cmds.setParent('..')
        
        RBFDriverLayout = cmds.rowLayout(nc=2, adj=1, h=24)
        RbfState = self.RBFCheck()
        cmds.button(l=u'创建RBF驱动', w=255, en=RbfState, c=lambda *args: self.doCreateRBFDriver(), ann=u'选择要去懂得辅助骨骼对应的身体骨骼\n右键-Adv模板')
        cmds.button(l='>')
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'使用Adv模版', en=RbfState, c=lambda *args: self.doAdvTemplateCreateRBF(), ann=u'基于Adv的身体骨架，创建出全身的辅助骨骼RBF驱动')
        cmds.setParent('..')
        
        def _select():
            sl = cmds.ls(sl=1, typ='transform')
            if not sl:
                return
            cmds.textFieldButtonGrp('%s_MeshTarget' %self.UiName, e=1, tx=sl[0])
        
        cmds.formLayout(form, e=1, af=((meshText, 'top', 0), (meshText, 'left', 0), (meshText, 'right', 0),
                                       (halfJointCB, 'left', 10), (halfJointCB, 'right', 0),
                                       (createJointLayout, 'left', 0), (mirrorJointButton, 'right', 0),
                                       (createCtrlButton, 'left', 0), (mirrorCtrlButton, 'right', 0),
                                       (separator, 'left', 0), (separator, 'right', 0),
                                       (SimpleDriverLayout, 'left', 0), (SimpleDriverLayout, 'right', 0),
                                       (RBFDriverLayout, 'left', 0), (RBFDriverLayout, 'right', 0)),
                                    ac=((halfJointCB, 'top', 0, meshText), 
                                       (createJointLayout, 'top', 2, halfJointCB), (mirrorJointButton, 'top', 2, halfJointCB),
                                       (createCtrlButton, 'top', 2, createJointLayout), (mirrorCtrlButton, 'top', 2, mirrorJointButton),
                                       (separator, 'top', 2, createCtrlButton),
                                       (SimpleDriverLayout, 'top', 2, separator),
                                       (RBFDriverLayout, 'top', 2, SimpleDriverLayout),),
                                    ap=((createJointLayout, 'right', 1, 50), (mirrorJointButton, 'left', 1, 50),
                                        (createCtrlButton, 'right', 1, 50), (mirrorCtrlButton, 'left', 1, 50)))
        cmds.showWindow(self.UiName)
        
    def doCreateJoint(self, slmesh, halfJoint=''):
        sllist = cmds.ls(sl=1, type='joint')
        if type(halfJoint) == str:
            halfJoint = cmds.checkBox('%s_halfJointCB' %self.UiName, q=1, v=1)
        allConstraint = []
        all0050 = []
        
        RayData = RayIntersection(om.MGlobal.getSelectionListByName(slmesh).getDagPath(0))
        for jnt in sllist:
            reArgsList = RayData.doIt(om.MGlobal.getSelectionListByName(jnt).getDagPath(0))
            newJntList = self.createJoint(jnt, reArgsList)   #_tempNode, slmesh
            for _newJnt in newJntList:
                cmds.parent(_newJnt, jnt)
            if halfJoint:
                jnt50 = cmds.duplicate(jnt, po=1, n='%s_50' %jnt)[0]
                advSet = cmds.listConnections(jnt50, type='objectSet')
                if advSet:
                    for i in advSet:
                        cmds.sets(jnt50, e=1, remove=i)
                jnt00 = cmds.createNode('transform', n='%s_00' %jnt)
                jnt00Offset = cmds.group(jnt00, n='%s_00Offset' %jnt)
                cmds.matchTransform(jnt00Offset, jnt50, pos=1, rot=1)
                allConstraint.append(cmds.parentConstraint(cmds.listRelatives(jnt, p=1)[0], jnt00Offset, mo=1, w=1)[0])
                allConstraint.append(cmds.pointConstraint(jnt, jnt50, offset=(0, 0, 0), w=1)[0])
                _roC = cmds.orientConstraint(jnt, jnt00, jnt50, offset=(0, 0, 0), w=1)[0]
                cmds.setAttr('%s.interpType' %_roC, 2)
                allConstraint.append(_roC)
                all0050.append(jnt00Offset)
                all0050.append(jnt50)
        if not cmds.ls('RBF_System', type='transform'):
            cmds.group(cmds.createNode('transform', n='RBF_Constraint'), cmds.createNode('transform', n='RBF_halfRot'), w=1, n='RBF_System')
        if halfJoint:
            cmds.parent(allConstraint, 'RBF_Constraint')
            cmds.parent(all0050, 'RBF_halfRot')

    def doAdvTemplateCreateJoint(self, slmesh):
        cmds.select(cmds.ls(("Head_M", "Neck_M", "Scapula_L", "Shoulder_L", "Elbow_L", "Wrist_L", "Scapula_R", "Shoulder_R", "Elbow_R", "Wrist_R", 
        "IndexFinger1_L", "IndexFinger2_L", "IndexFinger3_L", "IndexFinger1_R", "IndexFinger2_R", "IndexFinger3_R", 
        "MiddleFinger1_L", "MiddleFinger2_L", "MiddleFinger3_L", "MiddleFinger1_R", "MiddleFinger2_R", "MiddleFinger3_R", 
        "RingFinger1_L", "RingFinger2_L", "RingFinger3_L", "RingFinger1_R", "RingFinger2_R", "RingFinger3_R", 
        "PinkyFinger1_L", "PinkyFinger2_L", "PinkyFinger3_L", "PinkyFinger1_R", "PinkyFinger2_R", "PinkyFinger3_R", 
        "ThumbFinger2_L", "ThumbFinger3_L", "ThumbFinger2_R", "ThumbFinger3_R",   #"ThumbFinger1_L"
        "Hip_L", "Knee_L", "Ankle_L", "Toes_L", "Hip_R", "Knee_R", "Ankle_R", "Toes_R",
        "Spine1_M", "Spine2_M", "Spine3_M", ), typ='joint'), r=1)   #Chest_M
        self.doCreateJoint(slmesh, 1)
        cmds.select(cmds.ls(('ShoulderPart1_L', 'ShoulderPart1_R', 'HipPart1_L', 'HipPart1_R', 'KneePart1_L', 'KneePart1_R'), typ='joint'), r=1)
        self.doCreateJoint(slmesh, 0)
        cmds.delete(cmds.ls(("Scapula_L_Modify3", "Scapula_R_Modify3", "IndexFinger1_L_Modify1", "IndexFinger1_R_Modify1", 
                    "MiddleFinger1_L_Modify0", "MiddleFinger1_L_Modify1", "MiddleFinger1_R_Modify0", "MiddleFinger1_R_Modify1", 
                    "RingFinger1_L_Modify0", "RingFinger1_L_Modify1", "RingFinger1_R_Modify0", "RingFinger1_R_Modify1", 
                    "PinkyFinger1_L_Modify0", "PinkyFinger1_R_Modify0", "Toes_L_Modify2", "Toes_L_Modify3", "Toes_R_Modify2", "Toes_R_Modify3"), typ='joint'))
        
    def createJoint(self, jnt, reArgsList):   #ToolList, mesh=''
        jntDagPath = om.MGlobal.getSelectionListByName(jnt).getDagPath(0)
        jntMatrix = jntDagPath.inclusiveMatrix()

        jntLoc = om.MFloatPoint(jntMatrix.getElement(3, 0), jntMatrix.getElement(3, 1), jntMatrix.getElement(3, 2))
        zSorted = sorted(reArgsList, key=lambda _loc:_loc[0].z)
        xSorted = sorted(reArgsList, key=lambda _loc:_loc[0].x)
        
        if round(jntLoc.x, 5) < 0:   #骨骼在右侧
            createList = [zSorted[-1], zSorted[0], xSorted[0], xSorted[-1]]
        else:
            createList = [zSorted[-1], zSorted[0], xSorted[-1], xSorted[0]]
        
        #pattern = re.compile("[0-9]+")
        newJntList = []
        for _jntindex, _arg in enumerate(createList):
            rot = self.getRotation(jntMatrix, jntLoc, _arg[0])
            '''
            if _arg[1]:   #hitFaceID
                """
                #根据四点坐标生成平面(会在场景中实际生成物体),分配UV
                #最终生成平面法线方向不能确定, 需要确定生成的点顺序 否则会翻转
                #点顺序会影响最终法线方向
                omFnMesh = om.MFnMesh()
                loc = [om.MPoint(0, 0, 0, 1), om.MPoint(1, 0, 0, 1), om.MPoint(0, 0, 1, 1), om.MPoint(1, 0, 1, 1)]
                omFnMesh.create(loc, [4], [0, 1, 3, 2], [0, 1, 0, 1], [0, 0, 1, 1])
                omFnMesh.assignUVs([0, 1, 0, 1], [0, 0, 1, 1])
                """
                face2edge = cmds.ls(cmds.polyListComponentConversion('%s.f[%s]' %(mesh, _arg[1]), ff=1, te=1), fl=1)
                secedge = face2edge[1]
                if len(face2edge) > 3:
                    edge2vtx = set(pattern.findall(cmds.polyInfo(face2edge[0], ev=1)[0])[1:])
                    for e in face2edge[1:]:
                        if not edge2vtx.intersection(set(pattern.findall(cmds.polyInfo(e, ev=1)[0])[1:])):
                            secedge = e
                            break
                #ToolList = [_tempcFME1, _tempcFME2, _tempLoft, _temppOCI]
                cmds.setAttr('%s.edgeIndex[0]' %ToolList[0], int(face2edge[0].split('e[', 1)[-1][:-1]))
                cmds.setAttr('%s.edgeIndex[0]' %ToolList[1], int(secedge.split('e[', 1)[-1][:-1]))
                tangentU = cmds.getAttr('%s.tu' %ToolList[3])[0]
                tangentV = cmds.getAttr('%s.tv' %ToolList[3])[0]
                normal = cmds.polyInfo('%s.f[%s]' %(mesh, _arg[1]), fn=1)[0].split(': ', 1)[-1][:-2].split(' ')

                #矩阵构成为 [[法线x, 法线y, 法线z, 0], [切线Ux, 切线Uy, 切线Uz, 0], [切线Vx, 切线Vy, 切线Vz, 0], [位置x, 位置y, 位置z, 0]]
                decMatrix = om.MMatrix([float(normal[0]), float(normal[1]), float(normal[2]), 0, 
                                            tangentU[0], tangentU[1], tangentU[2], 0, 
                                            tangentV[0], tangentV[1], tangentV[2], 0, 
                                            0, 0, 0, 1])
                rad = om.MTransformationMatrix(decMatrix).rotation()
            else:
                jntEuler = om.MEulerRotation([math.radians(i) for i in cmds.xform(jnt, q=1, ws=1, ro=1)], order=cmds.getAttr('%s.ro' %jnt)).reorder(om.MEulerRotation.kXYZ)
                rot = [math.degrees(i) for i in jntEuler]
            '''
            cmds.select(cl=1)
            newJntList.append(cmds.joint(p=(_arg[0].x, _arg[0].y, _arg[0].z), n='%s_Modify%s' %(jnt, _jntindex)))
            cmds.setAttr('%s.r' %newJntList[-1], rot[0], rot[1], rot[2])
        return newJntList

    def getRotation(self, jntMatrix, jntLoc, pointLoc):
        #取骨骼轴向量
        vectory = jntForword = om.MFloatVector(jntMatrix.getElement(0, 0), jntMatrix.getElement(0, 1), jntMatrix.getElement(0, 2))
        #骨骼指向
        normal = om.MFloatVector(pointLoc.x - jntLoc.x, pointLoc.y - jntLoc.y, pointLoc.z - jntLoc.z)
        normal.normalize()

        vectorz = -normal ^ jntForword
        vectorz.normalize()

        #vectory = -normal ^ jntForword
        #vectory.normalize()
        #vectorz = normal ^ jntForword
        #vectorz.normalize()

        #矩阵构成为 [[法线x, 法线y, 法线z, 0], [切线Ux, 切线Uy, 切线Uz, 0], [切线Vx, 切线Vy, 切线Vz, 0], [位置x, 位置y, 位置z, 0]]
        decMatrix = om.MMatrix([normal.x, normal.y, normal.z, 0,
                                vectory.x, vectory.y, vectory.z, 0,
                                vectorz.z, vectorz.y, vectorz.z, 0,
                                0, 0, 0, 1])
        '''
        #分解出旋转矩阵
        norm = count = 0
        while count < 100 or norm > .0001:
            Mnext = om.MMatrix.kIdentity
            Mit = decMatrix.transpose().inverse()
            for i, v in enumerate(decMatrix):
                Mnext[i] = (v + Mit[i]) * 0.5
            norm = 0
            for i in range(3):
                n = abs(decMatrix.getElement(i, 0) - Mnext.getElement(i, 0)) + \
                    abs(decMatrix.getElement(i, 1) - Mnext.getElement(i, 1)) + \
                    abs(decMatrix.getElement(i, 2) - Mnext.getElement(i, 2))
                norm = max(norm, n)
            decMatrix = Mnext
            count += 1
        rad = om.MEulerRotation().decompose(decMatrix, om.MEulerRotation.kXYZ)   #解构出弧度
        '''
        rad = om.MTransformationMatrix(decMatrix).rotation()
        return om.MVector(math.degrees(rad.x), math.degrees(rad.y), math.degrees(rad.z))   #rotate = math.degrees(rad.x)   # = rad.x * (180 / 3.14159265)
    
    def doMirrorJoint(self):
        negMatrix = om.MMatrix.kIdentity
        negMatrix.setElement(0, 0, -1)
        def mirrorMatrix(sourceDag, target):
            _Matrix = sourceDag.inclusiveMatrix()
            _NegMatrix = _Matrix * negMatrix
            Rt = om.MTransformationMatrix(_NegMatrix).translation(om.MSpace.kWorld)
            cmds.xform(target, ws=1, t=(Rt[0], Rt[1], Rt[2]))
            Rro = om.MTransformationMatrix(_NegMatrix).rotation()
            cmds.xform(target, ws=1, ro=(math.degrees(Rro.x), math.degrees(Rro.y), math.degrees(Rro.z)))

        slList = cmds.ls(sl=1, type='joint')
        if slList:
            for i in slList:
                if '_L_Modify' in i:
                    replaceR = i.replace('_L_Modify', '_R_Modify')
                    mirrorMatrix(om.MGlobal.getSelectionListByName(i).getDagPath(0), replaceR)
                elif '_M_Modify2' in i:
                    replaceM = i.replace('_M_Modify2', '_M_Modify3')
                    mirrorMatrix(om.MGlobal.getSelectionListByName(i).getDagPath(0), replaceM)
        else:
            if cmds.ls('*_L_Modify*'):
                lJointMList = om.MGlobal.getSelectionListByName('*_L_Modify*')
                for i in range(lJointMList.length()):
                    jntDag = lJointMList.getDagPath(i)
                    if jntDag.apiType() == om.MFn.kJoint:
                        replaceR = lJointMList.getSelectionStrings(i)[0].replace('_L_Modify', '_R_Modify')
                        mirrorMatrix(jntDag, replaceR)
            if cmds.ls('*_M_Modify2'):
                mJointMList = om.MGlobal.getSelectionListByName('*_M_Modify2')
                for i in range(mJointMList.length()):
                    jntDag = mJointMList.getDagPath(i)
                    if jntDag.apiType() == om.MFn.kJoint:
                        replaceM = mJointMList.getSelectionStrings(i)[0].replace('_M_Modify2', '_M_Modify3')
                        mirrorMatrix(jntDag, replaceM)
        DisplayYes().showMessage(u"完成")

    def doCreateCtrl(self):
        ctrlData = [((-.5 ,.5 ,.5 ),(-.5 ,.5 ,-.5 ),(.5 ,.5 ,-.5 ),(.5 ,.5 ,.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(-.5 ,-.5 ,-.5 ),(-.5 ,.5 ,-.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(.5 ,-.5 ,.5 ),(.5 ,.5 ,.5 ),(.5 ,.5 ,-.5 ),(.5 ,-.5 ,-.5 ),(.5 ,-.5 ,.5 ),(.5 ,-.5 ,-.5 ),(-.5 ,-.5 ,-.5)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)]
        ctrlData2 = [((-1 ,1 ,1 ),(-1 ,1 ,-1 ),(1 ,1 ,-1 ),(1 ,1 ,1 ),(-1 ,1 ,1 ),(-1 ,-1 ,1 ),(-1 ,-1 ,-1 ),(-1 ,1 ,-1 ),(-1 ,1 ,1 ),(-1 ,-1 ,1 ),(1 ,-1 ,1 ),(1 ,1 ,1 ),(1 ,1 ,-1 ),(1 ,-1 ,-1 ),(1 ,-1 ,1 ),(1 ,-1 ,-1 ),(-1 ,-1 ,-1)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)]
        
        allCtrl = []
        allConstraint = []
        doList = cmds.ls(sl=1, typ='joint') if cmds.ls(sl=1, typ='joint') else cmds.ls('*_L_Modify*', '*_R_Modify*', '*_M_Modify*', typ='joint')
        for jnt in doList:
            _surfix = ''
            if '_L_Modify' in jnt:
                _ifix = jnt.replace("_L_", '_')
                _surfix = '_L'
            elif '_R_Modify' in jnt:
                _ifix = jnt.replace("_R_", '_')
                _surfix = '_R'
            elif '_M_Modify' in jnt:
                _ifix = jnt.replace("_M_", '_')
                _surfix = '_M'
            else:
                continue
            _ctrlGrp = cmds.group(n='%s_Ctrl_Grp' %jnt, em=1, w=1)
            allCtrl.append(_ctrlGrp)
            _RbfCtrl = cmds.curve(n='%s_CtrlRbf%s' %(_ifix, _surfix), d=1, p=ctrlData2[0], k=ctrlData2[1])
            _curShape = cmds.listRelatives(_RbfCtrl, c=1)[0]
            cmds.setAttr("%s.overrideEnabled" %_curShape, 1)
            cmds.setAttr('%s.overrideColor' %_curShape, 6)
            cmds.parent(_RbfCtrl, _ctrlGrp)
            _Ctrl = cmds.curve(n='%s_Ctrl' %jnt, d=1, p=ctrlData[0], k=ctrlData[1])
            cmds.parent(_Ctrl, _RbfCtrl)
            cmds.matchTransform(_ctrlGrp, jnt, pos=1, rot=1)   #pos=1, rot=1, scl=1
            _jntName = jnt.split('_Modify')[0]
            _jnt50 = cmds.ls('%s_50' %_jntName, l=1, typ='joint')
            if _jnt50 and 'RBF_halfRot' in _jnt50[0]:
                cmds.parentConstraint(_jnt50[0], _ctrlGrp, mo=1, w=1)
            else:
                cmds.parentConstraint(_jntName, _ctrlGrp, mo=1, w=1)
            allConstraint.append(cmds.parentConstraint(_Ctrl, jnt, w=1)[0])
            #allConstraint.append(cmds.scaleConstraint(_Ctrl, jnt, w=1)[0])
            cmds.connectAttr('%s.s' %_RbfCtrl, '%s.s' %jnt, f=1)
            cmds.setAttr('%s.displayLocalAxis' %jnt, 0)
        cmds.parent(allCtrl, 'RBF_System')
        cmds.parent(allConstraint, 'RBF_Constraint')

        if not cmds.ls('RBF_System.RBF_Rig'):
            cmds.addAttr("RBF_System", ln="RBF_Rig", at='bool')
            cmds.setAttr('RBF_System.RBF_Rig', e=1, keyable=1)
            cmds.setAttr('RBF_System.RBF_Rig', 1)
        Rbf_Rig_Crv = cmds.ls("*_CtrlRbf_*", type="transform")
        for cur in Rbf_Rig_Crv:
            cmds.connectAttr('RBF_System.RBF_Rig', '%s.visibility' %cmds.listRelatives(cur, c=1, s=1)[0], f=1)
        DisplayYes().showMessage(u"完成")

    def doMirrorCtrl(self):
        def mirrorShape(source, target):
            cmds.connectAttr('%s.local' %cmds.listRelatives(source, s=1)[0], '%s.create' %cmds.listRelatives(target, s=1)[0], f=1)
            cmds.refresh()
            cmds.disconnectAttr('%s.local' %cmds.listRelatives(source, s=1)[0], '%s.create' %cmds.listRelatives(target, s=1)[0])
            
        slList = cmds.ls(sl=1, type='transform') if cmds.ls(sl=1, type='transform') else cmds.ls('*_M_Modify2_Ctrl', '*_L_Modify*_Ctrl', '*_Modify2_CtrlRbf_M', '*_Modify*_CtrlRbf_L', type='transform')
        for i in slList:
            if '_L_Modify' in i:
                replaceR = i.replace('_L_Modify', '_R_Modify')
                mirrorShape(i, replaceR)
            elif '_M_Modify2_Ctrl' in i:   #endswith
                replaceM = i.replace('_M_Modify2', '_M_Modify3')
                mirrorShape(i, replaceM)
            elif '_CtrlRbf_L' in i:   #endswith
                replaceR = i.replace('_CtrlRbf_L', '_CtrlRbf_R')
                mirrorShape(i, replaceR)
            elif '_Modify2_CtrlRbf_M' in i:   #endswith
                replaceM = i.replace('_Modify2_CtrlRbf_M', '_Modify3_CtrlRbf_M')
                mirrorShape(i, replaceM)
            
    def doCreateSimpleDriver(self):
        slList = cmds.ls(sl=1, typ='joint')
        if not slList:
            om.MGlobal.displayError(u'请选择要简易驱动的骨骼')
            return
        for n, Axis in enumerate(['x', 'y', 'z']):
            if cmds.menuItem('SimpleDriverAxis_RB%s%s' %(n, self.UiName), q=1, cb=1):
                break
        PosNeg = 1 if cmds.menuItem('SimpleDriverPos_RB%s' %self.UiName, q=1, cb=1) else -1
        
        for _jnt in slList:
            modifyCtrl = cmds.listRelatives(cmds.ls('%s_Modify*_Ctrl' %_jnt, typ='transform'), p=1)
            if not modifyCtrl:
                om.MGlobal.displayWarning(u'%s 没有对应的Modify控制器' %_jnt)
                continue
            unit = cmds.createNode('unitConversion')
            cmds.setAttr('%s.cf' %unit, 0.6366198 * PosNeg)
            cmds.connectAttr('%s.r%s' %(_jnt, Axis), '%s.input' %unit, f=1)
            for _ctrl in modifyCtrl:
                cmds.addAttr(_ctrl, ln='mult', at='double', min=0, dv=1)
                cmds.setAttr('%s.mult' %_ctrl, e=1, cb=1)
                math = cmds.createNode('floatMath')
                cmds.setAttr('%s.operation' %math, 2)
                cmds.connectAttr('%s.output' %unit, '%s.floatA' %math, f=1)
                cmds.connectAttr('%s.mult' %_ctrl, '%s.floatB' %math, f=1)
                mathMax = cmds.createNode('floatMath')
                cmds.setAttr('%s.operation' %mathMax, 5)
                cmds.connectAttr('%s.outFloat' %math, '%s.floatA' %mathMax, f=1)
                negUnit = cmds.createNode('unitConversion')
                cmds.setAttr('%s.cf' %negUnit, -1)
                cmds.connectAttr('%s.outFloat' %math, '%s.input' %negUnit, f=1)
                cmds.connectAttr('%s.output' %negUnit, '%s.floatB' %mathMax, f=1)
                cmds.connectAttr('%s.outFloat' %mathMax, '%s.tx' %_ctrl, f=1)

    def RBFCheck(self):
        try:
            if not cmds.pluginInfo('MayaUERBFPlugin', q=1, r=1):
                cmds.loadPlugin('MayaUERBFPlugin', qt=1)
        except RuntimeError as e:
            print(e)
            om.MGlobal.displayError(u'没找到RBF插件')
            return 0
        return 1

    def doCreateRBFDriver(self):
        if cmds.confirmDialog(t=u'提醒', icn='warning', m=u'RBF会使用外部插件，请不要在没有允许的情况下在项目中使用', b=[u'继续', u'取消'], db=u'取消', cb=u'取消', ds=u'取消') == u'取消':
            return
        slList = cmds.ls(sl=1, type='joint')
        if not slList:
            om.MGlobal.displayError(u'请选择要RBF驱动的骨骼')
            return
        rbfApi = UERbf.UERBFAPI(view=False)
        for i in slList:
            newSolver = rbfApi.create_rbf_solver('%s_UERBFSolver' %i, [i])
            newSolver.set_distance_method(2)
            newSolver.set_normalize_method(1)
            newSolver.set_function_type(0)
            _JntInfo = i.split('_')
            rbfApi.add_driven_transforms(cmds.ls('%s_Modify*_CtrlRbf_%s' %(_JntInfo[0], _JntInfo[1]), type='transform'), newSolver)

    def doAdvTemplateCreateRBF(self):
        if cmds.confirmDialog(t=u'提醒', icn='warning', m=u'RBF会使用外部插件，请不要在没有允许的情况下在项目中使用', b=[u'继续', u'取消'], db=u'取消', cb=u'取消', ds=u'取消') == u'取消':
            return
        advTemplate = [
            ['Head_M', [], 
                ['Head_M_Rzn40', [0, 0, -40]], ['Head_M_Rz25', [0, 0, 25]], ['Head_M_Ryn40', [0, -40, 0]], ['Head_M_Ry40', [0, 40, 0]]],
            ['Neck_M', [], 
                ['Neck_M_Rzn50', [0, 0, -50]], ['Neck_M_Rz40', [0, 0, 40]], ['Neck_M_Ryn40', [0, -40, 0]], ['Neck_M_Ry40', [0, 40, 0]]],
            ['Spine1_M', [], 
                ['Spine1_M_Rzn40', [0, 0, -40]], ['Spine1_M_Rz40', [0, 0, 40]], ['Spine1_M_Ryn40', [0, -40, 0]], ['Spine1_M_Ry40', [0, 40, 0]]],
            ['Spine2_M', [], 
                ['Spine2_M_Rzn40', [0, 0, -40]], ['Spine2_M_Rz40', [0, 0, 40]], ['Spine2_M_Ryn40', [0, -40, 0]], ['Spine2_M_Ry40', [0, 40, 0]]], 
            ['Spine3_M', [], 
                ['Spine3_M_Rzn40', [0, 0, -40]], ['Spine3_M_Rz40', [0, 0, 40]], ['Spine3_M_Ryn40', [0, -40, 0]], ['Spine3_M_Ry40', [0, 40, 0]]],
            ['Scapula_L', [], 
                ['Scapula_L_Ryn40', [0, -40, 0]], ['Scapula_L_Rzn30', [0, 0, -30]], ['Scapula_L_Rz30', [0, 0, 30]]],
            ['Shoulder_L', [], 
                ['Shoulder_L_Ryn50', [0, -50, 0]], ['Shoulder_L_Ryn110', [0, -110, 0]], ['Shoulder_L_Ry35', [0, 35, 0]], ['Shoulder_L_Rz80', [0, 0, 80]], ['Shoulder_L_Rzn80', [0, 0, -80]], 
                ['Shoulder_L_Ryn110_Rz40', [0, -110, 40]], ['Shoulder_L_Ryn110_Rzn40', [0, -110, -40]], ['Shoulder_L_Ryn110_Rz80', [0, -110, 80]], ['Shoulder_L_Ryn110_Rzn80', [0, -110, -80]]],
            ['Elbow_L', cmds.ls('ShoulderPart1_Modify*_CtrlRbf_L', type='transform'), 
                ['Elbow_L_Rz90', [0, 0, 90]], ['Elbow_L_Rz120', [0, 0, 120]]],
            ['Wrist_L', [], 
                ['Wrist_L_Ry80', [0, 80, 0]], ['Wrist_L_Ryn90', [0, -90, 0]], ['Wrist_L_Rz60', [0, 0, 60]], ['Wrist_L_Rzn60', [0, 0, -60]], 
                ['Wrist_L_Ry80_Rz60', [0, 80, 60]], ['Wrist_L_Ry80_Rzn60', [0, 80, -60]], ['Wrist_L_Ryn90_Rz60', [0, -90, 60]], ['Wrist_L_Ryn90_Rzn60', [0, -90, -60]]],
            ['Hip_L', [], 
                ['Hip_L_Rz90', [0, 0, 90]], ['Hip_L_Rzn50', [0, 0, -50]], ['Hip_L_Ryn90', [0, -90, 0]], ['Hip_L_Rx45_Rz90', [45, 0, 90]]],
            ['Knee_L', cmds.ls('HipPart1_Modify*_CtrlRbf_L', type='transform') + ['KneePart1_Modify1_CtrlRbf_L', 'KneePart1_Modify3_CtrlRbf_L'], 
                ['Knee_L_Rzn90', [0, 0, -90]], ['Knee_L_Rzn120', [0, 0, -120]]], 
            ['Ankle_L', ['KneePart1_Modify0_CtrlRbf_L', 'KneePart1_Modify2_CtrlRbf_L'], 
                ['Ankle_L_Rzn60', [0, 0, -60]], ['Ankle_L_Rz50', [0, 0, 50]], ['Ankle_L_Ry50', [0, 50, 0]], ['Ankle_L_Ryn50', [0, -50, 0]]],
            ['Toes_L', [], 
                ['Toes_L_Rz60', [0, 0, 60]], ['Toes_L_Rzn60', [0, 0, -60]]]
        ]
        rbfApi = UERbf.UERBFAPI(view=False)
        for i in advTemplate:
            newSolver = rbfApi.create_rbf_solver('%s_UERBFSolver' %i[0], [i[0]])
            newSolver.set_distance_method(2)
            newSolver.set_normalize_method(1)
            newSolver.set_function_type(0)
            _JntInfo = i[0].split('_')
            rbfApi.add_driven_transforms(cmds.ls('%s_Modify*_CtrlRbf_%s' %(_JntInfo[0], _JntInfo[1]), type='transform') + i[1], newSolver)
            for _pose in i[2:]:
                print(i[0], _pose[1])
                cmds.setAttr('FK%s.r' %i[0], _pose[1][0], _pose[1][1], _pose[1][2])
                #cmds.refresh()
                rbfApi.create_pose(_pose[0], newSolver)
            cmds.setAttr('FK%s.r' %i[0], 0, 0, 0)


class RayIntersection():

    def __init__(self, objDagPath):
        self.allVector = [om.MVector.kXaxisVector, om.MVector.kXnegAxisVector, 
                        om.MVector.kYaxisVector, om.MVector.kYnegAxisVector, 
                        om.MVector.kZaxisVector, om.MVector.kZnegAxisVector]
        self.objFnMesh = om.MFnMesh(objDagPath)
        self.FnMeshParams = self.objFnMesh.autoUniformGridParams()
    
    def doIt(self, jntDagPath, TwistAxis='x'):
        """
        objDagPath: 模型MDagPath
        jntApiList: 骨骼MSelectionList
        """
        if TwistAxis == 'x':
            rayDirection = self.allVector[2:]
        elif TwistAxis == 'y':
            rayDirection = self.allVector[0,1,4,5]
        elif TwistAxis == 'z':
            rayDirection = self.allVector[:4]
        
        jntWorldMatrix = jntDagPath.inclusiveMatrix()
        jntWorldLoc = om.MPoint(jntWorldMatrix.getElement(3, 0), jntWorldMatrix.getElement(3, 1), jntWorldMatrix.getElement(3, 2))
        #jntWorldLoc = om.MTransformationMatrix(jntWorldMatrix).translation(om.MSpace.kWorld)
        closePoint, closeFaceID = self.objFnMesh.getClosestPoint(jntWorldLoc, om.MSpace.kWorld)
        closeDistance = closePoint.distanceTo(jntWorldLoc)
        
        reArgList = []
        for _direction in rayDirection:
            reArgs = self.objFnMesh.closestIntersection(
                om.MFloatPoint(jntWorldLoc),
                om.MFloatVector(_direction * jntWorldMatrix),
                om.MSpace.kWorld,
                closeDistance * 2.5,   #射线最大距离
                False,
                accelParams = self.FnMeshParams
            )   #return: hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2
            if reArgs and reArgs[1]:   #2018不返回None有默认值 加一个数值存在判断
                reArgList.append([reArgs[0], reArgs[2]])
            else:
                reArgList.append([jntWorldLoc + (_direction * jntWorldMatrix), None])
        return reArgList


#CreateModifyJoint().Ui()
