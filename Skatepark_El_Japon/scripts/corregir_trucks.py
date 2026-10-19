import bpy,math
from pathlib import Path
from mathutils import Matrix,Vector
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_giro_trucks.blend')),copy=True)
root=bpy.data.objects['SKATE | control general'];R=root.matrix_world;Ri=R.inverted();changed=[]
for o in list(bpy.data.collections['SKATE COMPLETO | montaje'].objects):
 if not o.name.startswith(('Truck delantero |','Truck trasero |','RUEDA ','Rodamiento ','Separador rueda ')):continue
 center=sum((Ri@o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
 sign=1 if center.y>0 else -1
 pivot=Vector((0,sign*.2079625,.08))
 transform=R@Matrix.Translation(pivot)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-pivot)@Ri
 o.matrix_world=transform@o.matrix_world;changed.append(o.name)
bpy.context.view_layer.update()
area=bpy.context.area
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;r=sp.region_3d;r.view_perspective='ORTHO';r.view_location=R@Vector((0,0,.06));r.view_rotation=Vector((0,0,1)).to_track_quat('-Z','Y');r.view_distance=1.15
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('TRUCKS CORREGIDOS',len(changed))
