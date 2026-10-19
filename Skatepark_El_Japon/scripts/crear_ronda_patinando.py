import bpy,math,json
from pathlib import Path
from mathutils import Vector
s=bpy.context.scene;p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_ronda.blend')),copy=True)
col=bpy.data.collections.new('RONDA | camara a nivel de patinador');s.collection.children.link(col)
d=bpy.data.cameras.new('Ronda | gran angular 20mm');d.lens=20;d.clip_start=.05;d.clip_end=300
c=bpy.data.objects.new('CAM RONDA | patinando por Japon',d);col.objects.link(c);c.rotation_mode='QUATERNION'
# Arc-length sampling keeps the skating speed constant through the oval.
points=[Vector((3.8*math.cos(i*2*math.pi/4000),-1-7*math.sin(i*2*math.pi/4000),1.62)) for i in range(4001)]
lengths=[0.0]
for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+(b-a).length)
import bisect
def pos(distance):
 distance%=lengths[-1];i=bisect.bisect_right(lengths,distance)-1
 return points[i].lerp(points[i+1],(distance-lengths[i])/(lengths[i+1]-lengths[i]))
last=None
for f in range(241,721):
 distance=(f-241)/479*lengths[-1]
 eye=pos(distance);target=pos(distance+2.8);target.z=1.35
 c.location=eye;q=(target-eye).to_track_quat('-Z','Y')
 if last is not None and q.dot(last)<0:q.negate()
 c.rotation_quaternion=q;last=q.copy()
 c.keyframe_insert(data_path='location',frame=f,group='Ronda a velocidad constante')
 c.keyframe_insert(data_path='rotation_quaternion',frame=f,group='Mirada hacia el recorrido')
c['descripcion']='Ronda en primera persona, altura 1.62 m, 16 segundos. Trayectoria central alrededor de los obstaculos.'
s.timeline_markers.new('RONDA | patinando de cerca',frame=241).camera=c
s.timeline_markers.new('RONDA | vuelta completa',frame=720)
s.frame_end=max(s.frame_end,720);s.use_preview_range=True;s.frame_preview_start=241;s.frame_preview_end=720
s.frame_set(241);s.camera=c
for o in bpy.context.selected_objects:o.select_set(False)
c.select_set(True);bpy.context.view_layer.objects.active=c
out=p.parent/'animacion_intro';out.mkdir(exist_ok=True)
(out/'ronda.json').write_text(json.dumps({'inicio':241,'fin':720,'segundos':16,'altura_m':1.62,'longitud_m':lengths[-1],'velocidad_m_s':lengths[-1]/16},indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.region_3d.view_camera_zoom=12
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('RONDA CREADA 241-720')
