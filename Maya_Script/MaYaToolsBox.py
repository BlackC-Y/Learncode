# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from maya import cmds, mel
from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2
from maya import OpenMaya as Om, OpenMayaAnim as OmAni, OpenMayaUI as OmUI
from maya.api import OpenMaya as om, OpenMayaAnim as omAni
import decimal
import re
import os

class MaYaToolsBox():

    __Verision = 1.0
    
    def ToolUi(self):
        self.Info = {
        'createLocator': [u'在选择物体的位置创建Locator', 'self.createLocator()'],
        'polytoCurve': [u'批量提取曲线 - 仅适用于单片模型', 'self.polytoCurve()'],
        'movevtx': [u'修型时传递点 \n选择要传递的点 填写被传递的模型', 'self.movevtx_UI()'],
        'samevtx': [u'移动点达到对称修形 \n选择原模型上要对称的点 分别填写模型', 'self.samevtx_UI()'],
        'xiuxingJoint': [u'创建修型骨骼(高自定义) \n选择要修型的骨骼', 'self.xiuxingJoint()'],
        'xiuxingJointHang': [u'创建修型骨骼(航少版) \n选择要修型的骨骼', 'self.xiuxingJointHang()'],
        'TransferUV': [u'传递UV \n选择UV模型+要传递的模型', 'self.TransferUV()'],
        'createFollicleOnface': [u'在surface曲面上创建毛囊和骨骼', 'self.createFollicleOnface_UI()'],
        'CopyWeightTool': [u'拷贝权重工具', 'CopyWeightTool().Ui()'],
        'cur2IK_FX': [u'动力学曲线 IK', 'cur2IK_FX_Ui()'],
        'DataSave': [u'临时储存物体或位置', 'DataSaveUi().Ui()'],
        'PSD_Pose': [u'PSD修型', 'PSD_PoseUi_KitKat().ToolUi()'],
        'Rivet': [u'Rivet铆钉', 'cRivet("follicle")'],
        'WeightTool': [u'点权重调整 \nSave/Load权重', 'WeightTool_JellyBean().ToolUi()'],
        'WeightCheckTool': [u'权重最大影响值检查 清理', 'WeightCheckTool_JellyBean().ToolUi()'],
            }

        ToolUi = 'MaYaToolsBox'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.columnLayout('MainCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.textField('searchText', h=24, tcc=lambda *args: self.refreshToolList(cmds.textField('searchText', q=1, tx=1)))
        cmds.textScrollList('ToolList', ams=0, h=200, sc=lambda *args:
                                cmds.text('detailText', e=1, l=self.Info[cmds.textScrollList('ToolList', q=1, si=1)[0]][0]))
        cmds.columnLayout('EditCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.setParent('..')
        cmds.text('detailText', p='EditCL', h=100, l=u'说明:')
        cmds.button(l=u'执行', c=lambda *args: self.doProc())
        for i in self.Info:
            cmds.textScrollList('ToolList', e=1, a=i)
        cmds.showWindow(ToolUi)

    def refreshToolList(self, string):
        cmds.textScrollList('ToolList', e=1, ra=1)
        for i in self.Info:
            if string.lower() in i.lower() or string.lower() in self.Info[i][0].lower():
                cmds.textScrollList('ToolList', e=1, a=i)

    def doProc(self):
        cmd = self.Info[cmds.textScrollList('ToolList', q=1, si=1)[0]][1]
        exec(cmd)

    def createLocator(self):
        alist = cmds.ls(sl=1, fl=1)
        for i in alist:
            txyz = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr(cmds.spaceLocator(n=i+'_loc')[0]+'.translate', txyz[0], txyz[1], txyz[2])

    def polytoCurve(self):
        blist = cmds.ls(sl=1)
        for i in blist:
            vnum = cmds.polyEvaluate(i, v=1)
            for v in range(vnum):
                enum = cmds.ls(cmds.polyListComponentConversion(i + '.vtx[' + str(v) + ']', fv=1, ff=1, fuv=1, fvf=1, te=1), fl=1)
                if len(enum) == 4:
                    break
            arclen = []
            for e in enum:
                elist = cmds.polySelectSp(e, q=1, loop=1)
                earclen = 0.0
                for el in elist:
                    earclen += cmds.arclen(el)
                arclen.append(earclen)
            cmds.polySelectSp(enum[arclen.index(max(arclen))], loop=1)
            cname = cmds.rename(cmds.polyToCurve(
                ch=0, form=2, degree=3), i + '_Cur')
            if cmds.xform(cname + '.cv[0]', q=1, ws=1, t=1)[1] < cmds.xform(cname + '.cv[' + str(cmds.getAttr(cname + ".controlPoints", size=1)) + ']', q=1, ws=1, t=1)[1]:
                cmds.reverseCurve(cname, ch=0, rpo=1)

    def movevtx_UI(self):
        ui = 'ToolsBoxUI1'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='movevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('UI1objTextFieldGrp', l=u'模型', h=28, cw2=(30, 130))
        cmds.button('UI1RunButton', l="Run", h=28, w=100, c=lambda*args: self.movevtx(cmds.textFieldGrp('UI1objTextFieldGrp', q=1, tx=1)))
        cmds.window(ui, e=True, wh=(180, 100))
        cmds.showWindow(ui)

    def movevtx(self, obj=''):
        # UI
        clist = cmds.ls(sl=1, fl=1)
        for i in clist:
            flo = []
            targe = obj + '.vtx[' + i.split('[', 1)[1]
            for u in range(3):
                flo.append(cmds.xform(i, q=1, t=1, ws=1)[u] - cmds.xform(targe, q=1, t=1, ws=1)[u])
            cmds.select(targe, r=1)
            cmds.move(flo[0], flo[1], flo[2], r=1, os=1, wd=1)
        cmds.select(cl=1)

    def samevtx_UI(self):
        # UI
        ui = 'ToolsBoxUI2'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='samevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('UI2obj1TextFieldGrp',l=u'已修形模型', h=28, cw2=(60, 150))
        cmds.textFieldGrp('UI2obj2TextFieldGrp',l=u'要对称模型', h=28, cw2=(60, 150))
        cmds.button('RunButton', l="Run", h=28, w=100, c=lambda *args:
                    self.samevtx(cmds.textFieldGrp('UI2obj1TextFieldGrp', q=1, tx=1), cmds.textFieldGrp('UI2obj2TextFieldGrp', q=1, tx=1)))
        cmds.window(ui, e=True, wh=(220, 100))
        cmds.showWindow(ui)

    def samevtx(self, obj1='', obj2=''):
        list = cmds.ls(sl=1, fl=1)
        obj = list[0].split('.', 1)[0]
        mel.eval("reflectionSetMode objectx;")
        for i in list:
            lvtxT = cmds.xform(obj1+'.'+i.split('.', 1)[1], q=1, os=1, t=1)
            cmds.select(i, sym=1, r=1)
            dvtx = cmds.ls(sl=1, fl=1)
            del dvtx[dvtx.index(i)]
            cmds.xform(obj2+'.'+dvtx[0].split('.', 1)[1], os=1, t=(lvtxT[0]*-1, lvtxT[1], lvtxT[2]))
        mel.eval("reflectionSetMode none;")

    def xiuxingJoint(self):
        Raxial = 'Y'     #Z
        Taxial = 'z'     #y
        joint = cmds.ls(sl=1, type="joint")[0]
        cmds.select(cl=1)
        blendJoint = cmds.joint(n=joint+"_BlendJoint")
        cmds.delete(cmds.parentConstraint(joint, blendJoint, w=1))
        cmds.parent(blendJoint, joint)
        cmds.setAttr(blendJoint+".rotate", 0, 0, 0)
        cmds.setAttr(blendJoint+".jointOrient", 0, 0, 0)
        cmds.select(cl=1)
        blendJointEnd = cmds.joint(n=joint+"_BlendJointEnd")
        cmds.delete(cmds.parentConstraint(joint, blendJointEnd, w=1))
        cmds.parent(blendJointEnd, blendJoint)
        cmds.setAttr(blendJointEnd+".rotate", 0, 0, 0)
        cmds.setAttr(blendJointEnd+".jointOrient", 0, 0, 0)
        cmds.select(cl=1)
        cmds.addAttr(blendJointEnd, ln="BlendJointScale", at='double', min=0, dv=1)
        cmds.addAttr(blendJointEnd, ln="vectorV", at='double', dv=0)
        cmds.setAttr(blendJointEnd+".BlendJointScale", e=1, keyable=1)
        cmds.setAttr(blendJointEnd+".vectorV", -1)
        cmds.setAttr(blendJointEnd+".BlendJointScale", 0.05)
        mathNode = cmds.createNode("multiplyDivide")
        cmds.connectAttr(joint+".rotate", mathNode+".input1", f=1)
        cmds.setAttr(mathNode+".input2", -.5, -.5, -.5)
        cmds.connectAttr(mathNode+".output", blendJoint+".rotate", f=1)
        floatMathA = cmds.createNode("floatMath")
        cmds.setAttr(floatMathA+".operation", 2)
        floatMathB = cmds.createNode("floatMath")
        cmds.setAttr(floatMathB+".operation", 2)
        floatMathC = cmds.createNode("floatMath")
        cmds.connectAttr(blendJointEnd+".BlendJointScale", floatMathA+".floatB", f=1)
        cmds.connectAttr(blendJointEnd+".vectorV", floatMathA+".floatA", f=1)
        cmds.setAttr(floatMathC+".floatB", 0.2)
        cmds.connectAttr(floatMathA + ".outFloat", floatMathB + ".floatB", f=1)
        cmds.connectAttr(floatMathB + ".outFloat", floatMathC + ".floatA", f=1)
        cmds.connectAttr(floatMathC + ".outFloat", blendJointEnd + ".t" + Taxial, f=1)
        cmds.connectAttr(joint + ".rotate" + Raxial, floatMathB + ".floatA", f=1)

    def xiuxingJointHang(self):
        jot_name = cmds.ls(sl=1, typ="joint")
        jot_bs_name1 = cmds.joint(n=(jot_name[0] + "_bs"), rad=3)
        jot_bs_name2 = cmds.joint(n=(jot_name[0] + "_bsend"), rad=3)
        jot_rotY = cmds.getAttr(jot_name[0] + ".jointOrientY")
        jot_rotZ = cmds.getAttr(jot_name[0] + ".jointOrientZ")
        jot_attibuteY = [".tx", ".ty", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
        jot_attibuteZ = [".tx", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
        cmds.select(cl=1)
        cnmulti1 = cmds.createNode('multiplyDivide')
        cnmulti2 = cmds.createNode('multiplyDivide')
        cnmulti3 = cmds.createNode('addDoubleLinear')
        cnmulti4 = cmds.createNode('multiplyDivide')
        cmds.connectAttr(jot_name[0] + ".rotate", cnmulti1 + ".input1", f=1)
        cmds.setAttr(cnmulti1 + ".input2", -.5, -.5, -.5)
        cmds.connectAttr(cnmulti1 + ".output", jot_bs_name1 + ".rotate", f=1)
        if abs(jot_rotY) > abs(jot_rotZ):
            cmds.connectAttr(cnmulti1 + ".input1Y", cnmulti4 + ".input1X", f=1)
            cmds.setAttr(cnmulti4 + ".input2X", 0.01)
            cmds.connectAttr(cnmulti4 + ".outputX", cnmulti2 + ".input1X", f=1)
            cmds.addAttr('jot_bs_name2', ln="BS_Long", at='double', min=-10, max=10, dv=0)
            cmds.setAttr(jot_bs_name2 + ".BS_Long", e=1, keyable=1)
            cmds.connectAttr(jot_bs_name2 + ".BS_Long", cnmulti2 + ".input2X", f=1)
            cmds.addAttr('jot_bs_name2', ln="mumu", at='double')
            cmds.connectAttr(cnmulti2 + ".outputX", cnmulti3 + ".input1", f=1)
            cmds.connectAttr(jot_bs_name2 + ".mumu", cnmulti3 + ".input2", f=1)
            cmds.connectAttr(cnmulti3 + ".output", jot_bs_name2 + ".translateZ", f=1)
            if jot_rotY > 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", 0.5)
            elif jot_rotY < 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", -0.5)
            for i in range(7):
                cmds.setAttr(jot_bs_name2 + jot_attibuteY[i], lock=1, keyable=0, channelBox=0)
        elif abs(jot_rotZ) > abs(jot_rotY):
            cmds.connectAttr(cnmulti1 + ".input1Z", cnmulti4 + ".input1X", f=1)
            cmds.setAttr(cnmulti4 + ".input2X", 0.01)
            cmds.connectAttr(cnmulti4 + ".outputX", cnmulti2 + ".input1X", f=1)
            cmds.addAttr(jot_bs_name2, ln="BS_Long", at='double', min=-10, max=10, dv=1)
            cmds.setAttr(jot_bs_name2 + ".BS_Long", e=1, keyable=0, channelBox=1)
            cmds.connectAttr(jot_bs_name2 + ".BS_Long", cnmulti2 + ".input2X", f=1)
            cmds.addAttr(jot_bs_name2, ln="mumu", at='double')
            cmds.connectAttr(cnmulti2 + ".outputX", cnmulti3 + ".input1", f=1)
            cmds.connectAttr(jot_bs_name2 + ".mumu", cnmulti3 + ".input2", f=1)
            cmds.connectAttr(cnmulti3 + ".output", jot_bs_name2 + ".translateY", f=1)
            if jot_rotZ < 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", -0.5)
            elif jot_rotZ > 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", 0.5)
            for i in range(7):
                cmds.setAttr(jot_bs_name2 + jot_attibuteZ[i], lock=1, keyable=0, channelBox=0)

    def TransferUV(self):
        dobj = cmds.ls(sl=1)
        if cmds.polyEvaluate(dobj[0], v=1) != cmds.polyEvaluate(dobj[1], v=1):
            dupobj = cmds.duplicate(dobj[1], rr=1)
            cmds.transferAttributes(dobj[0], dupobj, pos=0, nml=0, uvs=2, col=2, spa=0, sus="map1", tus="map1", sm=3, fuv=0, clb=1)
            cmds.delete(dupobj, ch=1)
            cmds.polyTransfer(dobj[1], uv=1, ao=dupobj[0])
            cmds.delete(dupobj)
        else:
            cmds.polyTransfer(dobj[1], uv=1, ao=dobj[0])

    def createFollicleOnface_UI(self):
        ui = 'ToolsBoxUI3'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='createFollicleOnface')
        cmds.columnLayout(cat=("both", 2), columnWidth=180, rowSpacing=3)
        cmds.textFieldGrp('UI3nameTextFieldGrp', l=u'名称', h=28, cw2=(50, 100))
        cmds.intFieldGrp('UI3numIntFieldGrp', l=u'数量', h=28, cw2=(50, 100))
        cmds.flowLayout(columnSpacing=5)
        cmds.checkBox('UI3JointcheckBox', l=u'创建骨骼', w=80)
        cmds.button('UI3RunButton', l="Run", h=28, w=80, c=lambda *args: self.createFollicleOnface(
                    cmds.textFieldGrp('UI3nameTextFieldGrp', q=1, tx=1),
                    cmds.intFieldGrp('UI3numIntFieldGrp', q=1, v1=1),
                    cmds.checkBox('UI3JointcheckBox', q=1, v=1)))
        cmds.setParent('..')
        cmds.showWindow(ui)

    def createFollicleOnface(self, name = '', num = '', joint = 0):
        #UI
        shape = cmds.listRelatives(cmds.ls(sl=1)[0],s=1,type='nurbsSurface')
        if not shape:
            Om.MGlobal.displayError(u'没选择曲面')
            return
        Follicle_Grp = name + "_foll_grp"
        Joint_Grp = name + "_Joint_grp"
        if cmds.ls(Follicle_Grp,typ='transform') or cmds.ls(Joint_Grp,typ='transform'):
            Om.MGlobal.displayError(u'有重名毛囊或骨骼')
            return
        cmds.group(em=1, n=Follicle_Grp)
        if joint:
            cmds.group(em=1, n=Joint_Grp)
        for i in range(num):
            if i == num:
                break
            follicT = cmds.rename(cmds.listRelatives(cmds.createNode('follicle'),p=1), name+'_foll')
            follicS = cmds.rename(cmds.listRelatives(follicT,s=1),name+'_follShape')
            cmds.connectAttr(shape+".worldSpace[0]", follicS+".inputSurface", f=1)
            cmds.connectAttr(shape+".worldMatrix[0]", follicS+".inputWorldMatrix", f=1)
            cmds.connectAttr(follicS+".outTranslate", follicT+".translate", f=1)
            cmds.connectAttr(follicS+".outRotate", follicT+".rotate", f=1)
            cmds.setAttr(follicS+".parameterV", .5)
            cmds.setAttr(follicS+".parameterU", i*1.0/(num-1))
            cmds.parent(follicT,Follicle_Grp)
            if cmds.checkBox('UI3JointcheckBox',q=1,v=1):
                cmds.select(cl=1)
                jointN = cmds.joint(n=name+i+'Joint')
                cmds.parentConstraint(follicT,jointN,weight=1)
                cmds.parent(jointN,Joint_Grp)

    def cRivet(self, mode):
        slmesh = cmds.ls(sl=1, o=1, typ='mesh')
        slsurface = cmds.ls(sl=1, o=1, typ='nurbsSurface')
        if slmesh:
            twoEdge = cmds.filterExpand(sm=32)
            if len(twoEdge) != 2:
                Om.MGlobal.displayError('Select (Two Mesh Edge)')
                return
            nCFME1 = cmds.createNode('curveFromMeshEdge', n='rivetCFME01')
            cmds.setAttr(nCFME1 + '.ei[0]', int(twoEdge[0].split('[')[1].split(']')[0]))
            cmds.connectAttr(slmesh[0] + '.w', nCFME1 + '.im', f=1)
            nCFME2 = cmds.createNode('curveFromMeshEdge', n='rivetCFME02')
            cmds.setAttr(nCFME2 + '.ei[0]', int(twoEdge[1].split('[')[1].split(']')[0]))
            cmds.connectAttr(slmesh[0] + '.w', nCFME2 + '.im', f=1)
            nLoft = cmds.createNode('loft', n='rivetLoft01')
            cmds.setAttr(nLoft + '.u', 1)
            cmds.connectAttr(nCFME1 + '.oc', nLoft + '.ic[0]', f=1)
            cmds.connectAttr(nCFME2 + '.oc', nLoft + '.ic[1]', f=1)
            if mode == 'follicle':
                locN, locgrpN = self.cLoc(0)
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr(nFollicle + '.visibility', 0)
                cmds.setAttr(nFollicle + '.sim', 0)
                cmds.connectAttr(locN + '.U', nFollicle + '.pu', f=1)
                cmds.connectAttr(locN + '.V', nFollicle + '.pv', f=1)
                cmds.connectAttr(nLoft + '.os', nFollicle + '.is', f=1)
            else:
                locN, locgrpN = self.cLoc(0)
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr(nPOSI + '.top', 1)
                cmds.connectAttr(locN + '.U', nPOSI + '.u', f=1)
                cmds.connectAttr(locN + '.V', nPOSI + '.v', f=1)
                cmds.connectAttr(nLoft + '.os', nPOSI + '.is', f=1)
        elif slsurface:
            onepoint = cmds.filterExpand(sm=41)
            if len(onepoint) != 1:
                Om.MGlobal.displayError('Select (One nurbsSurface Point)')
                return
            pointUV = re.findall(r'[[](.*?)[]]', onepoint[0])
            if mode == 'follicle':
                locN, locgrpN = self.cLoc(0, 1.0 / (cmds.getAttr('%s.mxu' %slsurface[0]) / float(pointUV[0])), 1.0 / (cmds.getAttr('%s.mxv' %slsurface[0]) / float(pointUV[1])))
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr(nFollicle + '.visibility', 0)
                cmds.setAttr(nFollicle + '.sim', 0)
                cmds.connectAttr(locN + '.U', nFollicle + '.pu', f=1)
                cmds.connectAttr(locN + '.V', nFollicle + '.pv', f=1)
                cmds.connectAttr(slsurface[0] + '.ws', nFollicle + '.is', f=1)
            else:
                locN, locgrpN = self.cLoc(1, float(pointUV[0]), float(pointUV[1]))
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr(nPOSI + '.top', 0)
                cmds.connectAttr(locN + '.U', nPOSI + '.u', f=1)
                cmds.connectAttr(locN + '.V', nPOSI + '.v', f=1)
                cmds.connectAttr(slsurface[0] + '.ws', nPOSI + '.is', f=1)
        else:
            Om.MGlobal.displayError('Select (Mesh Edge) or (nurbsSurface Point)')
            return
        if mode == 'follicle':
            cmds.connectAttr(nFollicle + '.ot', locgrpN + '.t', f=1)
            cmds.connectAttr(nFollicle + '.or', locgrpN + '.r', f=1)
        elif mode == 'Matrix':
            if not cmds.pluginInfo('decomposeMatrix', q=1, l=1):
                cmds.loadPlugin('matrixNodes', quiet=1)
            nFBFM = cmds.createNode('fourByFourMatrix', n='rivetFBFM01')
            cmds.connectAttr(nPOSI + '.nx', nFBFM + '.in00', f=1)
            cmds.connectAttr(nPOSI + '.ny', nFBFM + '.in01', f=1)
            cmds.connectAttr(nPOSI + '.nz', nFBFM + '.in02', f=1)
            cmds.connectAttr(nPOSI + '.tux', nFBFM + '.in10', f=1)
            cmds.connectAttr(nPOSI + '.tuy', nFBFM + '.in11', f=1)
            cmds.connectAttr(nPOSI + '.tuz', nFBFM + '.in12', f=1)
            cmds.connectAttr(nPOSI + '.tvx', nFBFM + '.in20', f=1)
            cmds.connectAttr(nPOSI + '.tvy', nFBFM + '.in21', f=1)
            cmds.connectAttr(nPOSI + '.tvz', nFBFM + '.in22', f=1)
            cmds.connectAttr(nPOSI + '.px', nFBFM + '.in30', f=1)
            cmds.connectAttr(nPOSI + '.py', nFBFM + '.in31', f=1)
            cmds.connectAttr(nPOSI + '.pz', nFBFM + '.in32', f=1)
            nDM = cmds.createNode('decomposeMatrix', n='rivetDM01')
            cmds.connectAttr(nFBFM + '.output', nDM + '.inputMatrix', f=1)
            cmds.connectAttr(nDM + '.outputTranslate', locgrpN + '.t', f=1)
            cmds.connectAttr(nDM + '.outputRotate', locgrpN + '.r', f=1)
        elif mode == 'Aim':
            nAimC = cmds.createNode('aimConstraint', p=locgrpN, n='%s_AimConstraint1' %locN)
            cmds.setAttr(nAimC + '.tg[0].tw', 1)
            cmds.setAttr(nAimC + '.a', 0, 1, 0, type='double3')
            cmds.setAttr(nAimC + '.u', 0, 0, 1, type='double3')
            cmds.connectAttr(nPOSI + '.n', nAimC + '.tg[0].tt', f=1)
            cmds.connectAttr(nPOSI + '.tv', nAimC + '.wu', f=1)
            cmds.connectAttr(nPOSI + '.p', locgrpN + '.t', f=1)
            cmds.connectAttr(nAimC + '.cr', locgrpN + '.r', f=1)

    def cLoc(self, mode, uV = .5, vV = .5):
        locName = 'rivet%s' % (len(cmds.ls('rivet*', typ='locator')) + 1)
        locN = cmds.spaceLocator(n=locName)[0]
        cmds.group(locN, n=locN + '_grp')
        if mode:
            cmds.addAttr(locN, ln='U', at='double', dv=0)
            cmds.addAttr(locN, ln='V', at='double', dv=0)
        else:
            cmds.addAttr(locN, ln='U', at='double', min=0, max=1, dv=0)
            cmds.addAttr(locN, ln='V', at='double', min=0, max=1, dv=0)
        cmds.setAttr(locN + '.U', e=1, keyable=1)
        cmds.setAttr(locN + '.U', uV)
        cmds.setAttr(locN + '.V', e=1, keyable=1)
        cmds.setAttr(locN + '.V', vV)
        #for i in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
        #    cmds.setAttr(locN + i, lock=1)
        return locN, locN + '_grp'
    

class CopyWeightTool():

    __Verision = 1.32

    def Ui(self):
        ToolUi = 'CopyWeightTool'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(300, 85))
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('sourceText', l='soure', bl='Select', adj=2, ed=0, cw3=[40, 200, 60],
                                bc=lambda *args: cmds.textFieldButtonGrp('sourceText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('sourceText', q=1, tx=1)), r=1))
        cmds.textFieldButtonGrp('targeText', l='targe', bl='Select', adj=2, ed=0, cw3=[40, 200, 60],
                                bc=lambda *args: cmds.textFieldButtonGrp('targeText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('targeText', q=1, tx=1)), r=1))
        cmds.button('Run', c=lambda *args: self.Runfun())
        cmds.showWindow(ToolUi)

    def Runfun(self):
        _temp1_ = cmds.textFieldButtonGrp('sourceText', q=1, tx=1)
        _temp2_ = cmds.textFieldButtonGrp('targeText', q=1, tx=1)
        if not _temp1_ or not _temp2_:
            return
        sourelist = cmds.ls(self.strProc(_temp1_), fl=1)
        targelist = cmds.ls(self.strProc(_temp2_), fl=1)
        soureObj = cmds.ls(sourelist, o=1)[0]
        targeObj = cmds.ls(targelist, o=1)
        if cmds.objectType(soureObj, i='mesh'):
            soureObj = cmds.listRelatives(soureObj, p=1)[0]
        if cmds.objectType(targeObj[0], i='mesh'):
            targeObj = cmds.listRelatives(targeObj[0], p=1)
        same = 1 if soureObj == targeObj[0] else 0

        soureSkCluster = mel.eval('findRelatedSkinCluster("%s")' % soureObj)
        if not soureSkCluster:
            cmds.error('Soure No Skin')
            return
        if not '.f[' in _temp1_:
            sourelist = cmds.ls(cmds.polyListComponentConversion(sourelist, fv=1, fe=1, fuv=1, fvf=1, tf=1), fl=1)
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)
        jntLock = [cmds.getAttr(j + '.liw') for j in infJointList]
        
        if same:
            _TempObj_ = cmds.duplicate(soureObj, rr=1)[0]
            allList = ['%s.f[%s]' % (soureObj, i) for i in range(cmds.polyEvaluate(_TempObj_, f=1))]
            _difflist_ = list(set(allList).difference(set(sourelist)))
            _list_ = [i.replace(soureObj, _TempObj_) for i in _difflist_]
            #_list_ = ['%s.f[%s]' % (_TempObj_, i) for i in range(cmds.polyEvaluate(_TempObj_, f=1)) if not '%s.f[%s]' % (soureObj, i) in set(sourelist)]
            if cmds.ls(_list_):
                cmds.delete(_list_)
            cmds.skinCluster(infJointList, _TempObj_, tsb=1, dr=4)
            cmds.copySkinWeights(soureObj, _TempObj_, nm=1, sa='closestPoint', ia='oneToOne', nr=1)
            soureObj = _TempObj_

        #_list_ = [_TempObj_]
        # finalCopyList = _list_ + targelist   塞进列表第一位
        for i in targeObj:
            if not mel.eval('findRelatedSkinCluster("%s")' % i):
                cmds.skinCluster(infJointList, i, tsb=1, mi=cmds.getAttr('%s.maxInfluences' % soureSkCluster), dr=4)
                targelist = i
            else:
                if not '.vtx[' in _temp2_:
                    targelist = cmds.ls(cmds.polyListComponentConversion(targelist, ff=1, fe=1, fuv=1, fvf=1, tv=1), fl=1)
            cmds.copySkinWeights(soureObj, targelist, nm=1, sa='closestPoint', ia=('oneToOne', 'closestJoint'), nr=1)
        if same:
            cmds.delete(_TempObj_)
        for j, l in zip(infJointList, jntLock):
            cmds.setAttr(j + '.liw', l)
        print('Finish!')

    def strProc(self, Onestr):
        return [i[2:-1] for i in Onestr[1:-1].split(', ')] if ', ' in Onestr else [Onestr[3:-2]]


ui_variable = {}


class cur2IK_FX_Ui(QtWidgets.QWidget):

    def __init__(self):
        self._cur2IK_FX_Verision = 2.51
        super(cur2IK_FX_Ui, self).__init__(shiboken2.wrapInstance(long(OmUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.UiName = 'cur2IK_FX'
        # self.setFocus()
        self.setupUi()

    def setupUi(self):
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        self.setObjectName(self.UiName)
        #self.resize(260, 500)
        #self.setMinimumSize(260, 500)
        self.setFixedSize(260, 500)
        self.MainverticalLayout = QtWidgets.QVBoxLayout(self)
        self.MainverticalLayout.setObjectName("MainverticalLayout")
        self.MainverticalLayout.setSpacing(3)
        self.MainverticalLayout.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.child1 = QtWidgets.QWidget()
        self.child1.setObjectName("child1")
        self.child1verLayout = QtWidgets.QVBoxLayout(self.child1)
        self.child1verLayout.setObjectName("child1verticalLayout")
        self.child1verLayout.setSpacing(5)
        self.child1verLayout.setContentsMargins(8, 5, 8, 3)

        self.horLayoutA = QtWidgets.QHBoxLayout()
        self.horLayoutA.setObjectName("horLayout")
        self.RebuildIntText = QtWidgets.QLabel(self.child1)
        self.RebuildIntText.setMinimumSize(QtCore.QSize(80, 26))
        self.RebuildIntText.setObjectName("RebuildIntText")
        ui_variable['RebuildInt'] = self.RebuildInt = QtWidgets.QLineEdit(self.child1)
        self.RebuildInt.setMinimumSize(QtCore.QSize(100, 22))
        self.RebuildInt.setObjectName("RebuildInt")
        self.horLayoutA.addWidget(self.RebuildIntText)
        self.horLayoutA.addWidget(self.RebuildInt)
        self.child1verLayout.addLayout(self.horLayoutA)

        self.horLayoutB = QtWidgets.QHBoxLayout()
        self.horLayoutB.setObjectName("horLayout")
        self.CurveNameText = QtWidgets.QLabel(self.child1)
        self.CurveNameText.setMinimumSize(QtCore.QSize(80, 26))
        self.CurveNameText.setObjectName("CurveNameText")
        ui_variable['CurveName'] = self.CurveName = QtWidgets.QLineEdit(self.child1)
        self.CurveName.setMinimumSize(QtCore.QSize(100, 22))
        self.CurveName.setObjectName("CurveName")
        self.horLayoutB.addWidget(self.CurveNameText)
        self.horLayoutB.addWidget(self.CurveName)
        self.child1verLayout.addLayout(self.horLayoutB)

        self.horLayoutC = QtWidgets.QHBoxLayout()
        self.horLayoutC.setObjectName("horLayout")
        self.SelectPolyCurve = QtWidgets.QPushButton(self.child1)
        self.SelectPolyCurve.setMinimumSize(QtCore.QSize(80, 26))
        self.SelectPolyCurve.setObjectName("SelectPolyCurve")
        self.reverseCurve = QtWidgets.QPushButton(self.child1)
        self.reverseCurve.setMinimumSize(QtCore.QSize(80, 26))
        self.reverseCurve.setObjectName("reverseCurve")
        self.horLayoutC.addWidget(self.SelectPolyCurve)
        self.horLayoutC.addWidget(self.reverseCurve)
        self.child1verLayout.addLayout(self.horLayoutC)

        self.lineA = QtWidgets.QFrame(self.child1)
        self.lineA.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineA.setMinimumSize(QtCore.QSize(100, 10))
        self.lineA.setObjectName("line")
        self.child1verLayout.addWidget(self.lineA)

        self.horLayoutD = QtWidgets.QHBoxLayout()
        self.horLayoutD.setObjectName("horLayout")
        self.horLayoutD.setSpacing(3)
        ui_variable['FromJointBG'] = self.FromJointBG = QtWidgets.QCheckBox(self.child1)
        self.FromJointBG.setObjectName("FromJointBG")
        self.FromJointBG.setMinimumSize(QtCore.QSize(100, 26))
        self.FromJointWar = QtWidgets.QLabel(self.child1)
        self.FromJointWar.setObjectName("FromJointWar")
        self.FromJointWar.setAlignment(QtCore.Qt.AlignCenter)
        self.FromJointWar.setStyleSheet("color:yellow")
        self.FromJointWar.setVisible(False)
        spacerItemA = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horLayoutD.addWidget(self.FromJointBG)
        self.horLayoutD.addWidget(self.FromJointWar)
        self.horLayoutD.addItem(spacerItemA)
        self.child1verLayout.addLayout(self.horLayoutD)

        self.horLayoutE = QtWidgets.QHBoxLayout()
        self.horLayoutE.setObjectName("horLayout")
        self.horLayoutE.setSpacing(3)
        ui_variable['SkinCtrlbox'] = self.SkinCtrlbox = QtWidgets.QCheckBox(self.child1)
        self.SkinCtrlbox.setObjectName("SkinCtrlbox")
        self.SkinCtrlbox.setMinimumSize(QtCore.QSize(130, 26))
        ui_variable['ctrlNumhorLineEdit'] = self.ctrlNumLineEdit = QtWidgets.QLineEdit(self.child1)
        self.ctrlNumLineEdit.setMinimumSize(QtCore.QSize(35, 22))
        self.ctrlNumLineEdit.setValidator(QtGui.QIntValidator())
        self.ctrlNumLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ctrlNumLineEdit.setText('5')
        self.ctrlNumLineEdit.setObjectName("ctrlNumLineEdit")
        spacerItemB = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horLayoutE.addWidget(self.SkinCtrlbox)
        self.horLayoutE.addWidget(self.ctrlNumLineEdit)
        self.horLayoutE.addItem(spacerItemB)
        self.child1verLayout.addLayout(self.horLayoutE)

        self.gridLayoutWidget = QtWidgets.QWidget(self.child1)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        ui_variable['IKFKCtrlbox'] = self.IKFKCtrlbox = QtWidgets.QCheckBox(self.child1)
        self.IKFKCtrlbox.setMinimumSize(QtCore.QSize(100, 26))
        self.IKFKCtrlbox.setObjectName("IKFKCtrlbox")
        # self.IKFKCtrlbox.setChecked(True)
        ui_variable['IKjointbox'] = self.IKjointbox = QtWidgets.QCheckBox(self.child1)
        self.IKjointbox.setMinimumSize(QtCore.QSize(80, 26))
        self.IKjointbox.setObjectName("IKjointbox")
        #self.selectboxGrp = QtWidgets.QButtonGroup(self.child1)
        # self.selectboxGrp.addButton(self.selectboxA,11)
        # self.selectboxGrp.addButton(self.selectboxB,12)

        ui_variable['FXCurvebox'] = self.FXCurvebox = QtWidgets.QCheckBox(self.child1)
        self.FXCurvebox.setMinimumSize(QtCore.QSize(80, 26))
        self.FXCurvebox.setObjectName("FXCurvebox")
        ui_variable['OnlyFXCurvebox'] = self.OnlyFXCurvebox = QtWidgets.QCheckBox(self.child1)
        self.OnlyFXCurvebox.setMinimumSize(QtCore.QSize(100, 26))
        self.OnlyFXCurvebox.setObjectName("FXCurvebox")

        self.JointIntText = QtWidgets.QLabel(self.child1)
        self.JointIntText.setMinimumSize(QtCore.QSize(100, 26))
        self.JointIntText.setObjectName("JointIntText")
        ui_variable['JointInt'] = self.JointInt = QtWidgets.QLineEdit(self.child1)
        self.JointInt.setMinimumSize(QtCore.QSize(100, 20))
        self.JointInt.setValidator(QtGui.QIntValidator())
        self.JointInt.setText('8')
        self.JointInt.setObjectName("JointInt")

        self.HairSystemText = QtWidgets.QLabel(self.child1)
        self.HairSystemText.setMinimumSize(QtCore.QSize(80, 26))
        self.HairSystemText.setObjectName("HairSystemText")
        ui_variable['SelectHairSystem'] = self.SelectHairSystem = QtWidgets.QComboBox(self.child1)
        self.SelectHairSystem.setObjectName("SelectHairSystem")
        self.SelectHairSystem.setMinimumSize(QtCore.QSize(100, 22))
        self.SelectHairSystem.installEventFilter(self)

        self.NucleusText = QtWidgets.QLabel(self.child1)
        self.NucleusText.setMinimumSize(QtCore.QSize(60, 26))
        self.NucleusText.setObjectName("NucleusText")
        ui_variable['SelectNucleus'] = self.SelectNucleus = QtWidgets.QComboBox(self.child1)
        self.SelectNucleus.setObjectName("SelectNucleus")
        self.SelectNucleus.setMinimumSize(QtCore.QSize(100, 22))
        self.SelectNucleus.installEventFilter(self)

        self.gridLayout.addWidget(self.IKFKCtrlbox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.IKjointbox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.FXCurvebox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.OnlyFXCurvebox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.JointIntText, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.JointInt, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.HairSystemText, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.SelectHairSystem, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.NucleusText, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.SelectNucleus, 4, 1, 1, 1)
        self.child1verLayout.addWidget(self.gridLayoutWidget)

        self.BuildCtrl = QtWidgets.QPushButton(self.child1)
        self.BuildCtrl.setObjectName("BuildCtrl")
        self.child1verLayout.addWidget(self.BuildCtrl)

        child1spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.child1verLayout.addItem(child1spacerItem0)

        self.PoseEdit = QtWidgets.QPushButton(self.child1)
        self.PoseEdit.setMaximumSize(QtCore.QSize(100, 26))
        self.PoseEdit.setObjectName("PoseEdit")
        self.child1verLayout.addWidget(self.PoseEdit)

        self.tabWidget.addTab(self.child1, "")

        self.child2 = QtWidgets.QWidget()
        self.child2.setObjectName("child2")
        self.child2verLayout = QtWidgets.QVBoxLayout(self.child2)
        self.child2verLayout.setObjectName("child2verticalLayout")
        self.child2verLayout.setSpacing(8)
        self.child2verLayout.setContentsMargins(8, 5, 8, 3)

        self.SelCtrlCurve = QtWidgets.QPushButton(self.child2)
        self.SelCtrlCurve.setMinimumSize(QtCore.QSize(100, 26))
        self.SelCtrlCurve.setObjectName("SelCtrlCurve")
        self.child2verLayout.addWidget(self.SelCtrlCurve)

        self.CShape = QtWidgets.QPushButton(self.child2)
        self.CShape.setMinimumSize(QtCore.QSize(100, 26))
        self.CShape.setObjectName("CShape")
        self.child2verLayout.addWidget(self.CShape)

        self.horizontalLayoutF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutF.setObjectName("horizontalLayout")
        self.horizontalLayoutF.setSpacing(3)
        self.RotX = QtWidgets.QPushButton(self.child2)
        self.RotX.setMinimumSize(QtCore.QSize(75, 26))
        self.RotX.setObjectName("RotX")
        self.RotY = QtWidgets.QPushButton(self.child2)
        self.RotY.setMinimumSize(QtCore.QSize(75, 26))
        self.RotY.setObjectName("RotY")
        self.RotZ = QtWidgets.QPushButton(self.child2)
        self.RotZ.setMinimumSize(QtCore.QSize(75, 26))
        self.RotZ.setObjectName("RotZ")
        self.horizontalLayoutF.addWidget(self.RotX)
        self.horizontalLayoutF.addWidget(self.RotY)
        self.horizontalLayoutF.addWidget(self.RotZ)
        self.child2verLayout.addLayout(self.horizontalLayoutF)

        self.horizontalLayoutG = QtWidgets.QHBoxLayout()
        self.horizontalLayoutG.setObjectName("horizontalLayout")
        self.horizontalLayoutG.setSpacing(3)
        self.ScaleAdd = QtWidgets.QPushButton(self.child2)
        self.ScaleAdd.setMinimumSize(QtCore.QSize(100, 26))
        self.ScaleAdd.setObjectName("ScaleAdd")
        self.ScaleSub = QtWidgets.QPushButton(self.child2)
        self.ScaleSub.setMinimumSize(QtCore.QSize(100, 26))
        self.ScaleSub.setObjectName("ScaleSub")
        self.horizontalLayoutG.addWidget(self.ScaleAdd)
        self.horizontalLayoutG.addWidget(self.ScaleSub)
        self.child2verLayout.addLayout(self.horizontalLayoutG)

        self.horizontalLayoutH = QtWidgets.QHBoxLayout()
        self.horizontalLayoutH.setObjectName("horizontalLayout")
        self.horizontalLayoutH.setSpacing(3)
        self.SColorview = QtWidgets.QPushButton(self.child2)
        self.SColorview.setMinimumSize(QtCore.QSize(80, 26))
        self.SColorview.setObjectName("SColorview")
        self.horizontalLayoutH.addWidget(self.SColorview)
        ui_variable['SColorInt'] = self.SColorInt = QtWidgets.QSlider(self.child2)
        self.SColorInt.setMinimum(1)
        self.SColorInt.setMaximum(31)
        self.SColorInt.setOrientation(QtCore.Qt.Horizontal)
        self.SColorInt.setObjectName("SColorInt")
        self.horizontalLayoutH.addWidget(self.SColorInt)
        self.child2verLayout.addLayout(self.horizontalLayoutH)

        child2spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.child2verLayout.addItem(child2spacerItem0)

        self.tabWidget.addTab(self.child2, "")
        self.MainverticalLayout.addWidget(self.tabWidget)

        ui_variable['Statusbar'] = self.Statusbar = QtWidgets.QStatusBar(self)
        self.Statusbar.setStyleSheet("color:yellow")
        self.Statusbar.setObjectName("Statusbar")
        self.MainverticalLayout.addWidget(self.Statusbar)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        Dynamic_ApplePie().Ready_GetNode('HairSystem')
        Dynamic_ApplePie().Ready_GetNode('Nucleus')

        self.RebuildIntText.setText(u"重建段数")
        self.RebuildInt.setPlaceholderText(u"重建段数")
        self.CurveNameText.setText(u"曲线名")
        self.CurveName.setPlaceholderText(u"曲线名")
        self.SelectPolyCurve.setText(u"选模型的线")
        self.SelectPolyCurve.clicked.connect(lambda *args: cur2IK_ApplePie().SelectPolyCurve())
        self.reverseCurve.setText(u"反转曲线")
        self.reverseCurve.clicked.connect(lambda *args: cur2IK_ApplePie().reverseCurve())
        self.FromJointBG.setText(u"从骨骼开始")
        self.FromJointBG.clicked.connect(lambda: self.setdisable())
        self.FromJointWar.setText(u"请顺序选择开始和结束骨骼\n且不能进行批量操作")
        self.SkinCtrlbox.setText(u"骨骼控制             数量： ")
        self.IKFKCtrlbox.setText(u"IKFK控制")
        self.IKjointbox.setText(u'建立IK骨骼')
        self.FXCurvebox.setText(u"添加动力学")
        self.OnlyFXCurvebox.setText(u"仅动力学曲线")
        self.OnlyFXCurvebox.clicked.connect(lambda: self.setdisable())
        self.JointIntText.setText(u"骨骼段数")
        self.HairSystemText.setText(u"HairSystem")
        self.NucleusText.setText(u"Nucleus")
        if int(cmds.about(v=1)) > 2016:
            self.SelectHairSystem.currentTextChanged.connect(lambda *args: Dynamic_ApplePie().Acondition())
            self.SelectNucleus.currentTextChanged.connect(lambda *args: Dynamic_ApplePie().Acondition())
        else:
            self.SelectHairSystem.currentIndexChanged.connect(lambda *args: Dynamic_ApplePie().Acondition())
            self.SelectNucleus.currentIndexChanged.connect(lambda *args: Dynamic_ApplePie().Acondition())
        self.BuildCtrl.setText(u"Build")
        self.BuildCtrl.clicked.connect(lambda *args: cur2IK_ApplePie().createCtrl())
        self.PoseEdit.setText(u"PoseEdit_ADV")
        self.PoseEdit.clicked.connect(lambda *args: cur2IK_ApplePie().PoseCheck())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child1), u"本体")

        self.SelCtrlCurve.setText(u'选择控制器')
        self.SelCtrlCurve.clicked.connect(lambda *args: cur2IK_ApplePie().SelCurve())
        self.CShape.setText(u"换个形状")
        self.CShape.clicked.connect(lambda *args: cur2IK_ApplePie().cShape())
        self.RotX.setText(u"RotX")
        self.RotX.clicked.connect(lambda *args: cur2IK_ApplePie().RSCurve('RX'))
        self.RotY.setText(u"RotY")
        self.RotY.clicked.connect(lambda *args: cur2IK_ApplePie().RSCurve('RY'))
        self.RotZ.setText(u"RotZ")
        self.RotZ.clicked.connect(lambda *args: cur2IK_ApplePie().RSCurve('RZ'))
        self.ScaleAdd.setText(u"放大曲线")
        self.ScaleAdd.clicked.connect(lambda *args: cur2IK_ApplePie().RSCurve('SA'))
        self.ScaleSub.setText(u"缩小曲线")
        self.ScaleSub.clicked.connect(lambda *args: cur2IK_ApplePie().RSCurve('SS'))
        self.SColorInt.valueChanged.connect(lambda*args: self.changeSColorInt())
        self.SColorview.setText(u"更改颜色")
        self.SColorview.clicked.connect(lambda *args: cur2IK_ApplePie().ChangeCurveColor())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child2), u"曲线DLC")

        #self.setParent(shiboken2.wrapInstance(long(OmUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   #置顶
        self.setWindowTitle('pTCIK by_Y')
        ui_variable['Statusbar'].showMessage('Ver %s' % self._cur2IK_FX_Verision)
        self.show()

    def eventFilter(self, object, event):  # 鼠标移动就会触发...淦
        if object == self.SelectHairSystem:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                Dynamic_ApplePie().Ready_GetNode('HairSystem')
            # if event.type() == QtCore.QEvent.MouseButtonDblClick:
            #    if event.button() == QtCore.Qt.RightButton:
            #        pass
            return super(cur2IK_FX_Ui, self).eventFilter(object, event)
        elif object == self.SelectNucleus:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                Dynamic_ApplePie().Ready_GetNode('Nucleus')
            return super(cur2IK_FX_Ui, self).eventFilter(object, event)

    def setdisable(self):
        if self.OnlyFXCurvebox.isChecked():
            self.SkinCtrlbox.setEnabled(False)
            self.ctrlNumLineEdit.setEnabled(False)
            self.IKFKCtrlbox.setEnabled(False)
            self.IKjointbox.setEnabled(False)
            self.FXCurvebox.setEnabled(False)
            self.JointInt.setEnabled(False)
            self.JointIntText.setEnabled(False)
        else:
            self.SkinCtrlbox.setEnabled(True)
            self.ctrlNumLineEdit.setEnabled(True)
            self.IKFKCtrlbox.setEnabled(True)
            self.IKjointbox.setEnabled(True)
            self.FXCurvebox.setEnabled(True)
            self.JointInt.setEnabled(True)
            self.JointIntText.setEnabled(True)
        if self.FromJointBG.isChecked():
            self.FromJointWar.setVisible(True)
            self.SkinCtrlbox.setEnabled(False)
            self.SkinCtrlbox.setChecked(True)
            self.JointInt.setEnabled(False)
        else:
            self.FromJointWar.setVisible(False)
            self.SkinCtrlbox.setEnabled(True)
            self.JointInt.setEnabled(True)

    def changeSColorInt(self):
        ColorInt = int(self.SColorInt.value())
        ColorIndex = [i*255 for i in cmds.colorIndex(ColorInt, q=1)]
        self.SColorview.setStyleSheet('background-color:rgb(%s,%s,%s)' % (ColorIndex[0], ColorIndex[1], ColorIndex[2]))
        #cmds.canvas('CCanvas', e=1, rgbValue=(ColorIndex[0], ColorIndex[1], ColorIndex[2]))


class cur2IK_ApplePie(object):

    curveShape = 0

    def __init__(self):
        ui_variable['Statusbar'].clearMessage()

    def SelectPolyCurve(self):
        Curvename = ui_variable['CurveName'].text()
        ReBNum = ui_variable['RebuildInt'].text()
        if not ReBNum:
            ui_variable['Statusbar'].showMessage(u'//没填重建段数')
            Om.MGlobal.displayError(u'//没填重建段数')
            return
        if not Curvename:
            ui_variable['Statusbar'].showMessage(u"//没填曲线名")
            Om.MGlobal.displayError(u"//没填曲线名")
            return
        polyEdgeN = cmds.ls(sl=1)
        # bothName = cmp(Curvename,cmds.ls())  #对比名称
        if cmds.ls(Curvename):
            ui_variable['Statusbar'].showMessage(u"//名称冲突")
            Om.MGlobal.displayError(u"//名称冲突")
            return
        cmds.undoInfo(ock=1)
        if cmds.confirmDialog(t='Confirm', m='尝试居中对齐?', b=['Yes', 'No'], db='Yes', cb='No', ds='No') == 'Yes':
            cmds.polyToCurve(ch=0, form=2, degree=3, n='__temp_cur')
            cmds.select(polyEdgeN, r=1)
            mel.eval('PolySelectConvert 3')
            selv = cmds.ls(sl=1, fl=1)
            for v in range(len(selv)):
                cmds.select(selv[v], r=1)
                mel.eval('PolySelectConvert 2')
                cmds.select(polyEdgeN, d=1)
                mel.eval('performSelContiguousEdges 0')
                cmds.cluster(n='__temp_clu')
            node_p = {}
            for c in range(len(cmds.ls('__temp_clu*Handle'))):
                temp_node = cmds.createNode('nearestPointOnCurve', n='__temp_node')
                cmds.connectAttr('__temp_cur.worldSpace[0]', temp_node + '.inputCurve')
                if not c:
                    cmds.connectAttr('__temp_cluHandleShape.origin', temp_node + '.inPosition')
                else:
                    cmds.connectAttr('__temp_clu%sHandleShape.origin' % c, temp_node + '.inPosition')
                node_p[c] = cmds.getAttr(temp_node + '.parameter')
            node_p_list = sorted(node_p.items(), key=lambda item: item[1])  # 字典排序
            tcws = [[0 for y in range(3)] for x in range(len(selv))]
            for v in range(len(selv)):
                c = '' if not node_p_list[v][0] else node_p_list[v][0]
                tcws[v][0] = cmds.getAttr('__temp_clu%sHandleShape.originX' % c)
                tcws[v][1] = cmds.getAttr('__temp_clu%sHandleShape.originY' % c)
                tcws[v][2] = cmds.getAttr('__temp_clu%sHandleShape.originZ' % c)
            cmds.curve(p=tcws, n=Curvename)
            reshape = cmds.listRelatives(Curvename, s=1)
            cmds.rename(reshape, Curvename + 'Shape')
            cmds.delete('__temp_*')
        else:
            cmds.select(polyEdgeN, r=1)
            pTCname = cmds.polyToCurve(ch=0, form=2, degree=3)
            cmds.rename(pTCname[0], Curvename)
        cmds.rebuildCurve(Curvename, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=int(ReBNum), d=3, tol=0.01)
        cvSize = cmds.getAttr(Curvename + ".controlPoints", size=1)
        cmds.delete(Curvename + '.cv[1]', Curvename + '.cv[%s]' % (cvSize-2))
        cmds.setAttr(Curvename + ".dispCV", 1)
        cmds.undoInfo(cck=1)

    def checkCurve(self):
        curlist = cmds.ls(sl=1)
        for i in curlist:
            if not cmds.listRelatives(i, s=1, type='nurbsCurve'):
                ui_variable['Statusbar'].showMessage(u'//有非曲线物体')
                Om.MGlobal.displayError(u'//有非曲线物体')
                return
        return curlist

    def reverseCurve(self):
        cmds.undoInfo(ock=1)
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            cmds.reverseCurve(i, ch=0, rpo=1)
        cmds.undoInfo(cck=1)

    def createCtrl(self):
        cmds.undoInfo(ock=1)
        if ui_variable['FromJointBG'].isChecked():
            slJoint = cmds.ls(sl=1, typ='joint')
            if len(slJoint) != 2:
                ui_variable['Statusbar'].showMessage(u'//从骨骼开始 - 需要选择两根骨骼')
                Om.MGlobal.displayError(u'//从骨骼开始 - 需要选择两根骨骼')
                return
            _jointpath = cmds.ls(slJoint[1], l=1)[0]
            '''
            #jntchild = cmds.listRelatives(slJoint[0], ad=1, c=1)   #向下遍历遇见分叉会出错
            #jntchild.reverse()
            #if i in set(jntchild):pass   #对列表判断时, 用set可以增加效率
            parentJnt = cmds.listRelatives(slJoint[1], ap=1, typ='joint')
            jointList = [slJoint[1],]
            while True:
                if not parentJnt or parentJnt[0] == slJoint[0]:
                    break
                jointList.append(parentJnt[0])
                parentJnt = cmds.listRelatives(parentJnt, ap=1, typ='joint')
            jointList.append(slJoint[0])
            if jointList[-1] != slJoint[0]:
            '''
            if not slJoint[0] in _jointpath:
                ui_variable['Statusbar'].showMessage(u'//所选骨骼不在同一层级中')
                Om.MGlobal.displayError(u'//所选骨骼不在同一层级中')
                return
            _List = _jointpath.split('|')[1:]
            _List = _List[_List.index(slJoint[0]):]
            self.JointList = _List
            ui_variable['JointInt'].setText(str(len(_List) - 1))
            _Pos = [cmds.xform(i, q=1, t=1, ws=1) for i in _List]
            cmds.rename(cmds.curve(d=3, ep=_Pos), slJoint[0] + '_chainCur')
            cmds.select('%s_chainCur' % slJoint[0], r=1)

        getlist = self.checkCurve()
        if not getlist:
            return
        if ui_variable['OnlyFXCurvebox'].isChecked():
            Dynamic_ApplePie().FXCurve(getlist)
            return
        if ui_variable['SkinCtrlbox'].isChecked():
            jointint = int(ui_variable['ctrlNumhorLineEdit'].text())
            self.jointCtrlNum = jointint
            for i in getlist:
                cmds.setAttr(i + ".dispCV", 0)
                if not cmds.ls(i + '.ctrlName'):
                    cmds.addAttr(i, ln='ctrlName', dt='string')
                _tempPos = cmds.createNode('pointOnCurveInfo')
                cmds.connectAttr(i + '.worldSpace[0]', _tempPos + '.inputCurve', f=1)
                cmds.setAttr(_tempPos + '.top', 1)
                _ctrlJointList = []
                for num in range(1, jointint + 1):
                    if num != 1:
                        cmds.setAttr(_tempPos + '.pr', 1.0 / float(jointint - 1) * (num - 1))
                    cmds.select(cl=1)
                    _pos = cmds.getAttr(_tempPos + '.p')[0]
                    jntN = cmds.joint(p=_pos, n='%s_control%s' % (i, num))
                    cmds.setAttr(jntN + '.v', 0)
                    _ctrlJointList.append(jntN)
                    createCur = cmds.circle(ch=0, n="%s_Ctrl" % jntN)[0]
                    ctrlgrp = cmds.group(cmds.group(n=createCur + "_SDK"), n=createCur + "_grp")
                    cmds.setAttr(ctrlgrp + '.t', _pos[0], _pos[1], _pos[2])
                    cmds.parent(jntN, createCur)
                    cmds.delete(cmds.tangentConstraint(i, ctrlgrp, w=1, aim=(0, 0, 1), u=(0, 1, 0), wut="scene"))
                cmds.skinCluster(_ctrlJointList, i, tsb=1, dr=4, mi=4)
                cmds.delete(_tempPos)
                cmds.setAttr(i + '.ctrlName', i + '_control*_Ctrl', type='string')
        else:
            for i in getlist:
                cmds.setAttr(i + ".dispCV", 0)
                cmds.DeleteHistory(i)
                if not cmds.ls(i + '.ctrlName'):
                    cmds.addAttr(i, ln='ctrlName', dt='string')
                curve = cmds.listRelatives(i, s=1, type="nurbsCurve")[0]
                numCVs = cmds.getAttr(i + ".controlPoints", size=1)
                for nu in range(numCVs):
                    createClu = cmds.cluster('%s.cv[%s]' % (curve, nu), n='%s_clu%s' % (i, nu + 1), rel=1)[1]
                    createCur = cmds.circle(ch=0, n="%s_control%s_Ctrl" % (i, nu + 1))[0]
                    ctrlgroup = cmds.group(cmds.group(n=createCur + "_SDK"), n=createCur + "_grp")
                    cmds.connectAttr(createClu + "Shape.origin", ctrlgroup + ".translate", f=1)
                    cmds.disconnectAttr(createClu + "Shape.origin", ctrlgroup + ".translate")
                    cmds.delete(cmds.tangentConstraint(i, ctrlgroup, w=1, aim=(0, 0, 1), u=(0, 1, 0), wut="scene"))
                    cmds.parentConstraint(createCur, createClu, mo=1)
                    cmds.select(cl=1)
                cmds.setAttr(i + '.ctrlName', i + '_control*_Ctrl', type='string')
        cmds.select(getlist, r=1)
        if ui_variable['IKFKCtrlbox'].isChecked():
            self.IKFKCtrl(ui_variable['SkinCtrlbox'].isChecked())
        if ui_variable['FXCurvebox'].isChecked():
            Dynamic_ApplePie().FXCurve(getlist)
        if ui_variable['IKjointbox'].isChecked():
            if ui_variable['FXCurvebox'].isChecked():
                for i in getlist:
                    self.CurveToIK(i + '_Blend')
            else:
                for i in getlist:
                    self.CurveToIK(i)
        cmds.undoInfo(cck=1)

    def IKFKCtrl(self, ctrlmode):
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            ctrlSize = self.jointCtrlNum if ctrlmode else cmds.getAttr(i + ".controlPoints", size=1)
            lastCtrl = "%s_control%s_Ctrl" % (i, ctrlSize)
            cmds.addAttr(lastCtrl, ln='IKFK', at='bool')
            cmds.setAttr(lastCtrl + ".IKFK", 1, e=1, k=1)
            for n in range(ctrlSize - 1):
                _tempcon = cmds.parentConstraint("%s_control%s_Ctrl" % (i, n + 1), "%s_control%s_Ctrl_grp" % (i, n + 2), mo=1)[0]
                cmds.connectAttr(lastCtrl + ".IKFK", '%s.%s' % (_tempcon, cmds.listAttr(_tempcon, st='*W0')[0]), f=1)

    def cShape(self):
        curSample = [
            [((-.5, .5, .5), (-.5, .5, -.5), (.5, .5, -.5), (.5, .5, .5), (-.5, .5, .5), (-.5, -.5, .5), (-.5, -.5, -.5), (-.5, .5, -.5), (-.5, .5, .5), (-.5, -.5, .5), (.5, -.5, .5), (.5, .5, .5), (.5, .5, -.5), (.5, -.5, -.5), (.5, -.5, .5), (.5, -.5, -.5), (-.5, -.5, -.5)), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)],
            [((0, 1, 0), (0, 0.92388, 0.382683), (0, 0.707107, 0.707107), (0, 0.382683, 0.92388), (0, 0, 1), (0, -0.382683, 0.92388), (0, -0.707107, 0.707107), (0, -0.92388, 0.382683), (0, -1, 0), (0, -0.92388, -0.382683), (0, -0.707107, -0.707107), (0, -0.382683, -0.92388), (0, 0, -1), (0, 0.382683, -0.92388), (0, 0.707107, -0.707107), (0, 0.92388, -0.382683), (0, 1, 0), (0.382683, 0.92388, 0), (0.707107, 0.707107, 0), (0.92388, 0.382683, 0), (1, 0, 0), (0.92388, -0.382683, 0), (0.707107, -0.707107, 0), (0.382683, -0.92388, 0), (0, -1, 0), (-0.382683, -0.92388, 0), (-0.707107, -0.707107, 0), (-0.92388, -0.382683, 0), (-1, 0, 0), (-0.92388, 0.382683, 0), (-0.707107, 0.707107, 0), (-0.382683, 0.92388, 0), (0, 1, 0), (0, 0.92388, -0.382683), (0, 0.707107, -0.707107), (0, 0.382683, -0.92388), (0, 0, -1), (-0.382683, 0, -0.92388), (-0.707107, 0, -0.707107), (-0.92388, 0, -0.382683), (-1, 0, 0), (-0.92388, 0, 0.382683), (-0.707107, 0, 0.707107), (-0.382683, 0, 0.92388), (0, 0, 1), (0.382683, 0, 0.92388), (0.707107, 0, 0.707107), (0.92388, 0, 0.382683), (1, 0, 0), (0.92388, 0, -0.382683), (0.707107, 0, -0.707107), (0.382683, 0, -0.92388), (0, 0, -1)), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52)],
            [((-1.6, -6.4, 0), (-1.6, -1.6, 0), (-6.4, -1.6, 0), (-6.4, 1.6, 0), (-1.6, 1.6, 0), (-1.6, 6.4, 0), (1.6, 6.4, 0), (1.6, 1.6, 0), (6.4, 1.6, 0), (6.4, -1.6, 0), (1.6, -1.6, 0), (1.6, -6.4, 0), (-1.6, -6.4, 0)), (0, 4.8, 9.6, 12.8, 17.6, 22.4, 25.6, 30.4, 35.2, 38.4, 43.2, 48, 51.2)],
        ]
        if cur2IK_ApplePie.curveShape == 4:
            cur2IK_ApplePie.curveShape = 0
        getlist = self.checkCurve()
        if not getlist:
            return
        cmds.undoInfo(ock=1)
        if cur2IK_ApplePie.curveShape == 3:
            cmds.circle(n='__temp_Shape')
        else:
            cmds.curve(d=1, p=curSample[cur2IK_ApplePie.curveShape][0], k=curSample[cur2IK_ApplePie.curveShape][1], n='__temp_Shape')
        for i in getlist:
            cmds.connectAttr('__temp_Shape.worldSpace[0]', cmds.listRelatives(i, s=1, type="nurbsCurve")[0] + '.create', f=1)
        cur2IK_ApplePie.curveShape += 1
        cmds.select(getlist, r=1)
        cmds.refresh()
        cmds.delete('__temp_Shape')
        # cmds.evalDeferred("cmds.delete('__temp_Shape')")  #延迟执行
        cmds.undoInfo(cck=1)

    def SelCurve(self):
        getlist = self.checkCurve()
        if not getlist:
            ui_variable['Statusbar'].showMessage(u'//未选择曲线或控制器')
            Om.MGlobal.displayError(u'//未选择曲线或控制器')
            return
        cmds.undoInfo(ock=1)
        cmds.select(cl=1)
        for i in getlist:
            if cmds.ls(i + '.ctrlName'):
                cmds.select(cmds.getAttr(i + '.ctrlName'), add=1)
            elif re.findall('_control\d*_Ctrl', i):
                cmds.select(i.rsplit('_', 2)[0] + '_control*_Ctrl', add=1)
            else:
                return
        cmds.undoInfo(cck=1)

    def RSCurve(self, mode):
        getlist = self.checkCurve()
        if not getlist:
            return
        cmds.undoInfo(ock=1)
        cmds.select(cl=True)
        for c in getlist:
            cmds.select(c + ".controlPoints[*]", add=1)
        if mode == 'RX':
            cmds.rotate(90, 0, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'RY':
            cmds.rotate(0, 90, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'RZ':
            cmds.rotate(0, 0, 90, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'SA':
            cmds.scale(1.2, 1.2, 1.2, r=1)
        elif mode == 'SS':
            cmds.scale(.8, .8, .8, r=1)
        cmds.select(getlist, r=1)
        cmds.undoInfo(cck=1)

    def ChangeCurveColor(self):
        ColorNum = int(ui_variable['SColorInt'].value())
        selCurve = cmds.ls(sl=1)
        cmds.undoInfo(ock=1)
        for n in range(len(selCurve)):
            CurShape = cmds.listRelatives(selCurve[n], c=1, s=1)
            cmds.setAttr(CurShape[0] + ".overrideEnabled", 1)
            cmds.setAttr(CurShape[0] + ".overrideColor", ColorNum)
        cmds.undoInfo(cck=1)

    def CurveToIK(self, curveN):   # 来自张老师
        JointNum = int(ui_variable['JointInt'].text())
        SavecurveN = curveN
        mz_dd = []
        mz_Loc = []
        if ui_variable['FromJointBG'].isChecked():
            _tempPr_ = cmds.createNode('nearestPointOnCurve', n='_tempGetparameter_')
            cmds.connectAttr(cmds.listRelatives(curveN, s=1)[0] + ".worldSpace[0]", _tempPr_ + ".inputCurve", f=1)
            _curveMax = cmds.getAttr(curveN + '.maxValue')
            _prfloat = []
            for i in self.JointList:
                _temppos = cmds.xform(i, q=1, ws=1, t=1)
                cmds.setAttr(_tempPr_ + '.ip', _temppos[0], _temppos[1], _temppos[2])
                _prfloat.append(cmds.getAttr(_tempPr_ + '.pr') / _curveMax)
            cmds.delete(_tempPr_)
        else:
            _prfloat = [1.0 * i / JointNum for i in range(JointNum + 1)]
        for i in range(JointNum + 1):
            #NodeA = cmds.createNode('motionPath', n='%s_MP%s' %(curveN, i))
            #cmds.setAttr(NodeA + ".fractionMode", 1)
            #cmds.setAttr(NodeA + ".follow", 1)
            #cmds.setAttr(NodeA + ".frontAxis", 0)
            #cmds.setAttr(NodeA + ".upAxis", 1)
            #cmds.setAttr(NodeA + ".worldUpType", Atype)
            NodeA = cmds.createNode('pointOnCurveInfo', n='%s_pOCI%s' % (curveN, i))
            cmds.setAttr(NodeA + ".top", 1)
            locB = cmds.spaceLocator(p=(0, 0, 0), n="%s_Loc%s" % (curveN, i))
            cmds.connectAttr(cmds.listRelatives(curveN, s=1)[0] + ".worldSpace[0]", NodeA + ".inputCurve", f=1)  # .geometryPath
            if cmds.objExists("%s.V%s" % (curveN, i)) == 0:
                cmds.addAttr(curveN, ln="V%s" % i, at='double', min=0, max=1, dv=0)
                #cmds.setAttr("%s.V%s" %(curveN, i), e=1, k=1)
            cmds.connectAttr("%s.V%s" % (curveN, i), NodeA + ".pr", f=1)  # .uValue
            cmds.setAttr("%s.V%s" % (curveN, i), _prfloat[i])
            cmds.connectAttr(NodeA + ".position", locB[0] + ".translate", f=1)
            # if Atype == 2:
            #    cmds.pathAnimation(NodeA, e=1, wuo=cmds.listRelatives(curveN, s=1)[0])
            mz_dd.append(NodeA)
            mz_Loc.append(locB[0])
        if '_Blend' in curveN:  # 修改名称
            curveN = curveN.rsplit('_', 1)[0]
        cmds.select(cl=1)
        locT = cmds.xform(mz_Loc[0], q=1, ws=1, t=1)
        jointN = cmds.joint(p=(locT[0], locT[1], locT[2]), n=curveN + "_IKJnt0")
        mz_jnt = [jointN, ]
        for i in range(1, len(mz_Loc)):
            locT = cmds.xform(mz_Loc[i], q=1, ws=1, t=1)
            jointN = cmds.joint(p=(locT[0], locT[1], locT[2]), n="%s_IKJnt%s" % (curveN, i))
            cmds.joint("%s_IKJnt%s" % (curveN, i - 1), e=1, zso=1, oj='xyz')
            mz_jnt.append(jointN)
        cmds.setAttr(mz_jnt[-1] + ".jo", 0, 0, 0)
        if not ui_variable['FromJointBG'].isChecked():
            _dupJnt = cmds.rename(cmds.duplicate(mz_jnt[0], rr=1), curveN + '_Jnt0')
            _childJnt = cmds.listRelatives(_dupJnt, f=1, c=1)
            for i in range(len(cmds.listRelatives(_dupJnt, ad=1, c=1))):
                _childJnt = cmds.listRelatives(cmds.rename(_childJnt, '%s_Jnt%s' % (curveN, i + 1)), f=1, c=1)
        cmds.select(cl=1)
        ctrlSize = self.jointCtrlNum if ui_variable['SkinCtrlbox'].isChecked() else cmds.getAttr(curveN + ".controlPoints", size=1)
        lastCtrl = "%s_control%s_Ctrl" % (curveN, ctrlSize)
        if cmds.objExists(lastCtrl + ".stretch") == 0:
            cmds.addAttr(lastCtrl, ln="stretch", at='double', min=0, max=1, dv=0)
            cmds.setAttr(lastCtrl + ".stretch", e=1, k=1)
        if cmds.objExists(curveN + ".scaleAttr") == 0:
            cmds.addAttr(curveN, ln="scaleAttr", at='double', dv=1)
            #cmds.setAttr(curveN + ".scaleAttr", e=1, k=1)
        for i in range(1, len(mz_dd)):
            mz_dB = cmds.createNode('distanceBetween', n=mz_dd[i] + "_dB")
            cmds.connectAttr(mz_dd[i-1] + ".position", mz_dd[i] + "_dB.point1", f=1)
            cmds.connectAttr(mz_dd[i] + ".position", mz_dd[i] + "_dB.point2", f=1)
            gh = cmds.getAttr(mz_dd[i] + "_dB.distance")
            cmds.createNode('multiplyDivide', n=mz_dd[i] + "_dB_MPA")
            cmds.connectAttr(mz_dd[i] + "_dB.distance", mz_dd[i] + "_dB_MPA.input1X", f=1)
            cmds.connectAttr(curveN + ".scaleAttr", mz_dd[i] + "_dB_MPA.input2X", f=1)
            cmds.setAttr(mz_dd[i] + "_dB_MPA.operation", 2)
            cmds.createNode('blendColors', n=mz_dd[i] + "_blendC")
            cmds.connectAttr(lastCtrl + ".stretch", mz_dd[i] + "_blendC.blender", f=1)
            cmds.connectAttr(mz_dd[i] + "_dB_MPA.outputX", mz_dd[i] + "_blendC.color1R", f=1)
            cmds.setAttr(mz_dd[i] + "_blendC.color2R", gh)
            cmds.connectAttr(mz_dd[i] + "_blendC.outputR", mz_jnt[i] + ".translateX", f=1)
        cmds.ikHandle(sol='ikSplineSolver', ccv=0, sj=mz_jnt[0], ee=mz_jnt[-1], c=SavecurveN, n=curveN + "_SplineIkHandle")
        if ui_variable['FromJointBG'].isChecked():
            for n, o in zip(self.JointList, mz_jnt):
                cmds.parentConstraint(o, n, mo=1)
        else:
            for i in range(len(cmds.listRelatives(curveN + '_IKJnt0', ad=1, c=1))):
                cmds.parentConstraint('%s_IKJnt%s' % (curveN, i), '%s_Jnt%s' % (curveN, i), mo=1)
        # cmds.select(SavecurveN)
        cmds.delete(mz_Loc)
        self.doFinish(curveN, SavecurveN)

    def doFinish(self, Name, fx):
        mainList = [Name, "%s_control*_Ctrl_grp" % Name, '%s_IKJnt0' % Name, '%s_SplineIkHandle' % Name]
        cluList = ['%s_clu*Handle' % Name]
        fxList = ['%s_Blend' % Name, '%s_toFX' % Name, '%s_OutFX' % Name, '%s_onlyCtrl' % Name]

        cmds.setAttr('%s.it' % Name, 0)
        cmds.setAttr('%s_IKJnt0.it' % Name, 0)
        if '_Blend' in fx:
            mainList = mainList + fxList
            for i in fxList:
                cmds.setAttr(i + '.it', 0)
            if not ui_variable['SkinCtrlbox'].isChecked():
                cmds.setAttr('%s_Blend.it' % Name, 1)
            cmds.hide(fxList)
        if not ui_variable['SkinCtrlbox'].isChecked():
            mainList = mainList + cluList
            cmds.setAttr('%s.it' % Name, 1)
            cmds.hide(cluList[0])
        cmds.group(mainList, n=Name + '_allGrp')
        cmds.hide('%s_SplineIkHandle' % Name, '%s_IKJnt0' % Name)
        if cmds.ls('buildPose') and cmds.ls('DeformationSystem', 'MotionSystem'):
            cmds.setAttr('buildPose.udAttr', '%s/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"%s_clu*Handle_Ctrl\";'
                         % (cmds.getAttr('buildPose.udAttr'), Name), type='string')

    # # # # # # # # # #
    def PoseCheck(self):
        if not cmds.ls('buildPose.udAttr'):
            ui_variable['Statusbar'].showMessage(u"//无Pose系统")
            Om.MGlobal.displayError(u"//无Pose系统")
            return
        buildposeText = cmds.getAttr('buildPose.udAttr')
        splitbuild = buildposeText.split('/*addItem*/')
        del splitbuild[0]
        splitText = [splitbuild[i].split('xform -os -t 0 0 0 -ro 0 0 0 ')[1] for i in range(len(splitbuild))]
        uiPose = 'PoseCheckList'
        if cmds.window(uiPose, q=1, ex=1):
            cmds.deleteUI(uiPose)
        cmds.window(uiPose, t='List')
        cmds.columnLayout(rs=5)
        cmds.textScrollList('PoseCheck_textList', nr=20, shi=4)
        cmds.button(l="Add", h=28, w=100, c=lambda*args: self.PoseEdit('add'))
        cmds.button(l="Delete", h=28, w=100, c=lambda*args: self.PoseEdit('delete'))
        cmds.showWindow(uiPose)
        for i in splitText:
            editi = (i.split('_clu*Handle_Ctrl\";')[0]).split('\"', 1)[1] if '_clu*Handle_Ctrl' in i else (i.split('\"', 1)[1]).rsplit('\"', 1)[0]
            if cmds.ls(editi, type='transform'):
                cmds.textScrollList('PoseCheck_textList', e=1, a=i)
            else:
                cmds.textScrollList('PoseCheck_textList', e=1, a=i + '  //NeedDelete//')

    def PoseEdit(self, mode):
        buildposeText = cmds.getAttr('buildPose.udAttr')
        if mode == 'delete':
            poseSplit = buildposeText.split('/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 %s;'
                                            % (cmds.textScrollList('PoseCheck_textList', q=1, si=1)[0].split(';')[0]))
            cmds.setAttr('buildPose.udAttr', poseSplit[0] + poseSplit[1], typ='string')
            cmds.textScrollList('PoseCheck_textList', e=1, rii=cmds.textScrollList('PoseCheck_textList', q=1, sii=1)[0])
        elif mode == 'add':
            if cmds.promptDialog(t='addPose', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
                inputText = cmds.promptDialog(q=1, t=1)
                lsinput = cmds.ls(inputText)
                if not lsinput:
                    cmds.error('无此物体')
                elif len(lsinput) >= 2:
                    cmds.error('有重复物体')
                cmds.setAttr('buildPose.udAttr', 
                                cmds.getAttr('buildPose.udAttr') + '/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"' + inputText + '\";', typ='string')
                cmds.textScrollList('PoseCheck_textList', e=1, a='\"' + inputText + '\";')
    # # # # # # # # # #


class Dynamic_ApplePie(object):

    def Acondition(self):
        if ui_variable['SelectHairSystem'].currentText() != 'Create New':
            ui_variable['SelectNucleus'].setEnabled(False)
        else:
            ui_variable['SelectNucleus'].setEnabled(True)

    def Ready_GetNode(self, mode):
        if mode == 'HairSystem':
            ui_variable['SelectHairSystem'].clear()
            hairsystemitem = cmds.listRelatives(cmds.ls(typ='hairSystem'), p=1)
            if hairsystemitem:
                for i in hairsystemitem:
                    ui_variable['SelectHairSystem'].addItem(i)
            ui_variable['SelectHairSystem'].addItem('Create New')
        if mode == 'Nucleus':
            ui_variable['SelectNucleus'].clear()
            nucleusitem = cmds.ls(typ='nucleus')
            if nucleusitem:
                for i in nucleusitem:
                    ui_variable['SelectNucleus'].addItem(i)
            ui_variable['SelectNucleus'].addItem('Create New')

    def ifdef(self, mode=''):
        qComboBox = []
        qComboBox.append(ui_variable['SelectNucleus'].currentText())
        qComboBox.append(ui_variable['SelectHairSystem'].currentText())
        if mode == 'NC':
            qComboBox[0] = cmds.createNode('nucleus')
            cmds.connectAttr('time1.outTime', qComboBox[0] + ".currentTime")
            if cmds.upAxis(q=1, axis=1) == "z":
                cmds.setAttr(qComboBox[0] + ".gravityDirection", 0, 0, -1)
        if mode == 'NC' or mode == 'HC':
            qComboBox[1] = cmds.createNode('hairSystem')
            cmds.setAttr(qComboBox[1] + ".hairsPerClump", 1)
            cmds.setAttr(qComboBox[1] + ".clumpWidth", 0)
            cmds.parent(cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0])
        if not cmds.connectionInfo(qComboBox[1] + ".nextState", sfd=1):
            mel.eval('addActiveToNSystem("%s", "%s")' % (cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0]))
            cmds.connectAttr('time1.outTime', qComboBox[1] + '.currentTime', f=1)
            cmds.connectAttr(qComboBox[0] + '.startFrame', qComboBox[1] + '.startFrame', f=1)
            qComboBox[1] = cmds.listRelatives(qComboBox[1], p=1)[0]
        if cmds.listAttr(qComboBox[1], st='ctrlMode'):
            reverseNode = cmds.listConnections(qComboBox[1], c=1, t='reverse')
            if not reverseNode:
                self.reNode = cmds.createNode("reverse")
                cmds.connectAttr(qComboBox[1] + ".ctrlMode", self.reNode + ".inputX")
            else:
                self.reNode = reverseNode[-1]
        else:
            cmds.addAttr(qComboBox[1], ln="ctrlMode", at="enum", en="onlyCtrl:FX:")
            cmds.setAttr(qComboBox[1] + ".ctrlMode", e=1, keyable=1)
            cmds.setAttr(qComboBox[1] + ".ctrlMode", 1)
            modeNode = cmds.createNode('animCurveUU', n='ModeDriveAni')
            cmds.connectAttr(qComboBox[1] + ".ctrlMode", modeNode + ".input", f=1)
            cmds.setKeyframe(modeNode, f=0, v=0)
            cmds.setKeyframe(modeNode, f=1, v=3)
            cmds.connectAttr(modeNode + ".output", qComboBox[1] + ".simulationMethod", f=1)
            self.reNode = cmds.createNode("reverse")
            cmds.connectAttr(qComboBox[1] + ".ctrlMode", self.reNode+".inputX")
        return qComboBox

    def FXCurve(self, curve):
        if not curve:
            ui_variable['Statusbar'].showMessage(u"//未选取曲线")
            Om.MGlobal.displayError(u"//未选取曲线")
            return
        cmds.undoInfo(ock=1)
        qComboBox = []
        if ui_variable['SelectNucleus'].currentText() != 'Create New' and not cmds.ls(typ='nucleus'):
            self.Ready_GetNode('Nucleus')
        if ui_variable['SelectNucleus'].currentText() == 'Create New':
            qComboBox = self.ifdef('NC')
        elif ui_variable['SelectHairSystem'].currentText() == 'Create New':
            qComboBox = self.ifdef('HC')
        else:
            qComboBox = self.ifdef()
        _tempctrlMode = cmds.getAttr(qComboBox[1] + ".ctrlMode")
        cmds.setAttr(qComboBox[1] + ".simulationMethod", 1)
        cmds.setAttr(qComboBox[0] + ".enable", 0)
        for i in range(len(curve)):
            _c = curve[i]
            hairfollicle = cmds.createNode('follicle')
            cmds.setAttr(hairfollicle + ".pointLock", 1)
            cmds.setAttr(hairfollicle + ".restPose", 1)
            cmds.setAttr(hairfollicle + ".startDirection", 1)
            cmds.setAttr(hairfollicle + ".degree", 3)
            _follicletransform = cmds.listRelatives(hairfollicle, p=1)[0]
            cmds.setAttr(_follicletransform + '.v', 0)
            cmds.parent(_follicletransform, qComboBox[1])
            hairNum = cmds.listConnections(qComboBox[1] + '.outputHair')
            if not hairNum:
                cmds.connectAttr(qComboBox[1] + '.outputHair[0]', hairfollicle + '.currentPosition', f=1)
                cmds.connectAttr(hairfollicle + '.outHair', qComboBox[1] + '.inputHair[0]', f=1)
            else:
                cmds.connectAttr('%s.outputHair[%s]' % (qComboBox[1], len(hairNum)), hairfollicle + '.currentPosition', f=1)
                cmds.connectAttr(hairfollicle + '.outHair', '%s.inputHair[%s]' % (qComboBox[1], len(hairNum)), f=1)
            cmds.rename(cmds.rebuildCurve(_c, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0,
                                          s=cmds.getAttr(_c + ".controlPoints", size=1) + 5, d=3, tol=0.01)[0], _c + '_toFX')
            cmds.duplicate(_c + '_toFX', rr=1, n=_c + '_onlyCtrl')
            cmds.duplicate(_c + '_toFX', rr=1, n=_c + '_Blend')
            cmds.connectAttr(cmds.listRelatives(_c + '_toFX', s=1)[0] + '.worldSpace[0]', cmds.listRelatives(_c + '_onlyCtrl', s=1)[0] + '.create', f=1)
            cmds.parent(_c + '_toFX', cmds.listRelatives(hairfollicle, p=1))
            cmds.connectAttr(cmds.listRelatives(_c + '_toFX', s=1, type='nurbsCurve')[0] + '.local', hairfollicle + '.startPosition', f=1)
            cmds.connectAttr(_c + '_toFX.worldMatrix[0]', hairfollicle+'.startPositionMatrix', f=1)
            cmds.connectAttr(hairfollicle + '.outCurve', cmds.duplicate(_c, rr=1, n=_c + '_OutFX')[0] + 'Shape.create', f=1)
            cmds.blendShape(_c + '_OutFX', _c + '_onlyCtrl', _c + '_Blend', n=_c + '_curveBS')
            cmds.connectAttr(qComboBox[1] + '.ctrlMode', '%s_curveBS.%s_OutFX' % (_c, _c))
            cmds.connectAttr(self.reNode + ".outputX", '%s_curveBS.%s_onlyCtrl' % (_c, _c))
        Dynamic_ApplePie().Ready_GetNode('HairSystem')
        Dynamic_ApplePie().Ready_GetNode('Nucleus')
        cmds.setAttr(qComboBox[1] + ".ctrlMode", _tempctrlMode)
        cmds.setAttr(qComboBox[0] + ".enable", 1)
        cmds.undoInfo(cck=1)


class DataSaveUi():

    __Verision = 1.21

    def Ui(self):
        self.UiN = 'DataSaveUi'
        UiN = self.UiN
        if cmds.window(UiN, q=1, ex=1):
            cmds.deleteUI(UiN)
        cmds.window(UiN, t=UiN, rtf=1, mb=1, mxb=0, wh=(250, 150))
        cmds.columnLayout('%s_MaincL' % UiN, cat=('both', 2), rs=2, cw=250, adj=1)
        cmds.rowLayout(nc=2, adj=1)
        cmds.text(l='', w=225)
        cmds.iconTextButton(i='addClip.png', w=20, h=20, c=lambda *args: self.addUiComponent())
        cmds.setParent('..')
        cmds.showWindow(UiN)
        self.addUiComponent()

    def addUiComponent(self):
        UiN = self.UiN
        #uiNum = 1 if mode == 'First' else int(cmds.columnLayout('%s_MaincL' %UiN, q=1, ca=1)[-1][-1]) + 1
        uiNum = len(cmds.columnLayout('%s_MaincL' % UiN, q=1, ca=1))
        cmds.columnLayout('%s_ComponentcL%s' % (UiN, uiNum), p='%s_MaincL' % UiN, cat=('both', 2), rs=2, cw=240, adj=1)
        cmds.rowLayout(nc=2)
        cmds.button(l='Save', w=120)
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'名称(用于再次选择)', c=lambda *args: self.saveData('Name', uiNum))
        cmds.menuItem(l=u'位移和旋转(用于选择物体对位)', c=lambda *args: self.saveData('Position', uiNum))
        cmds.menuItem(l=u'中心位置(用于选择物体对位)', c=lambda *args: self.saveData('CenterPosition', uiNum))
        cmds.button(l='Get', w=120, c=lambda *args: self.getData(uiNum))
        cmds.setParent('..')
        cmds.text('%s_ComponentText%s' % (UiN, uiNum), l='')
        cmds.popupMenu()
        cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.columnLayout('%s_ComponentcL%s' % (UiN, uiNum), e=1, vis=0))
        #cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.deleteUI('%s_ComponentcL%s' %(UiN, uiNum), lay=1))
        # 直接deleteUI时，导致数量和序号不匹配。再次添加时如果报错，Maya可能直接崩。
        cmds.text('%s_ComponentData%s' % (UiN, uiNum), l='', vis=0)

    def saveData(self, Type, uiNum):
        UiN = self.UiN
        if Type == 'Name':
            slList = cmds.ls(sl=1)
            if not slList:
                return
            cmds.text('%s_ComponentData%s' % (UiN, uiNum), e=1, l=str(slList))
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 名称')
        elif Type == 'Position':
            slList = cmds.ls(sl=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            _temploc_ = cmds.spaceLocator()
            cmds.delete(cmds.parentConstraint(slList[0], _temploc_, w=1))
            _data = '%s \n%s' % (cmds.xform(_temploc_, q=1, ws=1, t=1), cmds.xform(_temploc_, q=1, ws=1, ro=1))
            cmds.delete(_temploc_)
            cmds.text('%s_ComponentData%s' % (UiN, uiNum), e=1, l=_data)
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 位移和旋转')
        elif Type == 'CenterPosition':
            slList = cmds.ls(sl=1)
            if not slList:
                return
            _tempclu_ = cmds.cluster()[1]
            cmds.text('%s_ComponentData%s' % (UiN, uiNum), e=1, l=str(cmds.getAttr(_tempclu_ + 'Shape.origin')[0]))
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 中心位置')
            cmds.delete(_tempclu_)

    def getData(self, uiNum):
        UiN = self.UiN
        typString = cmds.text('%s_ComponentText%s' % (UiN, uiNum), q=1, l=1)
        data = cmds.text('%s_ComponentData%s' % (UiN, uiNum), q=1, l=1)
        lsList = cmds.ls(sl=1)
        if not data or not typString:
            return
        #print(data)
        if typString == u'已储存 名称':
            rlist = [i[2:-1] for i in data[1:-1].split(', ')] if ', ' in data else [data[3:-2]]
            cmds.select(rlist, add=1)
        elif typString == u'已储存 位移和旋转':
            if not lsList:
                return
            rlist = []
            for i in data.split(' \n'):
                _tempdata_ = i[1:-1].split(', ')
                rlist.append(_tempdata_)
            _temploc_ = cmds.spaceLocator()[0]
            cmds.xform(_temploc_, ws=1, t=rlist[0])
            cmds.xform(_temploc_, ws=1, ro=rlist[1])
            for i in lsList:
                cmds.delete(cmds.parentConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)
        elif typString == u'已储存 中心位置':
            if not lsList:
                return
            rlist = data[1:-1].split(', ')
            _temploc_ = cmds.spaceLocator()[0]
            cmds.setAttr(_temploc_ + '.t', float(rlist[0]), float(rlist[1]), float(rlist[2]))
            for i in lsList:
                cmds.delete(cmds.pointConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)


from maya.api import OpenMaya as om


class PSD_PoseUi_KitKat():

    __Verision = 0.82

    def ToolUi(self):
        ToolUi = 'PSD_Pose_KitKat'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='PSD_Pose', rtf=1, mb=1, mxb=0, wh=(250, 250))
        cmds.menu(l='Axis')
        cmds.radioMenuItemCollection()
        self.AxisItem = [
            cmds.menuItem(l='X', rb=1),
            cmds.menuItem(l='Y', rb=0),
            cmds.menuItem(l='Z', rb=0),
        ]
        cmds.menu(l='Setting')
        cmds.menuItem(l='MirrorName', c=lambda *args: cmds.columnLayout('MirrorName_Ly_KitKat', e=1, vis=1))
        cmds.menu(l='Help')
        cmds.menuItem(l='Help Doc', c=lambda *args: self.helpDoc())
        cmds.menu(l='     ', en=0)
        cmds.menu('loadobj_KitKat', l='| Load Object |')
        def _loadObj():
            lslist = cmds.ls(sl=1, o=1, typ='transform')
            if lslist:
                if cmds.listRelatives(lslist[0], s=1, typ='mesh'):
                    cmds.menu('loadobj_KitKat', e=1, l=lslist[0])
            else:
                cmds.menu('loadobj_KitKat', e=1, l='| Load Object |')
                if cmds.iconTextCheckBox('editPoseButton_KitKat', q=1, v=1):
                    cmds.iconTextButton('addPoseButton_KitKat', e=1, en=1)
                    cmds.iconTextButton('subPoseButton_KitKat', e=1, en=1)
                    cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
        cmds.menuItem(l='Load', c=lambda *args: _loadObj())
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=250)

        cmds.rowLayout(nc=3)
        _iconwh = 70
        cmds.iconTextButton('addPoseButton_KitKat', st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh, l='Add', c=lambda *args: self.AddCallBack())
        cmds.popupMenu()
        cmds.menuItem(l='Mirror', c=lambda *args: self.mirrorPose())
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
        cmds.iconTextButton('subPoseButton_KitKat', st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh, l='Delete',
                            c=lambda *args: self.DeleteProc())
        cmds.iconTextCheckBox('editPoseButton_KitKat', st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh, l='Edit',
                              cc=lambda *args: self.EditCallBack())
        cmds.setParent('..')

        cmds.rowLayout(nc=3)
        cmds.columnLayout(cat=('both', 0), rs=1, cw=_iconwh)
        cmds.iconTextButton(st="textOnly", l='Bake', h=26, c=lambda *args: self.BakePoseCallBack())
        cmds.iconTextButton(st="textOnly", l='Remake', h=26, c=lambda *args: self.RemakeBs())
        cmds.setParent('..')
        cmds.iconTextButton(st='iconAndTextVertical', i='kinMirrorJoint_S.png', l='Filp Target', w=_iconwh, h=52, c=lambda *args: self.FilpTarget())
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.FilpAxisItem = [
            cmds.menuItem(l='X', rb=1),
            cmds.menuItem(l='Y', rb=0),
            cmds.menuItem(l='Z', rb=0),
        ]
        cmds.iconTextButton(st='iconAndTextVertical', i='substGeometry.png', l='Bake Cloth', w=_iconwh, h=52, c='')
        cmds.setParent('..')
        cmds.text('editTarget_KitKat', vis=0)
        cmds.text('SaveMirrorL_KitKat', l='_L', vis=0)
        cmds.text('SaveMirrorR_KitKat', l='_R', vis=0)
        
        cmds.columnLayout('MirrorName_Ly_KitKat', cat=('both', 2), rs=2, cw=120, vis=0)
        _L = cmds.textFieldGrp(l='L', tx=cmds.text('SaveMirrorL_KitKat', q=1, l=1), cw2=(15, 95))
        _R = cmds.textFieldGrp(l='R', tx=cmds.text('SaveMirrorR_KitKat', q=1, l=1), cw2=(15, 95))
        _B = cmds.button(l='Save', c=lambda *args: _saveMirror(_L, _R))
        def _saveMirror(_L, _R):
            if cmds.window(ToolUi, q=1, ex=1):
                cmds.text('SaveMirrorL_KitKat', e=1, l=cmds.textFieldGrp(_L, q=1, tx=1))
                cmds.text('SaveMirrorR_KitKat', e=1, l=cmds.textFieldGrp(_R, q=1, tx=1))
            cmds.columnLayout('MirrorName_Ly_KitKat', e=1, vis=0)
        cmds.setParent('..')
        
        cmds.showWindow(ToolUi)

    def helpDoc(self):
        if cmds.window('HelpDoc_KitKat', q=1, ex=1):
            cmds.deleteUI('HelpDoc_KitKat')
        cmds.window('HelpDoc_KitKat', t='Help Doc', rtf=1, s=1, tlb=1, wh=(480, 500))
        _iconwh = 60
        cmds.columnLayout(cat=('both', 2), rs=2, cw=480)
        fn = 'fixedWidthFont'
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh, l='Add')
        cmds.popupMenu()
        cmds.menuItem(l='Mirror', c=lambda *args: self.mirrorPose())
        cmds.text(l=u'*初始化PSD(首次添加): 选择骨骼 + 控制器 \n*添加Pose: 选择骨骼/控制器 \n*右键菜单: Mirror功能, 可以镜像单个Pose或整个PSD节点', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh, l='Delete')
        cmds.text(l=u'选择一个PSD节点或多个Pose, 进行删除操作', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextCheckBox(st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh, l='Edit')
        cmds.text(l=u'选择单个Pose, 将跳转到选择的Pose \n*选择单个Pose, 调出当前修型开始编辑 \n按钮点亮时: 将当前的修型模型，塞回指定的BS', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st="textOnly", l='Bake', h=50, w=_iconwh)
        cmds.text(l=u'*选择一个PSD节点或多个Pose, 提取出修型目标体', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st="textOnly", l='Remake', h=50, w=_iconwh)
        cmds.text(l=u'*选择一个或多个修型目标体, 根据模型信息新增或修改指定Pose', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i='kinMirrorJoint_S.png', l='Filp Target', w=_iconwh, h=52)
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem(l='X', rb=1)
        cmds.menuItem(l='Y', rb=0)
        cmds.menuItem(l='Z', rb=0)
        cmds.text(l=u'*一般模型: 将选择的模型翻转, 得到一个对称的模型 \n*PSD模型: 将选择的修型目标体翻转, 得到一个对称的可通过Remake按钮\n \
                    添加Pose的修型目标体 \n右键菜单: 修改翻转对称轴', al='left', fn=fn)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i='substGeometry.png', l='Bake Cloth', w=_iconwh, h=52)
        cmds.text(l=u'*选择一个PSD节点或多个Pose, 将提取出指定Pose时的模型形状?', al='left', fn=fn)
        cmds.setParent('..')
        cmds.text(l=u'带 * 表示需要在 | Load Object | (加载模型)的前提下操作', h=50, fn='obliqueLabelFont')
        cmds.showWindow('HelpDoc_KitKat')

    def EditCallBack(self, stEd=0, fhEd=0):
        if stEd:
            cmds.iconTextButton('addPoseButton_KitKat', e=1, en=0)
            cmds.iconTextButton('subPoseButton_KitKat', e=1, en=0)
            cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=1)
            return
        if fhEd:
            cmds.iconTextButton('addPoseButton_KitKat', e=1, en=1)
            cmds.iconTextButton('subPoseButton_KitKat', e=1, en=1)
            cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
            return
        if not cmds.iconTextCheckBox('editPoseButton_KitKat', q=1, v=1):
            # 按钮为点亮状态
            self.EditCallBack(0, 1)
            self.transfer2Bs(cmds.text('editTarget_KitKat', q=1, l=1))
        else:
            if cmds.menu('loadobj_KitKat', q=1, l=1) == '| Load Object |':
                self.goToPose()
                cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
            else:
                if self.EditProc():   #调出bs, 开始编辑
                    self.EditCallBack(1)
                else:
                    self.EditCallBack(0, 1)

    def AddCallBack(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        _ConnectInfo = cmds.listConnections(sllist[0], d=0, t='joint')
        if cmds.nodeType(sllist[0]) == 'joint':
            _Joint = sllist[0]
        elif _ConnectInfo and cmds.ls('%s.ctrlJnt_Psd' % sllist[0]):
            #如果有链接信息 和 .ctrlJnt_Psd属性 说明选择的是个控制器
            _Joint = cmds.listConnections('%s.ctrlJnt_Psd' % sllist[0], d=0, t='joint')[0]
        elif cmds.ls('%s.isPose' % sllist[0]):
            _Joint = cmds.listConnections('%s.message' % cmds.listRelatives(sllist[0], p=1)[0], t='joint')[0]
            PoseName = sllist[0]
            self.goToPose(PoseName)
            _Ctrl = cmds.getAttr('%s.CtrlName' % sllist[0])
            _jntRotate = cmds.getAttr('%s.JointRotate' % sllist[0])[0]
            self.AddPoseProc(_Joint, [_Joint, PoseName, _Ctrl, _jntRotate, ''], 1)
            return
        else:
            return
        if not cmds.listConnections(_Joint, s=0, sh=1, t='poseInterpolator'):
            if len(sllist) < 2:
                om.MGlobal.displayError('No Select Controller')
                return
            self.AddPoseIProc(_Joint, sllist[1])
            return
        self.AddPoseProc(_Joint)
    
    def AddPoseIProc(self, _Joint, _Ctrl):
        _poseI = cmds.poseInterpolator(_Joint, n='%s_poseInterpolator' % _Joint)[0]
        _poseIShape = cmds.listRelatives(_poseI, s=1, typ="poseInterpolator")[0]
        cmds.connectAttr('%s.rotate' % _Ctrl, '%s.driver[0].driverController[0]' % _poseIShape, f=1)
        cmds.addAttr(_Joint, ln='Associated_Psd', at="message")
        cmds.connectAttr('%s.message' % _poseI, '%s.Associated_Psd' % _Joint, f=1)
        cmds.addAttr(_Ctrl, ln='ctrlJnt_Psd', at="message")
        cmds.connectAttr('%s.message' % _Joint, '%s.ctrlJnt_Psd' % _Ctrl, f=1)
        cmds.poseInterpolator(_poseIShape, e=1, ap="neutral")
        cmds.setAttr("%s.pose[%s].poseType" % (_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralSwing")), 1)
        cmds.setAttr("%s.pose[%s].poseType" % (_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralTwist")), 2)
        self.PoseAttr_add(cmds.group(n="%s_neutralPose" % _Joint, p=_poseI, em=1), 0, [_Joint, _Ctrl, 'neutralPose', (0,0,0)])
        for n in range(3):
            if cmds.menuItem(self.AxisItem[n], q=1, rb=1):
                break
        cmds.setAttr('%s.driver[0].driverTwistAxis' % _poseIShape, n)
        cmds.lockNode("%s_neutralPose" % _Joint, l=1)
        om.MGlobal.displayInfo('Create neutral Pose Finish!')
    
    def AddPoseProc(self, _Joint, Remake_Data=[], useAgain=''):
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
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
            _jntRotate = cmds.getAttr('%s.r' % _Joint)[0]
            for i in _jntRotate:
                i = round(i)
                if int('%d' %i) < 0:
                    _rotateData.append('n%d' % abs(i))
                else:
                    _rotateData.append('%d' %i)
            PoseName = '%s_%s_%s_%s' % (_Joint, _rotateData[0], _rotateData[1], _rotateData[2])
            if cmds.ls(PoseName):
                om.MGlobal.displayError('Pose already exists.')
                return
            for _Ctrl in cmds.listConnections('%s.message' % _Joint, t='transform'):
                if cmds.ls('%s.ctrlJnt_Psd' %_Ctrl):
                    break
            
            dupObj = cmds.duplicate(loadobj, n='%s_%s' % (loadobj, PoseName), rr=1)[0]
            _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
            cmds.setAttr('%s.overrideEnabled' % _dupObjShape, 1)
            cmds.setAttr('%s.overrideColor' % _dupObjShape, 20)
        
        _BsName = ''
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' % i):
                _BsName = i
                break
        if not _BsName:
            _BsName = cmds.blendShape(loadobj, n='Psd_BlendShape%s' % (len(cmds.ls('Psd_BlendShape*', typ='blendShape')) + 1))[0]
            cmds.blendShape(_BsName, e=1, automatic=1, g=loadobj)  # ?不明觉厉
            cmds.addAttr(_BsName, ln='Use2Psd', at='bool')
        
        if not useAgain:
            lsCposeI = cmds.listConnections('%s.Associated_Psd' % _Joint, d=0, t='transform')[0]
            _lsCposeIShape = cmds.listRelatives(lsCposeI, s=1)[0]
            self.PoseAttr_add(cmds.group(n=PoseName, p=lsCposeI, em=1), 0, [_Joint, _Ctrl, PoseName, _jntRotate])
            cmds.lockNode(PoseName, l=1)
            cmds.addAttr(lsCposeI, ln=PoseName, at='double', min=0, max=1, dv=0)
            poseAttr = '%s.%s' % (lsCposeI, PoseName)
            _poseId = cmds.poseInterpolator(_lsCposeIShape, e=1, ap=PoseName)
            cmds.setAttr('%s.pose[%s].poseType' % (_lsCposeIShape, _poseId), 1) #Type默认Swing
            cmds.connectAttr('%s.output[%s]' % (_lsCposeIShape, _poseId), poseAttr, f=1)
        else:
            poseAttr = '%s.%s' % (cmds.listConnections('%s.Associated_Psd' % _Joint, d=0, t='transform')[0], PoseName)
        
        _newBsId = cmds.getAttr('%s.w' % _BsName, mi=1)
        _newBsId = 0 if not _newBsId else _newBsId[-1] + 1
        cmds.blendShape(_BsName, e=1, tc=1, t=(loadobj, _newBsId, dupObj, 1), w=[_newBsId, 0]) #初始bs开关
        cmds.disconnectAttr('%s.worldMesh[0]' % dupObj, cmds.listConnections('%s.worldMesh[0]' % dupObj, p=1)[0])
        _newBsAttr = '%s.w[%s]' %(_BsName, _newBsId)
        cmds.aliasAttr(PoseName, _newBsAttr)
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=0, v=0)
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=1, v=1)

        cmds.setAttr(poseAttr, e=1, cb=1, l=1)
        if not Remake_Data or useAgain:
            self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
            cmds.select(dupObj, r=1)
            cmds.text('editTarget_KitKat', e=1, l=dupObj)
            cmds.setAttr('%s.v' % loadobj, 0)
            self.EditCallBack(1)
    
    def DeleteProc(self):
        sllist = cmds.ls(sl=1)
        if not sllist:
            return
        for a in sllist:
            if cmds.listRelatives(a, s=1, typ='poseInterpolator'):
                for b in cmds.listRelatives(a, c=1):
                    if cmds.ls('%s.isPose' % b):
                        self._deletePose(b)
                for j in cmds.listConnections('%s.message' % a, t='joint'):
                    if cmds.ls('%s.Associated_Psd' % j):
                        for c in cmds.listConnections('%s.message' % j):
                            if cmds.ls('%s.ctrlJnt_Psd' % c):
                                cmds.deleteAttr('%s.ctrlJnt_Psd' % c)
                                break
                        cmds.deleteAttr('%s.Associated_Psd' % j)
                        break
                cmds.delete(a)
            elif cmds.ls('%s.isPose' % a):
                self._deletePose(a)
                
    def _deletePose(self, name):
        cmds.lockNode(name, l=0)
        PoseName = cmds.getAttr('%s.PoseName' % name)
        if PoseName == 'neutralPose':
            cmds.delete(name)
            return
        a = cmds.listRelatives(name, p=1)[0]
        for c in cmds.listConnections('%s.%s' % (a, PoseName))[:-1]:
            if cmds.ls(c, typ='animCurveUU'):
                for d in cmds.listConnections('%s.output' % c):
                    if cmds.ls(d, typ='blendShape'):
                        for e in cmds.getAttr('%s.w' % d, mi=1):
                            if PoseName == cmds.aliasAttr('%s.w[%s]' % (d, e), q=1):
                                break
                        #_targetId = cmds.ls('%s.inputTarget[0].inputTargetGroup[*]' % d)[e].split('%s.inputTarget[0].inputTargetGroup[' % d)[1][:-1]
                        mel.eval('blendShapeDeleteTargetGroup %s %s' % (d, e))
        cmds.setAttr('%s.%s' % (a, PoseName), e=1, cb=1, l=0)
        cmds.deleteAttr(a, at=PoseName)
        cmds.poseInterpolator(cmds.listRelatives(a, s=1, typ='poseInterpolator')[0], e=1, dp=PoseName)
        cmds.delete(name)

    def EditProc(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return 0
        if cmds.ls('%s.isPose' % sllist[0]):
            self.goToPose(sllist[0])
            dupObj = self.extractPose(sllist[0])
            cmds.text('editTarget_KitKat', e=1, l=dupObj)
            cmds.select(dupObj, r=1)
            cmds.setAttr('%s.v' % loadobj, 0)
            return 1
        elif cmds.ls('%s.isEditMesh' % sllist[0]):
            cmds.text('editTarget_KitKat', e=1, l=sllist[0])
            return 1
        else:
            return 0
        
    def PoseAttr_add(self, transName, _type, _Data_):
        #if not cmds.ls('{}.PoseName'.format(transName)): 导致错误
        #    return
        cmds.addAttr(transName, ln='JointName', dt="string")
        cmds.setAttr('%s.JointName' % transName, _Data_[0], typ='string')
        cmds.addAttr(transName, ln='CtrlName', dt="string")
        cmds.setAttr('%s.CtrlName' % transName, _Data_[1], typ='string')
        cmds.addAttr(transName, ln='PoseName', dt="string")
        cmds.setAttr('%s.PoseName' % transName, _Data_[2], typ='string')
        cmds.addAttr(transName, ln="JointRotate", at='double3')
        cmds.addAttr(transName, ln="JointRotateX", at='double', dv=_Data_[3][0], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateY", at='double', dv=_Data_[3][1], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateZ", at='double', dv=_Data_[3][2], p="JointRotate")
        if not _type:
            cmds.addAttr(transName, ln='isPose', at="bool")
        elif _type == 1:
            cmds.addAttr(transName, ln='isEditMesh', at="bool")
            for i in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
                cmds.setAttr('%s%s' % (transName, i), l=0)
    
    def transfer2Bs(self, name):
        if not cmds.ls('%s.isEditMesh' % name):
            om.MGlobal.displayError('Object not exists.')
            return
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' % i):
                _BsName = i
        PoseName = cmds.getAttr('%s.PoseName' % name)
        _bsList = cmds.listAttr('%s.w[*]' % _BsName)
        for i in cmds.getAttr('%s.w' % _BsName, mi=1):
            if PoseName == cmds.aliasAttr('%s.w[%s]' % (_BsName, i), q=1):
                break
        self.goToPose(PoseName)
        cmds.blendShape(_BsName, e=1, t=(loadobj, i, name, 1.0), w=[i, 1])    #塞回去的时候有顺序问题
        cmds.aliasAttr(PoseName, '%s.w[%s]' %(_BsName, i))
        cmds.delete(name)
        cmds.setAttr('%s.v' % loadobj, 1)
    
    def goToPose(self, name=''):
        sllist = cmds.ls(sl=1)
        if sllist or name:
            if not name:
                name = sllist[0]
            _nAttr = '%s.CtrlName' % name
            _rAttr = '%s.JointRotate' % name
            if cmds.ls(_nAttr) and cmds.ls(_rAttr):
                _rotate = cmds.getAttr(_rAttr)[0]
                cmds.setAttr('%s.r' % cmds.getAttr(_nAttr), _rotate[0], _rotate[1], _rotate[2])
    
    def extractPose(self, name):
        #需要提前判断 loadobj 和 '%s.isPose'
        #rebuildSelectedTargetShape     cmds.sculptTarget(_BsName, e=1, r=1, t=0)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        _Joint = cmds.getAttr('%s.JointName' % name)
        _Ctrl = cmds.getAttr('%s.CtrlName' % name)
        _jntRotate = cmds.getAttr('%s.JointRotate' % name)[0]
        PoseName = cmds.getAttr('%s.PoseName' % name)
        dupObj = cmds.duplicate(loadobj, n='%s_%s' % (loadobj, PoseName), rr=1)[0]
        _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
        cmds.setAttr('%s.overrideEnabled' % _dupObjShape, 1)
        cmds.setAttr('%s.overrideColor' % _dupObjShape, 20)
        self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
        return dupObj
    
    def BakePoseCallBack(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        self.BakePose(sllist)
    
    def BakePose(self, data):
        _exPose = []
        if cmds.listRelatives(data, s=1, typ='poseInterpolator'):
            _childItem = cmds.listRelatives(data, c=1, typ='transform')
            for i in _childItem[1:]:
                if cmds.ls('%s.isPose' % i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
            self.goToPose(_childItem[0])
        else:
            for i in data:
                if cmds.ls('%s.isPose' % i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
                self.goToPose(cmds.listRelatives(cmds.listRelatives(i, p=1)[0], c=1, typ='transform')[0])
        cmds.select(_exPose, r=1)
        return _exPose

    def RemakeBs(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        for i in sllist:
            if not cmds.ls('%s.isEditMesh' % i):
                continue
            _Joint = cmds.getAttr('%s.JointName' % i)
            _Ctrl = cmds.getAttr('%s.CtrlName' % i)
            _jntRotate = cmds.getAttr('%s.JointRotate' % i)[0]
            PoseName = cmds.getAttr('%s.PoseName' % i)
            if not cmds.ls('%s.Associated_Psd' % _Joint):
                self.AddPoseIProc(_Joint, _Ctrl)
            elif cmds.ls(PoseName):
                self.goToPose(i)
                self.transfer2Bs(i)
                self.goToPose(cmds.listRelatives(cmds.listRelatives(i, p=1)[0], c=1, typ='transform')[0])
                continue
            cmds.setAttr('%s.r' % _Ctrl, _jntRotate[0], _jntRotate[1], _jntRotate[2])
            cmds.select(_Joint, r=1)
            self.AddPoseProc(_Joint, [_Joint, PoseName, _Ctrl, _jntRotate, i])
            self.goToPose(cmds.listRelatives(cmds.listRelatives(PoseName, p=1)[0], c=1, typ='transform')[0])
    
    def FilpTarget(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        _filpPose = []
        for i in sllist:
            sourceObj = cmds.duplicate(loadobj, n='_TempSourceMesh_')
            dupObj = cmds.duplicate(i, n='_TempFilpMesh_')
            bs = cmds.blendShape(dupObj[0], sourceObj[0], w=(0,1), tc=0)[0]
            cmds.refresh()
            for n in range(3):
                if cmds.menuItem(self.FilpAxisItem[n], q=1, rb=1):
                    break
            mel.eval('doBlendShapeFlipTarget %s 0 {"%s.0"}' % (n + 1, bs))
            
            if cmds.ls('%s.isEditMesh' % i):
                _Joint = cmds.getAttr('%s.JointName' % i)
                _Ctrl = cmds.getAttr('%s.CtrlName' % i)
                _jntRotate = cmds.getAttr('%s.JointRotate' % i)[0]
                PoseName = cmds.getAttr('%s.PoseName' % i)
                _old = cmds.text('SaveMirrorL_KitKat', q=1, l=1)
                _new = cmds.text('SaveMirrorR_KitKat', q=1, l=1)
                filpObj = cmds.duplicate(sourceObj[0], n=i.replace(_old, _new))[0]
                _filpObjShape = cmds.listRelatives(filpObj, s=1)[0]
                cmds.setAttr('%s.overrideEnabled' % _filpObjShape, 1)
                cmds.setAttr('%s.overrideColor' % _filpObjShape, 20)
                self.PoseAttr_add(filpObj, 1, [_Joint.replace(_old, _new), _Ctrl.replace(_old, _new), PoseName.replace(_old, _new), _jntRotate])
                _filpPose.append(filpObj)
            else:
                cmds.duplicate(sourceObj[0], n='%s_Filp' % i)
            cmds.delete(sourceObj, dupObj)
        cmds.select(_filpPose, r=1)
        return _filpPose

    def mirrorPose(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        exPose = self.BakePose(sllist)
        filpPose = self.FilpTarget()
        self.RemakeBs()
        cmds.delete(exPose, filpPose)


class setProjectTool():

    __Verision = 1.2  # 在maya文件夹中创建一个ProjectList文件

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
        cmds.popupMenu('rightC')
        cmds.menuItem(p='rightC', l='Add Project', c=lambda *args: self.refreshList('add'))
        cmds.menuItem(p='rightC', l='Delete Path', c=lambda *args: self.refreshList('delete'))
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


class WeightTool_JellyBean():

    __Verision = 0.85

    def ToolUi(self):
        ToolUi = 'WeightTool_JellyBean'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='WeightTool', rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.menu(l='SkinT', to=1)
        cmds.menuItem(d=1, dl="S/L")
        cmds.menuItem(l='Save', c=lambda *args: self.vtxSave_api())
        cmds.menuItem(l='Load', c=lambda *args: self.vtxLoad_api())
        cmds.menuItem(d=1)
        cmds.menuItem(l='WeightCheck', c=lambda *args: WeightCheckTool_JellyBean().ToolUi())
        cmds.menuItem(l='reset SkinPose', c=lambda *args: self.resetSkinPose())
        cmds.menu(l='RigT', to=1)
        cmds.menuItem(l='Create', c=lambda *args: self.createSelect())
        cmds.menuItem(l='Get', c=lambda *args: self.getSelect())
        cmds.columnLayout('FiristcL_JellyBean', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.text('spJobchangeVtx_JellyBean', p='FiristcL_JellyBean', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', 'WeightTool_JellyBean().refreshBoxChange(None)'], p='spJobchangeVtx_JellyBean')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh_JellyBean', i='refresh.png', w=20, h=20,
                              onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.popupMenu()
        cmds.menuItem('OFFmeunItem_JellyBean', l='OFF', cb=0)
        cmds.textField('searchText_JellyBean', h=22, tcc=lambda *args: self.refreshJointList(1, cmds.textField('searchText_JellyBean', q=1, tx=1)))
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem_JellyBean', l='Hierarchy', rb=1, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('AImeunItem_JellyBean', l='Alphabetically', rb=0, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('FImeunItem_JellyBean', l='Filter Zero', cb=0, c=lambda *args: self.refreshJointList(1))
        # cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_JellyBean', e=1, h=cmds.treeView('JointTV_JellyBean', q=1, h=1) + 20))
        # cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_JellyBean', e=1, h=cmds.treeView('JointTV_JellyBean', q=1, h=1) - 20))
        # invertSelection.png
        cmds.iconTextButton(i='invertSelection.png', w=20, h=20, c=self.reSelect)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout('JointTVLayout_JellyBean')
        cmds.treeView('JointTV_JellyBean', nb=1, h=100, scc=self._weightView, pc=(1, self.lock_unLock))
        cmds.text('saveData_JellyBean', l='', vis=0)
        cmds.popupMenu()
        #cmds.menuItem(l='Lock All')
        #cmds.menuItem(l='Unlock All')
        cmds.menuItem(l='Select Vtx', c=lambda *args: self.slVtx())
        cmds.formLayout('JointTVLayout_JellyBean', e=1, af=[('JointTV_JellyBean', 'top', 0), ('JointTV_JellyBean', 'bottom', 0),
                                                            ('JointTV_JellyBean', 'left', 3), ('JointTV_JellyBean', 'right', 3)])
        cmds.setParent('..')
        cmds.columnLayout(cat=('both', 2), rs=2, cw=225)
        cmds.rowLayout(nc=4, cw4=(50, 50, 50, 65))
        cmds.floatField('weighrfloat_JellyBean', w=52, h=26, pre=4, min=0, max=1,
                        ec=lambda *args: self.editVtxWeight(cmds.floatField('weighrfloat_JellyBean', q=1, v=1)))
        cmds.button(w=50, h=26, l='Copy', c=lambda *args: self.copyVtxWeight())
        cmds.button(w=50, h=26, l='Paste', c=lambda *args: self.pasteVtxWeight())
        cmds.popupMenu()
        cmds.menuItem(l='PasteAll', c=lambda *args: mel.eval("polyConvertToShell;artAttrSkinWeightPaste;"))
        cmds.button(w=65, h=26, l='Hammer', c=lambda *args: (mel.eval('weightHammerVerts'), self.refreshJointList(0)))
        cmds.setParent('..')
        cmds.rowLayout(nc=5, cw5=(43, 43, 43, 43, 43))
        cmds.button(w=43, h=26, l='Loop', c=lambda *args: cmds.polySelectSp(loop=1))
        cmds.button(w=43, h=26, l='Ring',
                    c=lambda *args: mel.eval("PolySelectConvert 2;PolySelectTraverse 2;polySelectEdges edgeRing;PolySelectConvert 3;"))
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
        cmds.floatField('ASFloat_JellyBean', v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c=lambda *args: self.editVtxWeight('+'))
        cmds.button(w=38, h=26, l='-', c=lambda *args: self.editVtxWeight('-'))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='M/D Weight', w=80)
        cmds.floatField('MDFloat_JellyBean', v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c=lambda *args: self.editVtxWeight('*'))
        cmds.button(w=38, h=26, l='/', c=lambda *args: self.editVtxWeight('/'))
        cmds.setParent('..')

        cmds.showWindow(ToolUi)

    def spJobStart(self):
        if cmds.text('spJobVtxParent_JellyBean', q=1, ex=1):
            return
        cmds.text('spJobVtxParent_JellyBean', p='FiristcL_JellyBean', vis=0)
        cmds.scriptJob(e=['Undo', 'WeightTool_JellyBean().refreshJointList(0)'], p='spJobVtxParent_JellyBean')
        cmds.scriptJob(e=['SelectionChanged', 'WeightTool_JellyBean().refreshJointList(0)'], p='spJobVtxParent_JellyBean')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent_JellyBean')
        cmds.scriptJob(uid=['WeightTool_JellyBean', 'WeightTool_JellyBean().refreshBoxChange(9)'])

        PaintSkinCmd = '"ArtPaintSkinWeightsToolOptions;"'
        if int(cmds.about(v=1)) > 2017:
            edgeCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"edge\\\", 0);")'
            vertexCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"vertex\\\", 0);")'
            faceCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"facet\\\", 0);")'
            objModeCmd = '"maintainActiveChangeSelectMode time1 0;"'  # python (\\\"WeightTool_JellyBean().refreshBoxChange(9)\\\");
        else:
            edgeCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"edge\\\");")'
            vertexCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"vertex\\\");")'
            faceCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"facet\\\");")'
            objModeCmd = '"changeSelectMode -component;changeSelectMode -object;"'
        mel.eval('global proc dagMenuProc(string $parent, string $object){ \
                if(!size($object)){ \
                string $lsList[] = `ls -sl -o`; if(!size($lsList)){return;} else{$object = $lsList[0];}} \
                if(objectType($object) == "joint"){ \
                string $selCmd = "python(\\\"cmds.treeView(\'JointTV_JellyBean\', e=1, cs=1);cmds.treeView(\'JointTV_JellyBean\', e=1, si=(\'" + $object + "\', 1));WeightTool_JellyBean()._weightView()\\\")"; \
                menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
                }else{ \
                menuItem -l "Paint Skin Weights Tool" -ec true -c %s -rp "NW" -p $parent; \
                menuItem -l "Vertex" -ec true -c %s -rp "W" -p $parent; \
                menuItem -l "Edge" -ec true -c %s -rp "N" -p $parent; \
                menuItem -l "Face" -ec true -c %s -rp "S" -p $parent; \
                menuItem -l "Object Mode" -ec true -c %s -rp "NE" -p $parent;}}'
                 % (PaintSkinCmd, vertexCmd, edgeCmd, faceCmd, objModeCmd))

    def refreshBoxChange(self, force):
        if force == 9 or cmds.menuItem('OFFmeunItem_JellyBean', q=1, cb=1):
            if cmds.text('spJobVtxParent_JellyBean', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent_JellyBean', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            if cmds.window('WeightTool_JellyBean', q=1, ex=1):
                cmds.iconTextCheckBox('refresh_JellyBean', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh_JellyBean', e=1, v=1)
            self.refreshJointList(0)

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
        siItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        _zero = cmds.menuItem('FImeunItem_JellyBean', q=1, cb=1)
        saveData = cmds.text('saveData_JellyBean', q=1, l=1).split('|')
        if refresh or _zero or saveData[0] != clusterName or saveData[1] != str(len(jointList)) or not cmds.treeView('JointTV_JellyBean', q=1, ch=''):
            cmds.treeView('JointTV_JellyBean', e=1, ra=1)
            if search:
                text = cmds.textField('searchText_JellyBean', q=1, tx=1)
                getList = [i for i in jointList if text in i]
                if getList:
                    jointList = getList
            jointList.sort()
            _jointList = []
            _valueList = []
            for i in jointList:
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=i)
                if _zero:
                    if float(Value):
                        _jointList.append(i)
                        _valueList.append(Value)
                else:
                    _jointList.append(i)
                    _valueList.append(Value)
            for j, v in zip(_jointList, _valueList):
                if cmds.menuItem('HImeunItem_JellyBean', q=1, rb=1):
                    self.addHItoList(j, _jointList)
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, ai=[j, ''])
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                if not cmds.treeView('JointTV_JellyBean', q=1, dls=1):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, ''))
                if float(v):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, '   |   %s' % v))
            if siItem:
                allItem = cmds.treeView('JointTV_JellyBean', q=1, ch='')
                _Temp_ = list(set(siItem).intersection(set(allItem)))  # 求并集
                for i in _Temp_:
                    cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))
        else:
            allItem = cmds.treeView('JointTV_JellyBean', q=1, ch='')
            for j in allItem:
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=j)
                if not cmds.treeView('JointTV_JellyBean', q=1, dls=1):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, ''))
                if not float(Value):
                    continue
                cmds.treeView('JointTV_JellyBean', e=1, dls=(j, '   |   %s' % Value))
        cmds.text('saveData_JellyBean', e=1, l='%s|%s' % (clusterName, len(jointList)))

    def addHItoList(self, i, jointList):
        jointP = cmds.listRelatives(i, p=1)
        if not jointP:
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, ''])
        elif cmds.treeView('JointTV_JellyBean', q=1, iex=jointP[0]):
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, jointP[0]])
        elif jointP[0] in jointList:
            self.addHItoList(jointP[0], jointList)
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, jointP[0]])
        else:
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, ''])

    def lock_unLock(self, jnt, but):
        slItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not slItem or len(slItem) == 1:
            slItem = [jnt]
        if cmds.getAttr(jnt + '.liw'):
            for i in slItem:
                cmds.setAttr(i + '.liw', 0)
                cmds.treeView('JointTV_JellyBean', e=1, i=(i, 1, 'Lock_OFF_grey.png'))
        else:
            for i in slItem:
                cmds.setAttr(i + '.liw', 1)
                cmds.treeView('JointTV_JellyBean', e=1, i=(i, 1, 'Lock_ON.png'))

    def reSelect(self):
        allItem = cmds.treeView('JointTV_JellyBean', q=1, iv=1)
        slItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not allItem or not slItem:
            return
        cmds.treeView('JointTV_JellyBean', e=1, cs=1)
        _Temp_ = list(set(allItem).difference(set(slItem)))  # 求差集 a有b没有
        for i in _Temp_:
            cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))

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
        sljntList = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not sljntList:
            om.MGlobal.displayError('Not Selected Joint')
            return
        if mode == '+' or mode == '-':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value + cmds.floatField('ASFloat_JellyBean', q=1, v=1)   \
                        if mode == '+' else Value - cmds.floatField('ASFloat_JellyBean', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        elif mode == '*' or mode == '/':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value * cmds.floatField('MDFloat_JellyBean', q=1, v=1)   \
                        if mode == '*' else Value / cmds.floatField('MDFloat_JellyBean', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        else:
            for v in selVtx:
                tvList = [(j, float(mode)) for j in sljntList]
                cmds.skinPercent(clusterName, v, tv=tvList)
        siItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        self.refreshJointList(0)
        for i in siItem:
            cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))

    def slVtx(self):
        slJnt = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        vtxList = []
        for i in slJnt:
            cmds.skinCluster(self.tempcluster, e=1, siv=i)
            vtxList.append(cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46]))
        cmds.select(vtxList, r=1)

    def _weightView(self):
        if cmds.iconTextCheckBox('refresh_JellyBean', q=1, v=1):
            if cmds.currentCtx() == 'artAttrSkinContext':
                mel.eval('setSmoothSkinInfluence "%s";' % cmds.treeView('JointTV_JellyBean', q=1, si=1)[0])
            self._weightfloat()

    def _weightfloat(self):
        treesl = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        sel = cmds.ls(sl=1, fl=1)
        if not treesl or not sel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        cmds.floatField('weighrfloat_JellyBean', e=1, v=float('%.4f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=treesl[0])))

    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError('Not Selected Vtx')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        mel.eval('artAttrSkinWeightCopy;')
        ValueList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000001, v=1)
        TransList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000001, t=None)
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
            om.MGlobal.displayError('Not Selected Vtx')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selObj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        if clusterName != self.vtxWeightInfo[0]:
            jointList = cmds.skinCluster(selObj, q=1, inf=1)
            for j in self.vtxWeightInfo[1]:
                if not j in jointList:
                    om.MGlobal.displayError('Joint are different !!!')
                    return
        tvList = [(self.vtxWeightInfo[1][i], self.vtxWeightInfo[2][i]) for i in range(len(self.vtxWeightInfo[1]))]
        # print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=1, tv=%s)' % (clusterName, i, tvList))
        self.refreshJointList(0)
    # # # # # # # # # #

    # # # # # Tool # # # # #
    def vtxSave_Mel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
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
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)  # vtxWeight (*.vtxWeight);;sdd (*.sdd)
        if not filePath:
            return
        with open(filePath[0], 'w') as vwfile:
            #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Save ...', max=len(selVtx))
            for i in selVtx:
                #cmds.progressBar(gMainProgressBar, e=1, s=1)
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                allWeight = 0
                for w in range(len(valueList)):
                    valueList[w] = round(valueList[w], 4)
                    allWeight += valueList[w]
                valueList[-1] += (1.0 - allWeight)
                tvList = [[transList[u], valueList[u]] for u in range(len(valueList))]
                wtStr = '%s--%s\r\n' % (i.split('.')[-1], tvList)
                vwfile.write(wtStr)
            #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_Mel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = []
        allLineapp = allLine.append
        with open(filePath[0], 'r') as vwfile:
            line = vwfile.readline()
            while line:
                allLineapp(line)
                line = vwfile.readline()

        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Load ...', max=len(allLine))
        for i in allLine:
            #cmds.progressBar(gMainProgressBar, e=1, s=1)
            strsplit = i.split('--')
            vtx = strsplit[0].strip()
            tvList = strsplit[-1].strip()
            exec('cmds.skinPercent("%s", "%s.%s", tv=%s)' % (clusterName, selobj, vtx, tvList))
        #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def vtxSave_Oapi(self):
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        #_prselList = []
        # selList.getSelectionStrings(_prselList)   #获取 MSelectionList 内容
        # print _prselList
        if selList.isEmpty():
            Om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容
        slMIt = Om.MItSelectionList(selList)
        MItDagPath = Om.MDagPath()
        MItcomponent = Om.MObject()
        slMIt.getDagPath(MItDagPath, MItcomponent)

        _selType = MDagPath.apiType()
        MDagPath.extendToShape()  # 获取当前物体的shape节点
        _selShapeType = MDagPath.apiType()
        if not _selType in set([110, 296, 267, 294, 279, ]):
            return
        elif _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294:
            suf = 'cv'
        elif _selShapeType == 279:
            suf = 'pt'

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
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

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)  # vtxWeight (*.vtxWeight);;sdd (*.sdd)
        if not filePath:
            return
        fileLine = []
        Lineapp = fileLine.append
        if not MItcomponent.isNull():  # component组件不为空(点), 线和面会强制转为点
            vertIter = Om.MItGeometry(MItDagPath, MItcomponent)
        else:
            vertIter = Om.MItGeometry(MObject)
        while not vertIter.isDone():
            infCount = Om.MScriptUtil()
            infCountPtr = infCount.asUintPtr()
            Om.MScriptUtil.setUint(infCountPtr, 0)
            weights = Om.MDoubleArray()
            skinNode.getWeights(MDagPath, vertIter.currentItem(), weights, infCountPtr)

            tvList = self.zeroWeightData_Save(weights, infNameList)
            wtStr = '%s[%s]--%s\r\n' % (suf, vertIter.index(), tvList)
            Lineapp(wtStr)
            vertIter.next()
        with open(filePath[0], 'w') as vwfile:
            for i in fileLine:
                vwfile.write(i)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_Oapi(self):
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        if selList.isEmpty():
            Om.MGlobal.displayError('Select Nothing')
            return
        elif selList.length() != 1:
            Om.MGlobal.displayError("Nothing selected")
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容

        _selType = MDagPath.apiType()
        if _selType != 110:
            Om.MGlobal.displayError('Please Select Object')
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
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

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            Om.MGlobal.displayWarning('Some Error. Please ReSelect')
            self.vtxLoad_Mel()
            return

        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        vertIter = Om.MItGeometry(MObject)
        _Num = 0
        while not vertIter.isDone():
            if vertIter.index() != int(allLine[_Num][0]):
                vertIter.next()
                continue
            jntindex = Om.MIntArray()
            weights = Om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i in range(len(allLine[_Num][1])):
                jntindexapp(infNameList.index(allLine[_Num][1][i]))
                weightsapp(allLine[_Num][2][i])
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, False)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def vtxSave_api(self):
        selList = om.MGlobal.getActiveSelectionList()
        if selList.isEmpty():
            om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表
        slMIt = om.MItSelectionList(selList)
        MItDagPath, MItcomponent = slMIt.getComponent()

        _selType = MDagPath.apiType()
        _selShapeType = MDagPath.extendToShape().apiType()
        if not _selType in set([110, 296, 267, 294, 279, ]):
            return
        elif _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294 or _selShapeType == 279:
            self.vtxSave_Oapi()
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)
        if not filePath:
            return
        fileLine = []
        Lineapp = fileLine.append
        if not MItcomponent.isNull():  # component组件不为空（点）,线和面会强制转为点
            vertIter = om.MItMeshVertex(MItDagPath, MItcomponent)
        else:
            vertIter = om.MItMeshVertex(MObject)
        while not vertIter.isDone():
            weights = skinNode.getWeights(MDagPath, vertIter.currentItem())[0]

            tvList = self.zeroWeightData_Save(weights, infNameList)
            wtStr = '%s[%s]--%s\r\n' % (suf, vertIter.index(), tvList)
            Lineapp(wtStr)
            vertIter.next()
        with open(filePath[0], 'w') as vwfile:
            for i in fileLine:
                vwfile.write(i)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_api(self):
        selList = om.MGlobal.getActiveSelectionList()
        if selList.isEmpty():
            om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表

        _selType = MDagPath.apiType()
        _selShapeType = MDagPath.extendToShape().apiType()
        if _selType != 110:
            om.MGlobal.displayError('Please Select Object')
            return
        if _selShapeType != 296:
            self.vtxLoad_Oapi()
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            om.MGlobal.displayWarning('Some Error. Please ReSelect')
            self.vtxLoad_Mel()
            return

        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        vertIter = om.MItMeshVertex(MObject)
        _Num = 0
        while not vertIter.isDone():
            if vertIter.index() != int(allLine[_Num][0]):
                vertIter.next()
                continue
            jntindex = om.MIntArray()
            weights = om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i in range(len(allLine[_Num][1])):
                jntindexapp(infNameList.index(allLine[_Num][1][i]))
                weightsapp(allLine[_Num][2][i])
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, False)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def zeroWeightData_Save(self, weights, infNameList, source=0):
        #去除0权重数据, source为1则输出源数据
        if source:
            return [[infNameList[it], weights[it]] for it in range(len(weights))]
        allWeight = 0
        transList = []
        valueList = []
        _jLappend = transList.append
        _wLappend = valueList.append
        for i in range(len(weights)):
            _tempweight = round(weights[i], 4)
            if _tempweight:
                _jLappend(infNameList[i])
                _wLappend(_tempweight)
            allWeight += _tempweight
        valueList[0] += (1.0 - allWeight)
        return [[transList[it], valueList[it]] for it in range(len(valueList))]

    def readWeightData_Load(self, path):
        allLine = []
        _allappend = allLine.append
        with open(path, 'r') as vwfile:
            line = vwfile.readline()
            while line:
                strsplit = line.split('--')
                if '][' in strsplit[0]:
                    return 'toMel'
                vtx = strsplit[0].split('[')[-1].split(']')[0]
                _data = strsplit[-1].strip()
                if '], [' in _data:
                    jointList = []
                    _jointListapp = jointList.append
                    weightList = []
                    _weightListapp = weightList.append
                    for i in _data[2:-2].split('], ['):
                        _str = i.split(', ')
                        _jointListapp(_str[0][2:-1])
                        _weightListapp(float(_str[1]))
                    _allappend([vtx, jointList, weightList])
                else:
                    _str = _data[2:-2].split(', ')
                    _allappend([vtx, [_str[0][2:-1]], [float(_str[1])]])
                # for item in eval(_data):
                #    jointList.append(item[0])
                #    weightList.append(item[1])
                #_allappend([vtx, jointList, weightList])
                line = vwfile.readline()
            _allappend([-1, None, None])
        return allLine

    def resetSkinPose(self):
        for obj in cmds.ls(sl=1):
            clusterName = mel.eval('findRelatedSkinCluster("%s")' % obj)
            if not clusterName:
                return
            sk_matrix = clusterName + '.matrix'
            mx_num = cmds.getAttr(sk_matrix, mi=1)
            infs = cmds.listConnections(sk_matrix, s=1, d=0, scn=1)
            if not infs:
                return
            for n in mx_num:
                inf = cmds.listConnections('%s[%d]' % (sk_matrix, n), s=1, d=0, scn=1)
                if not inf:
                    continue
                matrix = cmds.getAttr('%s.worldInverseMatrix[0]' % inf[0])
                cmds.setAttr('%s.pm[%d]' % (clusterName, n), matrix, typ='matrix')
                cmds.dagPose(inf[0], rs=1, n=cmds.listConnections('%s.bp' % clusterName, s=1, d=0, scn=1)[0])

    def createSelect(self):
        selvtx = cmds.ls(sl=1)
        selobj = cmds.ls(sl=1, o=1)[0]
        cluWs = cmds.getAttr(cmds.cluster(n='_tempClu_')[1] + 'Shape.origin')[0]
        Curname = cmds.circle(n='_selectCur_')[0]
        cmds.setAttr(Curname + '.translate', cmds.polyEvaluate(selobj, b=1)[0][1] + 1, cluWs[1], cluWs[2])
        cmds.addAttr(Curname, ln='vtxinfo', dt='string')
        cmds.setAttr(Curname + '.vtxinfo', '', type='string')
        for i in selvtx:
            cmds.setAttr(Curname + '.vtxinfo', '%s%s,' % (cmds.getAttr(Curname + '.vtxinfo'), i), type='string')
        cmds.delete('_tempClu_Handle')
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideEnabled', 1)
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideColor', 16)

    def getSelect(self):
        _tempVtx = []
        for c in cmds.ls(sl=1):
            if not cmds.ls('%s.vtxinfo' % c):
                return
            vtxList = cmds.getAttr('%s.vtxinfo' % c).split(',')[0:-1]
            for i in vtxList:
                _tempVtx.append(i)
        cmds.select(_tempVtx, r=1)
    # # # # # Tool # # # # #


class DisplayYes():  # 报绿

    def __init__(self):
        self.gCommandLine = mel.eval('$tmp = $gCommandLine')

    def showMessage(self, message):
        widget = shiboken2.wrapInstance(long(OmUI.MQtUtil.findControl(self.gCommandLine)), QtWidgets.QWidget)
        widget.findChild(QtWidgets.QLineEdit).setStyleSheet('background-color:rgb(10,200,15);' + 'color:black;')
        cmds.select('time1', r=1)
        WeightTool_JellyBean().refreshBoxChange(9)
        cmds.text('spJobReLine_DisplayYes', p='FiristcL_JellyBean', vis=0)   # p = Layout
        cmds.scriptJob(e=['SelectionChanged', 'DisplayYes().resetLine()'], p='spJobReLine_DisplayYes')
        Om.MGlobal.displayInfo(message)

    def resetLine(self):
        cmds.deleteUI('spJobReLine_DisplayYes', ctl=1)
        cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        mel.eval('source "initCommandLine.mel"')


class WeightCheckTool_JellyBean():

    def ToolUi(self):
        ToolUi = 'WeightCheckTool_JellyBean'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='WeightCheckTool', rtf=1, mb=1, wh=(500, 300))
        cmds.formLayout('MainformLayout_JellyBean')
        cmds.paneLayout('ListLayout_JellyBean', cn='vertical3', ps=(1, 1, 1))
        cmds.textScrollList('vtxList_JellyBean', ams=1, sc=lambda *args:
                            cmds.textScrollList('weightList_JellyBean', e=1, da=1, sii=cmds.textScrollList('vtxList_JellyBean', q=1, sii=1)))
        cmds.popupMenu()
        cmds.menuItem('SNmenuItem_JellyBean', l='View Object Name', cb=0, c=lambda *args: self.Load())
        cmds.textScrollList('weightList_JellyBean', ams=1, sc=lambda *args:
                            cmds.textScrollList('vtxList_JellyBean', e=1, da=1, sii=cmds.textScrollList('weightList_JellyBean', q=1, sii=1)))
        cmds.setParent('..')
        cmds.columnLayout('cLayout_JellyBean', cat=('right', 5), cw=100)
        cmds.text(l='', h=3)
        cmds.button(l='Load', w=80, h=26, c=lambda *args: self.Load())
        cmds.button(l='Clean', w=80, h=26, c=lambda *args: self.Clean())
        cmds.button(l='Remove Min', w=80, h=26, c=lambda *args: self.RemoveMin())
        cmds.popupMenu()
        cmds.menuItem(l='Remove as Value', c=lambda *args: self.RemoveValue())
        cmds.button(l='Select', w=80, h=26, c=lambda *args: self.selectVtx())
        cmds.text(l='Decimal', h=20)
        cmds.intField('DecimalInt_JellyBean', v=3)
        cmds.text(l='Influence', h=20)
        cmds.intField('InfluenceInt_JellyBean', v=3)
        cmds.text('ViewNum_JellyBean', vis=0, h=20)
        cmds.text('shapeInfo_JellyBean', vis=0)

        cmds.formLayout('MainformLayout_JellyBean', e=1, af=[('ListLayout_JellyBean', 'top', 0), ('ListLayout_JellyBean', 'bottom', 0),
                                                             ('ListLayout_JellyBean', 'left', 3), ('cLayout_JellyBean', 'right', 3)])
        cmds.formLayout('MainformLayout_JellyBean', e=1, ac=('ListLayout_JellyBean', 'right', 3, 'cLayout_JellyBean'))
        cmds.showWindow(ToolUi)

    def getSel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return None, None
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        selobj = cmds.ls(sl=1, o=1)[0]
        self.saveShape = selobj
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
            om.MGlobal.displayError('Select No Skin')
            return None, None
        return selVtx, clusterName

    def Load(self):
        cmds.text('ViewNum_JellyBean', e=1, vis=0)
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        cmds.textScrollList('vtxList_JellyBean', e=1, ra=1)
        cmds.textScrollList('weightList_JellyBean', e=1, ra=1)
        self.Number = []
        for i in selVtx:
            valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
            transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
            tvStr = ''
            if len(valueList) > cmds.intField('InfluenceInt_JellyBean', q=1, v=1):
                self.Number.append(i)
            for w, j in zip(valueList, transList):
                Value = str(w).rstrip('0').rstrip('.')
                tvStr += '%s ~ %s @ ' % (j, Value)
            if not cmds.menuItem('SNmenuItem_JellyBean', q=1, cb=1):
                i = i.split('.')[1]
            cmds.textScrollList('vtxList_JellyBean', e=1, a=i)
            cmds.textScrollList('weightList_JellyBean', e=1, a=tvStr)
        if self.Number:
            cmds.text('ViewNum_JellyBean', e=1, vis=1, l='Number: %s' % len(self.Number))
            if not cmds.menuItem('SNmenuItem_JellyBean', q=1, cb=1):
                _tempSl = [i.split('.')[1] for i in self.Number]
                cmds.textScrollList('vtxList_JellyBean', e=1, si=_tempSl)
            else:
                cmds.textScrollList('vtxList_JellyBean', e=1, si=self.Number)
            cmds.textScrollList('weightList_JellyBean', e=1, sii=cmds.textScrollList('vtxList_JellyBean', q=1, sii=1))
        cmds.text('shapeInfo_JellyBean', e=1, l=self.saveShape)

    def selectVtx(self):
        vtxList = cmds.textScrollList('vtxList_JellyBean', q=1, si=1)
        if not vtxList:
            cmds.select(cmds.polyListComponentConversion(self.saveShape, ff=1, fe=1, fuv=1, fvf=1, tv=1), r=1)
            cmds.hilite(self.saveShape)
            return
        if not '.' in vtxList[0]:
            _shapeN = cmds.text('shapeInfo_JellyBean', q=1, l=1)
            vtxList = ['%s.%s' % (_shapeN, i) for i in vtxList]
        else:
            _shapeN = cmds.ls(vtxList[0], o=1)
        cmds.hilite(_shapeN)
        cmds.select(vtxList, r=1)

    def Clean(self):
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        _decimal = '%.'+ str(cmds.intField('DecimalInt_JellyBean', q=1, v=1)) +'f'
        for i in selVtx:
            transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
            _tv = []
            for j in transList:
                # mel.eval('global proc float _rounding(float $f, int $n){float $N = pow(10, ($n));float $a = $f%(1/$N)*$N;float $B;     \
                #            if($a>0.5)$B = ceil($f*$N)/$N;else$B = floor($f*$N/$N);return $B;}')     #精度问题?
                #Value = mel.eval('_rounding(%s, %s)' %(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j), cmds.intField('DecimalInt', q=1, v=1)))
                Value = float(str(decimal.Decimal(str(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j))).
                                  quantize(decimal.Decimal(_decimal % 1))).rstrip('0').rstrip('.'))
                # if Value == 0:
                #    continue
                _tv.append([j, Value])
            num = 0
            for n in _tv:
                num += n[1]
            _tv[-1][1] = float(str(decimal.Decimal(str(_tv[-1][1] + 1 - num)).quantize(decimal.Decimal(_decimal % 1))).rstrip('0').rstrip('.'))
            cmds.skinPercent(clusterName, i, tv=_tv)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveMin(self):
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        Influence = cmds.intField('InfluenceInt_JellyBean', q=1, v=1)
        for v in selVtx:
            transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
            while len(transList) > Influence:
                valueList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, v=1)
                tvdic = {}
                for w, j in zip(valueList, transList):
                    tvdic[j] = w
                tvList = sorted(tvdic.items(), key=lambda item: item[1])
                cmds.skinPercent(clusterName, v, tv=(tvList[0][0], 0))
                transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
        for j, l in zip(transList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveValue(self):
        if cmds.promptDialog(t='RemoveValue', m='Value', tx='0.001', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
            reValue = float(cmds.promptDialog(q=1, tx=1))
            selVtx, clusterName = self.getSel()
            if not selVtx or not clusterName:
                return
            jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
            jntLock = []
            for j in jntList:
                jntLock.append(cmds.getAttr(j + '.liw'))
                cmds.setAttr(j + '.liw', 0)
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                reTvList = [(j, 0) for w, j in zip(valueList, transList) if w <= reValue]
                cmds.skinPercent(clusterName, i, tv=reTvList)
            for j, l in zip(jntList, jntLock):
                cmds.setAttr(j + '.liw', l)
            self.Load()


MaYaToolsBox().ToolUi()