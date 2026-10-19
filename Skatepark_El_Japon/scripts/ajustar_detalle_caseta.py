import bpy
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parents[1]
col=bpy.data.collections['07 | Entorno urbano aproximado']
bpy.context.view_layer.update()
body=bpy.data.objects['Caseta del parque'];vs=[body.matrix_world@Vector(v) for v in body.bound_box]
front=max(v.x for v in vs)+.01;y0=min(v.y for v in vs);y1=max(v.y for v in vs)
for o in list(bpy.data.objects):
 if o.name.startswith(('Caseta | proyeccion UV','Caseta | nervadura','Caseta | jardinera')):bpy.data.objects.remove(o,do_unlink=True)
me=bpy.data.meshes.new('Caseta fachada UV');me.from_pydata([(front,y0,.08),(front,y1,.08),(front,y1,3.0),(front,y0,3.0)],[],[(0,1,2,3)]);me.update()
me.materials.append(bpy.data.materials['CASETA | fachada IMG_4338']);uv=me.uv_layers.new(name='UV_Guia_003')
for lp in me.loops:
 v=me.vertices[lp.vertex_index].co;uv.data[lp.index].uv=((v.y-y0)/(y1-y0),(v.z-.08)/2.92)
o=bpy.data.objects.new('Caseta | proyeccion UV de foto',me);col.objects.link(o)
steel=bpy.data.materials['METAL | acero desgastado']
for k in range(14):
 y=y0+(y1-y0)*k/13;a=Vector((front-2.4,y,3.32));b=Vector((front+.15,y,3.32))
 bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.012,depth=(b-a).length,location=(a+b)/2)
 ob=bpy.context.object;ob.name='Caseta | nervadura de cubierta';ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();ob.data.materials.append(steel)
 for c in list(ob.users_collection):c.objects.unlink(ob)
 col.objects.link(ob)
o=bpy.data.objects['Cajon inclinado paralelo a bank'];o.data.materials.clear();o.data.materials.append(bpy.data.materials['CAJON | pintura negra gastada']);o.data.materials.append(bpy.data.materials['CONCRETO | desgaste y poros'])
for pol in o.data.polygons:pol.material_index=0
o.data.polygons[2].material_index=1
s=bpy.context.scene
s.camera=bpy.data.objects['CAM 03 | Cajones y barandas'];s.render.resolution_x=1440;s.render.resolution_y=960
s.render.filepath=str(p/'renders/fotos_y_satelite/02_modulo_izquierdo.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['CAM 04 | Planta'];s.render.resolution_x=1400;s.render.resolution_y=1250
s.render.filepath=str(p/'renders/fotos_y_satelite/04_planta.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['CAM 02 | Mural y quarters'];s.render.resolution_x=1440;s.render.resolution_y=960
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(p/'El_Japon_Planta_Corregida.blend'))
print('DETALLES AJUSTADOS')
