bl_info = {
    "name" : "Convertor",
    "author" : "Youssef Hossam",
    "description" : "",
    "blender" : (2, 91, 0),
    "version" : (1, 0, 2),
    "location" : "3D < Toolbar",
    "warning" : "",
    "category" : "Mesh"
}




import bpy
from bpy.types import (Operator, Panel, Menu, PropertyGroup)
from bpy.props import (BoolProperty, StringProperty, FloatProperty, EnumProperty, PointerProperty, IntProperty)  
import os

#let's create our first operator
class CIRCLE_OT(Operator):
    bl_label = "Convert to circle"
    bl_idname = "circle.main_ot"
    bevel : IntProperty(
        name="Divisions"
    )
    offset : IntProperty(
        name="Scale"
    )
    delete : BoolProperty(
        name="Delete added faces",
        description="A bool property",
        default = False
        )
    
    def execute (self, context):
        obj = context.object
        bpy.ops.mesh.bevel(offset=self.offset, offset_pct=0, segments=self.bevel, affect='VERTICES')
        bpy.ops.mesh.looptools_circle(custom_radius=False, fit='best', flatten=True, influence=100, lock_x=False, lock_y=False, lock_z=False, radius=1, regular=True)
        self.report({'INFO'}, "Turned to Circle")
        if (self.delete == True):
            bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}
    def invoke (self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)




#now let's create a panel for the operator
class CIRCLE_PT(Panel):
    bl_label = "Mesh tools"
    bl_idname = "circle.main_pt"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Convertor"
    def draw(self, context):
        Scene = context.scene
        my_tool = Scene.my_tool
        layout = self.layout
        row = layout.row()
        pcoll = preview_collections["main"]
        my_icon = pcoll["my_icon"]
        row.operator("circle.main_ot", text="Circle", icon_value=my_icon.icon_id)
        row = layout.row()
      
preview_collections = {}


class TEXT_PT(Panel):
    bl_label = "Text tools"
    bl_idname = "text.main_pt"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Convertor"
    def draw(self, context):
        Scene = context.scene
        my_tool = Scene.my_tool
        layout = self.layout
        row = layout.row()
        pcoll = preview_collections["main"]
        row.operator("clean.main_ot", text="Clean Text Topology")


class TEXT_OT(Operator):
    bl_label = "Enter a value upto 0.9"
    bl_idname = "clean.main_ot"
    topology : FloatProperty(
        name="Scale"
    )
    destructive : BoolProperty(
        name="Destructive workflow",
        description="A bool property",
        default = False
        )
    def execute(self, context):
        self.report({'INFO'}, "Cleaned Toplogy")
        bpy.ops.object.modifier_add(type='REMESH')
        bpy.context.object.modifiers["Remesh"].mode = 'SHARP'
        bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
        bpy.context.object.modifiers["Remesh"].octree_depth = 8
        bpy.context.object.modifiers["Remesh"].scale = self.topology
        if (self.destructive == True):
            bpy.ops.object.modifier_apply(modifier="Remesh", report=True)
        else:
            bpy.context.object.modifiers["Remesh"].name = "Convertor's Text Clean"
        return {'FINISHED'}
    def invoke (self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


#After creating a main panel and operator let's create a pie menu to make everything easy :)
class PieMenu_MT(Menu):
    bl_label = "Convertor"
    bl_idname = "pie_menu.main"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("circle.main_ot", text="Circle", icon="MESH_CIRCLE")
        pie.operator("clean.main_ot", text="Clean Text Topology")


addon_keymaps = []
classes = [CIRCLE_OT, CIRCLE_PT, PieMenu_MT, TEXT_OT, TEXT_PT]


def register():
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "ICONS")
    pcoll.load("my_icon", os.path.join(my_icons_dir, "icon.png"), 'IMAGE')
    preview_collections["main"] = pcoll
    for cls in classes:
        bpy.utils.register_class(cls)
    #let's create a shortcut for the pie menu
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type= 'T', value= 'PRESS', shift= True)
        kmi2 = km.keymap_items.new("circle.main_ot", type= 'F1', value= 'PRESS')
        kmi.properties.name = PieMenu_MT.bl_idname
        addon_keymaps.append((km, kmi, kmi2))
    bpy.types.Scene.my_tool = BoolProperty(name="delete")


def unregister():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()


#bpy.ops.wm.call_menu_pie(name="PieMenu_MT")
