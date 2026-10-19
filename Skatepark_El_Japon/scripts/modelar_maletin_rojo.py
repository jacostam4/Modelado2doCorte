import bpy,bmesh,shutil,json
from pathlib import Path
from mathutils import Vector,Matrix
p=Path(bpy.data.filepath);dst=p.parent/'texturas';dst.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_maletin.blend')),copy=True)
photo=dst/'maletin_rojo_referencia.png';shutil.copy2(r'C:\Users\juan_\AppData\Local\Temp\codex-clipboard-78f9e171-cb56-42b3-bb80-324ca89e0c35.png',photo)
o=bpy.data.objects['Barrera roja observada'];old=o.data;old.use_fake_user=True
lo=[min(v.co[i] for v in old.vertices) for i in range(3)];hi=[max(v.co[i] for v in old.vertices) for i in range(3)]
center=o.matrix_world@Vector([(lo[i]+hi[i])/2 for i in range(3)])
world=[o.matrix_world@v.co for v in old.vertices]
L=max(v.y for v in world)-min(v.y for v in world);W=max(v.x for v in world)-min(v.x for v in world);H=max(v.z for v in world)-min(v.z for v in world);ground=min(v.z for v in world)
assert L>W
# Normalized front outline: top handle notch, two fork openings, broken right foot.
profile=[(0,.02),(0,.96),(.025,1),(.43,1),(.455,.92),(.535,.92),(.56,1),(.98,1),(1,.96),(1,.34),(.965,.33),(.95,.36),(.925,.33),(.91,.30),(.89,.29),(.875,.25),(.85,.23),(.86,.16),(.89,.13),(.91,.04),(.98,.04),(.98,0),(.87,0),(.84,.16),(.63,.16),(.615,0),(.365,0),(.34,.16),(.14,.16),(.12,0),(.02,0)]
verts=[]
for sign in [1,-1]:
 for u,v in profile:
  depth=W*(.5-.14*v);verts.append((center.x+sign*depth,center.y+(u-.5)*L,ground+v*H))
n=len(profile);faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
me=bpy.data.meshes.new('Maletin | muesca huecos y rotura');me.from_pydata(verts,[],faces);me.update()
uv=me.uv_layers.new(name='UV_Foto_Maletin')
for f in me.polygons:
 f.material_index=0 if f.index<2 else 1
 for li in f.loop_indices:
  u,v=profile[me.loops[li].vertex_index%n]
  # Perspective-aware projection onto the supplied photograph, excluding the wall.
  bottom=Vector((80+900*u,395-42*u));top=Vector((67+895*u,79-56*u));px=bottom.lerp(top,v)
  uv.data[li].uv=(px.x/1084,1-px.y/420)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>4]);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(me);bm.free()
img=bpy.data.images.load(str(photo),check_existing=True);img.filepath='//texturas/'+photo.name;img.pack()
mat=bpy.data.materials.new('MALETIN | rojo desgastado fotografia');mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.83
tex=nt.nodes.new('ShaderNodeTexImage');tex.image=img;tex.extension='EXTEND';tex.location=(-500,100);nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.003;nt.links.new(tex.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
edge=bpy.data.materials.new('MALETIN | plastico rojo sucio');edge.use_nodes=True;nt=edge.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.86
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=23;noise.inputs['Detail'].default_value=4
r=nt.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.3;r.color_ramp.elements[0].color=(.025,.012,.009,1);r.color_ramp.elements[1].position=.65;r.color_ramp.elements[1].color=(.25,.055,.035,1);nt.links.new(noise.outputs['Fac'],r.inputs['Fac']);nt.links.new(r.outputs['Color'],bs.inputs['Base Color'])
me.materials.append(mat);me.materials.append(edge)
o.data=me;o.matrix_world=Matrix.Identity(4)
for mod in o.modifiers:mod.show_viewport=False;mod.show_render=False
bev=o.modifiers.new('Bordes de plastico moldeado','BEVEL');bev.width=.007;bev.segments=3;bev.material=1
o['detalle']='Maletin rojo para ollie: huecos inferiores, muesca superior, rotura lateral y paneles fotografiados.'
bpy.data.libraries.write(str(dst/'Maletin_Rojo_Materiales.blend'),{mat,edge},path_remap='RELATIVE',fake_user=True)
materials=set(m for ob in bpy.context.scene.objects for m in getattr(ob.data,'materials',[]) if m)
bpy.data.libraries.write(str(dst/'Materiales_El_Japon.blend'),materials,path_remap='RELATIVE',fake_user=True)
(dst/'maletin_verificacion.json').write_text(json.dumps({'objeto':o.name,'malla_cerrada':True,'largo':L,'altura':H,'ancho':W,'foto':str(photo)},indent=2))
for ob in bpy.context.selected_objects:ob.select_set(False)
o.select_set(True);bpy.context.view_layer.objects.active=o
area=bpy.context.area
def finish():
 area.type='VIEW_3D';r=area.spaces.active.region_3d;eye=center+Vector((3,-.8,1));r.view_rotation=(center-eye).to_track_quat('-Z','Y');r.view_location=center;r.view_distance=3.2
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('MALETIN MODELADO Y TEXTURIZADO')
