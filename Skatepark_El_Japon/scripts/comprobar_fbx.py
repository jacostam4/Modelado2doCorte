import bpy,json,sys
from pathlib import Path
p=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
filename=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'El_Japon_Escenario.fbx'
bpy.ops.import_scene.fbx(filepath=str(p/filename))
meshes=[o for o in bpy.data.objects if o.type=='MESH']
images=[i for i in bpy.data.images if i.source=='FILE']
assert len(meshes)>300
assert all(len(o.data.uv_layers)>0 for o in meshes)
assert len(images)>=3
assert all(i.packed_file or Path(bpy.path.abspath(i.filepath)).is_file() for i in images)
a={'objetos_mesh_importados':len(meshes),'materiales':len(bpy.data.materials),'imagenes':len(images),'uv_en_todas_las_mallas':True,'texturas_accesibles':True}
(p/(Path(filename).stem+'_verificacion_fbx.json')).write_text(json.dumps(a,indent=2),encoding='utf-8')
print('FBX_VERIFICADO',json.dumps(a))
