import maya.cmds as cmds


def system():
    sel = cmds.ls(sl=1)
    loc = ''
    if cmds.nodeType(cmds.listRelatives(sel[0],s=1)[0]) == 'locator':
        loc = sel[0]
    else:
         cmds.error()
    cmds.setAttr(loc+".visibility",0)
    decMatA = cmds.createNode('decomposeMatrix')
    cmds.connectAttr (loc+'.worldMatrix[0]',decMatA+'.inputMatrix',f=1)

    cPOM = cmds.createNode('closestPointOnMesh',n='_cPOM')
    cmds.connectAttr (decMatA+'.outputTranslate',cPOM+'.inPosition',f=1)

    vecProx = cmds.createNode('vectorProduct',n='vecProA1')
    cmds.setAttr (vecProx+".operation",2)
    cmds.setAttr (vecProx+".normalizeOutput",1)
    vecProz = cmds.createNode('vectorProduct',n='vecProA2')
    cmds.setAttr (vecProz+".input1X",1)
    cmds.setAttr (vecProz+".operation",2)
    cmds.setAttr (vecProz+".normalizeOutput",1)
    cmds.connectAttr (cPOM+'.normal',vecProx+'.input1',f=1)
    cmds.connectAttr (cPOM+'.normal',vecProz+'.input2',f=1)
    cmds.connectAttr (vecProz+'.output',vecProx+'.input2',f=1)
    
    MatrixOnMesh = cmds.createNode('fourByFourMatrix')
    cmds.connectAttr (vecProx+'.outputX',MatrixOnMesh+'.in00',f=1)
    cmds.connectAttr (vecProx+'.outputY',MatrixOnMesh+'.in01',f=1)
    cmds.connectAttr (vecProx+'.outputZ',MatrixOnMesh+'.in02',f=1)
    cmds.connectAttr (cPOM+'.normalX',MatrixOnMesh+'.in10',f=1)
    cmds.connectAttr (cPOM+'.normalY',MatrixOnMesh+'.in11',f=1)
    cmds.connectAttr (cPOM+'.normalZ',MatrixOnMesh+'.in12',f=1)
    cmds.connectAttr (vecProz+'.outputX',MatrixOnMesh+'.in20',f=1)
    cmds.connectAttr (vecProz+'.outputY',MatrixOnMesh+'.in21',f=1)
    cmds.connectAttr (vecProz+'.outputZ',MatrixOnMesh+'.in22',f=1)
    cmds.connectAttr (cPOM+'.positionX',MatrixOnMesh+'.in30',f=1)
    cmds.connectAttr (cPOM+'.positionY',MatrixOnMesh+'.in31',f=1)
    cmds.connectAttr (cPOM+'.positionZ',MatrixOnMesh+'.in32',f=1)

    mMatrixA = cmds.createNode('multMatrix')
    cmds.connectAttr (MatrixOnMesh+'.output',mMatrixA+'.matrixIn[0]',f=1)
    cmds.connectAttr (loc+'.worldInverseMatrix[0]',mMatrixA+'.matrixIn[1]',f=1)

    decMatB = cmds.createNode('decomposeMatrix')
    cmds.connectAttr (mMatrixA+'.matrixSum',decMatB+'.inputMatrix',f=1)

    condition = cmds.createNode('condition')
    cmds.setAttr (condition+".operation",2)
    cmds.setAttr (condition+".colorIfTrueR",1)
    cmds.setAttr (condition+".colorIfFalseR",0)
    cmds.connectAttr (decMatB+'.outputTranslateY',condition+'.firstTerm',f=1)

    mMatrixB = cmds.createNode('multMatrix')
    cmds.connectAttr (mMatrixA+'.matrixSum',mMatrixB+'.matrixIn[0]',f=1)
    cmds.spaceLocator(n=loc+'_ctrl')
    locws = cmds.xform(loc,q=1,ws=1,t=1)
    cmds.setAttr(loc+'_ctrl.tx',locws[0])
    cmds.setAttr(loc+'_ctrl.ty',locws[1])
    cmds.setAttr(loc+'_ctrl.tz',locws[2])
    cmds.parent (loc,loc+'_ctrl')
    cmds.connectAttr (loc+'_ctrl.worldMatrix[0]',mMatrixB+'.matrixIn[1]',f=1)
    
    decMatC = cmds.createNode('decomposeMatrix')
    cmds.connectAttr (mMatrixB+'.matrixSum',decMatC+'.inputMatrix',f=1)

    decMatD = cmds.createNode('decomposeMatrix')
    cmds.connectAttr (loc+'_ctrl.worldMatrix[0]',decMatD+'.inputMatrix',f=1)

    pairBlend = cmds.createNode('pairBlend')
    cmds.connectAttr (condition+'.outColorR',pairBlend+'.weight',f=1)
    cmds.connectAttr (decMatC+'.outputRotate',pairBlend+'.inRotate2',f=1)
    cmds.connectAttr (decMatC+'.outputTranslate',pairBlend+'.inTranslate2',f=1)
    cmds.connectAttr (decMatD+'.outputRotate',pairBlend+'.inRotate1',f=1)
    cmds.connectAttr (decMatD+'.outputTranslate',pairBlend+'.inTranslate1',f=1)

    cmds.select(cl=1)
    joint = cmds.joint(n='locskin')
    cmds.connectAttr (pairBlend+'.outRotate',joint+'.rotate',f=1)
    cmds.connectAttr (pairBlend+'.outTranslate',joint+'.translate',f=1)
    '''
    cmds.addAttr (loc+'_ctrl',ln="offset",at='double',dv=0)
    cmds.setAttr (loc+'_ctrl.offset',e=1,keyable=1)
    cmds.connectAttr(loc+'_ctrl.offset',loc+'.ty')
    '''

def dimian():
    sel = cmds.ls(sl=1)
    if cmds.nodeType(cmds.listRelatives(sel[0],s=1)[0]) == 'mesh':
        mTran = sel[0]
    else:
        cmds.error()
    mesh = cmds.listRelatives(mTran,s=1)[0]
    AcPOM = cmds.ls('_cPOM*')
    for i in AcPOM:
        cmds.connectAttr (mesh+'.outMesh',i+'.inMesh',f=1)
        cmds.connectAttr (mTran+'.worldMatrix[0]',i+'.inputMatrix',f=1)

system()