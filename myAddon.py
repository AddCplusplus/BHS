bl_info = {
    "name": "Helper Scripts",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy

# Функция удаления всех материалов с выделенных мешей
def remove_materials(self, context):
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if not selected_objects:
        self.report({'WARNING'}, "Нет выделенных мешей!")
    else:
        for obj in selected_objects:
            obj.data.materials.clear()
            print(f"Materials removed from: {obj.name}")
        self.report({'INFO'}, "All materials removed.")

# Функция удаления всех UV-каналов с выделенных мешей
def remove_uv(self, context):
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not selected_objects:
        self.report({'WARNING'}, "Нет выделенных мешей!")
    else:
        for obj in selected_objects:
            uv_layers = obj.data.uv_layers
            while uv_layers:
                uv_layers.remove(uv_layers[0])
            print(f"All UV layers removed from: {obj.name}")
        self.report({'INFO'}, "All UV layers removed.")

# Функция создания нового UV-канала для лайтмапов
def create_lightmap_uv(self, context):
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if not selected_objects:
        self.report({'WARNING'}, "Нет выделенных мешей!")
    else:
        for obj in selected_objects:
            uv_layers = obj.data.uv_layers
            if "UVLightMap_1" not in uv_layers:
                uv_layers.new(name="UVLightMap_1")
                print(f"Создан UVLightMap_1 для {obj.name}")
            else:
                print(f"{obj.name} уже имеет UVLightMap_1, пропускаем")
        self.report({'INFO'}, "New Lightmap UV created.")

# Функция переключения UV-каналов
def switch_uvs(self, context):
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH' and len(obj.data.uv_layers) >= 2:
            mesh = obj.data
            uv1 = mesh.uv_layers[0]
            uv2 = mesh.uv_layers[1]
            uv1_data = [d.uv.copy() for d in uv1.data]
            uv2_data = [d.uv.copy() for d in uv2.data]
            for i in range(len(uv1.data)):
                uv1.data[i].uv = uv2_data[i]
                uv2.data[i].uv = uv1_data[i]
            print(f"UV-каналы у {obj.name} переключены")

# Функция Smart UVs+
def smart_uvs_plus(self, context):
    selected_objects = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in selected_objects:
        if obj.type == 'MESH':  
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj  
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='SELECT')  
            bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.0)  
            bpy.ops.object.mode_set(mode='OBJECT')  
            obj.select_set(False)
    for obj in selected_objects:
        obj.select_set(True)

# Оператор удаления материалов
class SH_OT_RemoveMaterials(bpy.types.Operator):
    bl_idname = "sh.remove_materials"
    bl_label = "Remove Materials"

    def execute(self, context):
        remove_materials(self, context)
        return {'FINISHED'}

# Оператор удаления UV-каналов
class SH_OT_RemoveUV(bpy.types.Operator):
    bl_idname = "sh.remove_uv"
    bl_label = "Remove UV"

    def execute(self, context):
        remove_uv(self, context)
        return {'FINISHED'}

# Оператор создания нового UV-канала для лайтмапов
class SH_OT_CreateLightmapUV(bpy.types.Operator):
    bl_idname = "sh.create_lightmap_uv"
    bl_label = "New Lightmap UV"

    def execute(self, context):
        create_lightmap_uv(self, context)
        return {'FINISHED'}

# Оператор переключения UV-каналов
class SH_OT_SwitchUVs(bpy.types.Operator):
    bl_idname = "sh.switch_uvs"
    bl_label = "Switch 2 UVs"

    def execute(self, context):
        switch_uvs(self, context)
        return {'FINISHED'}

# Оператор Smart UVs+
class SH_OT_SmartUVsPlus(bpy.types.Operator):
    bl_idname = "sh.smart_uvs_plus"
    bl_label = "Smart UVs+"

    def execute(self, context):
        smart_uvs_plus(self, context)
        return {'FINISHED'}

# Добавление кнопки в панель
class SH_PT_Panel(bpy.types.Panel):
    bl_label = "Scripts Helper"
    bl_idname = "SH_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SH"

    def draw(self, context):
        layout = self.layout
        layout.operator("sh.remove_materials", text="Remove Materials", icon='TRASH')
        layout.operator("sh.remove_uv", text="Remove UV", icon='UV')
        layout.operator("sh.create_lightmap_uv", text="New Lightmap UV", icon='UV')
        layout.operator("sh.switch_uvs", text="Switch 2 UVs", icon='UV')
        layout.operator("sh.smart_uvs_plus", text="Smart UVs+", icon='UV')

# Регистрация классов
def register():
    bpy.utils.register_class(SH_OT_RemoveMaterials)
    bpy.utils.register_class(SH_OT_RemoveUV)
    bpy.utils.register_class(SH_OT_CreateLightmapUV)
    bpy.utils.register_class(SH_OT_SwitchUVs)
    bpy.utils.register_class(SH_OT_SmartUVsPlus)
    bpy.utils.register_class(SH_PT_Panel)

# Удаление классов при отключении аддона
def unregister():
    bpy.utils.unregister_class(SH_OT_RemoveMaterials)
    bpy.utils.unregister_class(SH_OT_RemoveUV)
    bpy.utils.unregister_class(SH_OT_CreateLightmapUV)
    bpy.utils.unregister_class(SH_OT_SwitchUVs)
    bpy.utils.unregister_class(SH_OT_SmartUVsPlus)
    bpy.utils.unregister_class(SH_PT_Panel)

if __name__ == "__main__":
    register()
