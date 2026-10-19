import bpy
from mathutils import Matrix,Vector
body=bpy.data.objects['Muneco de nieve | Sphere'];head=bpy.data.objects['Muneco de nieve | Sphere.001']
head.matrix_world=body.matrix_world@Matrix.Translation((0,0,2.817195415496826-1.0065339803695679))
bpy.context.view_layer.update()
area=bpy.context.area
def finish():
 area.type='VIEW_3D';r=area.spaces.active.region_3d;r.view_location=head.matrix_world.translation;r.view_distance=1.6
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);return None
bpy.app.timers.register(finish,first_interval=.7)
print('CABEZA RECOLOCADA',list(head.matrix_world.translation))
