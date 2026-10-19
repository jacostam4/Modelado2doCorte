import bpy
from mathutils import Matrix
body=bpy.data.objects['Muneco de nieve | Sphere']
head=bpy.data.objects['Muneco de nieve | Sphere.001']
if head.animation_data and head.animation_data.action:
    head.animation_data.action.use_fake_user=True
head.animation_data_clear()
head.parent=body
head.matrix_parent_inverse=Matrix.Identity(4)
head.matrix_basis=Matrix.Translation((0,0,2.817195415496826-1.0065339803695679))
bpy.context.view_layer.update()
f=bpy.context.scene.frame_current
expected=head.matrix_world.copy()
for test in (1,74,240,840):
    bpy.context.scene.frame_set(test)
    assert (head.matrix_world.translation-expected.translation).length<1e-5
bpy.context.scene.frame_set(f)
for o in bpy.context.selected_objects:o.select_set(False)
head.select_set(True)
bpy.context.view_layer.objects.active=head
area=bpy.context.area
def finish():
    area.type='VIEW_3D'
    area.spaces.active.region_3d.view_location=head.matrix_world.translation
    area.spaces.active.region_3d.view_distance=1.4
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return None
bpy.app.timers.register(finish,first_interval=1)
print('CABEZA CORREGIDA Y VERIFICADA EN 4 FOTOGRAMAS',tuple(head.matrix_world.translation))
