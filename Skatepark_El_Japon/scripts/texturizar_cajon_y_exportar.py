import bpy,json,shutil
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath);dst=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas');dst.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_ladrillo.blend')),copy=True)
src=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\texturas')
for f in src.iterdir():
 if f.is_file() and not (dst/f.name).exists():shutil.copy2(f,dst/f.name)
img=bpy.data.images.load(str(dst/'cajon_ladrillo_foto.jpg'),check_existing=True)
m=bpy.data.materials.new('CAJON | ladrillo real IMG_4336');m.use_nodes=True
nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.86
tex=nt.nodes.new('ShaderNodeTexImage');tex.image=img;tex.extension='EXTEND';tex.label='Ladrillo desgastado de la foto IMG_4336';tex.location=(-450,100)
nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.006;bump.location=(-180,-150);nt.links.new(tex.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
o=bpy.data.objects['CAJON FS 50-50 | cuerpo'];o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(m)
lo=[min(v.co[i] for v in o.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in o.data.vertices) for i in range(3)]
uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UV_Ladrillo')
for f in o.data.polygons:
 f.material_index=0
 axis=1 if abs(f.normal.x)>.5 else 0
 span=(hi[axis]-lo[axis]);longspan=max(hi[0]-lo[0],hi[1]-lo[1])
 for li in f.loop_indices:
  v=o.data.vertices[o.data.loops[li].vertex_index].co
  uv.data[li].uv=((v[axis]-lo[axis])/longspan,.12+.75*(v.z-lo[2])/(hi[2]-lo[2]))
# Dark worn top, independently assigned so other concrete surfaces do not change.
top=bpy.data.objects['CAJON FS 50-50 | tapa'];tm=bpy.data.materials.new('CAJON | tapa oscura gastada');tm.use_nodes=True
nodes=tm.node_tree.nodes;links=tm.node_tree.links;bs=nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=.45;bs.inputs['Roughness'].default_value=.55
noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=45
ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.025,.028,.025,1);ramp.color_ramp.elements[1].color=(.13,.12,.09,1)
links.new(noise.outputs['Fac'],ramp.inputs['Fac']);links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
top.data=top.data.copy();top.data.materials.clear();top.data.materials.append(tm)
exported=[]
for im in bpy.data.images:
 if im.source!='FILE':continue
 name=Path(bpy.path.abspath(im.filepath)).name or im.name
 if not Path(name).suffix:name+='.png'
 out=dst/name
 if im.packed_file:
  out.write_bytes(im.packed_file.data)
 else:
  original=Path(bpy.path.abspath(im.filepath))
  if original.exists() and original.resolve()!=out.resolve():shutil.copy2(original,out)
  elif not out.exists():
   im.filepath_raw=str(out);im.save()
 im.filepath=bpy.path.relpath(str(out));exported.append(str(out))
 assert out.exists()
materials=set(mat for ob in bpy.context.scene.objects for mat in getattr(ob.data,'materials',[]) if mat)
bpy.data.libraries.write(str(dst/'Materiales_El_Japon.blend'),materials,path_remap='RELATIVE',fake_user=True)
(dst/'LEEME.txt').write_text('Imagenes de textura del escenario El Japon.\nMateriales_El_Japon.blend contiene los materiales y texturas procedurales editables (Append > Material).\nCajon: ladrillo de IMG_4336, UV en laterales, tapa oscura independiente.\n',encoding='utf-8')
(dst/'inventario.json').write_text(json.dumps({'imagenes':exported,'materiales':len(materials)},indent=2),encoding='utf-8')
for ob in bpy.context.selected_objects:ob.select_set(False)
o.select_set(True);top.select_set(True);bpy.context.view_layer.objects.active=o
area=bpy.context.area;center=o.matrix_world@Vector([(lo[i]+hi[i])/2 for i in range(3)])
def finish():
 area.type='VIEW_3D';r=area.spaces.active.region_3d;eye=center+Vector((5,-3,2.8));r.view_rotation=(center-eye).to_track_quat('-Z','Y');r.view_location=center;r.view_distance=6
 area.spaces.active.shading.type='MATERIAL'
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('TEXTURAS GUARDADAS',len(exported),'MATERIALES',len(materials))
