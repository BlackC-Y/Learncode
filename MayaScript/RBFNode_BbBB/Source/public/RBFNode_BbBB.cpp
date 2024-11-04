#include "pch.h"
#include "RBFNode_BbBB.h"


RBFCompute::RBFCompute(){}
RBFCompute::~RBFCompute(){}

MObject RBFCompute::twistAxis;
MObject RBFCompute::driveMatrix;
MObject RBFCompute::pointVector;
MObject RBFCompute::defaultMatrix;
MTypeId RBFCompute::id(0x80000);
MObject RBFCompute::outcomputeValue;
MObject RBFCompute::outNowVector;
RBFCompute::OldValue RBFCompute::_saveOldValue = {-1, std::vector<MVector>()};


void* RBFCompute::creator(){
    return new RBFCompute();
}

MStatus RBFCompute::initialize(){
    MStatus status;

    //MFnCompoundAttribute cAttr;
    //MFnGenericAttribute gAttr;
    MFnEnumAttribute eAttr;
    MFnNumericAttribute nAttr;
    //MFnUnitAttribute uAttr;
    //MFnTypedAttribute typedAttr;
    MFnMatrixAttribute mAttr; //kMatrix

    //input
    twistAxis = eAttr.create("twistAxis", "twistAxis", 0);
    eAttr.addField("X", 0);
    eAttr.addField("Y", 1);
    eAttr.addField("Z", 2);

    driveMatrix = mAttr.create("driveMatrix", "driveMatrix", MFnMatrixAttribute::kDouble);

    defaultMatrix = mAttr.create("defaultMatrix", "defaultMatrix", MFnMatrixAttribute::kDouble);
    mAttr.setHidden(true);
    mAttr.setConnectable(false);

    pointVector = nAttr.create("pointVector", "pointVector", MFnNumericData::k3Double);
    nAttr.setArray(true);
    nAttr.setDisconnectBehavior(MFnAttribute::kDelete);

    status = addAttribute(twistAxis);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = addAttribute(driveMatrix);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = addAttribute(defaultMatrix);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = addAttribute(pointVector);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    //output
    outcomputeValue = nAttr.create("outcomputeValue", "outcomputeValue", MFnNumericData::kFloat, 0.0);
    nAttr.setArray(true);
    nAttr.setStorable(false);

    outNowVector = nAttr.create("outNowVector", "outNowVector", MFnNumericData::k3Double, 0.0);
    nAttr.setHidden(true);
    nAttr.setStorable(false);

    status = addAttribute(outcomputeValue);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = addAttribute(outNowVector);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    //attributeAffects 连接输入影响输出
    status = attributeAffects(twistAxis, outcomputeValue);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = attributeAffects(driveMatrix, outcomputeValue);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = attributeAffects(pointVector, outcomputeValue);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    status = attributeAffects(twistAxis, outNowVector);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = attributeAffects(driveMatrix, outNowVector);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    status = attributeAffects(defaultMatrix, outNowVector);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    return MS::kSuccess;
}

MStatus RBFCompute::compute(const MPlug& plug, MDataBlock& data) {
    MStatus returnStatus;

    MDataHandle input_twistAxis = data.inputValue(twistAxis, &returnStatus);
    MDataHandle input_driveMatrix = data.inputValue(driveMatrix, &returnStatus);
    MDataHandle input_defaultMatrix = data.inputValue(defaultMatrix, &returnStatus);
    MVector driveVector = {};
    unsigned short twistAxis;
    if (returnStatus != MS::kSuccess) {
        MGlobal::displayError("RBFCompute: ERROR getting data");
        return MS::kUnknownParameter;
    }
    else {
        twistAxis = input_twistAxis.asShort();
        MMatrix driveMatrix = input_driveMatrix.asMatrix();
        MMatrix defaultMatrix = input_defaultMatrix.asMatrix();
        driveVector = getNowVector(twistAxis, driveMatrix, defaultMatrix);

        MDataHandle outNowVectorHandle = data.outputValue(RBFCompute::outNowVector);
        outNowVectorHandle.setMVector(driveVector);
    }
    
    if (plug == outcomputeValue) {
        MArrayDataHandle input_pointVector = data.inputArrayValue(pointVector, &returnStatus);
        if (returnStatus != MS::kSuccess) {
            MGlobal::displayError("RBFCompute: ERROR getting data");
        }
        else {
            unsigned int count = input_pointVector.elementCount();
            //Eigen::Matrix <float, Eigen::Dynamic, Eigen::Dynamic> disMatrix;
            Eigen::MatrixXd disMatrix(count, count);
            Eigen::MatrixXd valueMatrix = Eigen::MatrixXd::Identity(count, count);
            Eigen::VectorXd driveDis(count);
            //std::vector<int> driveDis;
            
            Eigen::MatrixXd weightMatrix;
            bool recompute = false;
            if (twistAxis != _saveOldValue.twistAxis) {
                _saveOldValue.twistAxis = twistAxis;
                recompute = true;
            }
            if (count != _saveOldValue.pointVector.size()) {
                recompute = true;
            }
            else {
                for (unsigned short i = 0; i < count; i++) {
                    returnStatus = input_pointVector.jumpToArrayElement(i);
                    MDataHandle Data1 = input_pointVector.inputValue(&returnStatus);
                    if (Data1.asVector() != _saveOldValue.pointVector[i]) {
                        recompute = true;
                        break;
                    }
                }
            }

            if (recompute) {
                _saveOldValue.pointVector.clear();
                for (unsigned short i1 = 0; i1 < count; i1++) {
                    returnStatus = input_pointVector.jumpToArrayElement(i1);
                    MDataHandle Data1 = input_pointVector.inputValue(&returnStatus);
                    MVector Vector1 = Data1.asVector();
                    _saveOldValue.pointVector.push_back(Vector1);
                    driveDis(i1) = dis(driveVector, Vector1);
                    for (unsigned short i2 = 0; i2 < count; i2++) {
                        returnStatus = input_pointVector.jumpToArrayElement(i2);
                        MDataHandle Data2 = input_pointVector.inputValue(&returnStatus);
                        MVector Vector2 = Data2.asVector();
                        disMatrix(i1, i2) = dis(Vector1, Vector2);
                    }
                }
                weightMatrix = disMatrix.inverse() * valueMatrix;
                RBFCompute::_saveWeightMatrix = weightMatrix;
            }
            else {
                for (unsigned short i1 = 0; i1 < count; i1++) {
                    returnStatus = input_pointVector.jumpToArrayElement(i1);
                    MDataHandle Data1 = input_pointVector.inputValue(&returnStatus);
                    MVector Vector1 = Data1.asVector();
                    driveDis(i1) = dis(driveVector, Vector1);
                }
                weightMatrix = RBFCompute::_saveWeightMatrix;
            }

            Eigen::VectorXf outValue = (weightMatrix * driveDis).cast<float>();

            MArrayDataHandle outcomputeValueHandle = data.outputArrayValue(RBFCompute::outcomputeValue);
            unsigned short outCount;
            if (count > outcomputeValueHandle.elementCount()) {
                outCount = outcomputeValueHandle.elementCount();
            }
            else {
                outCount = count;
            }
            for (unsigned short i = 0; i < outCount; i++) {
                outcomputeValueHandle.jumpToArrayElement(i);
                float _ = outValue(i);
                if (_ > 1.0) {
                    outcomputeValueHandle.outputValue().setFloat(1.0);
                }
                else if (_ < 0.0) {
                    outcomputeValueHandle.outputValue().setFloat(0.0);
                }
                else {
                    outcomputeValueHandle.outputValue().setFloat(_);
                }
            }

            data.setClean(plug);
        }
    }
    else {
        return MS::kUnknownParameter;
    }
    return MS::kSuccess;
}

MVector RBFCompute::getNowVector(unsigned short twistAxis, MMatrix& Matrix, MMatrix& defaultMatrix) {
    double twistAxisValue = Matrix(3, twistAxis);
    if (twistAxisValue >= 0) {
        if (twistAxisValue == 0) {
            MGlobal::displayWarning("RBFCompute: 请检查轴向设置");
        }
        twistAxisValue = 1;
    }
    else {
        twistAxisValue = -1;
    }
    MMatrix targetMatrix = MMatrix();
    targetMatrix(3, twistAxis) = twistAxisValue;
    targetMatrix = (targetMatrix * Matrix) * defaultMatrix.inverse();
    return { targetMatrix(3, 0), targetMatrix(3, 1), targetMatrix(3, 2) };
}

double RBFCompute::dis(MVector& V1, MVector& V2) {
    return sqrt((V1.x - V2.x) * (V1.x - V2.x) + (V1.y - V2.y) * (V1.y - V2.y) + (V1.z - V2.z) * (V1.z - V2.z));
}


MStatus initializePlugin(MObject obj) {
    MStatus   status;
    MFnPlugin plugin(obj, "BbBB", "1.0", "Any");

    status = plugin.registerNode("RBFCompute", RBFCompute::id, RBFCompute::creator, RBFCompute::initialize);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MStatus   status;
    MFnPlugin plugin(obj);

    status = plugin.deregisterNode(RBFCompute::id);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    return status;
}
