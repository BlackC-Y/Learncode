#pragma once
#include "pch.h"


class RBFCompute : public MPxNode
{
	struct OldValue {
		short twistAxis;
		std::vector<MVector> pointVector;
	};

public:
	RBFCompute();
	~RBFCompute() override;

	MStatus	compute(const MPlug& plug, MDataBlock& data) override;

	static void* creator();
	static MStatus initialize();
	double dis(MVector& V1, MVector& V2);
	MVector getNowVector(unsigned short twistAxis, MMatrix& Matrix, MMatrix& defaultMatrix);

public:
	static MObject twistAxis;
	static MObject driveMatrix;
	static MObject pointVector;
	static MObject defaultMatrix;
	static MTypeId id;
	static MObject outcomputeValue;
	static MObject outNowVector;

private:
	Eigen::MatrixXd _saveWeightMatrix;
	static OldValue _saveOldValue;

};