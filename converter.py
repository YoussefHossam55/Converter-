bl_info = {
    "name" : "Convertor",
    "author" : "Youssef Hossam",
    "description" : "",
    "blender" : (2, 91, 0),
    "version" : (1, 0, 0), 
    "location" : "3D < Toolbar",
    "warning" : "",
    "category" : "Mesh"
}
    
    
    
    
import bpy
from bpy.types import Operator, Panel, Menu




#let's create our first operator
class CIRCLE_OT(Operator):
    bl_label = "Convert to circle"
    bl_idname = "circle.main_ot"
    def execute (self, context):     
        bpy.ops.mesh.bevel(offset=0.128623, offset_pct=0, affect='VERTICES')
        bpy.ops.mesh.subdivide(number_cuts=5)
        bpy.ops.mesh.looptools_circle(custom_radius=False, fit='best', flatten=True, influence=100, lock_x=False, lock_y=False, lock_z=False, radius=1, regular=True)
        

        return {'FINISHED'}

#now let's create a panel for the operator
class CIRCLE_PT(Panel):
    bl_label = "Circle"
    bl_idname = "circle.main_pt"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Convertor"
    bpy.props.FloatProperty(name= "Size", default= 1)
        
      
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('circle.main_ot', text="Circle", icon="MESH_CIRCLE")
      

    #edit icon = "EDITMODE_HLT"
    
    
    
    
#After creating a main panel and operator let's create a pie menu to make everything easy :)
class PieMenu_MT(Menu):
    bl_label = "Convertor"
    bl_idname = "pie_menu.main"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("circle.main_ot", text="Circle", icon="MESH_CIRCLE")
   
        
        
        
        
        
        
        
        


addon_keymaps = []
     
    
def register():
    bpy.utils.register_class(CIRCLE_OT)
    bpy.utils.register_class(CIRCLE_PT)
    bpy.utils.register_class(PieMenu_MT)
    
    #let's create a shortcut for the pie menu
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type= 'T', value= 'PRESS', shift= True)
        kmi.properties.name = PieMenu_MT.bl_idname
        addon_keymaps.append((km, kmi))
    
    
def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(CIRCLE_OT)
    bpy.utils.unregister_class(CIRCLE_PT)
    bpy.utils.unregister_class(PieMenu_MT)
    
    
    
if __name__ == "__main__":
    register()
    
    
#bpy.ops.wm.call_menu_pie(name="PieMenu_MT")





