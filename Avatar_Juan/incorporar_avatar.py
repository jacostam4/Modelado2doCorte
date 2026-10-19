import bpy,math
from mathutils import Vector
src=r'C:\Users\juan_\OneDrive\Escritorio\2do corte\Avatar\Juan_Avatar_Inicial.blend'
assert not bpy.data.objects.get('JUAN | control y esqueleto'),'Avatar ya presente'
# Determine the supporting floor before importing the avatar.
caseta=bpy.data.objects.get('Caseta del parque')
xy=(0,11.0)
if caseta:
 pts=[caseta.matrix_world@Vector(v) for v in caseta.bound_box]
 xy=(min(p.x for p in pts)-.75,min(p.y for p in pts)-.8)
hit,loc,*rest=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((*xy,8)),Vector((0,0,-1)))
z=loc.z if hit else 0
with bpy.data.libraries.load(src,link=False) as (a,b):b.collections=['JUAN | Avatar 1.80 m']
collection=b.collections[0];bpy.context.scene.collection.children.link(collection)
collection.name='14 | Juan avatar inicial'
rig=next(o for o in collection.objects if o.type=='ARMATURE');rig.location=(*xy,z)
bpy.context.view_layer.update()
for im in bpy.data.images:
 if im.name.startswith('IMG_4551'):
  im.filepath=r'C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas\Juan_referencia_frontal.jpg'
  if not im.packed_file:im.pack()
for o in bpy.context.selected_objects:o.select_set(False)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
area=bpy.context.area
def finish():
 area.type='VIEW_3D'
 r=area.spaces.active.region_3d;r.view_location=Vector((*xy,z+.95));r.view_distance=3.5
 r.view_rotation=(Vector((2,-5,1))).to_track_quat('Z','Y')
 area.spaces.active.shading.type='MATERIAL'
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
 return None
bpy.app.timers.register(finish,first_interval=1)
print('AVATAR INCORPORADO',tuple(rig.location),len(collection.objects))
