import bpy,math,random,pathlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
random.seed(23)
base=pathlib.Path(__file__).resolve().parent
sc=bpy.context.scene
head=bpy.data.objects['FBHead'];refcam=bpy.data.objects['fbCamera']
col=bpy.data.collections.new('JUAN | Avatar 1.80 m');sc.collection.children.link(col)
parts=[];bindings={}
def register(o,name,mat=None,bone='spine'):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);parts.append(o);bindings[o.name]=bone
 if mat:o.data.materials.clear();o.data.materials.append(mat)
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 return o
def material(name,color,rough=.6):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=rough
 return m
skin=material('Juan | piel',(.43,.235,.16),.65)
black=material('Algodon negro',(.003,.004,.006),.86)
hair=material('Cabello oscuro',(.012,.009,.007),.48)
denim=material('Denim azul lavado',(.14,.20,.28),.88)
rubber=material('Suela marfil',(.65,.66,.62),.72)
white=material('Cordones',(.55,.57,.56),.8)
for mat,scale,strength in [(black,280,.08),(denim,170,.14),(skin,380,.025)]:
 n=mat.node_tree.nodes;l=mat.node_tree.links;b=n.get('Principled BSDF')
 tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=.002
 l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],b.inputs['Normal'])
mat=denim;n=mat.node_tree.nodes;l=mat.node_tree.links
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=35;noise.inputs['Detail'].default_value=3
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.025,.046,.075,1);ramp.color_ramp.elements[1].color=(.14,.20,.28,1)
l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
photo=bpy.data.images.load(str(base/'referencias'/'IMG_4551.jpg'),check_existing=True);photo.pack()
face=skin.copy();face.name='Rostro | proyeccion fotografica frontal'
n=face.node_tree.nodes;l=face.node_tree.links
t=n.new('ShaderNodeTexImage');t.image=photo;t.extension='EXTEND'
uvnode=n.new('ShaderNodeUVMap');uvnode.uv_map='Foto frontal';l.new(uvnode.outputs['UV'],t.inputs['Vector'])
attr=n.new('ShaderNodeAttribute');attr.attribute_name='Mezcla fotografia'
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.43,.235,.16,1)
l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(t.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
sc.render.resolution_x=photo.size[0];sc.render.resolution_y=photo.size[1];sc.render.resolution_percentage=100
bpy.context.view_layer.update()
uv=head.data.uv_layers.new(name='Foto frontal')
for loop in head.data.loops:
 v=world_to_camera_view(sc,refcam,head.matrix_world@head.data.vertices[loop.vertex_index].co)
 uv.data[loop.index].uv=(v.x,v.y)
head.data.materials.clear();head.data.materials.append(face);head.data.materials.append(skin)
blend=head.data.attributes.new('Mezcla fotografia','FLOAT','POINT')
for v in head.data.vertices:blend.data[v.index].value=max(0,min(1,(-v.normal.y-.1)/.55))*max(0,min(1,(-v.co.y-.15)/.2))
for p in head.data.polygons:p.material_index=0
register(head,'Juan | cabeza fotografica',bone='head')
head.scale=(.1,)*3;head.location.z=1.8-1.38496518*.1
refcam.hide_render=True;refcam.hide_set(True)
def mesh(name,verts,faces,mat,bone='spine',sub=1):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);col.objects.link(o);register(o,name,mat,bone)
 if sub:
  m=o.modifiers.new('Suavizado','SUBSURF');m.levels=sub;m.render_levels=sub
 return o
def loft(name,rings,mat,bone='spine',N=32):
 verts=[]
 for x,y,z,rx,ry in rings:
  for i in range(N):
   a=2*math.pi*i/N;verts.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
 faces=[tuple(reversed(range(N)))]
 for j in range(len(rings)-1):
  for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 faces.append(tuple((len(rings)-1)*N+i for i in range(N)))
 return mesh(name,verts,faces,mat,bone)
def sphere(name,loc,scale,mat,bone='head'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc)
 o=bpy.context.object;o.scale=scale;return register(o,name,mat,bone)
def tube(name,pts,r,mat,bone='head'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,cu);col.objects.link(o);return register(o,name,mat,bone)
torso=loft('Juan | camiseta manga larga',[(0,0,.91,.17,.105),(0,0,.925,.18,.11),(0,0,1.01,.18,.115),(0,0,1.16,.185,.115),(0,0,1.31,.203,.12),(0,0,1.43,.225,.11),(0,0,1.48,.205,.087),(0,0,1.51,.083,.068),(0,0,1.515,.079,.066)],black)
# Actual photographed print, projected onto the front chest surface.
shirt=black.copy();shirt.name='Camiseta | grafica de la fotografia'
n=shirt.node_tree.nodes;l=shirt.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=photo
bw=n.new('ShaderNodeRGBToBW');l.new(t.outputs['Color'],bw.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.045;ramp.color_ramp.elements[1].position=.12
l.new(bw.outputs[0],ramp.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.003,.004,.006,1)
l.new(ramp.outputs[0],mix.inputs[0]);l.new(t.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
verts=[];faces=[]
for j in range(9):
 z=1.12+j*.031
 for i in range(13):
  x=-.15+i*.025;y=-.118*math.sqrt(max(.1,1-(x/.205)**2))-.0005
  verts.append((x,y,z))
for j in range(8):
 for i in range(12):k=j*13+i;faces.append((k,k+1,k+14,k+13))
# Bake only the shirt subdivision so photographic print lies on the fabric itself.
bpy.context.view_layer.objects.active=torso
bpy.ops.object.modifier_apply(modifier=torso.modifiers[0].name)
torso.data.materials.clear();torso.data.materials.append(shirt)
uv=torso.data.uv_layers.new()
for loop in torso.data.loops:
 co=torso.data.vertices[loop.vertex_index].co
 uv.data[loop.index].uv=(.10+(co.x+.15)/.3*.46,.17+(co.z-1.12)/.248*.25)
mask=torso.data.attributes.new('Zona estampado','FLOAT','POINT')
for v in torso.data.vertices:
 mask.data[v.index].value=max(0,min(1,(.155-abs(v.co.x))/.008))*max(0,min(1,(v.co.z-1.115)/.012))*max(0,min(1,(1.38-v.co.z)/.012))*(1 if v.co.y<0 else 0)
attr=n.new('ShaderNodeAttribute');attr.attribute_name='Zona estampado';mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(attr.outputs['Fac'],mult.inputs[0]);l.new(ramp.outputs[0],mult.inputs[1]);l.new(mult.outputs[0],mix.inputs[0])
loft('Juan | cuello tejido',[(0,0,1.495,.085,.071),(0,0,1.515,.082,.069),(0,0,1.524,.080,.067)],black)
loft('Juan | cintura jeans',[(0,.005,.87,.165,.1),(0,.005,.92,.175,.105),(0,.005,.96,.17,.10)],denim,'hips')
for side in (-1,1):
 tag='L' if side==1 else 'R'
 loft('Juan | pierna '+tag,[(side*.105,0,.075,.073,.082),(side*.105,0,.1,.076,.084),(side*.11,.005,.18,.083,.087),(side*.11,.008,.31,.078,.084),(side*.105,-.01,.46,.09,.092),(side*.1,0,.55,.095,.097),(side*.09,.005,.72,.099,.105),(side*.085,.005,.9,.102,.108),(side*.08,.005,.94,.10,.10)],denim,'leg.'+tag)
 # A pose, shoulder to wrist; loose cotton sleeves.
 loft('Juan | manga '+tag,[(side*.405,0,.965,.039,.042),(side*.408,0,.985,.045,.05),(side*.385,0,1.06,.055,.061),(side*.34,0,1.19,.066,.066),(side*.292,0,1.30,.075,.075),(side*.22,0,1.44,.083,.083),(side*.20,0,1.47,.078,.08)],black,'arm.'+tag)
 loft('Juan | puno '+tag,[(side*.411,0,.955,.039,.041),(side*.406,0,.99,.042,.043)],black,'forearm.'+tag)
 sphere('Juan | palma '+tag,(side*.425,-.004,.91),(.037,.023,.061),skin,'hand.'+tag)
 for k in range(4):
  x=side*(.399+k*.017);z=.863-([0,.012,.008,0][k])
  sphere('Juan | dedo '+tag+str(k),(x,-.006,z),(.009,.012,.037),skin,'hand.'+tag)
 sphere('Juan | pulgar '+tag,(side*.389,-.008,.912),(.015,.016,.035),skin,'hand.'+tag)
 shoe=loft('Juan | tenis negro '+tag,[(side*.108,-.045,.028,.088,.151),(side*.108,-.045,.04,.09,.153),(side*.108,-.04,.07,.088,.149),(side*.108,-.02,.105,.073,.11),(side*.108,.025,.14,.055,.057)],black,'foot.'+tag)
 loft('Juan | suela '+tag,[(side*.108,-.045,.01,.084,.147),(side*.108,-.045,.018,.09,.154),(side*.108,-.045,.039,.09,.154),(side*.108,-.045,.045,.087,.15)],rubber,'foot.'+tag)
 for j in range(5):
  y=-.10+j*.024;z=.103+j*.004
  tube('Juan | cordon '+tag+str(j),[(side*.108-.041,y,z),(side*.108+.041,y+.012,z)],.003,white,'foot.'+tag)
 for xoff in (-.073,.073):
  tube('Juan | costura denim '+tag+str(xoff),[(side*.105+xoff,.015,z) for z in (.15,.3,.45,.6,.75,.88)],.0008,white,'leg.'+tag)
# Wavy hair around the sides and nape, matching the photographed length.
for k in range(180):
 a=random.uniform(0,math.pi);x=.092*math.cos(a);y=.073*math.sin(a)+.01
 z=random.uniform(1.69,1.76);length=random.uniform(.11,.18)
 pts=[(x+.006*math.sin(j*.7+k),y+.007*math.cos(j*.6+k),z-length*j/18) for j in range(19)]
 tube('Juan | mechon %02d'%k,pts,random.uniform(.0015,.003),hair)
# Six-panel black cap and curved visor.
verts=[];faces=[];N=48
for j in range(13):
 a=j/12*math.pi/2
 for i in range(N):
  t=i/N*2*math.pi;verts.append((.108*math.cos(a)*math.cos(t),.108*math.cos(a)*math.sin(t)+.005,1.748+.085*math.sin(a)))
for j in range(12):
 for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
cap=mesh('Juan | gorra negra',verts,faces,black)
sol=cap.modifiers.new('Tela','SOLIDIFY');sol.thickness=.002
verts=[];faces=[]
for j in range(5):
 for i in range(25):
  a=-math.pi/2+i/24*math.pi;r=j/4
  verts.append((.103*math.sin(a),-.067-r*.087*math.cos(a),1.75-.012*r+.008*math.sin(a)**2))
for j in range(4):
 for i in range(24):k=j*25+i;faces.append((k,k+1,k+26,k+25))
bill=mesh('Juan | visera',verts,faces,black);bill.modifiers.new('Espesor','SOLIDIFY').thickness=.004
for k in range(6):
 a=k*math.pi/3;tube('Juan | costura gorra '+str(k),[(.104*math.cos(t)*math.cos(a),.095*math.cos(t)*math.sin(a)+.012,1.749+.075*math.sin(t)) for t in [j/20*math.pi/2 for j in range(21)]],.0007,black)
# Basic editable armature. Detailed skin weighting remains a separate refinement.
arm=bpy.data.armatures.new('Juan | esqueleto');rig=bpy.data.objects.new('JUAN | control y esqueleto',arm);col.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,h,t,parent=None):
 b=arm.edit_bones.new(name);b.head=h;b.tail=t
 if parent:b.parent=arm.edit_bones[parent]
bone('root',(0,0,0),(0,0,.2));bone('hips',(0,0,.88),(0,0,1.02),'root');bone('spine',(0,0,1.02),(0,0,1.49),'hips');bone('head',(0,0,1.49),(0,0,1.78),'spine')
for side in (-1,1):
 tag='L' if side==1 else 'R'
 bone('leg.'+tag,(side*.09,0,.91),(side*.105,-.01,.47),'hips');bone('shin.'+tag,(side*.105,-.01,.47),(side*.105,0,.1),'leg.'+tag);bone('foot.'+tag,(side*.105,0,.1),(side*.105,-.17,.05),'shin.'+tag)
 bone('arm.'+tag,(side*.2,0,1.46),(side*.34,0,1.19),'spine');bone('forearm.'+tag,(side*.34,0,1.19),(side*.408,0,.97),'arm.'+tag);bone('hand.'+tag,(side*.408,0,.97),(side*.425,0,.85),'forearm.'+tag)
bpy.ops.object.mode_set(mode='OBJECT')
for o in parts:
 bname=bindings[o.name]
 if o.type=='MESH':
  g=o.vertex_groups.new(name=bname);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
  if 'pierna ' in o.name or 'manga ' in o.name:
   tag=bname.split('.')[-1];second=('shin.' if 'pierna ' in o.name else 'forearm.')+tag;g2=o.vertex_groups.new(name=second)
   pivot=.47 if 'pierna ' in o.name else 1.19
   for v in o.data.vertices:
    w=max(0,min(1,(pivot+.07-v.co.z)/.14));g.add([v.index],1-w,'REPLACE');g2.add([v.index],w,'REPLACE')
  mod=o.modifiers.new('Deformacion esqueleto','ARMATURE');mod.object=rig
  o.parent=rig
 else:
  mw=o.matrix_world.copy();o.parent=rig;o.parent_type='BONE';o.parent_bone=bname;o.matrix_world=mw
rig['estatura_m']=1.80;rig['postura_skate']='Goofy';rig['estado']='Version inicial. Rostro frontal; pendiente ajuste multivista y pesos finos.'
# Presentation camera and lights in a separate collection.
studio=bpy.data.collections.new('ESTUDIO | presentacion');sc.collection.children.link(studio)
def studio_obj(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 studio.objects.link(o)
bpy.ops.object.camera_add(location=(2.65,-5.7,2.15));cam=bpy.context.object;studio_obj(cam);cam.name='Avatar | camara presentacion';cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=2.22;sc.camera=cam
for loc,power,size in [((2,-3,4),450,4),((-3,-1,2),280,3),((0,2,3),500,2)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;studio_obj(o);o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
sc.world.color=(.16,.16,.16);sc.render.engine='CYCLES';sc.cycles.samples=24
sc.render.resolution_x=900;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX';sc.render.image_settings.file_format='PNG';sc.render.film_transparent=True
sc.render.filepath=str(base/'Juan_avatar_previa.png')
for o in bpy.context.selected_objects:o.select_set(False)
rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.wm.save_as_mainfile(filepath=str(base/'Juan_Avatar_Inicial.blend'))
bpy.ops.render.render(write_still=True)
