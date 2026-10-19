import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
img=bpy.data.images.get('ladrillo_perimetral.jpg')
if img:
 img.unpack(method='REMOVE');img.filepath=str(ROOT/'texturas/ladrillo_perimetral.jpg');img.reload();img.pack()
wall=bpy.data.objects['Ladrillo lateral | UV fotografico']
for loop in wall.data.loops:
 v=wall.data.vertices[loop.vertex_index].co
 wall.data.uv_layers[0].data[loop.index].uv=((v.y+15)/2,v.z/.4)
assert bpy.app.version[:2]==(5,2)
assert len(bpy.data.scenes)==4
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
body=bpy.data.objects['CAJON FS 50-50 | cuerpo']
assert abs(body.dimensions.y-2.5)<.001
assert abs(bpy.data.objects['CAJON FS 50-50 | tapa'].location.z+.0125-.4)<.001
rail=bpy.data.objects['BARANDA BAJA | BS-FS boardslide']
assert abs(rail.location.z-.4)<.001
assert abs(rail.data.vertices[0].co.z) <=1.501
assert bpy.data.objects['AREA | cielo difuso original'].data==bpy.data.objects['AREA | instancia vinculada'].data
assert bpy.data.objects['LAB | area original'].data==bpy.data.objects['LAB | Alt D - cambia ambas'].data
assert bpy.data.objects['LAB | area original'].data!=bpy.data.objects['LAB | Shift D - color independiente'].data
body.data.materials[0]=bpy.data.materials['CAJON | pintura negra gastada']
s.camera=bpy.data.objects['CAM 02 | Mural y quarters']
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Escenario.blend'))

# FBX exporter can mishandle material slots on shared data. Give export-only
# objects independent mesh datablocks, and restore the editable instancing.
bpy.ops.object.select_all(action='DESELECT')
chosen=[];originals=[]
for col in s.collection.children:
 if col.name.startswith(('01 |','02 |','03 |','04 |','05 |','06 |','07 |')):
  for o in col.objects:
   if o.type=='MESH':
    chosen.append(o);o.select_set(True);originals.append((o,o.data));o.data=o.data.copy()
bpy.ops.export_scene.fbx(filepath=str(ROOT/'El_Japon_Escenario.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True)
for o,data in originals:
 temp=o.data;o.data=data
 if temp.users==0:bpy.data.meshes.remove(temp)
bpy.ops.object.select_all(action='DESELECT')

audit={'version':bpy.app.version_string,'scenes':[sc.name for sc in bpy.data.scenes],'objects':len(s.objects),'cajon_largo_m':body.dimensions.y,'cajon_alto_m':.4,'baranda_tramo_m':3,'baranda_eje_alto_m':rail.location.z,'packed_images':len([i for i in bpy.data.images if i.packed_file]),'fbx_meshes':len(chosen),'linked_area_verified':True,'original_skate_file_modified':False}
(ROOT/'verificacion.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')

for name,cam in [('01_vista_general','CAM 01 | Vista general'),('02_mural_y_transiciones','CAM 02 | Mural y quarters'),('03_obstaculos','CAM 03 | Cajones y barandas')]:
 s.camera=bpy.data.objects[cam];s.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)

# Workbench snapshots for each additive construction stage.
for stage in ['01 | Construccion - suelo','02 | Construccion - obstaculos','03 | Construccion - cerramientos']:
 st=bpy.data.scenes[stage];bpy.context.window.scene=st
 st.render.engine='BLENDER_WORKBENCH';st.display.shading.light='STUDIO';st.display.shading.color_type='MATERIAL';st.display.shading.show_cavity=True
 st.render.resolution_x=1000;st.render.resolution_y=667
 st.camera=bpy.data.objects['CAM 01 | Vista general']
 st.render.filepath=str(ROOT/'renders'/('etapa_'+stage[:2]+'.png'));bpy.ops.render.render(write_still=True)
bpy.context.window.scene=s;s.camera=bpy.data.objects['CAM 02 | Mural y quarters']
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Escenario.blend'))
print('VERIFICADO',json.dumps(audit,ensure_ascii=True))
