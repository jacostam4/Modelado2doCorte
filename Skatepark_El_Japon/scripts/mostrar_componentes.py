import bpy
from mathutils import Vector
names={'01 | RUEDA - modelo y UV','03 | TABLA STYX - 8.25 pulgadas','TRUCK 144 | Hanger reconstruido'}
def reveal(lc):
 if lc.name in names:
  lc.exclude=False;lc.hide_viewport=False;lc.collection.hide_viewport=False
 for child in lc.children:reveal(child)
reveal(bpy.context.view_layer.layer_collection)
objs=[]
for name in names:
 for o in list(bpy.data.collections[name].all_objects):
  if o is None:continue
  o.hide_viewport=False;o.hide_set(False)
  if o.type=='MESH':objs.append(o)
bpy.context.view_layer.update()
pts=[o.matrix_world@Vector(v) for o in objs for v in o.bound_box]
low=Vector(tuple(min(v[i] for v in pts) for i in range(3)));high=Vector(tuple(max(v[i] for v in pts) for i in range(3)))
center=(low+high)/2
area=bpy.context.area
def finish():
 area.type='VIEW_3D';space=area.spaces.active
 space.region_3d.view_perspective='PERSP';space.region_3d.view_location=center
 space.region_3d.view_rotation=Vector((-.8,1,-.65)).to_track_quat('-Z','Y')
 space.region_3d.view_distance=(high-low).length*1.5
 space.clip_start=.001;space.clip_end=100
 return None
bpy.app.timers.register(finish,first_interval=.7)
print('VISIBLES',len(objs),'PIEZAS',list(low),list(high))
