import bpy, math, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_intro.blend')),copy=True)
col=bpy.data.collections.new('INTRO | recorrido del skatepark')
s.collection.children.link(col)
d=bpy.data.cameras.new('Intro | lente 32mm');d.lens=32;d.clip_end=500
c=bpy.data.objects.new('CAM INTRO | recorrido general 8s',d);col.objects.link(c)
c.rotation_mode='QUATERNION'
s.camera=c
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=30;s.render.fps_base=1
corners=[Vector((x,y,z)) for x in (-8.5,8.5) for y in (-16,15.5) for z in (0,4)]
checks=[]
for f in range(1,241):
 t=(f-1)/239;u=t*t*(3-2*t)
 angle=math.radians(52-30*u);radius=39-8*u
 target=Vector((0,0,.8))
 eye=Vector((radius*math.cos(angle),radius*math.sin(angle),32-8*u))
 c.location=eye;c.rotation_quaternion=(target-eye).to_track_quat('-Z','Y')
 bpy.context.view_layer.update()
 for attempt in range(30):
  nd=[world_to_camera_view(s,c,v) for v in corners]
  if all(.055<=v.x<=.945 and .07<=v.y<=.93 and v.z>0 for v in nd):break
  c.location=target+(c.location-target)*1.025;bpy.context.view_layer.update()
 c.keyframe_insert(data_path='location',frame=f,group='Recorrido suave')
 c.keyframe_insert(data_path='rotation_quaternion',frame=f,group='Mirada al parque')
 if f in (1,120,240):checks.append({'frame':f,'location':list(c.location),'all_park_in_frame':all(0<v.x<1 and 0<v.y<1 for v in nd)})
c['descripcion']='Introduccion de 8 segundos, recorrido aereo suave con todo el skatepark dentro del encuadre.'
s.timeline_markers.new('INTRO | vista general',frame=1).camera=c
s.timeline_markers.new('INTRO | fin 8 segundos',frame=240)
s.use_preview_range=True;s.frame_preview_start=1;s.frame_preview_end=240
s.frame_set(1)
for ob in bpy.context.selected_objects:ob.select_set(False)
c.select_set(True);bpy.context.view_layer.objects.active=c
out=p.parent/'animacion_intro';out.mkdir(exist_ok=True)
(out/'verificacion.json').write_text(json.dumps(checks,indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.region_3d.view_camera_zoom=0
 bpy.ops.wm.save_as_mainfile(filepath=str(p))
 return None
bpy.app.timers.register(finish,first_interval=.7)
print('INTRO CREADA: 1-240, 30 fps',checks)
