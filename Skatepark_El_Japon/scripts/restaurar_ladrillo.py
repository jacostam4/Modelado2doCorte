import bpy
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath);o=bpy.data.objects['CAJON FS 50-50 | cuerpo']
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_restaurar_ladrillo.blend')),copy=True)
src=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas\cajon_ladrillo_foto.jpg')
im=bpy.data.images.load(str(src),check_existing=False);im.name='Cajon ladrillo | foto empacada';im.pack();im.filepath=bpy.path.relpath(str(src))
count=0
for m in o.data.materials:
 if m and m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE':n.image=im;count+=1
assert count>0,'No se encontro nodo de imagen del cajon'
area=bpy.context.area
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;sp.shading.type='MATERIAL';r=sp.region_3d
 center=o.matrix_world@sum((Vector(v) for v in o.bound_box),Vector())/8
 r.view_location=center;r.view_rotation=Vector((-5,3,-2.8)).to_track_quat('-Z','Y');r.view_distance=6;r.view_perspective='PERSP'
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('LADRILLO RESTAURADO Y EMPACADO',count)
