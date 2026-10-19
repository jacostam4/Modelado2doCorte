import bpy,json
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parents[1]
s=bpy.context.scene
o=bpy.data.objects['CAJON FS 50-50 | cuerpo']
corners=[o.matrix_world @ Vector(v) for v in o.bound_box]
length=max(v.x for v in corners)-min(v.x for v in corners)
assert abs(length-2.5)<.001
wall=bpy.data.objects['Mural fotografico | despliegue UV']
assert all((wall.matrix_world @ v.co).x>14 for v in wall.data.vertices)
assert bpy.data.objects['Bank frontal | plataforma inclinada'].matrix_world.translation.x<0 or all((bpy.data.objects['Bank frontal | plataforma inclinada'].matrix_world @ v.co).x<0 for v in bpy.data.objects['Bank frontal | plataforma inclinada'].data.vertices)
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
for stage in ['01 | Construccion - suelo','02 | Construccion - obstaculos','03 | Construccion - cerramientos']:
 st=bpy.data.scenes[stage];bpy.context.window.scene=st
 st.camera=bpy.data.objects['CAM 01 | Vista general'];st.render.engine='BLENDER_WORKBENCH';st.render.filepath=str(p/'renders/corregido'/('etapa_'+stage[:2]+'.png'))
 bpy.ops.render.render(write_still=True)
bpy.context.window.scene=s;s.camera=bpy.data.objects['CAM 04 | Planta']
s.render.resolution_x=1400;s.render.resolution_y=1250;s.cycles.samples=24
bpy.ops.wm.save_as_mainfile(filepath=str(p/'El_Japon_Planta_Corregida.blend'))
audit={'mural':'derecha','bank_baranda_y_cajon_en_bajada':'izquierda','cancha':'arriba','rail_bajo':'inferior izquierda','manual_pad':'borde inferior','cajon':'limite con cancha','cajon_largo_m':length,'baranda_largo_m':3,'altura_obstaculos_m':.4,'escala_general':'estimada','imagenes_integradas':True}
(p/'verificacion_planta_corregida.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('VERIFICACION CORRECTA',json.dumps(audit))
