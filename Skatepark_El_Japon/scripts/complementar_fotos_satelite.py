import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
cols={k:bpy.data.collections[v] for k,v in [('obst','03 | Cajones y barandas'),('ramp','02 | Rampas y transiciones'),('context','07 | Entorno urbano aproximado')]}
def assign(o,k):
 for c in list(o.users_collection):c.objects.unlink(o)
 cols[k].objects.link(o);return o
def box(name,loc,dims,material,k='context',bevel=.01):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=assign(bpy.context.object,k);o.name=name;o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if material:o.data.materials.append(material)
 o.data.uv_layers[0].name='UV_Guia_003'
 if bevel:
  m=o.modifiers.new('Bisel','BEVEL');m.width=bevel;m.segments=2
 return o
def photo(name,file):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(.25,.25,.25,1)
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.88
 im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'texturas'/file),check_existing=True);im.image.pack()
 uv=n.new('ShaderNodeUVMap');uv.uv_map='UV_Guia_003';l.new(uv.outputs['UV'],im.inputs['Vector']);l.new(im.outputs['Color'],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.15;b.inputs['Distance'].default_value=.008;l.new(im.outputs['Color'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
def mesh(name,vs,fs,mat,k,uv=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);cols[k].objects.link(o);me.materials.append(mat)
 layer=me.uv_layers.new(name='UV_Guia_003')
 for lp in me.loops:
  v=me.vertices[lp.vertex_index].co;layer.data[lp.index].uv=uv(v) if uv else (v.x/2,v.y/2)
 for ed in me.edges:ed.use_seam=True
 return o
def rod(name,a,b,r,mat,k='context',vertices=10):
 a=Vector(a);b=Vector(b);d=b-a
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(a+b)/2)
 o=assign(bpy.context.object,k);o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o
concrete=bpy.data.materials['CONCRETO | desgaste y poros'];dark=bpy.data.materials['CAJON | pintura negra gastada'];steel=bpy.data.materials['METAL | acero desgastado'];white=bpy.data.materials['FACHADA | blanco sucio'];green=bpy.data.materials['FACHADA | verde']
brickmat=photo('CAJON | ladrillo real IMG_4336','cajon_ladrillo_foto.jpg')
padmat=photo('MANUAL PAD | desgaste real IMG_4337','manualpad_frente_foto.jpg')
facmat=photo('ENTORNO | grafitis IMG_4336','fachada_verde_grafitis_foto.jpg')
hutmat=photo('CASETA | fachada IMG_4338','caseta_foto.jpg')

# Preserve known footprint and heights; enrich the ledge with real brickwork.
body=bpy.data.objects['CAJON FS 50-50 | cuerpo'];body.data.materials[0]=dark
bpy.data.objects['CAJON FS 50-50 | tapa'].data.materials[0]=steel
for y in [5.295,6.105]:
 mesh('Cajon | ladrillo fotografico UV',[(.95,y,.005),(3.45,y,.005),(3.45,y,.367),(.95,y,.367)],[(0,1,2,3)],brickmat,'obst',lambda v:((v.x-.95)/2.5,(v.z-.005)/.362))
for x in [.945,3.455]:
 mesh('Cajon | testero ladrillo UV',[(x,5.3,.005),(x,6.1,.005),(x,6.1,.367),(x,5.3,.367)],[(0,1,2,3)],brickmat,'obst',lambda v:((v.y-5.3)/2.5,(v.z-.005)/.362))
mesh('Manual pad | frente negro fotografico',[(-1.3,-4.045,.005),(2.1,-4.045,.005),(2.1,-4.045,.19),(-1.3,-4.045,.19)],[(0,1,2,3)],padmat,'obst',lambda v:((v.x+1.3)/3.4,(v.z-.005)/.185))
for o in bpy.data.objects:
 if o.name.startswith('MANUAL PAD | tapa'):o.data.materials[0]=steel
 if o.name.startswith('Cajon inclinado paralelo'):
  o.data.materials[0]=dark;o.data.materials.append(concrete)
  # The first profile edge is the inclined riding top.
  o.data.polygons[2].material_index=1

# Photographs show a hip with side slopes, rather than a wide flat bank.
old=bpy.data.objects.get('Bank del mural | plano inclinado')
if old:bpy.data.objects.remove(old,do_unlink=True)
hip=mesh('HIP del mural | forma de IMG_4334 y 4340',[(10.85,3.1,0),(10.85,8,0),(14.45,8,0),(14.45,3.1,0),(14.1,5.5,1.22),(14.45,5.5,1.22),(10.85,3.1,-.03),(10.85,8,-.03),(14.45,8,-.03),(14.45,3.1,-.03)],[(0,1,4),(1,2,5,4),(3,0,4,5),(2,3,5),(0,6,7,1),(1,7,8,2),(2,8,9,3),(3,9,6,0),(6,9,8,7)],concrete,'ramp')
hip['referencias']='IMG_4334, IMG_4340; emplazamiento confirmado a derecha en satelital'

# Hut alongside the upper side of the left-hand bank, visible in IMG_4338.
hutnames=[o for o in bpy.data.objects if o.name.startswith(('Caseta del parque','Caseta |'))]
center=bpy.data.objects['Caseta del parque'].matrix_world.translation.copy()
delta=Vector((-13.8,4.65,1.55))-center
for o in hutnames:o.location+=delta
bpy.context.view_layer.update()
bodyhut=bpy.data.objects['Caseta del parque']
corners=[bodyhut.matrix_world @ Vector(v) for v in bodyhut.bound_box]
front=max(v.x for v in corners)+.008;y0=min(v.y for v in corners);y1=max(v.y for v in corners)
for name in ['Caseta | puerta','Caseta | ventana']:
 ob=bpy.data.objects.get(name)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
mesh('Caseta | proyeccion UV de foto',[(front,y1,.08),(front,y0,.08),(front,y0,3.0),(front,y1,3.0)],[(0,1,2,3)],hutmat,'context',lambda v:((v.y-y0)/(y1-y0),(v.z-.08)/2.92))
# Roof ribs and low brick planter, as distinct geometry.
for i in range(14):
 y=y0+(y1-y0)*i/13
 rod('Caseta | nervadura de cubierta',(front-2.4,y,3.32),(front+.15,y,3.32),.018,steel)
box('Caseta | jardinera de ladrillo',(front+.18,4.65,.3),(.5,3.9,.6),dark)

# Long low building opposite the park across the court, observed in IMG_4336/4339.
box('Fachada baja frente a cancha | cuerpo',(0,25.3,1.35),(30,3.7,2.7),white)
mesh('Fachada frente cancha | grafitis de foto',[(-15,23.435,.05),(15,23.435,.05),(15,23.435,2.65),(-15,23.435,2.65)],[(0,1,2,3)],facmat,'context',lambda v:((v.x+15)/30,(v.z-.05)/2.6))
roof=mesh('Cubierta verde | faldones',[(-15.2,23.15,2.78),(15.2,23.15,2.78),(15.2,25.3,3.15),(-15.2,25.3,3.15),(-15.2,27.45,2.78),(15.2,27.45,2.78)],[(0,1,2,3),(3,2,5,4)],green,'context')
for i in range(61):
 x=-15.2+i*(30.4/60)
 rod('Cubierta verde | nervadura',(x,23.15,2.8),(x,25.3,3.17),.014,steel)
 rod('Cubierta verde | nervadura',(x,25.3,3.17),(x,27.45,2.8),.014,steel)

# Small frame and window-bar geometry refine the simplified neighboring facades.
windows=[o for o in list(cols['context'].objects) if ' | ventana' in o.name and o.type=='MESH']
for w in windows:
 bnds=[Vector(v) for v in w.bound_box];lo=Vector(tuple(min(v[i] for v in bnds) for i in range(3)));hi=Vector(tuple(max(v[i] for v in bnds) for i in range(3)))
 narrow=0 if hi.x-lo.x < hi.y-lo.y else 1;wide=1-narrow
 for t in [0,.25,.5,.75,1]:
  a=Vector((0,0,lo.z));b=Vector((0,0,hi.z));a[narrow]=b[narrow]=hi[narrow]+.016;a[wide]=b[wide]=lo[wide]+t*(hi[wide]-lo[wide])
  rod('Ventana | reja vertical',w.matrix_world@a,w.matrix_world@b,.012,steel)
 for z in [lo.z,hi.z]:
  a=Vector((0,0,z));b=a.copy();a[narrow]=b[narrow]=hi[narrow]+.016;a[wide]=lo[wide];b[wide]=hi[wide]
  rod('Ventana | marco horizontal',w.matrix_world@a,w.matrix_world@b,.018,steel)

# Simple photographic pavement wear, replacing the pristine ledge appearance.
for prefix in ['BARANDA BAJA |','BARANDA INCLINADA |']:
 for o in bpy.data.objects:
  if o.name.startswith(prefix):o['referencias']='IMG_4338 o IMG_4339; altura y largo plano aportados por usuario'

def camera(name,loc,target,lens=28):
 d=bpy.data.cameras.new(name);d.lens=lens;o=bpy.data.objects.new(name,d);bpy.data.collections['09 | Camaras'].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
detail=camera('CAM 05 | Cajon y cubierta verde',(5,-1,1.65),(1,12,1.45),30)
bank=bpy.data.objects['CAM 03 | Cajones y barandas'];bank.location=(0,-.5,1.9);bank.rotation_euler=(Vector((-12.8,1.3,.9))-bank.location).to_track_quat('-Z','Y').to_euler();bank.data.lens=27
mural=bpy.data.objects['CAM 02 | Mural y quarters'];mural.location=(3,-1,1.9);mural.rotation_euler=(Vector((13.7,0,1.1))-mural.location).to_track_quat('-Z','Y').to_euler();mural.data.lens=24
s['fotos_complementarias']='IMG_4334/4340: hip y mural; IMG_4336: cajon de ladrillo y cubierta verde; IMG_4337: manual pad; IMG_4338: caseta y modulo izquierdo; IMG_4339: baranda.'
note='Fotos + satelite: la planta mantiene la orientacion confirmada por el estudiante. Se complementan formas, materiales y entorno a partir de las fotos. El hip sustituye el bank rectangular; el cajon utiliza ladrillo fotografico y tapa oscura; la caseta y el edificio de cubierta verde llevan texturas UV. Las imagenes de las fachadas contienen oclusiones fotografiadas (objetos delante de los muros); no son un escaneo ni un registro metrico.\n'
bpy.data.texts.new('FOTOS | Complemento del escenario').write(note)
(ROOT/'COMPLEMENTO_FOTOGRAFICO.txt').write_text(note,encoding='utf-8')
s.camera=mural;s.cycles.samples=24
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Planta_Corregida.blend'))
render=ROOT/'renders/fotos_y_satelite';render.mkdir(exist_ok=True)
for name,cam in [('01_mural_y_hip',mural),('02_modulo_izquierdo',bank),('03_cajon_y_cubierta_verde',detail),('04_planta',bpy.data.objects['CAM 04 | Planta'])]:
 s.camera=cam;s.render.resolution_x=1440;s.render.resolution_y=960
 if name=='04_planta':s.render.resolution_x=1400;s.render.resolution_y=1250
 s.render.filepath=str(render/(name+'.png'));bpy.ops.render.render(write_still=True)
s.camera=mural;s.render.resolution_x=1440;s.render.resolution_y=960
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
o=bpy.data.objects['CAJON FS 50-50 | cuerpo'];corners=[o.matrix_world@Vector(v) for v in o.bound_box];assert abs(max(v.x for v in corners)-min(v.x for v in corners)-2.5)<.001
assert abs(bpy.data.objects['BARANDA BAJA | BS-FS boardslide'].location.z-.4)<.001
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Planta_Corregida.blend'))
print('FOTOS Y SATELITE COMPLEMENTADOS')
