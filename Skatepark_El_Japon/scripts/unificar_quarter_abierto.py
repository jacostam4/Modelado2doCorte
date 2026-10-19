import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector
root=Path(bpy.data.filepath).parent
backup=root/'El_Japon_antes_quarter_curvo.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(backup),copy=True)
names=['Quarter derecho | mural','Quarter lateral | retorno de esquina']
old=[bpy.data.objects[n] for n in names]
col=old[0].users_collection[0]
pts=[[o.matrix_world@v.co for v in o.data.vertices] for o in old]
height=max(v.z for v in pts[0]); base=min(v.z for v in pts[0])
lipY=max(v.y for v in pts[0])-.65
lipX=max(v.x for v in pts[1])-.65
xstart=min(v.x for v in pts[0]); yend=min(v.y for v in pts[1])
run=lipY-min(v.y for v in pts[0]); radius=run+.42
cx=lipX-radius; cy=lipY-radius
assert cx>xstart and cy>yend
path=[]
for i in range(25):
 t=i/24; path.append((xstart+(cx-xstart)*t,lipY,0,1))
for i in range(1,65):
 a=math.pi/2*(1-i/64); nx=math.cos(a); ny=math.sin(a)
 path.append((cx+radius*nx,cy+radius*ny,nx,ny))
for i in range(1,25):
 t=i/24; path.append((lipX,cy+(yend-cy)*t,1,0))
# Elliptical quarter: tangent to floor at entry and vertical at coping.
profile=[(-run*(1-math.sin(math.pi/2*j/64)),height*(1-math.cos(math.pi/2*j/64))) for j in range(65)]
profile += [(.65,height),(.65,base),(-run,base)]
n=len(profile); verts=[]; faces=[]
for x,y,nx,ny in path:
 verts.extend((x+nx*d,y+ny*d,z) for d,z in profile)
for i in range(len(path)-1):
 for j in range(n):
  k=(j+1)%n; faces.append((i*n+j,(i+1)*n+j,(i+1)*n+k,i*n+k))
faces += [tuple(range(n-1,-1,-1)),tuple((len(path)-1)*n+j for j in range(n))]
me=bpy.data.meshes.new('Quarter continuo | superficie soldada'); me.from_pydata(verts,[],faces); me.update()
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
assert all(e.is_manifold for e in bm.edges)
bm.to_mesh(me); bm.free()
ob=bpy.data.objects.new('Quarter derecho y lateral | esquina curva',me); col.objects.link(ob)
for m in old[0].data.materials: me.materials.append(m)
for p in me.polygons: p.use_smooth=p.index<(len(path)-1)*n and p.index%n<64
uv=me.uv_layers.new(name='UV_Quarter'); distances=[0.0]
for i in range(1,len(path)):
 distances.append(distances[-1]+math.hypot(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1]))
for p in me.polygons:
 for li in p.loop_indices:
  vi=me.loops[li].vertex_index; row,j=divmod(vi,n)
  uv.data[li].uv=(distances[row]/2, (profile[j][0]+run+profile[j][1])/2)
ob['descripcion']='Quarter continuo con esquina redondeada; entrada tangente al suelo y salida vertical.'
# Single continuous steel tube, including round corner.
cv=bpy.data.curves.new('Coping continuo curvo','CURVE'); cv.dimensions='3D'; cv.resolution_u=1; cv.bevel_depth=.025; cv.bevel_resolution=5; cv.use_fill_caps=True
sp=cv.splines.new('POLY'); sp.points.add(len(path)-1)
for p,(x,y,nx,ny) in zip(sp.points,path): p.co=(x-.009*nx,y-.009*ny,height+.014,1)
cop=bpy.data.objects.new('Quarter esquina curva | canto metalico continuo',cv); col.objects.link(cop)
steel=bpy.data.objects.get(names[0]+' | coping')
if steel and steel.data.materials: cv.materials.append(steel.data.materials[0])
cop.parent=ob
archive=bpy.data.collections.new('RESPALDO | quarters anteriores ocultos'); bpy.context.scene.collection.children.link(archive)
for name in names:
 for o in [bpy.data.objects.get(name),bpy.data.objects.get(name+' | coping')]:
  if o:
   archive.objects.link(o)
   for c in list(o.users_collection):
    if c!=archive: c.objects.unlink(o)
archive.hide_render=True; archive.hide_viewport=True
for o in bpy.context.selected_objects:o.select_set(False)
ob.select_set(True); bpy.context.view_layer.objects.active=ob
area=bpy.context.area; area.type='VIEW_3D'
region=area.spaces.active.region_3d
target=Vector(((xstart+lipX)/2,(yend+lipY)/2,.65))
eye=target+Vector((-7,-10,7))
region.view_rotation=(target-eye).to_track_quat('-Z','Y'); region.view_distance=10; region.view_location=target
area.spaces.active.overlay.show_extras=False
bpy.ops.wm.save_as_mainfile(filepath=str(root/'El_Japon_Escenario.blend'))
(root/'quarter_curvo_verificacion.json').write_text(json.dumps({'archivo':bpy.data.filepath,'respaldo':str(backup),'vertices':len(me.vertices),'caras':len(me.polygons),'malla_cerrada':True,'altura':height,'radio_esquina':radius,'recorrido_transicion':run},indent=2))
print('QUARTER CURVO TERMINADO Y GUARDADO')
