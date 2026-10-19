import bpy,math,sys
from mathutils import Vector,Matrix,Quaternion
from pathlib import Path
s=bpy.context.scene;r=bpy.data.objects['Armature'];mug=bpy.data.objects['Mug | Mug']
out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
def smooth(t):
 t=max(0,min(1,t));return t*t*t*(10+t*(-15+6*t))
def bones_key(f):
 for p in r.pose.bones:
  p.keyframe_insert(data_path='rotation_quaternion',frame=f)
  if p.name=='Hips':p.keyframe_insert(data_path='location',frame=f)
def aim(name,target):
 p=r.pose.bones[name];bpy.context.view_layer.update()
 mat=p.matrix.copy();q=mat.to_3x3().col[1].normalized().rotation_difference((Vector(target)-mat.translation).normalized())
 p.matrix=Matrix.Translation(mat.translation)@q.to_matrix().to_4x4()@mat.to_3x3().to_4x4()
 bpy.context.view_layer.update()
def ik(upper,lower,target,pole):
 bpy.context.view_layer.update();a=r.pose.bones[upper].head.copy();target=Vector(target);delta=target-a;dist=delta.length;u=delta.normalized()
 la=r.data.bones[upper].length;lb=r.data.bones[lower].length;dist=min(dist,la+lb-.001)
 x=(la*la-lb*lb+dist*dist)/(2*dist);height=math.sqrt(max(0,la*la-x*x))
 v=Vector(pole)-a;v=(v-u*v.dot(u)).normalized();elbow=a+u*x+v*height
 aim(upper,elbow);aim(lower,target)
if r.animation_data and r.animation_data.action:r.animation_data.action.use_fake_user=True
r.animation_data_clear();r.rotation_mode='XYZ';r.rotation_euler=(0,0,-math.pi/2);r.location=(7.37,.32,0)
for p in r.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis=Matrix.Identity(4)
# Hide the previous procedural avatar if it is still in the scene.
old=bpy.data.collections.get('14 | Juan avatar inicial')
if old:old.hide_render=True;old.hide_viewport=True
cupscale=mug.matrix_world.to_scale().copy()
if mug.animation_data and mug.animation_data.action:mug.animation_data.action.use_fake_user=True
mug.animation_data_clear();mug.parent=None;mug.rotation_mode='QUATERNION'
# Original mug spans local Z 0..2.5337. Its handle extends along local Y.
def pose(f,drink=0,look=0):
 s.frame_set(f)
 for p in r.pose.bones:p.matrix_basis=Matrix.Identity(4)
 hip=r.pose.bones['Hips'];mat=hip.bone.matrix_local.copy();mat.translation=Vector((0,0,.515));hip.matrix=mat
 bpy.context.view_layer.update()
 for side,sign in [('Left',1),('Right',-1)]:
  ik(side+'UpLeg',side+'Leg',(sign*.14,-.46,.095),(sign*.2,-1,.5))
  aim(side+'Foot',r.pose.bones[side+'Foot'].head+Vector((0,-.14,-.076)))
 # Small torso turn precedes the gaze toward the skateboard.
 for name,angle in [('Spine2',-10*look),('Neck',-18*look),('Head',-37*look)]:
  p=r.pose.bones[name];mat=p.matrix.copy();p.matrix=Matrix.Translation(mat.translation)@Matrix.Rotation(math.radians(angle),4,'Z')@mat.to_3x3().to_4x4();bpy.context.view_layer.update()
 ik('LeftArm','LeftForeArm',(.16,-.30,.58),(.40,-.1,.78));aim('LeftHand',r.pose.bones['LeftHand'].head+Vector((0,-.07,-.03)))
 wrist=Vector((-.22,-.31,.88)).lerp(Vector((-.08,-.18,1.08)),drink)
 ik('RightArm','RightForeArm',wrist,(-.50,-.18,.88));aim('RightHand',wrist+Vector((.07,-.025,.015)))
 # Curl the fingers around the handle, preserving the thumb opposition.
 for p in r.pose.bones:
  if p.name.startswith('RightHand') and any(x in p.name for x in ('Index','Middle','Ring','Pinky')):
   p.rotation_quaternion=Quaternion((1,0,0),math.radians(48 if p.name.endswith('1') else 65))
  elif p.name.startswith('RightHandThumb'):p.rotation_quaternion=Quaternion((0,0,1),math.radians(-20))
 bpy.context.view_layer.update();bones_key(f)
 # Cup follows the same hand trajectory with its rim near the mouth at the peak.
 center=wrist+Vector((.085,-.035,-.045))
 rot=Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Rotation(math.radians(-13*drink),4,'X')
 mug.matrix_world=Matrix.Translation(r.matrix_world@center)@r.matrix_world.to_3x3().to_4x4()@rot@Matrix.Diagonal((*cupscale,1))
 mug.keyframe_insert(data_path='location',frame=f);mug.keyframe_insert(data_path='rotation_quaternion',frame=f);mug.keyframe_insert(data_path='scale',frame=f)
for f,d,l in [(1,0,0),(840,0,0),(960,0,0),(985,.25,0),(1018,1,0),(1042,1,0),(1070,.1,.2),(1095,0,.7),(1120,0,1),(1260,0,1)]:pose(f,d,l)
r.animation_data.action.name='Juan | sentado, taza y mirada al skate'
# Smooth curves with clamped handles prevent overshoot at the mouth and joints.
def curves(id):
 if id.animation_data and id.animation_data.action:
  for layer in id.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
curves(r);curves(mug)
# Bind the actual mug rigidly to the right hand so it cannot drift during interpolation.
s.frame_set(960);bpy.context.view_layer.update();cupworld=mug.matrix_world.copy()
mug.animation_data_clear();mug.parent=r;mug.parent_type='BONE';mug.parent_bone='RightHand';mug.matrix_parent_inverse=Matrix.Identity(4)
handparent=r.matrix_world@r.pose.bones['RightHand'].matrix@Matrix.Translation((0,r.data.bones['RightHand'].length,0))
mug.matrix_basis=handparent.inverted()@cupworld
camera_col=bpy.data.objects['CAM RONDA | patinando por Japon'].users_collection[0]
s.frame_set(840);previous=bpy.data.objects['CAM RONDA | patinando por Japon'];start=previous.matrix_world.translation.copy();qstart=previous.matrix_world.to_quaternion();lens0=previous.data.lens
data=bpy.data.cameras.new('Cierre | taza y skate');cam=bpy.data.objects.new('CAM CIERRE | Juan taza y tabla',data);camera_col.objects.link(cam);cam.rotation_mode='QUATERNION';data.clip_start=.04;data.clip_end=300
portrait=Vector((4.30,-1.65,1.40));focus=Vector((7.27,.30,.94));qportrait=(focus-portrait).to_track_quat('-Z','Y')
board=bpy.data.objects['TABLA | montada con lija'];boardfocus=sum((board.matrix_world@Vector(v) for v in board.bound_box),Vector())/8
end=boardfocus+Vector((1.10,-2.15,.65));qend=(boardfocus-end).to_track_quat('-Z','Y')
data.dof.use_dof=True;data.dof.aperture_fstop=6.3
for f in range(840,1261):
 if f<=960:
  u=smooth((f-840)/120);pos=start.lerp(portrait,u);q=qstart.slerp(qportrait,u);lens=lens0+(48-lens0)*u;dist=(focus-pos).length
 elif f<=1100:
  u=smooth((f-960)/140);pos=portrait.lerp(portrait+Vector((.20,.12,.02)),u);q=(focus-pos).to_track_quat('-Z','Y');lens=48;dist=(focus-pos).length
 else:
  u=smooth((f-1100)/130);a=portrait+Vector((.20,.12,.02));pos=a.lerp(end,u)
  # Broad arc stays within the open skating area.
  pos.x-=1.2*math.sin(math.pi*u);target=focus.lerp(boardfocus,u);q=(target-pos).to_track_quat('-Z','Y');lens=48+(55-48)*u;dist=(target-pos).length
 cam.location=pos;cam.rotation_quaternion=q;data.lens=lens;data.dof.focus_distance=dist
 cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_quaternion',frame=f);data.keyframe_insert(data_path='lens',frame=f);data.keyframe_insert(data_path='dof.focus_distance',frame=f)
s.timeline_markers.new('CIERRE | acercamiento al cajon',frame=841).camera=cam
for name,f in [('JUAN | gesto de beber',960),('JUAN | mira la tabla',1070),('CAMARA | sigue la mirada',1100),('FINAL | skate junto a caseta',1230)]:s.timeline_markers.new(name,frame=f)
s.frame_end=1260;s.use_preview_range=True;s.frame_preview_start=1;s.frame_preview_end=1260
s.frame_set(1018);s.camera=cam
if bpy.app.background:
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'cierre_revision.blend'))
else:
 area=bpy.context.area
 def finish():
  area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
  bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);return None
 bpy.app.timers.register(finish,first_interval=1)
print('CIERRE CREADO: 841-1260; sentado, taza, mirada, tabla')
