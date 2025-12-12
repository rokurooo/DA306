bl_info = {
    "name" : "Group Car Montage Animation",
    "blender" : (2, 80, 0), #Blender version (2.80.0)
    "category" : "Object",
}
import bpy

# Define properties first
bpy.types.Scene.xlimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0
)
bpy.types.Scene.ylimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0
)
bpy.types.Scene.zlimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0
)

bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
    name="Bool", 
    default=False
)

def xscaling(self, context):
    """Update function for slider"""
    customScale = context.scene.xlimit
    # Execute the operator with the current slider value
    bpy.ops.opr.x_scale(customScale = customScale)
    
def yscaling(self, context):
    """Update function for slider"""
    customScale = context.scene.ylimit
    # Execute the operator with the current slider value
    bpy.ops.opr.y_scale(customScale = customScale)

def zscaling(self, context):
    """Update function for slider"""
    customScale = context.scene.zlimit
    # Execute the operator with the current slider value
    bpy.ops.opr.z_scale(customScale = customScale)


# Update the property with the update function
bpy.types.Scene.xlimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0, 
    update=xscaling
)
bpy.types.Scene.ylimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0, 
    update=yscaling
)
bpy.types.Scene.zlimit = bpy.props.FloatProperty(
    name="Value", 
    default=0.5, 
    min=0.0, 
    soft_max=10.0, 
    update=zscaling
)

"""
bpy.types.Scene.my_checkbox = bpy.props.BoolProperty(
    name="Bool", 
    default=False,
    update=update_rainbow
)
"""


class Mytools_Panel(bpy.types.Panel):
    bl_label = "Car Montage"
    bl_idname = "VIEW3D_PT_Animating"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animating"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # Adding MESH section
        row = layout.row()
        row.label(text="Setup")
        row = layout.row()
        row.operator("opr.cam", text="Setup Scene")
        row.operator("opr.target", text="Add Target")
        
        # Delete section
        row = layout.row()
        row.operator("object.delete", text="Delete")
        
        # animate
        row = layout.row()
        row.operator("opr.cam_animate", text="Animate")
        
        # My Slider section
        row = layout.row()
        row.label(text="Limit adjustment")
        row = layout.row()
        row.prop(scene, "xlimit", text="X")
        row = layout.row()
        row.prop(scene, "ylimit", text="Y")
        row = layout.row()
        row.prop(scene, "zlimit", text="Z")
        

class X_Limit_Scale(bpy.types.Operator):
    bl_idname = "opr.x_scale"
    bl_label = "Scale by Slider"
    bl_options = {'REGISTER', 'UNDO'}
    customScale: bpy.props.FloatProperty( name="Value", default=0.5 ) # type: ignore
    
    def execute(self, context):
        obj = bpy.data.objects['limit']
        obj.scale.x = self.customScale
        return {'FINISHED'}

class Y_Limit_Scale(bpy.types.Operator):
    bl_idname = "opr.y_scale"
    bl_label = "Scale by Slider"
    bl_options = {'REGISTER', 'UNDO'}

    customScale: bpy.props.FloatProperty( name="Value", default=0.5 ) # type: ignore

    def execute(self, context):
        obj = bpy.data.objects['limit']
        obj.scale.y = self.customScale
        return {'FINISHED'}

class Z_Limit_Scale(bpy.types.Operator):
    bl_idname = "opr.z_scale"
    bl_label = "Scale by Slider"
    bl_options = {'REGISTER', 'UNDO'}

    customScale: bpy.props.FloatProperty( name="Value", default=0.5 ) # type: ignore

    def execute(self, context):
        obj = bpy.data.objects['limit']
        obj.scale.z = self.customScale
        return {'FINISHED'}
    


class Camera(bpy.types.Operator):
    bl_idname = "opr.cam"
    bl_label = "spawn and move camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        bpy.ops.object.empty_add( type = "PLAIN_AXES" )
        bpy.context.object.name = "target"
        bpy.ops.object.empty_add( type = "CUBE" )
        bpy.context.object.name = "limit"

        bpy.ops.object.camera_add()
        bpy.context.object.name = "custom camera"
        bpy.context.object.location = (0, 0, 0)
        camera = bpy.data.objects['custom camera']
        # adding track to constrain
        bpy.ops.object.constraint_add(type = 'TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target"]


        bpy.ops.object.light_add(type="SUN")
        bpy.context.object.name = "custom sun"
        bpy.context.object.location = (4, -10, 5)
        # adding track to constrain
        bpy.ops.object.constraint_add(type = 'TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target"]


        bpy.ops.object.light_add(type="AREA")
        bpy.context.object.name = "show light 1"
        bpy.context.object.location = (2, -5, -0.6)
        # adding track to constrain
        bpy.ops.object.constraint_add(type = 'TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target"]

        bpy.ops.object.light_add(type="AREA")
        bpy.context.object.name = "show light 2"
        bpy.context.object.location = (2, 5, -0.6)
        # adding track to constrain
        bpy.ops.object.constraint_add(type = 'TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target"]

        
        

        return {'FINISHED'}

# declaring end frame
# bpy.context.scene.frame_end = 25 

Fseconds = 24

class animate(bpy.types.Operator):
    bl_idname = "opr.cam_animate"
    bl_label = "Animate the camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        camera = bpy.data.objects['custom camera']
        target = bpy.data.objects['target']
        limit = bpy.data.objects['limit']
        sun = bpy.data.objects['custom sun']
        area_lights = [ bpy.data.objects['show light 1'].data, bpy.data.objects['show light 2'].data]



        myscene = bpy.context.scene
        x_limit = limit.scale.x
        y_limit = limit.scale.y
        z_limit = limit.scale.z


        # animation startu

        camera.location = (x_limit + 5, y_limit + 10, z_limit + 2)
        camera.keyframe_insert(data_path="location", frame = 0)
        target.location = (0, 0, 0)
        target.keyframe_insert(data_path="location", frame = 0)

        # still frame
        camera.location = (x_limit + 5, y_limit + 10, z_limit + 2)
        camera.keyframe_insert(data_path="location", frame = Fseconds*2)
        target.location = (0, 0, 0)
        target.keyframe_insert(data_path="location", frame = Fseconds*2)
        
        # slowly fly in to the car
        camera.location = (x_limit + 5, 0, z_limit + 2)
        camera.keyframe_insert(data_path="location", frame = Fseconds*5)
        target.location = (x_limit - 1, 0, 0)
        target.keyframe_insert(data_path="location", frame = Fseconds*5)

        # drone shot
        camera.location = (x_limit + 15, y_limit + 15, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*5)+1)
        target.location = (0, 0, 0)
        target.keyframe_insert(data_path="location", frame = (Fseconds*5)+1)
        
        camera.location = (x_limit + 20, 0, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*8)
        
        camera.location = (x_limit + 15, -y_limit - 15, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*10)
        
        camera.location = (0, -y_limit - 20, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*12)
        
        camera.location = (-x_limit - 15, -y_limit - 15, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*14)
        
        camera.location = (-x_limit - 20, 0, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*16)
        
        camera.location = (-x_limit - 15, y_limit + 15, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*18)
        
        camera.location = (0, y_limit + 20, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*20)

        camera.location = (x_limit + 15, y_limit + 15, z_limit + 10)
        camera.keyframe_insert(data_path="location", frame = Fseconds*22)
        target.location = (0, 0, 0)
        target.keyframe_insert(data_path="location", frame = Fseconds*22)

        # Positive side pan
        target.location = (-x_limit, 0, 0)
        camera.location = (-x_limit, y_limit + 5, 0)
        target.keyframe_insert(data_path="location", frame = (Fseconds*22)+1)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*22)+1)
        
        target.location = (x_limit, 0, 0)
        camera.location = (x_limit, y_limit + 5, 0)
        target.keyframe_insert(data_path="location", frame = (Fseconds*27))
        camera.keyframe_insert(data_path="location", frame = (Fseconds*27))

        # Front view slow move to up
        target.location = (x_limit - 5, 0, 0)
        camera.location = (x_limit + 7, 0, 2)
        target.keyframe_insert(data_path="location", frame = (Fseconds*27)+1)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*27)+1)

        camera.location = (x_limit, 0, z_limit + 3)

        camera.keyframe_insert(data_path="location", frame = (Fseconds*30))

        # Negative side pan
        target.location = (x_limit, 0, 0)
        camera.location = (x_limit, -(y_limit + 5), 0)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*30)+1)
        target.keyframe_insert(data_path="location", frame = (Fseconds*30)+1)
        
        target.location = (-x_limit, 0, 0)
        camera.location = (-x_limit, -(y_limit + 5), 0)
        target.keyframe_insert(data_path="location", frame = (Fseconds*35))
        camera.keyframe_insert(data_path="location", frame = (Fseconds*35))
        

        # Back view pan
        target.location = (-x_limit, -y_limit, z_limit-1)
        camera.location = (-(x_limit + 3), -y_limit, z_limit-2)
        target.keyframe_insert(data_path="location", frame = (Fseconds*35)+1)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*35)+1)

        camera.location = (-(x_limit + 3), 0, z_limit-2)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*37.5))

        target.location = (-x_limit, y_limit, z_limit-1)
        camera.location = (-(x_limit + 3), y_limit, z_limit-2)
        target.keyframe_insert(data_path="location", frame = (Fseconds*40))
        camera.keyframe_insert(data_path="location", frame = (Fseconds*40))


        # Slide through from the back comming out to the front
        target.location = (-x_limit, 0, 0)
        camera.location = (-(x_limit + 3), 0, 0)
        target.keyframe_insert(data_path="location", frame = (Fseconds*40)+1)
        camera.keyframe_insert(data_path="location", frame = (Fseconds*40)+1)

        target.location = (x_limit-3, 0, 0)
        camera.location = (x_limit, 0, z_limit)
        target.keyframe_insert(data_path="location", frame = (Fseconds*45))
        camera.keyframe_insert(data_path="location", frame = (Fseconds*45))

        target.location = (x_limit-3, 0, 0)
        camera.location = (x_limit+10, 0, z_limit)
        target.keyframe_insert(data_path="location", frame = (Fseconds*50))
        camera.keyframe_insert(data_path="location", frame = (Fseconds*50))

        
        # Sun Animation
        sun_data = sun.data
        sun_data.use_temperature = True
        sun.location = (4, -10, 5)
        sun_data.energy = 2
        sun_data.temperature = 3000.0
        sun.keyframe_insert(data_path="location", frame = 0)
        sun_data.keyframe_insert(data_path="energy", frame = 0)
        sun_data.keyframe_insert(data_path="temperature", frame = 0)

        sun.location = (0, 0, 5)
        sun_data.energy = 4
        sun_data.temperature = 5000.0
        sun.keyframe_insert(data_path="location", frame = Fseconds*25)
        sun_data.keyframe_insert(data_path="energy", frame = Fseconds*25)
        sun_data.keyframe_insert(data_path="temperature", frame = Fseconds*25)

        sun.location = (4, 10, 5)
        sun_data.energy = 0.5
        sun_data.temperature = 8000.0
        sun.keyframe_insert(data_path="location", frame = Fseconds*50)
        sun_data.keyframe_insert(data_path="energy", frame = Fseconds*50)
        sun_data.keyframe_insert(data_path="temperature", frame = Fseconds*50)

        end_frame = Fseconds*55
        
        # Area Lights Animation
        for i in area_lights:
            i.energy = 200
            i.shape = "RECTANGLE"
            i.size = 5
        light_colors = [( 1, 0.253, 0.253), (0.253, 0.253, 1)]

        even = 1
        start = 0
        while start < end_frame:
            if even == 1:
                area_lights[0].color = light_colors[0]
                area_lights[1].color = light_colors[1]
                even = 2
            elif even == 2:
                area_lights[0].color = light_colors[1]
                area_lights[1].color = light_colors[0]
                even = 1
            for i in area_lights:
                i.keyframe_insert(data_path="color", frame = start)
            start += Fseconds*1.5


        myscene.frame_end = end_frame

        return {'FINISHED'}


class Empty_target(bpy.types.Operator):
    bl_idname = "opr.target"
    bl_label = "spawn targets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # creating collections for empty targets that needs to be moved
        details_collections = "Target"
        collections_existed = False

        for Col in bpy.data.collections:
            if Col.name == details_collections:
                collections_existed = True
                break
        if not collections_existed:
                target_collection = bpy.data.collections.new(name="Target")
                bpy.context.scene.collection.children.link(target_collection)


        target_collection = bpy.data.collections.get("Target")
        bpy.ops.object.empty_add( type = "PLAIN_AXES" )
        bpy.context.object.name = "focus"
        obj = bpy.context.active_object
        
        target_collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
        return {'FINISHED'}


# List of all classes to register
classes = (
    Mytools_Panel,
    # Rainbow_OPS,
    X_Limit_Scale, Y_Limit_Scale, Z_Limit_Scale,
    Camera,
    Empty_target,
    animate,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # Remove properties
    del bpy.types.Scene.my_slider
    del bpy.types.Scene.my_checkbox
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()


"""
sequence:

+   vehicle move forward to camera  2secs
+   drone shot around the vehicle   4-5secs(full rotation)
+   front view                      3secs
+   side view panning both side     4-5secs(full side 10 secs)
+   back view panning close up      3secs
+   shoot through from back (back shot) 6secs

total = 30 seconds or more
"""