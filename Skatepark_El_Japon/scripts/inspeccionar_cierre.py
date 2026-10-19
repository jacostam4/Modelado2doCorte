import bpy,json
from pathlib import Path
from mathutils import Vector
out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
rig=bpy.data.objects['Armature']
def ob(o):
 return dict(name=o.name,type=o.type,matrix=[list(r) for r in o.matrix_world],dimensions=list(o.dimensions),bounds=[list(o.matrix_world@Vector(v)) for v in o.bound_box],parent=o.parent.name if o.parent else None,action=str(o.animation_data.action) if o.animation_data else None)
data={'rig':ob(rig),'bones':[dict(name=b.name,head=list(b.head_local),tail=list(b.tail_local),matrix=[list(r) for r in b.matrix_local],parent=b.parent.name if b.parent else None) for b in rig.data.bones],'objects':[ob(o) for o in bpy.context.scene.objects if any(t in o.name for t in ('CAJON FS','Mug','Caseta','SKATE |','TABLA |','CAM '))],'markers':[(m.name,m.frame,m.camera.name if m.camera else None) for m in bpy.context.scene.timeline_markers],'fps':bpy.context.scene.render.fps,'range':[bpy.context.scene.frame_start,bpy.context.scene.frame_end]}
(out/'inspeccion_cierre.json').write_text(json.dumps(data,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_antes_cierre_avatar.blend')),copy=True)
print('INSPECCION Y RESPALDO LISTOS')
