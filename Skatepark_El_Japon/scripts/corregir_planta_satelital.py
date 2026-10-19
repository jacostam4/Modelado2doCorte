import bpy,math,json
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
# Image convention: left/right follow the screenshot; up is the court side.
# This is not an assertion of geographic north.
swap=Matrix(((0,1,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)))
for o in list(bpy.data.objects):
 if o.type not in {'CAMERA','LIGHT'} and not o.name.startswith(('REF |','LAB |')):
  o.matrix_world=swap @ o.matrix_world
 elif o.type=='LIGHT' and not o.name.startswith('LAB |'):
  if o.data.type=='SUN':
   o.rotation_euler=(math.radians(28),math.radians(22),math.radians(35))
  else:o.location=swap @ o.location

def move_group(names,center):
 obs=[o for o in bpy.data.objects if any(o.name.startswith(n) for n in names)]
 pts=[o.matrix_world.translation for o in obs]
 if not pts:return
 old=sum(pts,Vector())/len(pts)
 delta=Vector((center[0]-old.x,center[1]-old.y,0))
 for o in obs:o.location+=delta

# Satellite: low rail near lower-left edge; long ledge near court boundary.
move_group(['BARANDA BAJA |'],(-8.2,-5.8))
move_group(['CAJON FS 50-50 |'],(2.2,5.7))
move_group(['MANUAL PAD |'],(.4,-5.9))
# Place manual pad and its taller ledge relative to the street perimeter.
for name,x,y in [('MANUAL PAD | plataforma baja',.4,-5.45),('MANUAL PAD | cajon lateral',.4,-6.85),('MANUAL PAD | tapa cajon',.4,-6.85)]:
 o=bpy.data.objects[name];o.location.x=x;o.location.y=y

# The left-hand module occupies a short end bay, rather than a deep block.
# Compress footprint only; obstacle heights remain at the photographed estimate.
bank_names=('Bank frontal |','Quarter del fondo frontal','Escalon bajo transversal','BARANDA INCLINADA |','Baranda inclinada |','Cajon inclinado')
T=Matrix.Translation(Vector((-14.5,0,0))) @ Matrix.Diagonal((.62,.72,1,1)) @ Matrix.Translation(Vector((14.5,0,0)))
for o in bpy.data.objects:
 if o.name.startswith(bank_names):o.matrix_world=T @ o.matrix_world
move_group(['Caseta del parque','Caseta |'],(-15.5,1.2))

# Retain the photographed left-to-right order of the mural and its ramps.
# Global coordinate exchange reflects handedness; correct the right end locally.
mirror_y=Matrix.Diagonal((1,-1,1,1))
for ob in bpy.data.objects:
 if ob.name.startswith(('Bank del mural','Quarter central bajo','Quarter derecho','Quarter lateral','Mural fotografico')):
  ob.matrix_world=mirror_y @ ob.matrix_world

# Camera arrangement consistent with the satellite image.
def orient(name,loc,target):
 o=bpy.data.objects[name];o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
overview=orient('CAM 01 | Vista general',(30,-35,31),(0,4,0))
overview.data.lens=40
mural=orient('CAM 02 | Mural y quarters',(-6,-5,2.3),(14,0,1.65));mural.data.lens=25
obstacles=orient('CAM 03 | Cajones y barandas',(9,-6,2.6),(-10,-.5,.65));obstacles.data.lens=25
top=orient('CAM 04 | Planta',(0,7.5,55),(0,7.5,0));top.data.type='ORTHO';top.data.ortho_scale=36
top.rotation_euler=(0,0,0)
for sc in bpy.data.scenes:
 sc.camera=overview
s.camera=top
s['planta_corregida']='Vista satelital aportada por el estudiante. Mural a derecha; bank, cajon inclinado y baranda a izquierda; cancha arriba. Orientacion de pantalla, no norte geografico.'
s['posiciones_estimadas']='Rail bajo: (-8.2,-5.8). Cajon: (2.2,5.7). Manual pad: (0.4,-5.45). Posiciones aproximadas desde imagen sin escala.'
s['pendiente']='Avatar, tabla y trucos no integrados. Gap exacto, alturas secundarias y distancias del perimetro pendientes de medicion.'
img=bpy.data.images.load(str(ROOT/'referencias/satelital_japon.png'),check_existing=True);img.pack()
o=bpy.data.objects.new('REF | Planta satelital - orientacion confirmada',None);o.empty_display_type='IMAGE';o.data=img;o.empty_display_size=12;o.location=(42,0,0);o.hide_render=True
bpy.data.collections['10 | Referencias fotograficas'].objects.link(o);o.hide_set(True)

# Native guide retains all original educational scenes and material data.
txt=bpy.data.texts.new('CORRECCION | Planta satelital')
txt.write('Orientacion confirmada por el estudiante: muro de retratos a la DERECHA; modulo de baranda y cajon en bajada a la IZQUIERDA. Cancha arriba. La calle con el manual pad queda abajo. La imagen no ofrece escala: planta y posiciones son aproximadas.\nLa escena original se conserva en El_Japon_Escenario.blend. Esta version se guarda en El_Japon_Planta_Corregida.blend.\n')
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   r=a.spaces.active.region_3d;r.view_perspective='ORTHO';r.view_rotation=(1,0,0,0);r.view_location=(0,7.5,0);r.view_distance=42
   a.spaces.active.shading.type='MATERIAL'
bpy.context.window.scene=s
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Planta_Corregida.blend'))

RENDERS=ROOT/'renders/corregido';RENDERS.mkdir(exist_ok=True)
s.cycles.samples=24
for name,cam,size in [('01_planta_satelital',top,(1400,1250)),('02_perspectiva_general',overview,(1440,960)),('03_hacia_mural',mural,(1440,960)),('04_hacia_bank',obstacles,(1440,960))]:
 s.camera=cam;s.render.resolution_x=size[0];s.render.resolution_y=size[1];s.render.filepath=str(RENDERS/(name+'.png'));bpy.ops.render.render(write_still=True)
s.camera=top;s.render.resolution_x=1400;s.render.resolution_y=1250
body=bpy.data.objects['CAJON FS 50-50 | cuerpo']
world_corners=[body.matrix_world @ Vector(c) for c in body.bound_box]
assert abs(max(v.x for v in world_corners)-min(v.x for v in world_corners)-2.5)<.001
assert abs(bpy.data.objects['BARANDA BAJA | BS-FS boardslide'].location.z-.4)<.001
assert all(i.packed_file for i in bpy.data.images if i.source=='FILE')
(ROOT/'verificacion_planta_corregida.json').write_text(json.dumps({'mural':'derecha','modulo_bajada':'izquierda','cancha':'arriba','baranda_baja':'inferior izquierda','manual_pad':'borde inferior','cajon':'limite con cancha','cajon_largo_m':2.5,'baranda_largo_m':3,'altura_obstaculos_m':.4,'dimensiones_restantes':'estimadas','imagenes_integradas':True},indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'El_Japon_Planta_Corregida.blend'))
print('PLANTA CORREGIDA GUARDADA')
