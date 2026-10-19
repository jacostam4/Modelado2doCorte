import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Matrix,Vector
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name('El_Japon_antes_mural_y_piramide.blend')),copy=True)
bank=bpy.data.objects['Bank del mural | plano inclinado']
points=[bank.matrix_world@Vector(v) for v in bank.bound_box]
yback=min(v.y for v in points); depth=max(v.y for v in points)-yback
height=max(v.z for v in points); halfwidth=(max(v.x for v in points)-min(v.x for v in points))/2
court=bpy.data.objects['Cancha contigua | asfalto']
boundary=min((court.matrix_world@Vector(v)).x for v in court.bound_box)
# Preserve the old bank mesh as an unlinked datablock for recovery.
bank.data.use_fake_user=True
# Half a pyramid cut through the apex: two riding faces and a vertical rear cut.
verts=[(boundary-halfwidth,yback,0),(boundary+halfwidth,yback,0),(boundary,yback+depth,0),(boundary,yback,height)]
faces=[(0,2,3),(2,1,3),(1,0,3),(0,1,2)]
me=bpy.data.meshes.new('Media piramide | dos caras y punta');me.from_pydata(verts,[],faces);me.update()
for mat in bank.data.materials:me.materials.append(mat)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(me);bm.free()
uv=me.uv_layers.new(name='UV_Media_Piramide')
for face in me.polygons:
 for li in face.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v.x/2,(v.y+v.z)/2)
bank.data=me;bank.matrix_world=Matrix.Identity(4);bank.name='Media piramide | skatepark - cancha'
bank['forma']='Dos caras inclinadas hacia skatepark y cancha; punta superior sin plataforma.'
# Same rigid rotation used to exchange the two end groups.
report=json.loads(p.with_name('intercambio_extremos_verificacion.json').read_text())
dy=report['antes_caseta'][1][0]+report['antes_quarters'][1][1]
T=Matrix.Translation((0,dy,0))@Matrix.Rotation(math.pi,4,'Z')
walls=[o for o in bpy.context.scene.objects if o.name.startswith(('Muro del mural |','Mural fotografico |','Reja mural |'))]
assert len(walls)>=3
for o in walls:o.matrix_world=T@o.matrix_world
bpy.context.view_layer.update()
for o in bpy.context.selected_objects:o.select_set(False)
bank.select_set(True);bpy.context.view_layer.objects.active=bank
p.with_name('mural_piramide_verificacion.json').write_text(json.dumps({'objetos_mural_movidos':len(walls),'piramide_vertices':verts,'malla_cerrada':True,'altura_estimada':height,'limite_cancha_x':boundary},indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;r=sp.region_3d
 target=Vector((1,-10,1));eye=target+Vector((15,19,13))
 r.view_rotation=(target-eye).to_track_quat('-Z','Y');r.view_location=target;r.view_distance=25
 sp.overlay.show_extras=False
 bpy.ops.wm.save_as_mainfile(filepath=str(p))
 return None
bpy.app.timers.register(finish,first_interval=.7)
print('MURAL Y MEDIA PIRAMIDE VERIFICADOS')
