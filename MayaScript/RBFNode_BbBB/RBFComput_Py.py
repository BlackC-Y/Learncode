# -*- coding: UTF-8 -*-
import math, sys
import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


class RBFCompute(om.MPxNode):

    NodeName = "RBFCompute_Py"
    NodeId = om.MTypeId(0x87000)
    #input
    twistAxis = None
    driveMatrix = None
    defaultMatrix = None
    pointVector = None
    #output
    outcomputeValue = None
    outNowVector = None
    _saveOldValue = [-1, []]
    _saveWeightMatrix = None

    @staticmethod
    def creator():
        return RBFCompute()

    @staticmethod
    def initializer():
        #cAttr = om.MFnCompoundAttribute()
        #gAttr = om.MFnGenericAttribute()
        #uAttr = om.MFnUnitAttribute()
        #typedAttr = om.MFnTypedAttribute()
        nAttr = om.MFnNumericAttribute()
        mAttr = om.MFnMatrixAttribute()
        eAttr = om.MFnEnumAttribute()

        #input
        RBFCompute.twistAxis = eAttr.create("twistAxis", "twistAxis", 0)
        eAttr.addField("X", 0)
        eAttr.addField("Y", 1)
        eAttr.addField("Z", 2)

        RBFCompute.driveMatrix = mAttr.create("driveMatrix", "driveMatrix", om.MFnMatrixAttribute.kDouble)

        RBFCompute.defaultMatrix = mAttr.create("defaultMatrix", "defaultMatrix", om.MFnMatrixAttribute.kDouble)
        mAttr.hidden = True
        mAttr.connectable = False

        RBFCompute.pointVector = nAttr.create("pointVector", "pointVector", om.MFnNumericData.k3Double)
        nAttr.array = True
        nAttr.disconnectBehavior = om.MFnAttribute.kDelete

        RBFCompute.addAttribute(RBFCompute.twistAxis)
        RBFCompute.addAttribute(RBFCompute.driveMatrix)
        RBFCompute.addAttribute(RBFCompute.defaultMatrix)
        RBFCompute.addAttribute(RBFCompute.pointVector)

        #output
        RBFCompute.outcomputeValue = nAttr.create("outcomputeValue", "outcomputeValue", om.MFnNumericData.kFloat, 0.0)
        nAttr.array = True
        nAttr.storable = False

        RBFCompute.outNowVector = nAttr.create("outNowVector", "outNowVector", om.MFnNumericData.k3Double, 0.0)
        nAttr.hidden = True
        nAttr.storable = False
        
        RBFCompute.addAttribute(RBFCompute.outcomputeValue)
        RBFCompute.addAttribute(RBFCompute.outNowVector)

        RBFCompute.attributeAffects(RBFCompute.twistAxis, RBFCompute.outcomputeValue)
        RBFCompute.attributeAffects(RBFCompute.driveMatrix, RBFCompute.outcomputeValue)
        RBFCompute.attributeAffects(RBFCompute.pointVector, RBFCompute.outcomputeValue)

        RBFCompute.attributeAffects(RBFCompute.twistAxis, RBFCompute.outNowVector)
        RBFCompute.attributeAffects(RBFCompute.driveMatrix, RBFCompute.outNowVector)
        RBFCompute.attributeAffects(RBFCompute.defaultMatrix, RBFCompute.outNowVector)
    
    def compute(self, plug, data):
        
        input_twistAxis = data.inputValue(self.twistAxis)
        input_driveMatrix = data.inputValue(self.driveMatrix)
        input_defaultMatrix = data.inputValue(self.defaultMatrix)

        twistAxis = input_twistAxis.asShort()
        driveMatrix = input_driveMatrix.asMatrix()
        defaultMatrix = input_defaultMatrix.asMatrix()
        driveVector =  self.getNowVector(twistAxis, driveMatrix, defaultMatrix)

        outNowVectorHandle = data.outputValue(self.outNowVector)
        outNowVectorHandle.set3Double(driveVector[0], driveVector[1], driveVector[2])
            
        if (plug == self.outcomputeValue):
            input_pointVector = data.inputArrayValue(self.pointVector)

            count = len(input_pointVector)
            disMatrix = [[0] * count for _ in range(count)]
            valueMatrix = [[0] * count for _ in range(count)]
            driveDis = []

            recompute = False
            if twistAxis != self._saveOldValue[0]:
                self._saveOldValue[0] = twistAxis
                recompute = True
            if count != len(self._saveOldValue[1]):
                recompute = True
            else:
                for i1 in range(count): 
                    input_pointVector.jumpToPhysicalElement(i1)
                    if input_pointVector.inputValue().asDouble3() != self._saveOldValue[1][i1]:
                        recompute = True
                        break
            
            if recompute:
                self._saveOldValue[1] = []
                for i1 in range(count): 
                    input_pointVector.jumpToPhysicalElement(i1)
                    Vector1 = input_pointVector.inputValue().asDouble3()
                    self._saveOldValue[1].append(Vector1)
                    driveDis.append(self.dis(driveVector, Vector1))
                    for i2 in range(count):
                        input_pointVector.jumpToPhysicalElement(i2)
                        Vector2 = input_pointVector.inputValue().asDouble3()
                        disMatrix[i1][i2] = self.dis(Vector1, Vector2)
                        if i1 == i2:
                            valueMatrix[i1][i2] = 1
                inverseMatrix = self.inverse_matrix(disMatrix)
                if inverseMatrix == None:
                    return
                weightMatrix = self.multiply(inverseMatrix, valueMatrix)
                self._saveWeightMatrix = weightMatrix
            else:
                for i1 in range(count): 
                    input_pointVector.jumpToPhysicalElement(i1)
                    Vector1 = input_pointVector.inputValue().asDouble3()
                    driveDis.append(self.dis(driveVector, Vector1))
                weightMatrix = self._saveWeightMatrix


            outValue = [0] * count
            for i1 in range(count):
                for i2 in range(count):
                    outValue[i1] += weightMatrix[i2][i1] * driveDis[i2]
            outcomputeValueHandle = data.outputArrayValue(self.outcomputeValue)
            outputCount = len(outcomputeValueHandle) if count > len(outcomputeValueHandle) else count
            for i in range(outputCount):
                outcomputeValueHandle.jumpToPhysicalElement(i)
                _ = outValue[i]
                if _ > 1.0:
                    outcomputeValueHandle.outputValue().setFloat(1.0)
                elif _ < 0.0:
                    outcomputeValueHandle.outputValue().setFloat(0.0)
                else:
                    outcomputeValueHandle.outputValue().setFloat(_)
            
            data.setClean(plug)
            return
    
    def getNowVector(self, twistAxis, Matrix, defaultMatrix):
        twistAxisValue = Matrix.getElement(3, twistAxis)
        if twistAxisValue >= 0:
            if twistAxisValue == 0:
                om.MGlobal.displayError(u"请检查轴向设置")
            twistAxisValue = 1
        else:
            twistAxisValue = -1
        targetMatrix = om.MMatrix().setElement(3, twistAxis, twistAxisValue) * Matrix
        targetMatrix = targetMatrix * defaultMatrix.inverse()
        return [targetMatrix.getElement(3, 0), targetMatrix.getElement(3, 1), targetMatrix.getElement(3, 2)]
        
    def dis(self, V1, V2):
        return math.sqrt((V1[0] - V2[0]) * (V1[0] - V2[0]) + (V1[1] - V2[1]) * (V1[1] - V2[1]) + (V1[2] - V2[2]) * (V1[2] - V2[2]))
    
    def inverse_matrix(self, Matrix):
        def transpose(mat):
            return list(map(list, zip(*mat)))

        def matrix_minor(Matrix, i, j):
            return [row[:j] + row[j+1:] for row in (Matrix[:i] + Matrix[i+1:])]

        def determinant(Matrix):
            if len(Matrix) == 2:
                return Matrix[0][0] * Matrix[1][1] - Matrix[0][1] * Matrix[1][0]

            det = 0
            for c in range(len(Matrix)):
                det += ((-1)**c) * Matrix[0][c] * determinant(matrix_minor(Matrix, 0, c))
            return det

        count = len(Matrix)
        det = determinant(Matrix)
        if det == 0:
            print('det 0') 
            return None
        if count == 2:
            return [[Matrix[1][1] / det, -1 * Matrix[0][1] / det], [-1 * Matrix[1][0] / det, Matrix[0][0] / det]]

        cfs = []
        for r in range(count):
            cfRow = []
            for c in range(count):
                minor = matrix_minor(Matrix, r, c)
                cfRow.append(((-1)**(r+c)) * determinant(minor))
            cfs.append(cfRow)
        cfs = transpose(cfs)
        for row in range(len(cfs)):
            for col in range(len(cfs)):
                cfs[row][col] = cfs[row][col] / det
        return cfs

    def multiply(self, M1, M2):
        if not M1:
            return
        count = len(M1)
        relsutMatrix = [[0] * count for _ in range(count)]
        for i1 in range(count):
            for i2 in range(count):
                for i3 in range(count):
                    relsutMatrix[i1][i2] += M1[i1][i3] * M2[i3][i2]
        return relsutMatrix

def initializePlugin(object):
    plugin = om.MFnPlugin(object, "BbBB", "1.0", "Any")
    try:
        plugin.registerNode(RBFCompute.NodeName, RBFCompute.NodeId, RBFCompute.creator, RBFCompute.initializer)
    except:
        sys.stderr.write("Failed to register node: %s" %RBFCompute.NodeName)
        raise

def uninitializePlugin(object):
    plugin = om.MFnPlugin(object)
    try:
        plugin.deregisterNode(RBFCompute.NodeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" %RBFCompute.NodeName)
        raise
    
