import bpy
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath);dst=p.parent/'texturas';dst.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_cajon_negro.blend')),copy=True)
o=bpy.data.objects['Cajon inclinado paralelo a bank'];o.data=o.data.copy()
def worn(name,colors,rough,metal):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;b=n.get('Principled BSDF');b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal
 coord=n.new('ShaderNodeTexCoord');coord.location=(-750,0)
 noise=n.new('ShaderNodeTexNoise');noise.location=(-550,70);noise.inputs['Scale'].default_value=19;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.8;l.new(coord.outputs['Object'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.location=(-300,130);r=ramp.color_ramp;r.elements.remove(r.elements[1]);r.elements[0].position=colors[0][0];r.elements[0].color=(*colors[0][1],1)
 for pos,col in colors[1:]:r.elements.new(pos).color=(*col,1)
 l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],b.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.location=(-100,-150);bump.inputs['Strength'].default_value=.23;bump.inputs['Distance'].default_value=.004;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],b.inputs['Normal']);return m
black=worn('CAJON INCLINADO | negro desconchado',[(.25,(.009,.012,.014)),(.60,(.023,.028,.033)),(.68,(.035,.038,.04)),(.705,(.32,.30,.26)),(.82,(.48,.45,.38))],.87,.05)
top=worn('CAJON INCLINADO | tapa gris rozada',[(.25,(.07,.075,.08)),(.5,(.20,.21,.20)),(.66,(.37,.36,.32)),(.8,(.5,.48,.42))],.62,.25)
o.data.materials.clear();o.data.materials.append(black);o.data.materials.append(top)
normal_matrix=o.matrix_world.to_3x3().inverted().transposed()
for f in o.data.polygons:f.material_index=1 if (normal_matrix@f.normal).normalized().z>.5 else 0
assert any(f.material_index==1 for f in o.data.polygons)
bpy.data.libraries.write(str(dst/'Cajon_Inclinado_Negro.blend'),{black,top},path_remap='RELATIVE',fake_user=True)
materials=set(mat for ob in bpy.context.scene.objects for mat in getattr(ob.data,'materials',[]) if mat)
bpy.data.libraries.write(str(dst/'Materiales_El_Japon.blend'),materials,path_remap='RELATIVE',fake_user=True)
for ob in bpy.context.selected_objects:ob.select_set(False)
o.select_set(True);bpy.context.view_layer.objects.active=o
center=sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
area=bpy.context.area
def finish():
 area.type='VIEW_3D';r=area.spaces.active.region_3d;eye=center+Vector((5,-3,2.5));r.view_rotation=(center-eye).to_track_quat('-Z','Y');r.view_location=center;r.view_distance=6
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('CAJON NEGRO TEXTURIZADO Y MATERIALES EXPORTADOS')
