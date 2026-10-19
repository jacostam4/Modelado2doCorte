import bpy
from pathlib import Path
s=bpy.context.scene;p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name(p.stem+'_antes_transicion.blend')),copy=True)
a=bpy.data.objects['CAM INTRO | recorrido general 8s'];b=bpy.data.objects['CAM RONDA | patinando por Japon']
s.frame_set(240);start=a.location.copy();qa=a.rotation_quaternion.copy()
s.frame_set(241);end=b.location.copy();qb=b.rotation_quaternion.copy()
# Shift all channels of the round forward by four seconds.
action=b.animation_data.action
for layer in action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:
     k.co.x+=120;k.handle_left.x+=120;k.handle_right.x+=120
for m in s.timeline_markers:
 if m.name.startswith('RONDA |'):m.frame+=120
d=bpy.data.cameras.new('Transicion | descenso suave');c=bpy.data.objects.new('CAM TRANSICION | aereo a patinador',d);b.users_collection[0].objects.link(c);c.rotation_mode='QUATERNION';d.clip_start=.05;d.clip_end=500
for f in range(240,362):
 t=(f-240)/121;u=t*t*t*(10+t*(-15+6*t))
 c.location=start.lerp(end,u);c.rotation_quaternion=qa.slerp(qb,u);d.lens=a.data.lens+(b.data.lens-a.data.lens)*u
 c.keyframe_insert(data_path='location',frame=f)
 c.keyframe_insert(data_path='rotation_quaternion',frame=f)
 d.keyframe_insert(data_path='lens',frame=f)
s.timeline_markers.new('TRANSICION | descenso a la pista',frame=241).camera=c
s.use_preview_range=True;s.frame_preview_start=1;s.frame_preview_end=840;s.frame_set(1);s.camera=a
area=bpy.context.area
def finish():
 area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
print('TRANSICION LISTA: INTRO 1-240, DESCENSO 241-360, RONDA 361-840')
