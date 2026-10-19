import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name('El_Japon_antes_union_tres_rampas.blend')),copy=True)
q=bpy.data.objects['Quarter derecho y lateral | esquina curva']
py=bpy.data.objects['Media piramide | skatepark - cancha']
verts=[tuple(q.matrix_world@v.co) for v in q.data.vertices]
n=68
assert len(verts)==7684
faces=[tuple(f.vertices) for f in q.data.polygons if not all(i<n for i in f.vertices)]
smooth=[f.use_smooth for f in q.data.polygons if not all(i<n for i in f.vertices)]
start=verts[:n]; x0=start[0][0]; base=start[-1][2]
peak=max((py.matrix_world@v.co for v in py.data.vertices),key=lambda v:v.z)
tip=max((py.matrix_world@v.co for v in py.data.vertices),key=lambda v:v.y)
outer=max((py.matrix_world@v.co for v in py.data.vertices),key=lambda v:v.x)
prev=list(range(n)); lips=[]
def mix(a,b,t):return a+(b-a)*t
for k in range(1,121):
 x=mix(x0,peak.x,k/120)
 if x<.25:
  t=(x-x0)/(.25-x0); h=mix(start[64][2],.92,t); toe=mix(start[0][1],-12.1,t); lip=mix(start[64][1],-14.0,t); back=mix(start[65][1],peak.y,t); w=0
 elif x<2.8:
  h=.92;toe=-12.1;lip=-14.0;back=peak.y;w=0
 else:
  t=(x-2.8)/(peak.x-2.8);h=mix(.92,peak.z,t);toe=mix(-12.1,tip.y,t);lip=mix(-14.0,peak.y,t);back=peak.y;w=t
 row=[]
 for j in range(65):
  a=math.pi/2*j/64;u=mix(math.sin(a),j/64,w);z=h*mix(1-math.cos(a),j/64,w)
  row.append((x,mix(toe,lip,u),z))
 row += [(x,back,h),(x,back,base),(x,toe,base)]
 ids=list(range(len(verts),len(verts)+n));verts+=row
 for j in range(n):
  j2=(j+1)%n;faces.append((prev[j],ids[j],ids[j2],prev[j2]));smooth.append(j<64 and x<2.8)
 lips.append((x,lip,h+.014));prev=ids
# Close toward the court with the second inclined face, sharing the ridge.
end=len(verts);verts.append((outer.x,outer.y,base))
for j in range(n):faces.append((prev[j],end,prev[(j+1)%n]));smooth.append(False)
me=bpy.data.meshes.new('Mural | tres rampas superficie continua');me.from_pydata(verts,[],faces);me.update()
for f,s in zip(me.polygons,smooth):f.use_smooth=s
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bad=sum(not e.is_manifold for e in bm.edges)
assert bad==0,bad
seen=set();stack=[next(iter(bm.verts))]
while stack:
 v=stack.pop()
 if v in seen:continue
 seen.add(v);stack.extend(e.other_vert(v) for e in v.link_edges)
assert len(seen)==len(bm.verts)
bm.to_mesh(me);bm.free()
for mat in q.data.materials:me.materials.append(mat)
uv=me.uv_layers.new(name='UV_Conjunto_Mural')
for f in me.polygons:
 for li in f.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v.x/2,(v.y+v.z)/2)
ob=bpy.data.objects.new('Mural | piramide y dos quarters conectados',me);q.users_collection[0].objects.link(ob)
# Existing curved coping remains; new low-quarter coping follows the height blend.
central=bpy.data.objects['Quarter central bajo | mural | coping'];central.hide_render=True;central.hide_set(True)
cv=bpy.data.curves.new('Coping | conexion quarter bajo','CURVE');cv.dimensions='3D';cv.bevel_depth=.025;cv.bevel_resolution=4;cv.use_fill_caps=True
points=[(start[64][0],start[64][1],start[64][2]+.014)]+[v for v in lips if v[0]<=2.8]
sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
for pt,co in zip(sp.points,points):pt.co=(*co,1)
for m in central.data.materials:cv.materials.append(m)
co=bpy.data.objects.new('Coping | quarter bajo conectado',cv);ob.users_collection[0].objects.link(co)
for o in (q,py,bpy.data.objects['Quarter central bajo | mural']):o.hide_render=True;o.hide_set(True)
for o in bpy.context.selected_objects:o.select_set(False)
ob.select_set(True);bpy.context.view_layer.objects.active=ob
p.with_name('tres_rampas_verificacion.json').write_text(json.dumps({'componentes':1,'aristas_no_manifold':bad,'vertices':len(me.vertices),'caras':len(me.polygons),'referencia':'Foto detalle mural aportada por usuario; dimensiones estimadas'},indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D';r=area.spaces.active.region_3d;target=Vector((1,-12,.8));eye=target+Vector((6,18,9));r.view_rotation=(target-eye).to_track_quat('-Z','Y');r.view_location=target;r.view_distance=21
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('TRES RAMPAS CONECTADAS; MALLA CERRADA VERIFICADA')
