import maya.cmds as cmds
import maya.mel as mm

def IKFKWin():

    uiA = 'ApplePieB_testB'
    try:
        cmds.deleteUI(uiA)
    except:
        pass
    
    cmds.window(uiA,t="IKFKRig",menuBar=1)
    cmds.columnLayout(columnAttach=("both",2),rowSpacing=5,columnWidth=250)
    cmds.button('FitlocButton',l="import FitSystem",h=28,c=lambda*args:ApplePieB_BuildJoint().FitSystem())
    cmds.button('mirrorButton',l="Mirror",h=28,c=lambda*args:ApplePieB_BuildJoint().mirrorJoint())
    cmds.flowLayout(columnSpacing=45)
    cmds.button('ChangeJointButton',l="changeVis",h=28,w=100,c=lambda*args:ApplePieB_BuildJoint().ChangeVis(''))
    cmds.button('BuildJointButton',l="Build",h=28,w=100,c=lambda*args:ApplePieB_BuildJoint().buildL_IKLeg())
    cmds.setParent('..')

    cmds.window(uiA,e=1,wh=(260,500))
    cmds.showWindow(uiA)

class ApplePieB_BuildJoint(object):

    def __init__(self):
        pass

    def FitSystem(self):
        import tempfile
        listname = cmds.ls()
        if 'FitSystem' in listname:
            cmds.error('Have System or Same Name')
        with tempfile.NamedTemporaryFile('w+t',suffix='.mel',delete=False) as tempfileA:
            tempfileA.write('     \
            createNode transform -n \"FitSystem\";     \
                rename -uid \"831DF7C8-4AF1-B035-FE23-98B88386F7F5\";     \
            createNode nurbsCurve -n \"FitSystemShape\" -p \"FitSystem\";     \
                rename -uid \"6D6B564F-4EC4-C44A-C4CE-76B56BA92169\";     \
                setAttr -k off \".v\";     \
                setAttr \".cc\" -type \"nurbsCurve\"      \
                    3 8 2 no 3     \
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10     \
                    11     \
                    3.134446499564898 1.9192949363953893e-16 -3.1344464995648984     \
                    2.7142929292443649e-16 2.7142929292443649e-16 -4.4327767502175508     \
                    -3.134446499564898 1.9192949363953888e-16 -3.1344464995648975     \
                    -4.4327767502175526 1.4070942476024109e-32 -2.2979592950099322e-16     \
                    -3.134446499564898 -1.919294936395389e-16 3.134446499564898     \
                    -4.4403427878412899e-16 -2.7142929292443668e-16 4.4327767502175535     \
                    3.134446499564898 -1.9192949363953888e-16 3.1344464995648975     \
                    4.4327767502175526 -3.7014716840440396e-32 6.044962003119836e-16     \
                    3.134446499564898 1.9192949363953893e-16 -3.1344464995648984     \
                    2.7142929292443649e-16 2.7142929292443649e-16 -4.4327767502175508     \
                    -3.134446499564898 1.9192949363953888e-16 -3.1344464995648975     \
                    ;     \
            createNode joint -n \"RootFit_joint\" -p \"FitSystem\";     \
                rename -uid \"5AFD3410-4291-6ED2-47AD-198182403F27\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.9709482123357001e-16 9.8285101990184405 -0.177172081380293 ;     \
                setAttr -l on \".tx\";     \
                setAttr \".r\" -type \"double3\" 1.59027734073176e-14 2.2263882770244598e-14 -2.2263882770244598e-14 ;     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".jo\" -type \"double3\" 90 8.8321986828207741 89.999999999999986 ;     \
                setAttr \".ssc\" no;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"SpineFit_joint\" -p \"RootFit_joint\";     \
                rename -uid \"5B4CD265-41D9-6C38-BE63-C1A1B7A49736\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.7561552005093699 0 -7.5302564402681704e-16 ;     \
                setAttr -l on \".tz\";     \
                setAttr \".r\" -type \"double3\" 6.7940406962849701e-16 2.50577257396594e-14 -8.5874976399514899e-14 ;     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".jo\" -type \"double3\" 0 0 3.1062237164616202 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ChestFit_joint\" -p \"SpineFit_joint\";     \
                rename -uid \"5EC016B2-496B-5B64-BF7E-079FF1AEE1C3\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.4259059316898699 -4.4408920985006301e-16 -6.23605439536448e-16 ;     \
                setAttr -l on \".tz\";     \
                setAttr \".r\" -type \"double3\" -2.5330783029728399e-14 -2.2486456079175096e-13 1.7015967545829799e-13 ;     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".ssc\" no;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ScapulaFit_joint\" -p \"ChestFit_joint\";     \
                rename -uid \"168CCFC7-45E1-BC64-C961-B6BD45C6ED26\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 0.68383900369522999 0.438408709664173 0.436536 ;     \
                setAttr \".ro\" 2;     \
                setAttr \".jo\" -type \"double3\" -122.045348813239 89.978769446430903 62.874799969304 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ShoulderFit_joint\" -p \"ScapulaFit_joint\";     \
                rename -uid \"4E0DCF3A-4F66-524E-2604-62B9860CA584\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -1.0925440911344499 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.00030235216151690497 -0.011608264599795 -2.9840096586894398 ;     \
                setAttr \".pa\" -type \"double3\" -4.1293130717023494e-07 0 0 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ElbowFit_joint\" -p \"ShoulderFit_joint\";     \
                rename -uid \"1474980E-46C1-B0D6-1EAA-A9AD814D6A64\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -2.61424750819923 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0 0 6.3821889474817599 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"WristFit_joint\" -p \"ElbowFit_joint\";     \
                rename -uid \"02F68D6C-4A32-FCB9-C383-CBA988F878B4\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -2.2826010691551399 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"CupFit_joint\" -p \"WristFit_joint\";     \
                rename -uid \"9C5499A4-4DEC-FB10-C51E-119730B6F548\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.19735405836598699 0.11260430613877601 0.0010846172039968799 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"PinkyFinger1Fit_joint\" -p \"CupFit_joint\";     \
                rename -uid \"3274CA20-4BC4-F2C7-A5F5-C5B79DED570E\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.60324957333521501 0.31630125090128802 0.072771951143005595 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -3.1934272258485401 8.5540945674290096 -23.941276169156598 ;     \
                setAttr \".pa\" -type \"double3\" -0.21586850671656499 -15.8568973437946 -7.9762775885025512 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"PinkyFinger2Fit_joint\" -p \"PinkyFinger1Fit_joint\";     \
                rename -uid \"4DA41052-4D45-D0EE-387C-2095CC89C5B5\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.23273731694135499 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.26683083077943698 -0.71917589712380303 -0.034439123916583499 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 0.71999997359173995 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"PinkyFinger3Fit_joint\" -p \"PinkyFinger2Fit_joint\";     \
                rename -uid \"4D249BB9-4A64-E364-2A2B-97AE6C28740E\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.14229054952105699 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 2.1588765498947899 -5.7546090601920099 -0.24956300887686902 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 5.7599997887354597 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"PinkyFinger4Fit_joint\" -p \"PinkyFinger3Fit_joint\";     \
                rename -uid \"EA922242-4D13-4EC8-61DD-B49A3BCDB67F\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.17793092221366899 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"RingFinger1Fit_joint\" -p \"CupFit_joint\";     \
                rename -uid \"6B244477-4F9A-94EF-A491-CF8029E9CB88\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.67948422373835404 0.17024130281869301 0.045182638936632102 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -0.27735236068149199 2.1128094904078298 -10.860478591292001 ;     \
                setAttr \".pa\" -type \"double3\" -0.07133019936876682 -2.8352236419285801 -1.44176523252515 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"RingFinger2Fit_joint\" -p \"RingFinger1Fit_joint\";     \
                rename -uid \"EC9A70E6-4825-ABC7-B456-44A9EAEE7116\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.289519126772529 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -0.283179149379163 2.1599955702212199 0.0043909097710733303 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 -2.1600000310934702 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"RingFinger3Fit_joint\" -p \"RingFinger2Fit_joint\";     \
                rename -uid \"31E01F78-48AC-232F-60C2-34AC2F7DF220\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.17506745854880101 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.56783371126567495 -4.3198948128062504 -0.0301920990901875 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 4.3200001190538604 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"RingFinger4Fit_joint\" -p \"RingFinger3Fit_joint\";     \
                rename -uid \"57B568A3-4607-2BA9-F6F9-E49BED27A17C\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.193695846302153 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"MiddleFinger1Fit_joint\" -p \"WristFit_joint\";     \
                rename -uid \"9954CEC8-4F42-D0AD-0B1E-BCA1D0E4B137\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.96179807285942198 0.052834594619845299 -3.84741120118548e-05 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -0.069474194582375803 4.7753179570066697 -4.2146644098138211 ;     \
                setAttr \".pa\" -type \"double3\" -2.4903031680136702e-17 3.8068719241856397 -4.0949047407001498 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"MiddleFinger2Fit_joint\" -p \"MiddleFinger1Fit_joint\";     \
                rename -uid \"A54D012C-4133-AA43-6428-83B74670FF6C\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.31063934596668502 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.0366789489497742 -2.51999858603003 -0.0025734866818090101 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 2.5199999009299199 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"MiddleFinger3Fit_joint\" -p \"MiddleFinger2Fit_joint\";     \
                rename -uid \"733B06F1-4851-1634-66A7-63B48EE6927C\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.17127181467682201 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.053454832742631402 -3.6712936380785002 -0.0014021136006168099 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 3.6712939054552702 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"MiddleFinger4Fit_joint\" -p \"MiddleFinger3Fit_joint\";     \
                rename -uid \"35C77E59-4077-8D46-E8AD-D6946940A3F1\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.20934532736616501 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"IndexFinger1Fit_joint\" -p \"WristFit_joint\";     \
                rename -uid \"B372577A-4D07-54A1-926D-8397E6ADBFB9\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.87351292049165297 -0.18848618711093501 0.0173761705485838 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0.90355498163943293 3.1740263719564301 12.518932082915301 ;     \
                setAttr \".pa\" -type \"double3\" 0.065532877363568803 20.527688987272199 -2.5422327562497999 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"IndexFinger2Fit_joint\" -p \"IndexFinger1Fit_joint\";     \
                rename -uid \"FF9FE652-4AFA-EEC4-7516-90AEF59DAFBA\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.26386319706148198 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"IndexFinger3Fit_joint\" -p \"IndexFinger2Fit_joint\";     \
                rename -uid \"08F28651-4BA7-83B1-7952-65A18F051EB1\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.17551664883474999 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -1.6418340242712399 -5.7596206078047896 0.066225387226028803 ;     \
                setAttr \".pa\" -type \"double3\" 0 0 5.7600000490223504 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"IndexFinger4Fit_joint\" -p \"IndexFinger3Fit_joint\";     \
                rename -uid \"1768BCC9-47E4-FC52-7334-1D99E7088584\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.185485727298735 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ThumbFinger1Fit_joint\" -p \"WristFit_joint\";     \
                rename -uid \"4329AEFD-4C22-F1ED-DB5B-8EA2AA3539E7\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.21221537596599299 -0.13257524882348001 0.100847669101745 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" -52.264000000008501 19.323320728479199 35.059772150528801 ;     \
                setAttr \".pa\" -type \"double3\" -34.462082586865904 -8.7285733235282201 -1.7903981777634801 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ThumbFinger2Fit_joint\" -p \"ThumbFinger1Fit_joint\";     \
                rename -uid \"E33ED5CA-47C4-9987-FA41-BEBCE93DB625\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.350882004753308 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ThumbFinger3Fit_joint\" -p \"ThumbFinger2Fit_joint\";     \
                rename -uid \"7E3120F2-4C1F-6646-1243-B9BEDE5751C3\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.16867759392760601 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ThumbFinger4Fit_joint\" -p \"ThumbFinger3Fit_joint\";     \
                rename -uid \"5B2539A8-494F-52C1-CC36-89ABF06DE8CA\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.20329531863702799 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"NeckFit_joint\" -p \"ChestFit_joint\";     \
                rename -uid \"A7F05595-4B29-5105-7109-798DB25D2A43\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.0940762794857799 0 4.5826128503803998e-15 ;     \
                setAttr -l on \".tz\";     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 6.5397546330015201e-15 -4.4785430244359099e-15 15.2501013231209 ;     \
                setAttr \".pa\" -type \"double3\" -1.79404477487463e-16 6.8425179703802998e-15 0 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"HeadFit_joint\" -p \"NeckFit_joint\";     \
                rename -uid \"7190888B-4CC8-CE57-EF63-5598B44B11CA\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.5550714897106299 7.1054273576010003e-15 -1.87909084312516e-16 ;     \
                setAttr -l on \".tz\";     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 0 0 -10.323099411909 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"JawFit_joint\" -p \"HeadFit_joint\";     \
                rename -uid \"350922F9-4670-D906-B563-88A0EAE8ADBA\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.28087979879352598 0.40553446789889402 -6.41125795588967e-16 ;     \
                setAttr -l on \".tz\";     \
                setAttr \".r\" -type \"double3\" 1.9008584441061501e-16 1.14729983783598e-16 -7.4424979546246296e-13 ;     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr \".jo\" -type \"double3\" 0 0 117.77221494634301 ;     \
                setAttr \".radi\" 0.500000000000001;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"JawEndFit_joint\" -p \"JawFit_joint\";     \
                rename -uid \"5C13F9ED-4249-7C64-4962-4EB52861F679\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.0828940539241301 -1.4210854715202001e-14 -2.16840434499724e-18 ;     \
                setAttr -l on \".tz\";     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"HeadEndFit_joint\" -p \"HeadFit_joint\";     \
                rename -uid \"3E5F2B4D-4946-8885-2C13-49844498E6AB\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 1.5016973184746301 -5.4123372450476401e-16 4.18068523820481e-16 ;     \
                setAttr -l on \".tz\";     \
                setAttr -l on \".rx\";     \
                setAttr -l on \".ry\";     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"EyeFit_joint\" -p \"HeadFit_joint\";     \
                rename -uid \"B4B41F10-4988-BFF6-0821-E092F0E4EE46\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" 0.22356767632738261 1.0518800800190506 0.34230099999999569 ;     \
                setAttr \".ro\" 2;     \
                setAttr \".jo\" -type \"double3\" -1.6153170302846096e-14 1.6153170302846093e-14 -90.000000000000014 ;     \
                setAttr \".pa\" -type \"double3\" 8.9959671327899898e-14 0 0 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"EyeEndFit_joint\" -p \"EyeFit_joint\";     \
                rename -uid \"46BCA0FF-4AED-7EC3-421D-E6947B2B85E4\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.1708708547866532 0 -5.5511151231257827e-17 ;     \
                setAttr \".ro\" 1;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"HipFit_joint\" -p \"RootFit_joint\";     \
                rename -uid \"E3607B38-4A5B-40BF-500A-6B83DF81C1E8\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.198520732814675 -0.085016123982221997 0.819687 ;     \
                setAttr \".ro\" 2;     \
                setAttr \".jo\" -type \"double3\" -179.42796161305 1.78922001078616 3.6707670017174201 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"KneeFit_joint\" -p \"HipFit_joint\";     \
                rename -uid \"0047455D-4752-600D-1E40-5F8E8C4A7351\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -4.9741244450505704 0 0 ;     \
                setAttr \".ro\" 2;     \
                setAttr \".jo\" -type \"double3\" 1.7075473008465099e-06 0 -9.4300858589301608 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"AnkleFit_joint\" -p \"KneeFit_joint\";     \
                rename -uid \"E3B18FF8-4DA7-C8DF-ACC1-B182ED3B90A8\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -3.83018252050943 0 0 ;     \
                setAttr \".ro\" 3;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ToesFit_joint\" -p \"AnkleFit_joint\";     \
                rename -uid \"7A29A7BE-4665-E0F6-B656-1C980FBAE70F\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.56355517488546303 -1.38757153761192 0.053472985469894797 ;     \
                setAttr \".ro\" 5;     \
                setAttr \".jo\" -type \"double3\" 1.6945897733566502 0.81048168159287104 91.598725152936396 ;     \
                setAttr \".pa\" -type \"double3\" -0.00019030234564052401 0.00053514845282692 25.864574245063601 ;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode joint -n \"ToesEndFit_joint\" -p \"ToesFit_joint\";     \
                rename -uid \"D6EDE439-4908-C196-0C7A-3EAD5BD01064\";     \
                addAttr -is true -ci true -h true -k true -sn \"filmboxTypeID\" -ln \"filmboxTypeID\"      \
                    -smn 5 -smx 5 -at \"short\";     \
                setAttr \".t\" -type \"double3\" -0.62689640295075999 0 0 ;     \
                setAttr \".ro\" 5;     \
                setAttr -k on \".filmboxTypeID\" 5;     \
            createNode transform -n \"L_FootFit_loc1\" -p \"FitSystem\";     \
                rename -uid \"96D527E3-48C0-0432-D4E1-17AFFCC16149\";     \
                setAttr \".t\" -type \"double3\" 1.0928430805715872 0 3.0393272224503067 ;     \
            createNode locator -n \"L_FootFit_locShape1\" -p \"L_FootFit_loc1\";     \
                rename -uid \"752228C1-4A57-8AF5-E315-63948DB8EF1F\";     \
                setAttr -k off \".v\";     \
            createNode transform -n \"L_FootFit_loc2\" -p \"FitSystem\";     \
                rename -uid \"A9E53379-48E2-41C6-481A-8E9BE684DA01\";     \
                setAttr \".t\" -type \"double3\" 1.0025870461371376 0 -2.0812335990234176 ;     \
            createNode locator -n \"L_FootFit_locShape2\" -p \"L_FootFit_loc2\";     \
                rename -uid \"1F86DCF1-42D2-DB3C-DA4B-48922525B587\";     \
                setAttr -k off \".v\";     \
            createNode transform -n \"L_FootFit_loc3\" -p \"FitSystem\";     \
                rename -uid \"C811F4D4-412D-7B2E-F3D7-CA9BA180B62D\";     \
                setAttr \".t\" -type \"double3\" 0.2596338313776263 0 0.95835763320530087 ;     \
            createNode locator -n \"L_FootFit_locShape3\" -p \"L_FootFit_loc3\";     \
                rename -uid \"CC1B4818-4A6F-22B9-FD34-CAA933F2577A\";     \
                setAttr -k off \".v\";     \
            createNode transform -n \"L_FootFit_loc4\" -p \"FitSystem\";     \
                rename -uid \"C0F2BDB0-49E4-A25C-9E42-10868907B796\";     \
                setAttr \".t\" -type \"double3\" 2.043478024313389 0 0.98256201119452791 ;     \
            createNode locator -n \"L_FootFit_locShape4\" -p \"L_FootFit_loc4\";     \
                rename -uid \"BB796A5A-427D-9E2B-E62F-DAA7B1C4D329\";     \
                setAttr -k off \".v\";     \
            connectAttr \"RootFit_joint.s\" \"SpineFit_joint.is\";     \
            connectAttr \"SpineFit_joint.s\" \"ChestFit_joint.is\";     \
            connectAttr \"ChestFit_joint.s\" \"ScapulaFit_joint.is\";     \
            connectAttr \"ScapulaFit_joint.s\" \"ShoulderFit_joint.is\";     \
            connectAttr \"ShoulderFit_joint.s\" \"ElbowFit_joint.is\";     \
            connectAttr \"ElbowFit_joint.s\" \"WristFit_joint.is\";     \
            connectAttr \"WristFit_joint.s\" \"CupFit_joint.is\";     \
            connectAttr \"CupFit_joint.s\" \"PinkyFinger1Fit_joint.is\";     \
            connectAttr \"PinkyFinger1Fit_joint.s\" \"PinkyFinger2Fit_joint.is\";     \
            connectAttr \"PinkyFinger2Fit_joint.s\" \"PinkyFinger3Fit_joint.is\";     \
            connectAttr \"PinkyFinger3Fit_joint.s\" \"PinkyFinger4Fit_joint.is\";     \
            connectAttr \"CupFit_joint.s\" \"RingFinger1Fit_joint.is\";     \
            connectAttr \"RingFinger1Fit_joint.s\" \"RingFinger2Fit_joint.is\";     \
            connectAttr \"RingFinger2Fit_joint.s\" \"RingFinger3Fit_joint.is\";     \
            connectAttr \"RingFinger3Fit_joint.s\" \"RingFinger4Fit_joint.is\";     \
            connectAttr \"WristFit_joint.s\" \"MiddleFinger1Fit_joint.is\";     \
            connectAttr \"MiddleFinger1Fit_joint.s\" \"MiddleFinger2Fit_joint.is\";     \
            connectAttr \"MiddleFinger2Fit_joint.s\" \"MiddleFinger3Fit_joint.is\";     \
            connectAttr \"MiddleFinger3Fit_joint.s\" \"MiddleFinger4Fit_joint.is\";     \
            connectAttr \"WristFit_joint.s\" \"IndexFinger1Fit_joint.is\";     \
            connectAttr \"IndexFinger1Fit_joint.s\" \"IndexFinger2Fit_joint.is\";     \
            connectAttr \"IndexFinger2Fit_joint.s\" \"IndexFinger3Fit_joint.is\";     \
            connectAttr \"IndexFinger3Fit_joint.s\" \"IndexFinger4Fit_joint.is\";     \
            connectAttr \"WristFit_joint.s\" \"ThumbFinger1Fit_joint.is\";     \
            connectAttr \"ThumbFinger1Fit_joint.s\" \"ThumbFinger2Fit_joint.is\";     \
            connectAttr \"ThumbFinger2Fit_joint.s\" \"ThumbFinger3Fit_joint.is\";     \
            connectAttr \"ThumbFinger3Fit_joint.s\" \"ThumbFinger4Fit_joint.is\";     \
            connectAttr \"ChestFit_joint.s\" \"NeckFit_joint.is\";     \
            connectAttr \"NeckFit_joint.s\" \"HeadFit_joint.is\";     \
            connectAttr \"HeadFit_joint.s\" \"JawFit_joint.is\";     \
            connectAttr \"JawFit_joint.s\" \"JawEndFit_joint.is\";     \
            connectAttr \"HeadFit_joint.s\" \"HeadEndFit_joint.is\";     \
            connectAttr \"HeadFit_joint.s\" \"EyeFit_joint.is\";     \
            connectAttr \"EyeFit_joint.s\" \"EyeEndFit_joint.is\";     \
            connectAttr \"RootFit_joint.s\" \"HipFit_joint.is\";     \
            connectAttr \"HipFit_joint.s\" \"KneeFit_joint.is\";     \
            connectAttr \"KneeFit_joint.s\" \"AnkleFit_joint.is\";     \
            connectAttr \"AnkleFit_joint.s\" \"ToesFit_joint.is\";     \
            connectAttr \"ToesFit_joint.s\" \"ToesEndFit_joint.is\";     \
            select -cl;     \
            ')
        ##print (tempfileA.name)
        cmds.file(tempfileA.name,i=1,type="mel",mergeNamespacesOnClash=False,pr=0)
        cmds.group('L_FootFit_loc1','L_FootFit_loc2','L_FootFit_loc3','L_FootFit_loc4',n='L_FootFitloc')

    def ChangeVis(self,noff):

        if noff == 'ff':
            cmds.setAttr("FitSystem.visibility",0)
        elif noff == 'n':
            cmds.setAttr("FitSystem.visibility",1)
        else:
            visib = cmds.getAttr('FitSystem.visibility')
            if visib == 0:
                cmds.setAttr("FitSystem.visibility",1)
            else:
                cmds.setAttr("FitSystem.visibility",0)

    def createcurve(self,Sample,ename):
        
        LR1loc = LR2loc = LR3loc = LR4loc = LRankle = [0,0,0]
        if Sample == 'Foot':     
            #L_R_T       
            LoR = ename.split('_',1)[0]
            LR1loc = cmds.xform((LoR+'_FootFit_loc1'),q=1,ws=1,t=1) #1.5 0 3
            LR2loc = cmds.xform((LoR+'_FootFit_loc2'),q=1,ws=1,t=1) #1 0 -2
            LR3loc = cmds.xform((LoR+'_FootFit_loc3'),q=1,ws=1,t=1) #0 0 0
            LR4loc = cmds.xform((LoR+'_FootFit_loc4'),q=1,ws=1,t=1) #2 0 1
            LRankle = cmds.xform(('AnkleIK_'+LoR),q=1,ws=1,t=1) #1 1 0
        curSample = [
                [((-.5 ,.5 ,.5 ),(-.5 ,.5 ,-.5 ),(.5 ,.5 ,-.5 ),(.5 ,.5 ,.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(-.5 ,-.5 ,-.5 ),(-.5 ,.5 ,-.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(.5 ,-.5 ,.5 ),(.5 ,.5 ,.5 ),(.5 ,.5 ,-.5 ),(.5 ,-.5 ,-.5 ),(.5 ,-.5 ,.5 ),(.5 ,-.5 ,-.5 ),(-.5 ,-.5 ,-.5)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)],
                [((0,1,0),(0,0.92388,0.382683),(0,0.707107,0.707107),(0,0.382683,0.92388),(0,0,1),(0,-0.382683,0.92388),(0,-0.707107,0.707107),(0,-0.92388,0.382683),(0,-1,0),(0,-0.92388,-0.382683),(0,-0.707107,-0.707107),(0,-0.382683,-0.92388),(0,0,-1),(0,0.382683,-0.92388),(0,0.707107,-0.707107),(0,0.92388,-0.382683),(0,1,0),(0.382683,0.92388,0),(0.707107,0.707107,0),(0.92388,0.382683,0),(1,0,0),(0.92388,-0.382683,0),(0.707107,-0.707107,0),(0.382683,-0.92388,0),(0,-1,0),(-0.382683,-0.92388,0),(-0.707107,-0.707107,0),(-0.92388,-0.382683,0),(-1,0,0),(-0.92388,0.382683,0),(-0.707107,0.707107,0),(-0.382683,0.92388,0),(0,1,0),(0,0.92388,-0.382683),(0,0.707107,-0.707107),(0,0.382683,-0.92388),(0,0,-1),(-0.382683,0,-0.92388),(-0.707107,0,-0.707107),(-0.92388,0,-0.382683),(-1,0,0),(-0.92388,0,0.382683),(-0.707107,0,0.707107),(-0.382683,0,0.92388),(0,0,1),(0.382683,0,0.92388),(0.707107,0,0.707107),(0.92388,0,0.382683),(1,0,0),(0.92388,0,-0.382683),(0.707107,0,-0.707107),(0.382683,0,-0.92388),(0,0,-1)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52)],
                [((-1.6,-6.4,0),(-1.6,-1.6,0),(-6.4,-1.6,0),(-6.4,1.6,0),(-1.6,1.6,0),(-1.6,6.4,0),(1.6,6.4,0),(1.6,1.6,0),(6.4,1.6,0),(6.4,-1.6,0),(1.6,-1.6,0),(1.6,-6.4,0),(-1.6,-6.4,0)),(0,4.8,9.6,12.8,17.6,22.4,25.6,30.4,35.2,38.4,43.2,48,51.2)],
                [((LR4loc[0],LR2loc[1],LR2loc[2]),(LR4loc[0],LRankle[1],LR2loc[2]),(LR3loc[0],LRankle[1],LR2loc[2]),(LR3loc[0],LR2loc[1],LR2loc[2]),(LR4loc[0],LR2loc[1],LR2loc[2]),(LR4loc[0],LR2loc[1],LR1loc[2]),(LR3loc[0],LR2loc[1],LR1loc[2]),(LR3loc[0],LR2loc[1],LR2loc[2]),(LR3loc[0],LRankle[1],LR2loc[2]),(LR3loc[0],LRankle[1],LR3loc[2]),(LR3loc[0],LR2loc[1],LR1loc[2]),(LR4loc[0],LR2loc[1],LR1loc[2]),(LR4loc[0],LRankle[1],LR4loc[2]),(LR3loc[0],LRankle[1],LR3loc[2]),(LR3loc[0],LRankle[1],LR2loc[2]),(LR4loc[0],LRankle[1],LR2loc[2]),(LR4loc[0],LRankle[1],LR4loc[2])),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)],
                    ]
        if Sample == 10:
            cmds.circle(ch=0,n=ename)
        elif Sample == 'Foot':
            cmds.curve(d=1,p=curSample[3][0],k=curSample[3][1],n=ename)
        else:
            cmds.curve(d=1,p=curSample[Sample][0],k=curSample[Sample][1],n=ename)
        SDKgroup = cmds.group(n=(ename+"_SDK"))
        ctrlgroup = cmds.group(n=(ename+"_grp"))
        #return [ename]

    def setAttt(self,Name,mode,size):
        if '1' in mode:
            cmds.setAttr((Name+".tx"),size)
        elif '2' in mode:
            cmds.setAttr((Name+".ty"),size)
        elif '3' in mode:
            cmds.setAttr((Name+".tz"),size)
        elif '4' in mode:
            cmds.setAttr((Name+".rx"),size)
        elif '5' in mode:
            cmds.setAttr((Name+".ry"),size)
        elif '6' in mode:
            cmds.setAttr((Name+".rz"),size)
        elif mode == '7':
            cmds.setAttr((Name+".tx"),size)
            cmds.setAttr((Name+".ty"),size)
            cmds.setAttr((Name+".tz"),size)
            cmds.setAttr((Name+".rx"),size)
            cmds.setAttr((Name+".ry"),size)
            cmds.setAttr((Name+".rz"),size)

    def mirrorJoint(self):
        
        self.ChangeVis('ff')
        cmds.makeIdentity('FitSystem',apply=1,t=0,r=0,s=1,n=0)
        try:
            cmds.delete('R_FootFitloc')
            cmds.delete('Root_M')
        except:
            pass
        cmds.mirrorJoint('RootFit_joint',mirrorBehavior=1,searchReplace=("Fit_joint","_Z"))
        cmds.parent('Root_Z',w=1)
        mm.eval("SelectHierarchy;")
        Zjoint = cmds.ls(sl=1)
        for i in Zjoint:
            cmds.setAttr((i+".tx"),lock=0)
            cmds.setAttr((i+".ty"),lock=0)
            cmds.setAttr((i+".tz"),lock=0)
            cmds.setAttr((i+".rx"),lock=0)
            cmds.setAttr((i+".ry"),lock=0)
            cmds.setAttr((i+".rz"),lock=0)
        cmds.makeIdentity(apply=1,t=0,r=1,s=0,n=0,pn=1)
        MjointName = ["Root_Z","Spine_Z","Chest_Z","Neck_Z","Head_Z","HeadEnd_Z","Jaw_Z","JawEnd_Z"]
        for i in MjointName:
            new_name = i.replace('_Z','_M')
            cmds.rename(i,new_name)
        ljoint = []
        for i in Zjoint:
            if i not in MjointName:
                ljoint.append(i)
        for i in ljoint:
            new_name = i.replace("_Z","_R")
            cmds.rename(i,new_name)
        cmds.mirrorJoint('Scapula_R',mirrorBehavior=1,searchReplace=("_R","_L"))
        cmds.mirrorJoint('Hip_R',mirrorBehavior=1,searchReplace=("_R","_L"))
        cmds.mirrorJoint('Eye_R',mirrorBehavior=1,searchReplace=("_R","_L"))
        setJlist = ["Spine_M","Chest_M","Neck_M","Head_M","HeadEnd_M","JawEnd_M","EyeEnd_L","EyeEnd_R","Knee_L","Knee_R","Ankle_L","Ankle_R","ToesEnd_L","ToesEnd_R",
                    "Shoulder_L","Shoulder_R","Elbow_L","Elbow_R","Wrist_L","Wrist_R",
                    "ThumbFinger2_L","ThumbFinger3_L","ThumbFinger4_L","IndexFinger2_L","IndexFinger3_L","IndexFinger4_L",
                    "MiddleFinger2_L","MiddleFinger3_L","MiddleFinger4_L","RingFinger2_L","RingFinger3_L","RingFinger4_L",
                    "PinkyFinger2_L","PinkyFinger3_L","PinkyFinger4_L"]
        for i in setJlist:
            self.setAttt(i,['2','3'],0)
        Lloc = ['L_FootFit_loc1','L_FootFit_loc2','L_FootFit_loc3','L_FootFit_loc4']
        Rloc = ['R_FootFit_loc1','R_FootFit_loc2','R_FootFit_loc3','R_FootFit_loc4']
        for i in range(0,len(Lloc),1):
            cmds.duplicate(Lloc[i],rr=1,n=Rloc[i])
        cmds.group(Rloc,n='R_FootFitloc',w=1)
        cmds.xform('R_FootFitloc',os=1,piv=(0,0,0))
        cmds.parent('R_FootFitloc','FitSystem')
        cmds.setAttr("R_FootFitloc.scaleX",-1)
        cmds.setAttr("R_FootFitloc.visibility",0)
        #self.buildL_IKLeg()

    def buildL_IKLeg(self):

        LoR = ['L','R']
        kkn = ['IK_','FK_','CN_']
        leg_name = ['Hip','Knee','Ankle','Toes','ToesEnd']
        dn = []

        self.WSGroup = cmds.group(em=1,n='world_pos_grp')
        self.RGroup = cmds.group(em=1,n='root_pos_grp')
        for i in range(len(LoR)):

            for k in kkn:
                for l in leg_name:
                    dn = cmds.duplicate((l+'_'+LoR[i]),rr=1,po=1,n=(l+k+LoR[i]))
                    if l == 'Hip':
                        cmds.parent(dn,w=1)
                for p in range(len(leg_name),1,-1):
                    p = p-1
                    n = p-1
                    cmds.parent((leg_name[p]+k+LoR[i]),(leg_name[n]+k+LoR[i]))

            #3K7z
            LR1loc = cmds.xform((LoR[i]+'_FootFit_loc1'),q=1,ws=1,t=1)
            LR2loc = cmds.xform((LoR[i]+'_FootFit_loc2'),q=1,ws=1,t=1)
            LR3loc = cmds.xform((LoR[i]+'_FootFit_loc3'),q=1,ws=1,t=1)
            LR4loc = cmds.xform((LoR[i]+'_FootFit_loc4'),q=1,ws=1,t=1)
            self.LRHip = cmds.xform('HipIK_'+LoR[i],q=1,ws=1,t=1)
            self.LRKnee = cmds.xform('KneeIK_'+LoR[i],q=1,ws=1,t=1)
            self.LRAnkle = cmds.xform('AnkleIK_'+LoR[i],q=1,ws=1,t=1)
            self.LRToes = cmds.xform('ToesIK_'+LoR[i],q=1,ws=1,t=1)

            AnkleIKH = cmds.ikHandle(sj=('HipIK_'+LoR[i]),ee=('AnkleIK_'+LoR[i]),n='AnkleIK_'+LoR[i]+'_ikHandle',sol="ikRPsolver")
            ToesIKH = cmds.ikHandle(sj=('AnkleIK_'+LoR[i]),ee=('ToesIK_'+LoR[i]),n='ToesIK_'+LoR[i]+'_ikHandle',sol="ikSCsolver")
            ToesEndIKH = cmds.ikHandle(sj=('ToesIK_'+LoR[i]),ee=('ToesEndIK_'+LoR[i]),n='ToesEndIK_'+LoR[i]+'_ikHandle',sol="ikSCsolver")

            ToesEndIKg = cmds.group(AnkleIKH[0],ToesIKH[0],ToesEndIKH[0],n='ToesEndIK_'+LoR[i]+'_grp')
            cmds.setAttr((ToesEndIKg+'.rp'),LR1loc[0],LR1loc[1],LR1loc[2],e=1)
            HeelIKg = cmds.group(ToesEndIKg,n='HeelIK_'+LoR[i]+'_grp')
            cmds.setAttr((HeelIKg+'.rp'),LR2loc[0],LR2loc[1],LR2loc[2],e=1)
            AnkleIKg = cmds.group(HeelIKg,n='AnkleIK_'+LoR[i]+'_grp')
            cmds.setAttr((AnkleIKg+'.rp'),self.LRAnkle[0],self.LRAnkle[1],self.LRAnkle[2],e=1)
            ToesInIKg = cmds.group(ToesEndIKg,n='ToesInIK_'+LoR[i]+'_grp')
            cmds.setAttr((ToesInIKg+'.rp'),LR3loc[0],LR3loc[1],LR3loc[2],e=1)
            ToesOutIKg = cmds.group(ToesInIKg,n='ToesOutIK_'+LoR[i]+'_grp')
            cmds.setAttr((ToesOutIKg+'.rp'),LR4loc[0],LR4loc[1],LR4loc[2],e=1)
            ToesIKg = cmds.group(ToesEndIKH[0],n='ToesIK_'+LoR[i]+'_grp')
            cmds.setAttr((ToesIKg+'.rp'),self.LRToes[0],self.LRToes[1],self.LRToes[2],e=1)
            BallIKg = cmds.group(AnkleIKH[0],ToesIKH[0],n='BallIK_'+LoR[i]+'_grp')
            cmds.setAttr((BallIKg+'.rp'),self.LRToes[0],self.LRToes[1],self.LRToes[2],e=1)

            self.createcurve('Foot',(LoR[i]+'_FootIK'))
            cmds.setAttr((LoR[i]+'_FootIK.rp'),LR2loc[0],LR2loc[1],LR2loc[2],e=1)
            cmds.parent(AnkleIKg,(LoR[i]+'_FootIK'))
            attribute = ['Tose','Roll','TipX','TipY','HeelY','Side']
            for attr in attribute:
                cmds.addAttr((LoR[i]+'_FootIK'),ln=attr,at='double',dv=0)
                cmds.setAttr((LoR[i]+'_FootIK.'+attr),e=1,keyable=1)
            cmds.connectAttr((LoR[i]+'_FootIK.Tose'),(ToesIKg+'.rotateX'),f=1)
            cmds.connectAttr((LoR[i]+'_FootIK.TipX'),(ToesEndIKg+'.rotateX'),f=1)
            cmds.connectAttr((LoR[i]+'_FootIK.TipY'),(ToesEndIKg+'.rotateY'),f=1)
            cmds.connectAttr((LoR[i]+'_FootIK.HeelY'),(HeelIKg+'.rotateY'),f=1)

            Node = cmds.createNode('floatMath')
            cmds.setAttr((Node+".operation"),4)
            cmds.setAttr((Node+".floatB"),0)
            cmds.connectAttr((LoR[i]+'_FootIK.Roll'),(Node+'.floatA'),f=1)
            cmds.connectAttr((Node+'.outFloat'),(HeelIKg+'.rotateX'),f=1)
            Node = cmds.createNode('floatMath')
            cmds.setAttr((Node+".operation"),5)
            cmds.setAttr((Node+".floatB"),0)
            cmds.connectAttr((LoR[i]+'_FootIK.Roll'),(Node+'.floatA'),f=1)
            cmds.connectAttr((Node+'.outFloat'),(BallIKg+'.rotateX'),f=1)
            Node = cmds.createNode('floatMath')
            cmds.setAttr((Node+".operation"),4)
            cmds.setAttr((Node+".floatB"),0)
            cmds.connectAttr((LoR[i]+'_FootIK.Side'),(Node+'.floatA'),f=1)
            cmds.connectAttr((Node+'.outFloat'),(ToesInIKg+'.rotateZ'),f=1)
            Node = cmds.createNode('floatMath')
            cmds.setAttr((Node+".operation"),5)
            cmds.setAttr((Node+".floatB"),0)
            cmds.connectAttr((LoR[i]+'_FootIK.Side'),(Node+'.floatA'),f=1)
            cmds.connectAttr((Node+'.outFloat'),(ToesOutIKg+'.rotateZ'),f=1)

            #极向量+跟随
            locnA = cmds.spaceLocator(n='poleLeg_'+LoR[i]+'_loc')
            cmds.parent(locnA[0],('HipIK_'+LoR[i]))
            self.setAttt(locnA[0],'7',0)
            Kne = cmds.getAttr('Knee_'+LoR[i]+'.tx')
            self.setAttt(locnA[0],'1',Kne)
            if i == 0:
                self.setAttt(locnA[0],'2',-5)
            elif i == 1:
                self.setAttt(locnA[0],'2',5)
            cmds.parent(locnA,w=1)
            polelocws = cmds.xform(locnA,q=1,ws=1,t=1)
            polelegcur = 'poleLeg_'+LoR[i]+'_Ctrl'
            self.createcurve(1,polelegcur)
            for s in range(0,3,1):
                self.setAttt(polelegcur+'_grp',str(s+1),polelocws[s])
            CurShapeA = cmds.listRelatives(polelegcur,children=1,s=1)
            cmds.setAttr((CurShapeA[0]+".overrideEnabled"),1)
            cmds.setAttr((CurShapeA[0]+".overrideColor"),13)
            cmds.select(cl=1)
            cmds.select(polelegcur+'.controlPoints[*]',add=1)
            cmds.scale(.3,.3,.3,r=1)
            cmds.poleVectorConstraint(polelegcur,AnkleIKH[0],weight=1)

            cmds.select(cl=1)
            Follow_joint = 'poleLeg_'+LoR[i]+'_Follow_joint'
            Follow_joint1 = 'poleLeg_'+LoR[i]+'_Follow_joint1'
            cmds.joint(p=(self.LRHip[0],self.LRHip[1],self.LRHip[2]),n=Follow_joint)
            cmds.joint(p=(self.LRAnkle[0],self.LRAnkle[1],self.LRAnkle[2]),n=Follow_joint1)
            cmds.joint(Follow_joint,e=1,zso=1,oj='xyz',sao='xup')
            poleLegik = cmds.ikHandle(sj=(Follow_joint),ee=(Follow_joint1),n='poleLeg_'+LoR[i]+'_Follow_ikHandle',sol="ikRPsolver")
            cmds.pointConstraint(AnkleIKH[0],poleLegik[0],offset=(0,0,0),weight=1)
            cmds.parent(poleLegik,BallIKg)
            cmds.pointConstraint(('HipIK_'+LoR[i]),(Follow_joint),offset=(0,0,0),weight=1)
            poleLeg_uploc = cmds.spaceLocator(n='poleLeg_'+LoR[i]+'_up_loc')
            cmds.parent(poleLeg_uploc[0],Follow_joint)
            self.setAttt(poleLeg_uploc[0],'7',0)
            cmds.pointConstraint(Follow_joint,poleLegik[0],poleLeg_uploc[0],offset=(0,0,0),weight=1)
            cmds.parent(locnA,poleLeg_uploc)
            cmds.addAttr(polelegcur,ln="Follow",at='double',min=0,max=1,dv=1)
            cmds.setAttr((polelegcur+'.Follow'),e=1,keyable=1)
            EmGA = cmds.group(em=1,n='poleLeg_'+LoR[i]+'_Follow_world')
            parentCA = cmds.parentConstraint(locnA,EmGA,('poleLeg_'+LoR[i]+'_Ctrl_grp'),mo=1,weight=1)
            reNo = cmds.createNode('reverse')
            cmds.connectAttr((polelegcur+'.Follow'),(reNo+'.inputX'),f=1)
            cmds.connectAttr((polelegcur+'.Follow'),(parentCA[0]+'.poleLeg_'+LoR[i]+'_locW0'),f=1)
            cmds.connectAttr((reNo+'.outputX'),(parentCA[0]+'.poleLeg_'+LoR[i]+'_Follow_worldW1'),f=1)
            cmds.parent(EmGA,self.WSGroup)

            poleCur = cmds.curve(d=1,p=((0,0,0),(0,0,0)),k=(0,1),n='pole_'+LoR[i]+'_Curve')
            cmds.setAttr(poleCur+'.inheritsTransform',0)
            CurShapeB = cmds.listRelatives(poleCur,children=1,s=1)
            self.LRpoleCtrl = cmds.xform('poleLeg_'+LoR[i]+'_Ctrl',q=1,ws=1,t=1) 
            poleCurlocA = cmds.spaceLocator(n='poleCur_'+LoR[i]+'_locA')
            for s in range(0,3,1):
                self.setAttt(poleCurlocA[0],str(s+1),self.LRpoleCtrl[s])
            poleCurlocB = cmds.spaceLocator(n='poleCur_'+LoR[i]+'_locB')
            for s in range(0,3,1):
                self.setAttt(poleCurlocB[0],str(s+1),self.LRKnee[s])
            cmds.connectAttr((poleCurlocA[0]+'Shape.worldPosition[0]'),(CurShapeB[0]+'.controlPoints[0]'),f=1)
            cmds.connectAttr((poleCurlocB[0]+'Shape.worldPosition[0]'),(CurShapeB[0]+'.controlPoints[1]'),f=1)
            cmds.parent(poleCurlocA[0],'poleLeg_'+LoR[i]+'_Ctrl')
            cmds.parent(poleCurlocB[0],'KneeIK_'+LoR[i])
            cmds.parent(poleCur,(LoR[i]+'_FootIK'))
            cmds.setAttr(CurShapeB[0]+".overrideEnabled",1)
            cmds.setAttr(CurShapeB[0]+".overrideDisplayType",2)

            cmds.setAttr('poleLeg_'+LoR[i]+'_up_loc.v',0)
            cmds.setAttr('poleCur_'+LoR[i]+'_locA.v',0)
            cmds.setAttr('poleCur_'+LoR[i]+'_locB.v',0)

            #IK拉伸
            cmds.addAttr((LoR[i]+'_FootIK'),ln="_____",at='enum',en="_____:",dv=0)
            cmds.setAttr((LoR[i]+'_FootIK._____'),e=1,keyable=1)
            cmds.addAttr((LoR[i]+'_FootIK'),ln='legStretch',at='double',min=0.1,max=10,dv=1)
            cmds.setAttr((LoR[i]+'_FootIK.legStretch'),e=1,keyable=1)
            cmds.addAttr((LoR[i]+'_FootIK'),ln='kneeStretch',at='double',min=0.1,max=10,dv=1)
            cmds.setAttr((LoR[i]+'_FootIK.kneeStretch'),e=1,keyable=1)
            cmds.addAttr((LoR[i]+'_FootIK'),ln='autoStretch',at='double',min=0,max=1,dv=0)
            cmds.setAttr((LoR[i]+'_FootIK.autoStretch'),e=1,keyable=1)

            cmds.curve(d=1,p=(self.LRHip,self.LRKnee),k=(0,1),n='Hip_'+LoR[i]+'_len')
            cmds.curve(d=1,p=(self.LRKnee,self.LRAnkle),k=(0,1),n='Knee_'+LoR[i]+'_len')
            cmds.createNode('curveInfo',n='Hip_'+LoR[i]+'_lenInfo')
            cmds.connectAttr(cmds.listRelatives('Hip_'+LoR[i]+'_len',s=1)[0]+'.worldSpace[0]','Hip_'+LoR[i]+'_lenInfo.inputCurve',f=1)
            cmds.createNode('curveInfo',n='Knee_'+LoR[i]+'_lenInfo')
            cmds.connectAttr(cmds.listRelatives('Knee_'+LoR[i]+'_len',s=1)[0]+'.worldSpace[0]','Knee_'+LoR[i]+'_lenInfo.inputCurve',f=1)

            cmds.setAttr(cmds.spaceLocator(n=LoR[i]+'_Leg_distanceloc')[0]+'.t',self.LRHip[0],self.LRHip[1],self.LRHip[2])
            cmds.setAttr(cmds.spaceLocator(n=LoR[i]+'_Ankle_distanceloc')[0]+'.t',self.LRAnkle[0],self.LRAnkle[1],self.LRAnkle[2])
            cmds.setAttr(cmds.spaceLocator(n=LoR[i]+'_pole_distanceloc')[0]+'.t',self.LRpoleCtrl[0],self.LRpoleCtrl[1],self.LRpoleCtrl[2])
            #cmds.setAttr(cmds.spaceLocator(n=LoR[i]+'_Ankle_distancelocT')[0]+'.t',self.LRAnkle[0],self.LRAnkle[1],self.LRAnkle[2])
            cmds.rename(cmds.listRelatives(cmds.createNode('distanceDimShape'),p=1)[0],LoR[i]+'_Leg_distance')
            cmds.connectAttr(LoR[i]+'_Leg_distancelocShape.worldPosition[0]',LoR[i]+'_Leg_distanceShape.startPoint',f=1)
            cmds.connectAttr(LoR[i]+'_Ankle_distancelocShape.worldPosition[0]',LoR[i]+'_Leg_distanceShape.endPoint',f=1)
            cmds.rename(cmds.listRelatives(cmds.createNode('distanceDimShape'),p=1)[0],LoR[i]+'_Legtopole_distance')
            cmds.connectAttr(LoR[i]+'_Leg_distancelocShape.worldPosition[0]',LoR[i]+'_Legtopole_distanceShape.startPoint',f=1)
            cmds.connectAttr(LoR[i]+'_pole_distancelocShape.worldPosition[0]',LoR[i]+'_Legtopole_distanceShape.endPoint',f=1)
            cmds.rename(cmds.listRelatives(cmds.createNode('distanceDimShape'),p=1)[0],LoR[i]+'_poletoAnkle_distance')
            cmds.connectAttr(LoR[i]+'_Ankle_distancelocShape.worldPosition[0]',LoR[i]+'_poletoAnkle_distanceShape.startPoint',f=1)
            cmds.connectAttr(LoR[i]+'_pole_distancelocShape.worldPosition[0]',LoR[i]+'_poletoAnkle_distanceShape.endPoint',f=1)
            #cmds.rename(cmds.listRelatives(cmds.createNode('distanceDimShape'),p=1)[0],LoR[i]+'_poletoAnkle_distanceT')
            #cmds.connectAttr(LoR[i]+'_Ankle_distancelocTShape.worldPosition[0]',LoR[i]+'_poletoAnkle_distanceTShape.startPoint',f=1)
            #cmds.connectAttr(LoR[i]+'_pole_distancelocShape.worldPosition[0]',LoR[i]+'_poletoAnkle_distanceTShape.endPoint',f=1)
            cmds.pointConstraint('HipIK_L',LoR[i]+'_Leg_distanceloc',offset=(0,0,0),weight=1)
            cmds.parent(LoR[i]+'_Ankle_distanceloc','BallIK_'+LoR[i]+'_grp')
            cmds.parent(LoR[i]+'_pole_distanceloc','poleLeg_'+LoR[i]+'_Ctrl')
            #cmds.parent(LoR[i]+'_Ankle_distancelocT','AnkleIK_'+LoR[i])

            Nodef1 = cmds.createNode('floatMath')
            cmds.connectAttr('Hip_'+LoR[i]+'_lenInfo.arcLength',Nodef1+'.floatA',f=1)
            cmds.connectAttr(LoR[i]+'_FootIK.legStretch',Nodef1+'.floatB',f=1)
            cmds.setAttr((Nodef1+".operation"),2)
            Nodef2 = cmds.createNode('floatMath')
            cmds.connectAttr('Knee_'+LoR[i]+'_lenInfo.arcLength',Nodef2+'.floatA',f=1)
            cmds.connectAttr(LoR[i]+'_FootIK.kneeStretch',Nodef2+'.floatB',f=1)
            cmds.setAttr((Nodef2+".operation"),2)
            Nodef3 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodef1+'.outFloat',Nodef3+'.floatA',f=1)
            cmds.connectAttr(Nodef2+'.outFloat',Nodef3+'.floatB',f=1)
            Nodef4 = cmds.createNode('floatMath')
            cmds.connectAttr(LoR[i]+'_Leg_distanceShape.distance',Nodef4+'.floatA',f=1)
            cmds.connectAttr(Nodef3+'.outFloat',Nodef4+'.floatB',f=1)
            cmds.setAttr((Nodef4+".operation"),3)
            Nodef5 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodef4+'.outFloat',Nodef5+'.floatA',f=1)
            cmds.setAttr((Nodef5+".operation"),5)
            Nodeb1 = cmds.createNode('blendColors')
            cmds.connectAttr(LoR[i]+'_FootIK.autoStretch',Nodeb1+".blender",f=1)
            cmds.setAttr(Nodeb1+".color2",1,1,1,type='double3')
            cmds.connectAttr(Nodef5+'.outFloat',Nodeb1+".color1R",f=1)
            cmds.connectAttr(Nodef5+'.outFloat',Nodeb1+".color1G",f=1)
            Nodef6 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodeb1+'.outputR',Nodef6+'.floatA',f=1)
            cmds.connectAttr(LoR[i]+'_FootIK.legStretch',Nodef6+'.floatB',f=1)
            cmds.setAttr((Nodef6+".operation"),2)
            Nodef7 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodeb1+'.outputG',Nodef7+'.floatA',f=1)
            cmds.connectAttr(LoR[i]+'_FootIK.kneeStretch',Nodef7+'.floatB',f=1)
            cmds.setAttr((Nodef7+".operation"),2)
            Nodef8 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodef6+'.outFloat',Nodef8+'.floatA',f=1)
            cmds.setAttr(Nodef8+".floatB",cmds.getAttr('KneeIK_'+LoR[i]+".tx"))
            cmds.setAttr((Nodef8+".operation"),2)
            cmds.connectAttr(Nodef8+'.outFloat','KneeIK_'+LoR[i]+".tx",f=1)
            Nodef9 = cmds.createNode('floatMath')
            cmds.connectAttr(Nodef7+'.outFloat',Nodef9+'.floatA',f=1)
            cmds.setAttr(Nodef9+".floatB",cmds.getAttr('AnkleIK_'+LoR[i]+".tx"))
            cmds.setAttr((Nodef9+".operation"),2)
            cmds.connectAttr(Nodef9+'.outFloat','AnkleIK_'+LoR[i]+".tx",f=1)

            cmds.addAttr(('poleLeg_'+LoR[i]+'_Ctrl'),ln='kneeLock',at='double',min=0,max=1,dv=0)
            cmds.setAttr(('poleLeg_'+LoR[i]+'_Ctrl.kneeLock'),e=1,keyable=1)
            Nodef11 = cmds.createNode('floatMath')
            cmds.connectAttr(LoR[i]+'_Legtopole_distanceShape.distance',Nodef11+'.floatA',f=1)
            cmds.connectAttr('Hip_'+LoR[i]+'_lenInfo.arcLength',Nodef11+'.floatB',f=1)
            cmds.setAttr((Nodef11+".operation"),3)
            Nodef12 = cmds.createNode('floatMath')
            cmds.connectAttr(LoR[i]+'_poletoAnkle_distanceShape.distance',Nodef12+'.floatA',f=1)
            cmds.connectAttr('Knee_'+LoR[i]+'_lenInfo.arcLength',Nodef12+'.floatB',f=1)
            cmds.setAttr((Nodef12+".operation"),3)
            Nodeb2 = cmds.createNode('blendColors')
            cmds.connectAttr('poleLeg_'+LoR[i]+'_Ctrl.kneeLock',Nodeb2+".blender",f=1)
            cmds.connectAttr(Nodef11+'.outFloat',Nodeb2+".color1R",f=1)
            cmds.connectAttr(Nodef12+'.outFloat',Nodeb2+".color1G",f=1)
            cmds.connectAttr(Nodef6+'.outFloat',Nodeb2+".color2R",f=1)
            cmds.connectAttr(Nodef7+'.outFloat',Nodeb2+".color2G",f=1)
            cmds.connectAttr(Nodeb2+'.outputR',Nodef8+".floatA",f=1)
            cmds.connectAttr(Nodeb2+'.outputG',Nodef9+".floatA",f=1)

            cmds.group('Hip_'+LoR[i]+'_len','Knee_'+LoR[i]+'_len',LoR[i]+'_Leg_distanceloc',
                        LoR[i]+'_Leg_distance',LoR[i]+'_Legtopole_distance',LoR[i]+'_poletoAnkle_distance',n=LoR[i]+'_Leg_len_grp')
            cmds.setAttr(LoR[i]+'_Leg_len_grp.v',0)
            cmds.setAttr(LoR[i]+'_pole_distanceloc.v',0)
            #cmds.setAttr(LoR[i]+'_Ankle_distanceloc.v',0)
            cmds.setAttr('AnkleIK_'+LoR[i]+'_grp.v',0)

            #腿空间吸附
            cmds.addAttr((LoR[i]+'_FootIK'),ln="spaceSnap",at='enum',en="World:Root:")
            cmds.setAttr((LoR[i]+'_FootIK.spaceSnap'),e=1,keyable=1)
            footPWS = cmds.group(em=1,n=LoR[i]+'_FootIK_pos_world')
            footPR = cmds.group(em=1,n=LoR[i]+'_FootIK_pos_root')
            parentCA = cmds.parentConstraint(footPWS,footPR,LoR[i]+'_FootIK_SDK',mo=1 ,weight=1)
            cmds.parent(footPWS,self.WSGroup)
            cmds.parent(footPR,self.RGroup)
            reNo = cmds.createNode('reverse')
            cmds.connectAttr(LoR[i]+'_FootIK.spaceSnap', reNo+'.inputX',f=1)
            cmds.connectAttr(LoR[i]+'_FootIK.spaceSnap', parentCA[0]+'.'+LoR[i]+'_FootIK_pos_worldW0',f=1)
            cmds.connectAttr(reNo+'.outputX', parentCA[0]+'.'+LoR[i]+'_FootIK_pos_rootW1',f=1)

IKFKWin()
