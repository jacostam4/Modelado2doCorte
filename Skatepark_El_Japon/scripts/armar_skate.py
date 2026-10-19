import bpy,math,shutil
from pathlib import Path
from mathutils import Vector,Matrix
s=bpy.context.scene;p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_armado.blend')),copy=True)
col=bpy.data.collections.new('SKATE COMPLETO | montaje');s.collection.children.link(col)
root=bpy.data.objects.new('SKATE | control general',None);col.objects.link(root)
def link(o):
 for cc in list(o.users_collection):cc.objects.unlink(o)
 col.objects.link(o);o.parent=root;return o
def material(name,color,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough;return m
steel=material('Rodamientos | acero',(.42,.46,.5),1,.23);black=material('Shortys | negro',(.015,.018,.02),.7,.3);red=material('Rodamientos | sello rojo',(.45,.008,.015),.1,.4)
deck0=bpy.data.objects['STYX | TABLA 8.25 x 31.875'];deck=deck0.copy();deck.data=deck0.data.copy();col.objects.link(deck);deck.parent=root;deck.matrix_parent_inverse=Matrix.Identity(4);deck.matrix_basis=Matrix.Translation((0,0,.09));deck.name='TABLA | montada con lija'
src=bpy.data.collections['TRUCK 144 | Hanger reconstruido'];tr=bpy.data.objects['TR144 v2 | Complete truck 8.002'];inv=tr.matrix_world.inverted()
for sign in (-1,1):
 T=Matrix.Translation((0,sign*.2079625,.08))@Matrix.Rotation(math.pi if sign==1 else 0,4,'Z')@Matrix.Rotation(math.pi,4,'X')
 for o in list(src.all_objects):
  if not o or o.type!='MESH' or 'Mounting' in o.name:continue
  ob=o.copy();col.objects.link(ob);ob.parent=root;ob.matrix_parent_inverse=Matrix.Identity(4);ob.matrix_basis=T@inv@o.matrix_world;ob.hide_viewport=False;ob.hide_render=False;ob.hide_set(False);ob.name=('Truck delantero | ' if sign==1 else 'Truck trasero | ')+o.name
def ring(name,center,outer,inner,width,mat,axis='X',N=48):
 verts=[]
 for z,r in [(-width/2,outer),(width/2,outer),(-width/2,inner),(width/2,inner)]:
  for i in range(N):
   a=i*2*math.pi/N;v=(z,r*math.cos(a),r*math.sin(a)) if axis=='X' else (r*math.cos(a),r*math.sin(a),z)
   verts.append(tuple(Vector(center)+Vector(v)))
 faces=[]
 for i in range(N):
  j=(i+1)%N
  faces.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);ob=bpy.data.objects.new(name,me);col.objects.link(ob);ob.parent=root
 for f in me.polygons:f.use_smooth=True
 return ob
ws=sorted(list(bpy.data.collections['01 | RUEDA - modelo y UV'].objects),key=lambda o:o.name)
k=0
for sign in (-1,1):
 y=sign*(.2079625-.012);z=.025
 for side in (-1,1):
  x=side*.08525;o=ws[k].copy();col.objects.link(o);o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Translation((x,y,z))@Matrix.Rotation(side*math.pi/2,4,'Y');o.name=f'RUEDA {k+1} | STYX';o.hide_set(False);o.hide_render=False;k+=1
  for j,dx in enumerate((-.0085,.0085)):
   ctr=(x+dx,y,z);ring(f'Rodamiento {k}.{j+1} | aro exterior',ctr,.011,.009,.007,steel);ring(f'Rodamiento {k}.{j+1} | aro interior',ctr,.006,.004,.007,steel)
   for face in (-1,1):ring(f'Rodamiento {k}.{j+1} | sello', (ctr[0]+face*.0031,y,z),.009,.006,.0005,red)
  ring(f'Separador rueda {k}',(x,y,z),.0055,.004,.010,steel)
for sign in (-1,1):
 for x in (-.0206375,.0206375):
  for dy in (-.0269875,.0269875):
   y=sign*.2079625+dy
   bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.00235,depth=.0254,location=(x,y,.078));ob=link(bpy.context.object);ob.name='Shortys | tornillo 1 pulgada';ob.data.materials.append(black)
   bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.00235,radius2=.0045,depth=.0022,location=(x,y,.0902));ob=link(bpy.context.object);ob.name='Shortys | cabeza avellanada';ob.data.materials.append(black)
   for a in (0,math.pi/2):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,.09135));ob=link(bpy.context.object);ob.name='Shortys | cruz Phillips';ob.scale=(.005,.00065,.00015);ob.rotation_euler.z=a;ob.data.materials.append(steel)
   ring('Shortys | tuerca hexagonal',(x,y,.072),.0045,.0024,.0034,black,'Z',6)
# Use the supplied photo directly with a projective-style UV crop; no wall pixels.
dst=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas');dst.mkdir(exist_ok=True)
photo=dst/'Lija_SpiderMan_referencia.png';shutil.copy2(r'C:\Users\juan_\AppData\Local\Temp\codex-clipboard-55bb50d9-1512-46d8-b189-dab175961432.png',photo)
img=bpy.data.images.load(str(photo),check_existing=True);img.pack()
grip=material('LIJA | Spider-Man foto y grano',(.08,.08,.08),0,.94);nt=grip.node_tree;b=nt.nodes.get('Principled BSDF');tex=nt.nodes.new('ShaderNodeTexImage');tex.image=img;tex.extension='EXTEND'
uvn=nt.nodes.new('ShaderNodeUVMap');uvn.uv_map='UV_Lija_Fotografia';nt.links.new(uvn.outputs['UV'],tex.inputs['Vector']);nt.links.new(tex.outputs['Color'],b.inputs['Base Color'])
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=850;noise.inputs['Detail'].default_value=2;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.35;bump.inputs['Distance'].default_value=.00025;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],b.inputs['Normal'])
me=deck.data;me.materials.append(grip);idx=len(me.materials)-1;uv=me.uv_layers.new(name='UV_Lija_Fotografia')
for f in me.polygons:
 if f.normal.z>.35:f.material_index=idx
 for li in f.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;u=max(0,min(1,(v.x+.104775)/.20955));t=max(0,min(1,(v.y+.4048125)/.809625))
  left=Vector((389,1475)).lerp(Vector((345,183)),t);right=Vector((738,1450)).lerp(Vector((676,179)),t);px=left.lerp(right,u);uv.data[li].uv=(px.x/1200,1-px.y/1600)
for name in ['01 | RUEDA - modelo y UV','03 | TABLA STYX - 8.25 pulgadas','TRUCK 144 | Hanger reconstruido']:
 bpy.data.collections[name].hide_viewport=True;bpy.data.collections[name].hide_render=True
for o in bpy.context.selected_objects:o.select_set(False)
deck.select_set(True);bpy.context.view_layer.objects.active=deck
area=bpy.context.area
out=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\STYX_Skate_Armado.blend')
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;sp.shading.type='MATERIAL';r=sp.region_3d;r.view_perspective='PERSP';r.view_location=(0,0,.06);r.view_rotation=Vector((-.8,.9,-.65)).to_track_quat('-Z','Y');r.view_distance=1.25
 bpy.ops.wm.save_as_mainfile(filepath=str(out));return None
bpy.app.timers.register(finish,first_interval=.7)
print('SKATE ARMADO',out)
