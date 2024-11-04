# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om, OpenMayaAnim as omAni

from BbBBToolBox.deps import apiundo


# -----------------------------------------------------------------------------------
# define mel procedures for the scripted brush
# -----------------------------------------------------------------------------------
def initPaint():
  cmd = '''
    global string $tf_skinSmoothPatin_selection[];

    global proc tf_smoothBrush( string $context )
    {
      artUserPaintCtx -e -ic "tf_init_smoothBrush" -svc "tf_set_smoothBrushValue"
      -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }

    global proc tf_init_smoothBrush( string $name )
    {
        global string $tf_skinSmoothPatin_selection[];
        
        $tf_skinSmoothPatin_selection = {};
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        $objName = $obj[0];
        
        int $i = 0;
        for($vtx in $sel)
        {
            string $buffer[];
            int $number = `tokenize $vtx ".[]" $buffer`;
            $tf_skinSmoothPatin_selection[$i] = $buffer[2];
            $i++;
            if ($number != 0)
                $objName = $buffer[0];
        }
        
        python("paint = SmoothNapi.smoothPaintClass()"); 
    }

    global proc tf_set_smoothBrushValue( int $slot, int $index, float $val )        
    {
        global string $tf_skinSmoothPatin_selection[];

            if($tf_skinSmoothPatin_selection[0] != "")
            {
                if( stringArrayContains($index, $tf_skinSmoothPatin_selection) )
                    python("paint.setWeight("+$index+","+$val+")"); 
            }
            else
                python("paint.setWeight("+$index+","+$val+")");        
    }
  '''
  mel.eval(cmd)

# -----------------------------------------------------------------------------------
# execute the scripted brush tool and setup the tf_smoothBrush command
# -----------------------------------------------------------------------------------
def paint():
    cmd = '''
        ScriptPaintTool;
        artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;
    '''
    mel.eval(cmd)

# -----------------------------------------------------------------------------------
# execute the mel procedures for the scripted brush
# -----------------------------------------------------------------------------------
initPaint()

# -----------------------------------------------------------------------------------
# class for holding initializing skincluster relevant stuff
# -----------------------------------------------------------------------------------
class smoothPaintClass():
  
  def __init__(self):
    # select the skinned geo
    selection = om.MGlobal.getActiveSelectionList()

    # get dag path for selection
    #dagPath = selection.getDagPath(0)
    MDagPath = selection.getDagPath(0)  # 存储所选物体的路径
    #MObject = selection.getDependNode(0)  # 存储所选物体的组件的列表
    self.obj = MDagPath
    MDagPath.extendToShape()
    
    # currentNode is MObject to your mesh
    #currentNode = MDagPath.node()
    self.mitVtx = om.MItMeshVertex(MDagPath)
    
    # get skincluster from shape
    
    skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
    if skCluster:
        selection.add(skCluster)
        skinObj = selection.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        self.skinCluster = skinNode
    else:
        om.MGlobal.displayError("No SkinCluster to paint on")
    """
    try:
        itDG = om.MItDependencyGraph(currentNode, om.MFn.kSkinClusterFilter, om.MItDependencyGraph.kUpstream)
        while not itDG.isDone():
            oCurrentItem = itDG.currentItem()
            fnSkin = oma.MFnSkinCluster(oCurrentItem)
            self.skinCluster = fnSkin
            break
    except:
        om.MGlobal.displayError("No SkinCluster to paint on")
    """
    
  # -----------------------------------------------------------------------------------
  # function to read, average, and set all influence weights on the vertex
  # vtx     (int)     current vertex index
  # value   (float)   weight value from the artisan brush
  # -----------------------------------------------------------------------------------
  def setWeight(self, vtx, value):    
    dagPath = self.obj
    fnSkin = self.skinCluster
    mitVtx = self.mitVtx

    if not fnSkin:      # error out when there is no skinCluster defined
        om.MGlobal.displayError("No SkinCluster to paint on")
    else:
        component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
        om.MFnSingleIndexedComponent(component).addElement(vtx)   #生成组件Object

        #oldWeights = om.MDoubleArray()
        surrWeights = om.MDoubleArray()
        #infCount = om.MScriptUtil()
        #int = infCount.asUintPtr()
        #surrVtxArray = om.MIntArray()
        newWeights = om.MDoubleArray()
        infIndices = om.MIntArray()
        #prevVtxUtil = om.MScriptUtil( )
        #prevVtx = prevVtxUtil.asIntPtr()

        influence = 0
        #surrVtxArray = []
          
        # create mesh iterator and get conneted vertices for averaging
        mitVtx = om.MItMeshVertex (dagPath, component)
        surrVtxArray = mitVtx.getConnectedVertices()   #获取相连接的点
        surrVtxCount = len(surrVtxArray)
                
        surrComponents = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
        om.MFnSingleIndexedComponent(surrComponents).addElements( surrVtxArray )   #生成组件Object
        
        # read weight from single vertex (oldWeights) and from the surrounding vertices (surrWeights)
        oldWeights = fnSkin.getWeights(dagPath, component)
        influence = oldWeights[1]
        oldWeights = oldWeights[0]
        surrWeights = fnSkin.getWeights(dagPath, surrComponents)[0]
        
        # average all the surrounding vertex weights and multiply and blend it over the origWeight with the weight from the artisan brush
        for i in range(influence):
          infIndices.append(i)
          newWeights.append(0.0)
          for j in range(i, len(surrWeights), influence):
            newWeights[i] += (((surrWeights[j] / surrVtxCount) * value) + ((oldWeights[i] / surrVtxCount) * (1-value)))

        # set the final weights throught the skinCluster again
        aaaa = fnSkin.setWeights(dagPath, component, infIndices, newWeights, True, True)   #, oldWeights
        apiundo.commit(undo=lambda: fnSkin.setWeights(dagPath, component, infIndices, aaaa, True))

