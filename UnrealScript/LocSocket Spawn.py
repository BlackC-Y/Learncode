# -*- coding: utf-8 -*-
import os
import unreal

level_lib = unreal.EditorLevelLibrary()
util_lib = unreal.EditorUtilityLibrary()

Socket_Path = "/Game/Data/Temp/Socket_Loc"
def main():
    for asset in util_lib.get_selected_assets():
        name = asset.get_name()
        if not isinstance(asset,unreal.StaticMesh):
            continue

        container_path = os.path.splitext(asset.get_path_name())[0]
        container = unreal.load_asset(Socket_Path)
        if not container:
            print(f"失败路径 -> {container_path}")
            return
        container = level_lib.spawn_actor_from_object(container,unreal.Vector(0.0, 0.0, 0.0))
        r = unreal.AttachmentRule.SNAP_TO_TARGET
        for socket in container.root_component.get_all_socket_names():
            mesh = level_lib.spawn_actor_from_object(asset,unreal.Vector(0.0, 0.0, 0.0))
            mesh.attach_to_actor(container,socket,r,r,r,False)

if __name__ == "__main__":
    main()
