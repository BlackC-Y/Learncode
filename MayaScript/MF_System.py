# -*- coding: UTF-8 -*-
from maya import cmds
import maya.OpenMaya as Om
import decimal
import re
import math

def MFCreateUi():
    Ver = 1.1
    MFCreateUi = 'MFCreate'
    if cmds.window(MFCreateUi, q=1, ex=1):
        cmds.deleteUI(MFCreateUi)
    cmds.window(MFCreateUi, t='%s%s' %(MFCreateUi, Ver), wh=(120, 60), tlb=1)
    cmds.columnLayout(cat=('both', 2), rs=2, cw=120)
    cmds.button('CreateMFButton', l='Create_MF', c=lambda *args: createMF())
    if cmds.ls('master_MF'):
        cmds.button('CreateMFButton', e=1, bgc=[0, 1, 0])
        if not cmds.ls('MidJoint_loc'):
            cmds.button('CreateMFButton', e=1, nbg=0)
    cmds.showWindow(MFCreateUi)

def createMF():
    JointName = ['Center_Joint', 'YuAxis_Joint', 'YdAxis_Joint', 'XlAxis_Joint', 'XrAxis_Joint', 'ZfAxis_Joint', 'ZbAxis_Joint',
            'L2_1_Joint',               'L2_3_Joint',                             'L2_7_Joint',               'L2_9_Joint',
            'L1_1_Joint', 'L1_2_Joint', 'L1_3_Joint', 'L1_4_Joint', 'L1_6_Joint', 'L1_7_Joint', 'L1_8_Joint', 'L1_9_Joint',
            'L3_1_Joint', 'L3_2_Joint', 'L3_3_Joint', 'L3_4_Joint', 'L3_6_Joint', 'L3_7_Joint', 'L3_8_Joint', 'L3_9_Joint']
    if cmds.ls('master_MF|MidJoint_loc'):
        for i in ['MidJoint_loc', 'UpJoint_loc']:
            jointN = JointName[0] if i == 'MidJoint_loc' else JointName[1]
            cmds.select(cl=1)
            cmds.delete(cmds.parentConstraint(i, cmds.joint(n=jointN), w=1), i)
        midPosition = cmds.getAttr(JointName[0] + '.ty')
        distance = cmds.getAttr(JointName[1] + '.ty') - midPosition
        for i in JointName[2:]:
            cmds.select(cl=1)
            cmds.joint(n=i)
        for i in JointName[3:11]:
            cmds.setAttr(i + '.ty', midPosition)
        for i in JointName[11:19]:
            cmds.setAttr(i + '.ty', midPosition - distance)
        for i in JointName[19:]:
            cmds.setAttr(i + '.ty', midPosition + distance)
        cmds.setAttr(JointName[2] + '.ty', midPosition - distance)
        for n, s in zip([3, 5, 7, 7, 8, 9, 11, 11, 12, 13, 14, 16, 19, 19, 20, 21, 22, 24],
                        ['x', 'z', 'x', 'z', 'z', 'x', 'x', 'z', 'z', 'z', 'x', 'x', 'x', 'z', 'z', 'z', 'x', 'x']):
            cmds.setAttr('%s.t%s' % (JointName[n], s), distance)
        for n, s in zip([4, 6, 8, 9, 10, 10, 13, 15, 16, 17, 18, 18, 21, 23, 24, 25, 26, 26],
                        ['x', 'z', 'x', 'z', 'x', 'z', 'x', 'x', 'z', 'z', 'x', 'z', 'x', 'x', 'z', 'z', 'x', 'z']):
            cmds.setAttr('%s.t%s' % (JointName[n], s), -distance)
        _v = [(0, 1, 0), (1, 0, 0), (0, 0, 1)]
        Attr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
        for i, a in zip(JointName[:7], [9, 0, 0, 1, 1, 2, 2]):
            if a == 9:
                for v, n in zip(_v, [['CenterY_Joint', '.ry'], ['CenterX_Joint', '.rx'], ['CenterZ_Joint', '.rz']]):
                    cmds.delete(cmds.parentConstraint(i, cmds.parent(
                                    cmds.group(cmds.circle(nr=v, r=2*distance+1, n=n[0] + '_Ctrl'), n=n[0] + '_Ctrl_grp'), 'master_MF'), w=1),
                                cmds.parentConstraint(i, cmds.parent(
                                    cmds.nurbsPlane(ax=v, w=3.5*distance, ch=0, n=n[0].rsplit('_')[0] + '_Surface'), 'master_MF'), w=1))
                    for l in Attr:
                        if l == n[1]:
                            continue
                        cmds.setAttr('%s_Ctrl%s' % (n[0], l), l=1)
            else:
                cmds.delete(cmds.parentConstraint(i, cmds.parent(
                                cmds.group(cmds.circle(nr=_v[a], r=2*distance+1, n=i + '_Ctrl'), n=i + '_Ctrl_grp'), 'master_MF'), w=1),
                            cmds.parentConstraint(i, cmds.parent(
                                cmds.nurbsPlane(ax=_v[a], w=3.5*distance, ch=0, n=i.rsplit('_')[0] + '_Surface'), 'master_MF'), w=1))
                for l in Attr:
                    cmds.setAttr('%s_Ctrl%s' % (i, l), l=1)
                cmds.setAttr('%s_Ctrl.r%s' % (i, i[0].lower()), l=0)
        '''
        getUVface = Om.MSelectionList()
        getUVface.add('YuAxis_Surface')
        faceDagPath = Om.MDagPath()
        getUVface.getDagPath(0, faceDagPath)
        scriputil = Om.MScriptUtil()
        paramu = scriputil.asDoublePtr()
        scriputil2 = Om.MScriptUtil()
        paramv = scriputil2.asDoublePtr()
        _temp_getUVJoint = JointName[19:]
        _temp_getUVJoint.append('YuAxis_Joint')
        for i in _temp_getUVJoint:
            jointpos = cmds.xform(i, q=1, ws=1, t=1)
            mPoint = Om.MPoint(jointpos[0], jointpos[1], jointpos[2])
            surfacea = Om.MFnNurbsSurface(faceDagPath).getParamAtPoint(mPoint, paramu, paramv, Om.MSpace.kWorld)
            uvFloat.append([float(decimal.Decimal(str(scriputil.getDouble(paramu))).quantize(decimal.Decimal('%.3f' % 1))),
                                    float(decimal.Decimal(str(scriputil.getDouble(paramv))).quantize(decimal.Decimal('%.3f' % 1)))])
        '''
        cmds.select(cl=1)
        cmds.parent('Center_Joint', cmds.joint(n='RootJoint'))
        cmds.parent(JointName[1:], 'Center_Joint')
        cmds.parent('RootJoint', cmds.spaceLocator(n='_keyInfoLoc'), 'master_MF')
        cmds.setAttr(cmds.group(cmds.ls("master_MF|*_Surface"), n='MF_Surface_grp') + '.visibility', 0)
        posInfo = ''
        for i in JointName:
            xpos = cmds.xform(i, q=1, t=1, os=1)
            posInfo += '%s * %s * %s * %s | ' % (i, xpos[0], xpos[1], xpos[2])
        cmds.setAttr('master_MF.JointPos', posInfo, typ='string')
        cmds.button('CreateMFButton', e=1, nbg=0)
        cmds.button('CreateMFButton', e=1, en=0)
    else:
        masterC = cmds.circle(nr=(0, 1, 0), r=4, ch=0, n='master_MF')
        cmds.addAttr('|master_MF', ln="CtrlJoint", dt="string")
        cmds.addAttr('|master_MF', ln="JointPos", dt="string")
        cmds.setAttr(cmds.listRelatives(masterC, c=1, s=1)[0] + '.overrideEnabled', 1)
        cmds.setAttr(cmds.listRelatives(masterC, c=1, s=1)[0] + '.overrideColor', 17)
        cmds.setAttr(cmds.spaceLocator(n='MidJoint_loc')[0] + '.ty', 1)
        Attr = ['.tx', '.tz', '.rx', '.ry', '.rz']
        for i in Attr:
            cmds.setAttr('MidJoint_loc' + i, lock=1)
        cmds.setAttr(cmds.duplicate('MidJoint_loc', rr=1, n='UpJoint_loc')[0] + '.ty', 2)
        cmds.parent('UpJoint_loc', 'MidJoint_loc', masterC)
        cmds.button('CreateMFButton', e=1, bgc=[0, 1, 0])


class MFAni():

    def MFAniUi(self):
        freeRotate = 0
        MFAniUi = 'MFAni'
        if cmds.window(MFAniUi, q=1, ex=1):
                cmds.deleteUI(MFAniUi)
        cmds.window(MFAniUi, t=MFAniUi + '_v1.1', wh=(120, 150), tlb=1)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=120)
        cmds.button('SetVtrlButton', l='SetCtrl', c=lambda *args: self.setCtrl(None), vis=freeRotate)
        cmds.popupMenu()
        cmds.menuItem(l='Break', c=lambda *args: self.Break(None))
        cmds.checkBox('KeymodecheckBox', l='Key frame mode', onc=lambda *args: cmds.text('AniWartext', e=1, vis=1), ofc=lambda *args: cmds.text('AniWartext', e=1, vis=0))
        cmds.text('AniWartext', l='If just start make Ani,\nplease right click\nthis test.', vis=0)
        cmds.popupMenu()
        cmds.menuItem(l='Set the current frame to start', ann='Only uesd from First !!!', c=lambda *args: self.setcurrentframe())
        cmds.menuItem(l='Resume Joint Pos', ann='Restore start position', c=lambda *args: self.reJointPose())
        cmds.button(l='Rotate90', c=lambda *args: self.setCtrl(90))
        cmds.button(l='Rotate-90', c=lambda *args: self.setCtrl(-90))
        cmds.showWindow(MFAniUi)

        self.JointName = ['Center_Joint', 'YuAxis_Joint', 'YdAxis_Joint', 'XlAxis_Joint', 'XrAxis_Joint', 'ZfAxis_Joint', 'ZbAxis_Joint',
                            'L2_1_Joint',               'L2_3_Joint',                             'L2_7_Joint',               'L2_9_Joint',
                            'L1_1_Joint', 'L1_2_Joint', 'L1_3_Joint', 'L1_4_Joint', 'L1_6_Joint', 'L1_7_Joint', 'L1_8_Joint', 'L1_9_Joint',
                            'L3_1_Joint', 'L3_2_Joint', 'L3_3_Joint', 'L3_4_Joint', 'L3_6_Joint', 'L3_7_Joint', 'L3_8_Joint', 'L3_9_Joint']

    def setcurrentframe(self):
        currentframe = cmds.currentTime(q=1)
        for j in self.JointName[1:]:
            cmds.setKeyframe('%s.t' % j, '%s.r' % j, t=currentframe)
        cmds.setKeyframe('_keyInfoLoc.t', '_keyInfoLoc.r', t=currentframe)

    def reJointPose(self):
        for i in cmds.getAttr('|master_MF.JointPos').split('|')[:-1]:
            _tempJP = i.split(' * ')
            cmds.setAttr(_tempJP[0] + '.t', float(_tempJP[1]), float(_tempJP[2]), float(_tempJP[3]))

    def multMatrix(self, inM, axis, angle):
        tM = [[0 for y in range(3)] for x in range(3)]
        angle *= math.pi/180
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        cosa = float(decimal.Decimal(str(math.cos(angle))).quantize(decimal.Decimal('%.8f' % 1)))
        sina = float(decimal.Decimal(str(math.sin(angle))).quantize(decimal.Decimal('%.8f' % 1)))
        if axis == '.rx':
            tM[0][0] = 1
            tM[1][1] = tM[2][2] = cosa
            tM[1][2] = -sina
            tM[2][1] = sina
        elif axis == '.ry':
            tM[0][0] = tM[2][2] = cosa
            tM[0][2] = -sina
            tM[1][1] = 1
            tM[2][0] = sina
        elif axis == '.rz':
            tM[0][0] = tM[1][1] = cosa
            tM[0][1] = -sina
            tM[1][0] = sina
            tM[2][2] = 1
        multFinish = [
            inM[0]  * tM[0][0] + inM[1]  * tM[1][0] + inM[2]  * tM[2][0], inM[0]  * tM[0][1] + inM[1]  * tM[1][1] + inM[2]  * tM[2][1], inM[0]  * tM[0][2] + inM[1]  * tM[1][2] + inM[2]  * tM[2][2], inM[3],
            inM[4]  * tM[0][0] + inM[5]  * tM[1][0] + inM[6]  * tM[2][0], inM[4]  * tM[0][1] + inM[5]  * tM[1][1] + inM[6]  * tM[2][1], inM[4]  * tM[0][2] + inM[5]  * tM[1][2] + inM[6]  * tM[2][2], inM[7],
            inM[8]  * tM[0][0] + inM[9]  * tM[1][0] + inM[10] * tM[2][0], inM[8]  * tM[0][1] + inM[9]  * tM[1][1] + inM[10] * tM[2][1], inM[8]  * tM[0][2] + inM[9]  * tM[1][2] + inM[10] * tM[2][2], inM[11],
            inM[12] * tM[0][0] + inM[13] * tM[1][0] + inM[14] * tM[2][0], inM[12] * tM[0][1] + inM[13] * tM[1][1] + inM[14] * tM[2][1], inM[12] * tM[0][2] + inM[13] * tM[1][2] + inM[14] * tM[2][2], inM[15]
        ]
        return multFinish
        #multMatrix([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 2, 2, 1], '.ry', 90)

    def setCtrl(self, Rotate):
        ctrl = cmds.ls(sl=1)[0]
        if not re.match('\S*_Joint_Ctrl', ctrl):
            return
        midName = ctrl.split('_')[0]
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        getUVface = Om.MSelectionList()
        getUVface.add(midName + '_Surface')
        faceDagPath = Om.MDagPath()
        getUVface.getDagPath(0, faceDagPath)
        ctrlJoint = []
        for i in self.JointName:
            jointpos = cmds.xform(i, q=1, ws=1, t=1)
            distance = Om.MFnNurbsSurface(faceDagPath).distanceToPoint(Om.MPoint(jointpos[0], jointpos[1], jointpos[2]), Om.MSpace.kWorld)
            if float(decimal.Decimal(str(distance)).quantize(decimal.Decimal('%.3f' % 1))) == 0:
                ctrlJoint.append(i)
        if Rotate:
            rotateAxis = ['.rx', '.ry', '.rz']
            for i in rotateAxis:
                if not cmds.getAttr(ctrl + i, l=1):
                    _tempAxis = i
        newFrame = cmds.currentTime(q=1)
        preFrame = cmds.findKeyframe('_keyInfoLoc', t=(newFrame, newFrame), w='previous')
        halfFrame = int(newFrame - ((newFrame - preFrame) / 2))
        if cmds.checkBox('KeymodecheckBox', q=1, v=1):
            for j in ctrlJoint:
                if j == 'Center_Joint':
                    continue
                cmds.setKeyframe('%s.t' % j, '%s.r' % j, t=preFrame)
        twoAngle = 45 if Rotate == 90 else -45
        for f in [halfFrame, newFrame]:
            if 'Center_Joint' in ctrlJoint:
                ctrlJoint.remove('Center_Joint')
                for j in ctrlJoint:
                    cmds.xform(j, m=self.multMatrix(cmds.xform(j, q=1, m=1), _tempAxis, twoAngle))
            else:
                for j in ctrlJoint:
                    cmds.xform(j, m=self.multMatrix(cmds.xform(j, q=1, m=1), _tempAxis, twoAngle))
            if cmds.checkBox('KeymodecheckBox', q=1, v=1):
                for j in ctrlJoint:
                    cmds.setKeyframe('%s.t' % j, '%s.r' % j, t=f)
                cmds.setKeyframe('_keyInfoLoc.t', '_keyInfoLoc.r', t=f)
        cmds.select(ctrl, r=1)
        cmds.button('SetVtrlButton', e=1, bgc=[0, 1, 0])

    def Break(self, mode):
        _oldMidJoint = cmds.getAttr('master_MF.CtrlJoint')
        if not _oldMidJoint:
            sljnt = cmds.ls(sl=1, typ='joint')
            if not sljnt:
                #Om.MGlobal.displayWarning('Not find Break. If need Break, select Mid Joint')
                return
            _oldMidJoint = sljnt[0]
        childJ = cmds.listRelatives(_oldMidJoint, c=1)
        parentJ = cmds.listRelatives(_oldMidJoint, p=1)[0]
        cmds.parent(childJ, parentJ)
        if mode:
            return childJ
        if cmds.ls('_temp_CtrlConstraint'):
            cmds.delete('_temp_CtrlConstraint')
        cmds.setAttr('master_MF.CtrlJoint', '', typ='string')
        cmds.button('SetVtrlButton', e=1, nbg=0)

MFCreateUi()
MFAni().MFAniUi()