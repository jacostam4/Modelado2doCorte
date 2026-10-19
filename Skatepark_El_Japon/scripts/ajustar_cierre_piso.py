import bpy
from mathutils import Vector
s=bpy.context.scene;c=bpy.data.objects['CAM FINAL | Kickflip y piso']
for f in range(1650,1801):
 s.frame_set(f);t=max(0,min(1,(f-1650)/120));u=t*t*(3-2*t)
 c.location+=Vector((1.8*u,-1.5*u,0))
 c.keyframe_insert(data_path='location',frame=f)
s.frame_set(1562)
a=bpy.context.area
def done():
 a.type='VIEW_3D';a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.app.timers.register(done,first_interval=1)
