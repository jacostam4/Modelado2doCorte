import bpy,json
from pathlib import Path
from mathutils import Vector
p=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
names=['BARANDA BAJA | BS-FS boardslide','SKATE | control general','TABLA | montada con lija','Armature']
data=[]
for name in names:
 o=bpy.data.objects[name];data.append(dict(name=name,matrix=[list(r) for r in o.matrix_world],basis=[list(r) for r in o.matrix_basis],bounds=[list(o.matrix_world@Vector(v)) for v in o.bound_box],children=[c.name for c in o.children]))
(p/'inspeccion_truco.json').write_text(json.dumps(data,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_antes_nollie.blend')),copy=True)
print('RESPALDO E INSPECCION TRUCO LISTOS')
