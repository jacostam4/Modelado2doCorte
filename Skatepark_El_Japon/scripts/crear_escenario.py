import bpy, math, json, random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
random.seed(25)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.name='04 | EL JAPON - Escenario final'
scene.unit_settings.system='METRIC'
scene.unit_settings.length_unit='METERS'
scene.render.engine='CYCLES'
scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=1440
scene.render.resolution_y=960
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.fps=30
scene.frame_start=1; scene.frame_end=1800
scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('Cielo nublado del Japon')
scene.world.color=(.3,.3,.3)
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.62,.71,.82,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65

cols={}
for key,title in [('base','01 | Suelo y escala'),('ramp','02 | Rampas y transiciones'),('obst','03 | Cajones y barandas'),('wall','04 | Muros y mural UV'),('fence','05 | Cerramientos vinculados'),('court','06 | Cancha contigua'),('context','07 | Entorno urbano aproximado'),('light','08 | Sol y areas de luz'),('cam','09 | Camaras'),('refs','10 | Referencias fotograficas'),('lab','11 | Practica de instanciacion - desactivada')]:
 c=bpy.data.collections.new(title);cols[key]=c;scene.collection.children.link(c)

def place(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 cols[col].objects.link(o)
 return o

def mat(name,color,rough=.75,metal=0,noise=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=38;tex.inputs['Detail'].default_value=3
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*(v*.65 for v in color),1);ramp.color_ramp.elements[1].color=(*(min(1,v*1.22) for v in color),1)
  l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
  b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.23;b.inputs['Distance'].default_value=.012
  l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
 return m

concrete=mat('CONCRETO | desgaste y poros',(.43,.44,.43),noise=True)
dark=mat('CAJON | pintura negra gastada',(.065,.071,.067),noise=True)
steel=mat('METAL | acero desgastado',(.15,.17,.16),.36,.72,True)
rust=mat('METAL | oxido de postes',(.16,.11,.075),.68,.45,True)
asphalt=mat('CANCHA | asfalto envejecido',(.10,.11,.105),noise=True)
yellow=mat('CANCHA | linea amarilla gastada',(.44,.34,.10),.91)
brick=mat('MURO | ladrillo pintado gris',(.32,.34,.33),noise=True)
red=mat('BARRERA | rojo desgastado',(.28,.075,.055),noise=True)
white=mat('FACHADA | blanco sucio',(.57,.57,.51),noise=True)
beige=mat('FACHADA | amarillo palido',(.55,.49,.33),noise=True)
green=mat('FACHADA | verde',(.075,.19,.12),noise=True)
teal=mat('FACHADA | turquesa',(.055,.27,.29),noise=True)
glass=mat('VENTANA | vidrio oscuro',(.06,.115,.14),.22,.3)
leaf=mat('ARBOL | follaje verde',(.095,.18,.07),noise=True)
wood=mat('ARBOL | tronco',(.17,.12,.075),noise=True)

def photo_mat(name,file,rough=.85):
 m=mat(name,(.45,.45,.45),rough)
 n=m.node_tree.nodes;l=m.node_tree.links
 i=n.new('ShaderNodeTexImage');i.image=bpy.data.images.load(str(ROOT/'texturas'/file),check_existing=True);i.image.pack();i.label='Imagen fotografica del estudiante'
 uv=n.new('ShaderNodeUVMap');uv.uv_map='UV_Guia_003';l.new(uv.outputs['UV'],i.inputs['Vector']);l.new(i.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
 return m
mural=photo_mat('MURAL | IMG_4340 - imagen UV','mural_fotografico.jpg')
floor_mat=photo_mat('PISO | IMG_4338 - concreto UV','concreto_fotografico.jpg')
brick_photo=photo_mat('MURO | IMG_4337 - ladrillo UV','ladrillo_perimetral.jpg')

def mesh(name,verts,faces,material,col,uv=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);cols[col].objects.link(o)
 if material:me.materials.append(material)
 layer=me.uv_layers.new(name='UV_Guia_003')
 for p in me.polygons:
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co
   layer.data[li].uv=uv(v) if uv else (v.x,v.y)
 for e in me.edges:e.use_seam=True
 o['metodo']='Malla editable, costuras y coordenadas UV. Dimensiones estimadas desde fotografias.'
 return o

def box(name,loc,dims,material,col,bevel=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=place(bpy.context.object,col);o.name=name;o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if material:o.data.materials.append(material)
 if o.data.uv_layers:o.data.uv_layers[0].name='UV_Guia_003'
 for e in o.data.edges:e.use_seam=True
 if bevel:
  m=o.modifiers.new('Bisel de cantos','BEVEL');m.width=bevel;m.segments=2
 return o

def rod(name,a,b,r,material,col,verts=12):
 a=Vector(a);b=Vector(b);v=b-a
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=v.length,location=(a+b)/2)
 o=place(bpy.context.object,col);o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 o.data.uv_layers[0].name='UV_Guia_003'
 return o

def linked(src,name,delta,col=None):
 o=src.copy();o.data=src.data;cols[col].objects.link(o) if col else src.users_collection[0].objects.link(o)
 o.name=name;o.location+=Vector(delta);o['instancia']='Comparte datos con '+src.name+'; equivalente a Alt+D'
 return o

# Main flat skate surface, deliberately tiled to retain a real metric scale for UVs.
box('Losa estructural | 16 x 30 m',(0,0,-.12),(16,30,.24),concrete,'base',.025)
tile=mesh('Piso | losa fotografica original',[(-8,-15,.005),(-6,-15,.005),(-6,-13,.005),(-8,-13,.005)],[(0,1,2,3)],floor_mat,'base',lambda v:((v.x+8)/2,(v.y+15)/2))
for ix in range(8):
 for iy in range(15):
  if ix or iy:linked(tile,f'Piso | instancia {ix:02d}-{iy:02d}',(ix*2,iy*2,0),'base')
# Thin contraction joints: linked geometry, repeated in two directions.
j=box('Junta longitudinal | original',(-6,-.0,.009),(.012,30,.006),dark,'base',0)
for x in [-4,-2,0,2,4,6]:linked(j,'Junta longitudinal | vinculada',(x+6,0,0),'base')
j=box('Junta transversal | original',(0,-13,.009),(16,.012,.006),dark,'base',0)
for y in range(-11,15,2):linked(j,'Junta transversal | vinculada',(0,y+13,0),'base')

def profile_ramp(name,x0,x1,profile,col='ramp'):
 vs=[(x,y,z) for x in (x0,x1) for y,z in profile];n=len(profile)
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,concrete,col,lambda v:(v.x/2,v.y/2+v.z/2))

def quarter(name,x0,x1,toe,height,radius=2.1):
 # Circular transition; arc ends before vertical for the low quarters visible in photos.
 theta=math.acos(1-height/radius)
 curve=[(toe+radius*math.sin(theta*i/32),radius*(1-math.cos(theta*i/32))) for i in range(33)]
 end=curve[-1][0];profile=curve+[(end+.65,height),(end+.65,-.03),(toe,-.03)]
 o=profile_ramp(name,x0,x1,profile)
 for p in o.data.polygons:
  if p.index>=2 and p.index<34:p.use_smooth=True
 rod(name+' | coping',(x0,end,height+.018),(x1,end,height+.018),.025,steel,'ramp')
 return o

profile_ramp('Bank del mural | plano inclinado',-8,-3,[(10.4,0),(13.7,1.35),(14.5,1.35),(14.5,-.03),(10.4,-.03)])
quarter('Quarter central bajo | mural',-3,.8,11.5,.92,2.0)
quarter('Quarter derecho | mural',.8,8,10.9,1.22,2.1)
# Return transition, perpendicular to the mural; creates the photographed corner.
o=quarter('Quarter lateral | retorno de esquina',8.1,12.0,5.3,1.22,2.1)
from mathutils import Matrix
swap=Matrix(((0,1,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)))
for ob in [o]+[z for z in cols['ramp'].objects if z.name.startswith('Quarter lateral') and z!=o]:
 ob.matrix_world=swap @ ob.matrix_world
# Opposite end module: bank, small drop and inclined ledge/rail, as seen in IMG_4338.
profile_ramp('Bank frontal | plataforma inclinada',-5.3,3.5,[(-14.4,.8),(-11,.8),(-7.2,0),(-7.2,-.03),(-14.4,-.03)])
quarter('Quarter del fondo frontal',-5.3,3.5,11.5,.9,1.8)
q=bpy.data.objects['Quarter del fondo frontal'];q.rotation_euler.z=math.pi;q.location.z=.8
cp=bpy.data.objects['Quarter del fondo frontal | coping'];cp.rotation_euler.z+=math.pi;cp.location.x=-cp.location.x;cp.location.y=-cp.location.y;cp.location.z+=.8
box('Escalon bajo transversal | gap de referencia',(-1.9,-9.6,.39),(2.7,.22,.14),dark,'obst')

# Obstacles identifiable in photos. Long axes run along Y.
box('CAJON FS 50-50 | cuerpo',(6.1,-.7,.185),(.8,2.5,.37),dark,'obst',.018)
box('CAJON FS 50-50 | tapa',(6.1,-.7,.3875),(.86,2.56,.025),concrete,'obst',.014)
for x in [5.68,6.52]:box('CAJON FS 50-50 | cantonera',(x,-.7,.395),(.045,2.55,.01),steel,'obst',.004)
box('MANUAL PAD | plataforma baja',(-5.2,-1.5,.10),(2.8,3.4,.2),concrete,'obst')
box('MANUAL PAD | cajon lateral',(-6.42,-1.5,.28),(.36,3.5,.56),dark,'obst')
box('MANUAL PAD | tapa cajon',(-6.42,-1.5,.573),(.43,3.55,.035),concrete,'obst',.008)
rod('BARANDA BAJA | BS-FS boardslide',(1,-1.5,.4),(1,1.5,.4),.026,steel,'obst',20)
support=rod('BARANDA BAJA | soporte original',(1,-1.2,.0),(1,-1.2,.4),.027,rust,'obst')
for y in [0,1.2]:linked(support,'BARANDA BAJA | soporte vinculado',(0,y+1.2,0),'obst')
rod('BARANDA INCLINADA | Nollie BS lipslide',(1.55,-7.15,.65),(1.55,-11.8,1.4),.026,steel,'obst',20)
for y,z in [(-7.2,.65),(-9.5,1.02),(-11.7,1.38)]:
 ground=max(0,min(.8,(-y-7.2)*.8/3.8))
 rod('Baranda inclinada | soporte',(1.55,y,ground),(1.55,y,z),.025,rust,'obst')
profile_ramp('Cajon inclinado paralelo a bank',-4.7,-4.25,[(-11.9,1.18),(-7.2,.43),(-7.2,0),(-11.9,.75)],'obst')
rod('Cajon inclinado | cantonera',(-4.475,-11.9,1.19),(-4.475,-7.2,.44),.036,steel,'obst')

# Mural UV: one photographed image spanning a true geometric wall, not a background billboard.
box('Muro del mural | estructura',(0,14.85,1.95),(16,.25,3.9),brick,'wall')
mesh('Mural fotografico | despliegue UV',[(-8,14.71,.9),(8,14.71,.9),(8,14.71,3.75),(-8,14.71,3.75)],[(0,1,2,3)],mural,'wall',lambda v:((v.x+8)/16,(v.z-.9)/2.85))
box('Muro lateral bajo | estructura',(-8.13,-1.5,.38),(.25,27,.76),brick,'wall')
mesh('Ladrillo lateral | UV fotografico',[(-7.99,-15,0),(-7.99,12,0),(-7.99,12,.75),(-7.99,-15,.75)],[(0,1,2,3)],brick_photo,'wall',lambda v:((v.y+15)/2,v.z/.4))

# Upper mural fence: linked vertical bars and rails.
bar=rod('Reja mural | barrotes original',(-7.9,14.85,3.8),(-7.9,14.85,5.2),.014,rust,'fence',8)
for k in range(1,64):linked(bar,f'Reja mural | Alt D {k:02d}',(k*.25,0,0),'fence')
for z in [3.82,5.2]:rod('Reja mural | travesano',(-8,14.85,z),(8,14.85,z),.023,rust,'fence')
# Chain-link mesh beside the street. Each panel reuses exactly the same mesh.
vs=[];fs=[]
def wire_quad(y0,z0,y1,z1):
 dy=y1-y0;dz=z1-z0;L=math.hypot(dy,dz)
 if L<.00001:return
 wy=-dz/L*.005;wz=dy/L*.005;i=len(vs)
 vs.extend([(-8.05,y0+wy,z0+wz),(-8.05,y1+wy,z1+wz),(-8.05,y1-wy,z1-wz),(-8.05,y0-wy,z0-wz)]);fs.append((i,i+1,i+2,i+3))
for sign in [-1,1]:
 for off in [k*.25 for k in range(-12,14)]:
  pts=[]
  for y in [0,3]:
   z=sign*y+off
   if 0<=z<=2.2:pts.append((y,z))
  for z in [0,2.2]:
   y=(z-off)/sign
   if 0<=y<=3:pts.append((y,z))
  if len(pts)>=2:wire_quad(pts[0][0]-15,pts[0][1]+.8,pts[-1][0]-15,pts[-1][1]+.8)
panel=mesh('Malla eslabonada | panel original',vs,fs,steel,'fence')
for k in range(1,9):linked(panel,f'Malla eslabonada | instancia {k}',(0,k*3,0),'fence')
post=rod('Cerramiento | poste original',(-8.07,-15,.75),(-8.07,-15,3.05),.04,steel,'fence')
for k in range(1,10):linked(post,'Cerramiento | poste vinculado',(0,k*3,0),'fence')
for z in [.8,3]:rod('Cerramiento | travesano',(-8.07,-15,z),(-8.07,12,z),.024,steel,'fence')

# Adjacent sports court is part of the observed location.
box('Cancha contigua | asfalto',(15.5,0,-.06),(15,30,.12),asphalt,'court',0)
def line(name,points,r=.025,material=yellow,col='court'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=1
 p=cu.splines.new('POLY');p.points.add(len(points)-1)
 for v,co in zip(p.points,points):v.co=(*co,1)
 o=bpy.data.objects.new(name,cu);cols[col].objects.link(o);cu.materials.append(material);return o
line('Cancha | perimetro desgastado',[(9,-13,.014),(22,-13,.014),(22,13,.014),(9,13,.014),(9,-13,.014)])
line('Cancha | mitad',[(9,0,.016),(22,0,.016)])
line('Cancha | circulo central',[(15.5+2.6*math.cos(a*math.tau/90),2.6*math.sin(a*math.tau/90),.017) for a in range(91)])
for y,sgn in [(-13,1),(13,-1)]:
 line('Cancha | area',[(11.5,y,.016),(11.5,y+sgn*4,.016),(19.5,y+sgn*4,.016),(19.5,y,.016)])
 for x in [12.5,18.5]:rod('Cancha | porteria poste',(x,y,0),(x,y,2.2),.05,white,'court')
 rod('Cancha | porteria travesano',(12.5,y,2.2),(18.5,y,2.2),.05,white,'court')

# Urban context: simplified masses, distinct from photo-constrained skating geometry.
box('Calle lateral',(-12,0,-.10),(7,40,.18),asphalt,'context',0)
box('Anden lateral',(-15.3,0,.05),(1.2,40,.1),concrete,'context',0)
def building(name,loc,dims,material,front='y'):
 o=box(name,loc,dims,material,'context',.035)
 x,y,z=loc;w,d,h=dims
 for floor in range(max(1,int(h/2.8))):
  for xx in [-.28, .28]:
   if front=='y':
    box(name+' | ventana',(x+xx*w,y+d/2+.015,1.6+floor*2.7),(w*.23,.06,1.25),glass,'context',.005)
   else:box(name+' | ventana',(x+w/2+.015,y+xx*d,1.6+floor*2.7),(.06,d*.23,1.25),glass,'context',.005)
 box(name+' | remate',(x,y,z+h/2+.1),(w+.15,d+.15,.18),dark,'context')
 return o
building('Edificio amarillo de referencia',(-18,1,4.6),(5,14,9.2),beige,'x')
for y,m in [(-13,white),(-7,brick),(11,brick),(17,white)]:building('Vivienda lateral',(-17.8,y,3.1),(4.5,5.5,6.2),m,'x')
for x,w,h,m in [(-6,3.8,5,green),(-1.6,4,4.5,white),(3.3,4.2,7.8,teal),(8.1,4.3,7.1,white),(12.9,4.5,6.1,white),(18,5,5.9,green)]:
 building('Fachada del fondo',(x,-20,h/2),(w,5,h),m)
box('Caseta del parque',(5.5,-13.5,1.55),(3.4,2.2,3.1),brick,'context')
box('Caseta | puerta',(5.0,-12.38,1.35),(1,.06,2.5),dark,'context')
box('Caseta | ventana',(6.4,-12.37,1.8),(1.05,.08,1),glass,'context')
box('Caseta | cubierta',(5.5,-13.5,3.2),(3.8,2.65,.17),dark,'context')
box('Barrera roja observada',(-7.05,-1.8,.36),(.35,1.6,.72),red,'context',.08)
# A few trees behind the fence, with linked foliage meshes.
for x,y in [(-10,-16),(-9.5,-11),(24,13),(24,-9)]:
 rod('Arbol | tronco',(x,y,0),(x,y,4.5),.17,wood,'context')
 for k in range(7):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1.15,location=(x+random.uniform(-1.2,1.2),y+random.uniform(-1.2,1.2),4.5+random.uniform(-.6,1.2)))
  o=place(bpy.context.object,'context');o.name='Arbol | copa';o.scale=(1.25,1,.75);o.data.materials.append(leaf)

# Street lamps share geometry; actual light sources share their data as Alt+D examples.
lamp=rod('Poste urbano | original',(8.7,-9,0),(8.7,-9,7),.09,concrete,'context',12)
for y in [3,13]:linked(lamp,'Poste urbano | vinculado',(0,y+9,0),'context')
for y in [-9,3,13]:
 for side in [-1,1]:
  rod('Poste | brazo',(8.7,y,6.8),(8.7+side*1.25,y,7.15),.035,steel,'context')
  box('Poste | luminaria',(8.7+side*1.25,y,7.14),(.65,.3,.09),dark,'context')
line('Cable aereo',[(8.7,y,7.2-.4*math.sin((y+9)/22*math.pi)) for y in range(-9,14)],.012,steel,'context')

def light(name,typ,loc,power,color,size=5):
 d=bpy.data.lights.new(name,typ);d.energy=power;d.color=color
 if typ=='AREA':d.shape='DISK';d.size=size
 o=bpy.data.objects.new(name,d);cols['light'].objects.link(o);o.location=loc;return o
sun=light('SOL | direccion y sombras','SUN',(0,0,12),1.25,(1,.92,.81));sun.rotation_euler=(math.radians(28),math.radians(-22),math.radians(-35));sun.data.angle=.3
area=light('AREA | cielo difuso original','AREA',(-3,2,15),1800,(.74,.84,1),15)
linked(area,'AREA | instancia vinculada',(12,-10,-4),'light')

def camera(name,loc,target,lens=32):
 d=bpy.data.cameras.new(name);d.lens=lens;d.clip_end=350
 o=bpy.data.objects.new(name,d);cols['cam'].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
overview=camera('CAM 01 | Vista general',(28,-36,25),(1,0,1.3),38)
muralcam=camera('CAM 02 | Mural y quarters',(5,-7,2.25),(0,13,1.7),24)
streetcam=camera('CAM 03 | Cajones y barandas',(6,10,2.15),(-.3,-8,.65),25)
top=camera('CAM 04 | Planta',(0,0,45),(0,0,0),40);top.data.type='ORTHO';top.data.ortho_scale=38
scene.camera=overview

# Reference empties are editable and never render.
for n in range(4333,4342):
 img=bpy.data.images.load(str(ROOT/'referencias/imagenes'/f'IMG_{n}.jpg'));img.pack()
 o=bpy.data.objects.new(f'REF | IMG_{n}',None);o.empty_display_type='IMAGE';o.data=img;o.empty_display_size=5;cols['refs'].objects.link(o);o.location=(35,(n-4333)*5,3);o.rotation_euler.x=math.pi/2;o.hide_render=True;o.hide_set(True)

# Separate training collection: same light data vs independent copied data.
area2=light('LAB | area original','AREA',(35,0,4),500,(1,.25,.08),3);place(area2,'lab')
linked(area2,'LAB | Alt D - cambia ambas',(4,0,0),'lab')
dup=area2.copy();dup.data=area2.data.copy();cols['lab'].objects.link(dup);dup.name='LAB | Shift D - color independiente';dup.location+=(Vector((8,0,0)));dup.data.color=(.1,.35,1)
for typ,x in [('POINT',35),('SPOT',39)]:
 ob=light('LAB | '+typ,typ,(x,5,3),150,(1,1,1));place(ob,'lab')
cols['lab'].hide_render=True;cols['lab'].hide_viewport=True

# Stage scenes document genuine additive construction, with linked meshes.
for name,keys in [('01 | Construccion - suelo', ['base','cam','light']),('02 | Construccion - obstaculos',['base','ramp','obst','cam','light']),('03 | Construccion - cerramientos',['base','ramp','obst','wall','fence','cam','light'])]:
 st=bpy.data.scenes.new(name);st.unit_settings.system='METRIC';st.world=scene.world;st.camera=overview
 st.render.engine='CYCLES';st.cycles.samples=16;st.cycles.use_denoising=True
 st.render.resolution_x=1440;st.render.resolution_y=960;st.render.resolution_percentage=100
 for k in keys:st.collection.children.link(cols[k])
 st['etapa']=name

scene['descripcion']='Reconstruccion visual del skatepark El Japon a partir de IMG_4333 a IMG_4341. No es un levantamiento metrico.'
scene['escala_estimada']='Pista 16 x 30 m; baranda plana 3 m x 0.40 m; cajon 2.5 m x 0.40 m (medidas aproximadas del usuario). Ajustar con mediciones reales.'
scene['guia_003']='Texturas fotograficas Image Texture -> Principled BSDF; UV_Guia_003 y costuras en superficies.'
scene['guia_004']='Instancias vinculadas en piso, rejas, postes y luces; Sol y Areas; laboratorio separado con Area/Point/Spot.'
scene['pendiente']='Avatar y trucos no incluidos. Gap exacto y dimensiones pendientes de confirmar. Entorno urbano simplificado.'

readme='''EL JAPON - RECONSTRUCCION VISUAL EDITABLE\n\nFUENTES: Fotografias propias IMG_4333 a IMG_4341. Los MOV asociados son Live Photos cortas.\nDIMENSIONES: cajon 2.5 m de largo / 0.40 m alto; baranda baja 3 m / 0.40 m, medidas aproximadas aportadas por el usuario. Resto estimado; no hay levantamiento topografico.\n\nESCENAS DEL ARCHIVO\n01: losa y piso.\n02: rampas, cajones y barandas.\n03: muros, mural y cerramientos.\n04: escenario con entorno urbano e iluminacion.\n\nGUIA 003\nLas mallas tienen mapas UV y los objetos construidos por perfil tienen costuras marcadas. El piso, mural y ladrillo usan imagenes fotograficas conectadas a Base Color del Principled BSDF. Otros materiales usan ruido para desgaste y rugosidad.\n\nGUIA 004\nPiso, barrotes, paneles de malla, postes y soportes comparten datos: equivalente a Alt+D. Las dos luces AREA de la escena final comparten datos. La coleccion LAB, oculta, incluye un area original, su instancia vinculada y una copia independiente; ademas Point y Spot.\n\nANIMACION\n30 fps y rango 1-1800 para un minuto. Sin personaje ni trucos todavia. La geometria de los obstaculos es editable y utilizable para contactos.\n\nLIMITACIONES\nLa textura del mural contiene perspectiva y oclusiones de las fotos. Edificios y vegetacion son contexto aproximado. No se inventa un gap nuevo: el pequeno desnivel del bank queda como referencia hasta confirmar el gap real.\n'''
bpy.data.texts.new('LEEME | Guia del escenario').write(readme)
(ROOT/'LEEME.txt').write_text(readme,encoding='utf-8')

# Save with a useful perspective in Layout.
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.region_3d.view_distance=42
   a.spaces.active.region_3d.view_location=(1,0,1)
   a.spaces.active.region_3d.view_rotation=overview.rotation_euler.to_quaternion()
   a.spaces.active.shading.type='MATERIAL'
   a.spaces.active.clip_end=500
bpy.context.window.scene=scene
for o in bpy.context.selected_objects:o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Escenario.blend'))

# Export standalone scenery geometry for the course folder.
bpy.ops.object.select_all(action='DESELECT')
for key in ['base','ramp','obst','wall','fence','court','context']:
 for ob in cols[key].objects:
  if ob.type in {'MESH','CURVE'}:ob.select_set(True)
export_meshes=[]
for ob in bpy.context.selected_objects:
 if ob.type=='MESH':
  export_meshes.append((ob,ob.data));ob.data=ob.data.copy()
bpy.ops.export_scene.fbx(filepath=str(ROOT/'El_Japon_Escenario.fbx'),use_selection=True,object_types={'MESH'},bake_anim=False,path_mode='COPY',embed_textures=True)
for ob,original in export_meshes:
 temporary=ob.data;ob.data=original
 if temporary.users==0:bpy.data.meshes.remove(temporary)
bpy.ops.object.select_all(action='DESELECT')
# Review renders; rendered pixels are inspected before delivery.
for name,cam in [('01_vista_general',overview),('02_mural_y_transiciones',muralcam),('03_obstaculos',streetcam)]:
 scene.camera=cam;scene.render.filepath=str(ROOT/'renders'/f'{name}.png')
 bpy.ops.render.render(write_still=True)
scene.camera=muralcam
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Escenario.blend'))
print('DONE',len(bpy.data.objects),'objects')


