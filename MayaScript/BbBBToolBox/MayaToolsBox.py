# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from .pyside import QtWidgets, shiboken

from maya import cmds, mel
from maya import OpenMayaUI as OmUI
#from maya.api import OpenMaya as om

import BbBBToolBox.CtrlTool # MZ_CtrllTool
import BbBBToolBox.cur2IK_FX # cur2IKFX_ToolUi
import BbBBToolBox.DataSaveUi # DataSaveUi
import BbBBToolBox.ModelTool # SymmetryTool_BbBB, BlendShapeTool_BbBB, ModelUtils_BbBB
import BbBBToolBox.ModifyJointTool # CreateModifyJoint
import BbBBToolBox.ngSk2Weight # ngSk2Weight_BbBB, ngSmooth_BbBB, ngUtils_BbBB
import BbBBToolBox.OtherTools # otherTools
import BbBBToolBox.PSDshape # PSD_PoseUi
import BbBBToolBox.SmoothPaint
import BbBBToolBox.WeightTool # PointWeightTool_BbBB, WeightCheckTool_BbBB, WeightSL_BbBB, softSelectWeightTool_BbBB, CopyWeightTool_BbBB, WeightUtils_BbBB
import BbBBToolBox.Utils # QtStyle, Functions


def MayaToolsBox_BbBB(reloadVar=False):
    if reloadVar:
        try:
            from importlib import reload
        except:
            pass
        reload(BbBBToolBox.CtrlTool)
        reload(BbBBToolBox.cur2IK_FX)
        reload(BbBBToolBox.DataSaveUi)
        reload(BbBBToolBox.ModelTool)
        reload(BbBBToolBox.ModifyJointTool)
        reload(BbBBToolBox.ngSk2Weight)
        reload(BbBBToolBox.OtherTools)
        reload(BbBBToolBox.PSDshape)
        reload(BbBBToolBox.WeightTool)
        reload(BbBBToolBox.Utils)

    ToolUi = 'MaYaToolsBox_BbBB'
    if cmds.window(ToolUi, q=1, ex=1):
        cmds.deleteUI(ToolUi)

    def getTheme():
        theme = BbBBToolBox.Utils.Functions.readSetting('Global', 'theme')
        _theme = [0 for i in range(3)]
        if theme == 'black':
            _theme[0] = 1
        elif theme == "pink":
            _theme[1] = 1
        elif theme == 'eyegreen':
            _theme[2] = 1
        return _theme
    _theme = getTheme()
    
    cmds.window(ToolUi, t=u'Maya工具箱', rtf=1, mb=1, mxb=0, bgc=BbBBToolBox.Utils.BoxQtStyle.backgroundMayaColor())
    form = cmds.formLayout()
    fn = 'fixedWidthFont'
    pageLayout = cmds.columnLayout(cat=('left', 10), cw=80, h=450, rs=60, bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    cmds.text(l=u'菜单', al='center', h=20, w=70, fn=fn)
    cmds.popupMenu(button=1)
    cmds.menuItem(l=u'安装PyMel', c=lambda *args: BbBBToolBox.Utils.Functions.installPyMel())
    cmds.menuItem(divider=True)
    cmds.menuItem(subMenu=1, label=u'主题')
    cmds.radioMenuItemCollection()
    cmds.menuItem(rb=_theme[0], label=u'默认黑', c=lambda *args: BbBBToolBox.Utils.Functions.editSetting("Global", "theme", "black"))
    cmds.menuItem(rb=_theme[1], label=u'猛男粉', c=lambda *args: BbBBToolBox.Utils.Functions.editSetting("Global", "theme", "pink"))
    cmds.menuItem(rb=_theme[2], label=u'护眼绿', c=lambda *args: BbBBToolBox.Utils.Functions.editSetting("Global", "theme", "eyegreen"))
    
    cmds.iconTextRadioCollection()
    cmds.iconTextRadioButton(st='iconAndTextVertical', i1='toolSettings.png', w=75, h=70, l=u'工具列表', sl=1, fn=fn, hlc=BbBBToolBox.Utils.BoxQtStyle.backgroundMayaColor(), 
                        onc=lambda *args: switchPage('Tool'))
    cmds.iconTextRadioButton(st='iconAndTextVertical', i1='paintTextureDeformer.png', w=75, h=70, l=u'权重工具', fn=fn, hlc=BbBBToolBox.Utils.BoxQtStyle.backgroundMayaColor(),
                        onc=lambda *args: switchPage('WeightTool'))
    cmds.iconTextRadioButton(st='iconAndTextVertical', i1='polyCube.png', w=75, h=70, l=u'模型工具', fn=fn, hlc=BbBBToolBox.Utils.BoxQtStyle.backgroundMayaColor(),
                        onc=lambda *args: switchPage('ModelTool'))
    cmds.setParent('..')

    #工具列表页
    commendToolLayout = cmds.scrollLayout(cr=1, h=380, w=230, bv=0, vis=1)
    cmds.columnLayout(cat=('both', 2), cw=220, rs=4, adj=1)
    cmds.text(l=u'————  命令工具  ————', fn=fn, h=52)
    _ToolButtonList = [cmds.button(l=u'Rivet', ann=u'', 
                                   c=lambda *args: BbBBToolBox.OtherTools.otherTools.cRivet("follicle")),
                        cmds.button(l=u'传递UV', ann=u'选择UV模型+要传递的模型', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.TransferUV()),
                        cmds.button(l=u'修型反算', ann=u'先选源模型，再选修好型的 \n源模型应该在当时提取修型的位置', 
                                    c=lambda *args: BbBBToolBox.ModelTool.ModelUtils_BbBB.invertShape_Bs()),
                        cmds.button(l=u'创建Locator', ann=u'在选择物体的位置创建Locator', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.createLocator()),
                        cmds.button(l=u'排列骨骼轴向', ann=u'选择首个骨骼\n鼠标中键反向排序', 
                                    dgc=lambda *args: BbBBToolBox.OtherTools.otherTools.sortJointAxis(args[1]), 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.sortJointAxis()),
                        cmds.button(l=u'移除未知插件', ann=u'加快文件打开速度', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.removeUnknownPlugin()),
                        cmds.button(l=u'重置窗口位置', ann=u'找不到窗口时运行', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.resetWindowLoc()),
                        cmds.button(l=u'从模型提取曲线', ann=u'批量提取曲线 - 仅适用于单片模型', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.polytoCurve()),
                        cmds.button(l=u'重置骨骼蒙皮位置', ann=u'当骨骼出现位置变化后，可以将当前位置设为蒙皮位置', 
                                    c=lambda *args: BbBBToolBox.WeightTool.WeightUtils_BbBB.resetSkinPose()),
                        cmds.button(l=u'打印BlendShape重连命令', ann=u'选择BS节点 便于替换或修改bs节点', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.connectBsCommand()),
                        cmds.button(l=u'修复位移过大时模型抖动Adv', ann=u'选择所有的蒙皮骨骼\n绑定位移过大时 蒙皮会发抖', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.AdvskinClusterLargeFix()),
                        cmds.button(l=u'选择的物体 被最后选的物体约束', ann=u''),
    ]
    cmds.popupMenu(button=1)
    cmds.menuItem(l=u'父子', c=lambda *args: BbBBToolBox.OtherTools.otherTools.constraintFromLast(0))
    cmds.menuItem(l=u'点', c=lambda *args: BbBBToolBox.OtherTools.otherTools.constraintFromLast(1))
    cmds.menuItem(l=u'旋转', c=lambda *args: BbBBToolBox.OtherTools.otherTools.constraintFromLast(2))
    cmds.menuItem(l=u'缩放', c=lambda *args: BbBBToolBox.OtherTools.otherTools.constraintFromLast(3))
    cmds.setParent('..')
    cmds.setParent('..')

    uiToolLayout = cmds.scrollLayout(cr=1, h=380, w=230, bv=0, vis=1)
    cmds.columnLayout(cat=('both', 2), cw=220, rs=4, adj=1)
    cmds.text(l=u'————  界面工具  ————', fn=fn, h=52)
    _ToolButtonList += [cmds.button(l=u'PSD修型', ann=u'基于Maya空间姿势的修型面板', 
                                    c=lambda *args: BbBBToolBox.PSDshape.PSD_PoseUi().ToolUi()),
                        #cmds.button(l=u'曲面毛囊', ann=u'在surface曲面上创建毛囊和骨骼', 
                        #           c=lambda *args: BbBBToolBox.OtherTools.otherTools.createFollicleToModel_ToolUi()),
                        cmds.button(l=u'控制器Pro', ann=u'权哥 控制器工具', 
                                    c=lambda *args: BbBBToolBox.CtrlTool.MZ_CtrllTool().ToolUi()),
                        cmds.button(l=u'数据临时储存', ann=u'临时储存 物体、位置、蒙皮骨骼、物体颜色', 
                                    c=lambda *args: BbBBToolBox.DataSaveUi.DataSaveUi().ToolUi()),
                        cmds.button(l=u'简易修型骨骼', ann=u'单轴骨骼旋转驱动的修型骨骼', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.simpleModifyJoint_ToolUi()),
                        cmds.button(l=u'创建辅助骨骼', ann=u'可以创建并驱动辅助修型骨骼', 
                                    c=lambda *args: BbBBToolBox.ModifyJointTool.CreateModifyJoint().ToolUi()), 
                        cmds.button(l=u'添加测试动画', ann=u'给控制器添加测试动画', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.TestAnimKey_ToolUi()),
                        cmds.button(l=u'动力学曲线IK', ann=u'动力学曲线IK', 
                                    c=lambda *args: BbBBToolBox.cur2IK_FX.cur2IKFX_ToolUi()),
                        cmds.button(l=u'IKFK无缝切换', ann=u'IKFK无缝切换', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.IkFkSeamlessSwitch_ToolUi()),
                        cmds.button(l=u'镜像驱动关键帧', ann=u'依次选择 做好的驱动者，做好的被驱动者\n没做的驱动者, 没做的被驱动者', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.MirrorDriverKey_ToolUi()),
                        cmds.button(l=u'解决Maya报错', ann=u'解决错误的清单', 
                                    c=lambda *args: BbBBToolBox.OtherTools.otherTools.FixError_ToolUi()), 
    ]
    cmds.setParent('..')
    cmds.setParent('..')
    #cmds.setParent('..')

    #权重工具页
    weightToolLayout = cmds.scrollLayout(cr=1, h=380, w=440, vis=0)
    cmds.columnLayout(cat=('both', 2), cw=450, adj=1, rs=3)
    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'拷权重工具', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.WeightTool.CopyWeightTool_BbBB().ToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'权重检查工具', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.WeightTool.WeightCheckTool_BbBB().ToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    if BbBBToolBox.ngSk2Weight.ngUtils_BbBB.pluginCheck():
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'ng2权重工具', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
        BbBBToolBox.ngSk2Weight.ngSk2Weight_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.separator(height=3, style='in')

    _ToolButtonList.append(cmds.button(l=u'Smooth笔刷', ann=u'Smooth笔刷', 
                                       c=lambda *args: BbBBToolBox.SmoothPaint.paint()))
    _ToolButtonList.append(cmds.button(l=u'点权重工具', ann=u'点权重调整', 
                                       c=lambda *args: BbBBToolBox.WeightTool.PointWeightTool_BbBB().ToolUi()))
    _ToolButtonList.append(cmds.button(l=u'软选择权重工具', ann=u'通过软选择创建\调整权重', 
                                       c=lambda *args: BbBBToolBox.WeightTool.softSelectWeightTool_BbBB().ToolUi()))
    _ToolButtonList.append(cmds.button(l=u'强度1                                              Ng-Relax权重                                              30强度', 
                                        ann=u'鼠标中键点击按钮 从左到右强度不同', 
                                        dgc=lambda *args: BbBBToolBox.ngSk2Weight.ngSmooth_BbBB().doIt(int(args[1]/14.5)+1), 
                                        c=lambda *args: BbBBToolBox.ngSk2Weight.ngSmooth_BbBB().doIt()))
    cmds.rowLayout(nc=2, cw2=(215, 215), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
    _ToolButtonList.append(cmds.button(l=u'存权重', c=lambda *args: BbBBToolBox.WeightTool.WeightSL_BbBB().SLcheck('Save')))
    _ToolButtonList.append(cmds.button(l=u'取权重', c=lambda *args: BbBBToolBox.WeightTool.WeightSL_BbBB().SLcheck('Load')))
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    
    #模型工具页
    modelToolLayout = cmds.scrollLayout(cr=1, h=380, w=440, vis=0)
    cmds.columnLayout(cat=('both', 2), cw=450, adj=1, rs=3)
    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'模型对称工具', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.ModelTool.SymmetryTool_BbBB().ToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'重设_重建Bs目标', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.ModelTool.BlendShapeTool_BbBB.reBsTargetUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'提取Bs模型', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.ModelTool.BlendShapeTool_BbBB.ExBsModelToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'连接Bs控制', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.ModelTool.BlendShapeTool_BbBB.connectBSToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'检查完全相同模型', bgc=BbBBToolBox.Utils.BoxQtStyle.accentMayaColor())
    BbBBToolBox.ModelTool.BlendShapeTool_BbBB.checkSameModelToolUi(1)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.separator(height=3, style='in')

    cmds.setParent('..')
    cmds.setParent('..')

    cmds.formLayout(form, e=1, af=((pageLayout, 'top', 0), (pageLayout, 'left', 0), (pageLayout, 'bottom', 0), 
                                   (commendToolLayout, 'top', 0), (commendToolLayout, 'bottom', 0), 
                                   (uiToolLayout, 'top', 0), (uiToolLayout, 'bottom', 0), (uiToolLayout, 'right', 0),
                                   (weightToolLayout, 'top', 0), (weightToolLayout, 'bottom', 0), (weightToolLayout, 'right', 0),
                                   (modelToolLayout, 'top', 0), (modelToolLayout, 'bottom', 0), (modelToolLayout, 'right', 0)), 
                                ac=((commendToolLayout, 'left', 5, pageLayout), (weightToolLayout, 'left', 5, pageLayout), (modelToolLayout, 'left', 5, pageLayout),), 
                                ap=((commendToolLayout, 'right', 0, 57), (uiToolLayout, 'left', 0, 57))
        )
    for i in _ToolButtonList:
        shiboken.wrapInstance(int(OmUI.MQtUtil.findControl(i)), QtWidgets.QPushButton).setStyleSheet(BbBBToolBox.Utils.BoxQtStyle.QButtonStyle())
        
    cmds.showWindow(ToolUi)

    def switchPage(strIn):
        if strIn == "Tool":
            cmds.scrollLayout(commendToolLayout, e=1, vis=1)
            cmds.scrollLayout(uiToolLayout, e=1, vis=1)
            cmds.scrollLayout(weightToolLayout, e=1, vis=0)
            cmds.scrollLayout(modelToolLayout, e=1, vis=0)
        elif strIn == "WeightTool":
            cmds.scrollLayout(commendToolLayout, e=1, vis=0)
            cmds.scrollLayout(uiToolLayout, e=1, vis=0)
            cmds.scrollLayout(weightToolLayout, e=1, vis=1)
            cmds.scrollLayout(modelToolLayout, e=1, vis=0)
        elif strIn == "ModelTool":
            cmds.scrollLayout(commendToolLayout, e=1, vis=0)
            cmds.scrollLayout(uiToolLayout, e=1, vis=0)
            cmds.scrollLayout(weightToolLayout, e=1, vis=0)
            cmds.scrollLayout(modelToolLayout, e=1, vis=1)


#MayaToolsBox_BbBB().ToolUi()
