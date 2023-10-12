import bpy
import math
import time


def deco_time_exec(function):
    def fonction_modifier(*args, **kwargs):
        start_time = time.time()
        function(*args, **kwargs)
        stop_time = time.time()
        total_time = stop_time - start_time
        print("la fonction {} s'est executer en : {} s".format(function, total_time))
    return fonction_modifier


@deco_time_exec
def setup_tournette():
    mesh_data_to_render = clean_and_rename_scene()
        
    if not mesh_data_to_render:
        mesh_data_to_render = bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    custom_camera = create_new_camera()
    
    create_world_center_pivot()
    data_empty_object = bpy.data.objects['Empty']
    
    data_empty_object.select_set(True)
    bpy.data.objects['Camera'].select_set(True)
    
    bpy.ops.object.parent_set(type='OBJECT')

    bpy.context.scene.camera = custom_camera
    bpy.ops.view3d.camera_to_view_selected()
    custom_camera.rotation_euler = (1.40, 0, 0)
    
    animate_tournette(data_empty_object)

def create_world_center_pivot():
    bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

def create_new_camera():
    bpy.ops.object.camera_add(location=(0, -10, 2))
    custom_camera = bpy.context.object
    return custom_camera

def animate_tournette(data_obj, start_frame=0, end_frame=100):
    data_obj.rotation_euler = (0, 0, 0)
    data_obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    data_obj.rotation_euler = (0, 0, 2 * math.pi)
    data_obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)

def clean_and_rename_scene():
    object_to_render = ""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and not object_to_render:
            obj.name = "mesh_to_render_" + obj.name
            object_to_render = bpy.data.objects[obj.name]
            object_to_render.location = (0, 0, 0)
        if obj.type == 'CAMERA':
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.delete()
    return object_to_render

setup_tournette()
