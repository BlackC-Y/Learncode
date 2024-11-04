# -*- coding: UTF-8 -*-
import unreal

def ueRename01():
    #根据选择资产的文件夹名字进行重命名
    EditorUtilityLib = unreal.EditorUtilityLibrary()
    slList = EditorUtilityLib.get_selected_assets()   #获取选择的资产
    for i in slList:
        DirName = i.get_path_name().split('/')[-2]   #获取完整路径
        newName = 'T_%s_FaceActive' %(DirName.split('_', 1)[1])
        EditorUtilityLib.rename_asset(i, newName)

def ueRename02():
    EditorUtilityLib = unreal.EditorUtilityLibrary()
    slList = EditorUtilityLib.get_selected_assets()   #获取选择的资产
    for i in slList:
        newName = i.get_name().replace('T_', 'S_').rsplit('_', 1)[0]
        EditorUtilityLib.rename_asset(i, newName)

def ueRename03():
    #替换选中的名字
    EditorUtilityLib = unreal.EditorUtilityLibrary()
    slList = EditorUtilityLib.get_selected_assets()   #获取选择的资产
    for i in slList:
        newName = i.get_name().replace('_hm', '_bmx')
        EditorUtilityLib.rename_asset(i, newName)

def ueSetSelectMIParameter():
    #根据选择的材质实例，设置参数为层级内的贴图
    EditorUtilityLib = unreal.EditorUtilityLibrary()
    EditorAssetLib = unreal.EditorAssetLibrary()
    MaterialEditingLib = unreal.MaterialEditingLibrary()
    slList = EditorUtilityLib.get_selected_assets()
    for i in slList:
        DirPath = i.get_path_name().rsplit('/', 1)[0]   #获取完整路径
        DirName = i.get_path_name().split('/')[-2]
        #DirAssetList = EditorAssetLib.list_assets(DirPath, False)   #获取路径下全部资产
        chrName = 'T_%s_chr' %(DirName.split('_', 1)[1])
        faceName = 'T_%s_Face' %(DirName.split('_', 1)[1])
        faceActiveName = 'T_%s_faceActive' %(DirName.split('_', 1)[1])
        #设置材质实例属性
        MaterialEditingLib.set_material_instance_texture_parameter_value(i, 'SpriteTexture', EditorAssetLib.load_asset(f'{DirPath}/{chrName}.{chrName}'))
        MaterialEditingLib.set_material_instance_texture_parameter_value(i, 'Face', EditorAssetLib.load_asset(f'{DirPath}/{faceName}.{faceName}'))
        MaterialEditingLib.set_material_instance_texture_parameter_value(i, 'FaceActive', EditorAssetLib.load_asset(f'{DirPath}/{faceActiveName}.{faceActiveName}'))
        EditorAssetLib.save_asset(i.get_path_name(), False)

def ueSetSpriteDefaultMaterial():
    #设置资产的默认材质 为 选择路径下的材质
    EditorUtilityLib = unreal.EditorUtilityLibrary()
    EditorAssetLib = unreal.EditorAssetLibrary()
    slList = EditorUtilityLib.get_selected_assets()
    for i in slList:
        DirPath = i.get_path_name().rsplit('/', 1)[0]   #获取完整路径
        newMI = i.get_name().replace('S_', 'MI_')
        i.set_editor_property("default_material", EditorAssetLib.load_asset(f'{DirPath}/{newMI}'))

ueRename03()