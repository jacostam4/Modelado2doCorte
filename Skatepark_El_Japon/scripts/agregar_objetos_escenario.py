import bpy,math
from pathlib import Path
from mathutils import Vector,Matrix
s=bpy.context.scene;p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_agregar_objetos.blend')),copy=True)
def bounds(obs):
 pts=[o.matrix_world@Vector(v) for o in obs if o.type=='MESH' for v in o.bound_box]
 return Vector([min(v[i] for v in pts) for i in range(3)]),Vector([max(v[i] for v in pts) for i in range(3)])
with bpy.data.libraries.load(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\tabla\STYX_Skate_Armado.blend',link=False) as (a,b):b.collections=['SKATE COMPLETO | montaje']
sk=b.collections[0];s.collection.children.link(sk);sk.name='12 | Skate junto a caseta'
bpy.context.view_layer.update();obs=list(sk.all_objects);root=next(o for o in obs if o.type=='EMPTY' and 'control general' in o.name)
cas=bpy.data.objects['Caseta del parque'];lo,hi=bounds([cas]);x=lo.x-.55;y=(lo.y+hi.y)/2
dg=bpy.context.evaluated_depsgraph_get();hit,loc,*_=s.ray_cast(dg,Vector((x,y,10)),Vector((0,0,-1)))
floor=loc.z if hit else 0
sl,sh=bounds(obs);root.location+=Vector((x-(sl.x+sh.x)/2,y-(sl.y+sh.y)/2,floor-sl.z+.002))
col=bpy.data.collections.new('13 | Mug y muneco sobre cajon');s.collection.children.link(col)
with bpy.data.libraries.load(r'C:\Users\juan_\OneDrive\Escritorio\universidad\MUÑECO DE NIEVE.blend',link=False) as (a,b):b.objects=[n for n in a.objects if n not in ('Camera','Light')]
for o in b.objects:col.objects.link(o);o.hide_viewport=False;o.hide_render=False;o.hide_set(False)
bpy.context.view_layer.update()
mug=[o for o in b.objects if o.name.startswith('Mug')];snow=[o for o in b.objects if o not in mug]
top=bpy.data.objects['CAJON FS 50-50 | tapa'];tl,th=bounds([top]);center=(tl+th)/2;axis=0 if th.x-tl.x>th.y-tl.y else 1
for group,label,height,offset in [(snow,'Muneco de nieve',.45,-.5),(mug,'Mug',.15,.35)]:
 low,high=bounds(group);scale=height/(high.z-low.z);base=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z));target=center.copy();target.z=th.z+.002;target[axis]+=offset
 T=Matrix.Translation(target)@Matrix.Scale(scale,4)@Matrix.Translation(-base)
 for o in group:o.matrix_world=T@o.matrix_world;o.name=label+' | '+o.name
bpy.context.view_layer.update()
for o in bpy.context.selected_objects:o.select_set(False)
for o in b.objects:o.select_set(True)
bpy.context.view_layer.objects.active=mug[0]
area=bpy.context.area
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;sp.shading.type='MATERIAL';r=sp.region_3d;r.view_perspective='PERSP';r.view_location=center;r.view_rotation=Vector((-4,3,-2)).to_track_quat('-Z','Y');r.view_distance=5
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('OBJETOS AGREGADOS',len(obs),len(snow),len(mug),'skate',list(root.location))
