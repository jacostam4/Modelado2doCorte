import bpy,json
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name('El_Japon_antes_alargar_obstaculos.blend')),copy=True)
rail=bpy.data.objects['BARANDA BAJA | BS-FS boardslide'];box=bpy.data.objects['CAJON FS 50-50 | cuerpo']
def axis_center(o):
 lo=[min(v.co[i] for v in o.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in o.data.vertices) for i in range(3)]
 k=max(range(3),key=lambda i:hi[i]-lo[i]);a=o.matrix_world.to_3x3().col[k].normalized();c=o.matrix_world@Vector([(lo[i]+hi[i])/2 for i in range(3)])
 return a,c
def length(o,a):
 dots=[(o.matrix_world@v.co).dot(a) for v in o.data.vertices];return max(dots)-min(dots)
def stretch(o,a,c):
 o.data=o.data.copy();inv=o.matrix_world.inverted()
 for v in o.data.vertices:
  w=o.matrix_world@v.co;w+=a*((w-c).dot(a)*.5);v.co=inv@w
 o.data.update()
a,c=axis_center(rail);before=length(rail,a);stretch(rail,a,c);after=length(rail,a)
supports=sorted([o for o in bpy.context.scene.objects if o.name.startswith('BARANDA BAJA | soporte')],key=lambda o:o.matrix_world.translation.dot(a))
for i,o in enumerate(supports):
 target=c+a*((i/(len(supports)-1)-.5)*after*.8);m=o.matrix_world.copy();m.translation.x=target.x;m.translation.y=target.y;o.matrix_world=m
b,bc=axis_center(box);bl=length(box,b)
parts=[o for o in bpy.context.scene.objects if o.name.startswith('CAJON FS 50-50 |')]
for o in parts:stretch(o,b,bc)
bpy.context.view_layer.update()
assert abs(after/before-1.5)<.0001 and abs(length(box,b)/bl-1.5)<.0001
for o in bpy.context.selected_objects:o.select_set(False)
for o in [rail]+supports+parts:o.select_set(True)
bpy.context.view_layer.objects.active=rail
p.with_name('obstaculos_alargados_verificacion.json').write_text(json.dumps({'baranda_antes':before,'baranda_despues':after,'cajon_antes':bl,'cajon_despues':length(box,b),'soportes_recolocados':len(supports)},indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D'
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('BARANDA Y CAJON ALARGADOS 50 POR CIENTO')
