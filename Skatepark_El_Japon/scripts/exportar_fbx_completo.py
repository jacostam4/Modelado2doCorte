import bpy
from pathlib import Path
p=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='DESELECT')
deps=bpy.context.evaluated_depsgraph_get()
restore=[];temporary=[]
for c in bpy.context.scene.collection.children:
 if c.name.startswith(('01 |','02 |','03 |','04 |','05 |','06 |','07 |')):
  for o in list(c.objects):
   if o.type=='MESH':
    restore.append((o,o.data));o.data=o.data.copy();o.select_set(True)
   elif o.type=='CURVE':
    m=bpy.data.meshes.new_from_object(o.evaluated_get(deps),depsgraph=deps)
    if not m.uv_layers:
     uv=m.uv_layers.new(name='UV_Guia_003')
     for lp in m.loops:
      v=m.vertices[lp.vertex_index].co;uv.data[lp.index].uv=(v.x,v.y)
    ob=bpy.data.objects.new(o.name+' | FBX',m);c.objects.link(ob);ob.matrix_world=o.matrix_world;ob.select_set(True);temporary.append(ob)
bpy.ops.export_scene.fbx(filepath=str(p/(Path(bpy.data.filepath).stem+'.fbx')),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True)
for o,original in restore:
 m=o.data;o.data=original;bpy.data.meshes.remove(m)
for o in temporary:
 m=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(m)
print('EXPORTACION COMPLETA VERIFICABLE')
