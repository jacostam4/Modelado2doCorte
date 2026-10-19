import bpy,math
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
s=bpy.context.scene;r=bpy.data.objects['Armature'];board=bpy.data.objects['SKATE | control general'];rail=bpy.data.objects['BARANDA BAJA | BS-FS boardslide']
out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
assert not bpy.data.objects.get('CAM TRUCO | Nollie BS Lipslide'),'Truco ya creado'
def smooth(t):return t*t*(3-2*t)
def mixvalue(f,keys,index):
 if f<=keys[0][0]:return keys[0][index]
 for a,b in zip(keys,keys[1:]):
  if f<=b[0]:
   u=(f-a[0])/(b[0]-a[0]);u=smooth(u) if index!=2 else u
   return a[index]+(b[index]-a[index])*u
 return keys[-1][index]
def aim(name,target):
 p=r.pose.bones[name];bpy.context.view_layer.update();m=p.matrix.copy()
 q=m.to_3x3().col[1].normalized().rotation_difference((Vector(target)-m.translation).normalized())
 p.matrix=Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@m.to_3x3().to_4x4();bpy.context.view_layer.update()
def ik(upper,lower,target,pole):
 a=r.pose.bones[upper].head.copy();delta=Vector(target)-a;d=min(delta.length,r.data.bones[upper].length+r.data.bones[lower].length-.001);u=delta.normalized()
 la=r.data.bones[upper].length;lb=r.data.bones[lower].length;x=(la*la-lb*lb+d*d)/(2*d);h=math.sqrt(max(0,la*la-x*x))
 v=Vector(pole)-a;v=(v-u*v.dot(u)).normalized();aim(upper,a+u*x+v*h);aim(lower,target)
s.frame_set(1260)
for path in ('location','rotation_euler','scale'):r.keyframe_insert(data_path=path,frame=1260)
board.rotation_mode='QUATERNION'
for path in ('location','rotation_quaternion','scale'):board.keyframe_insert(data_path=path,frame=1260)
wheels=[]
for o in board.children:
 if o.name.startswith('RUEDA '):
  o.rotation_mode='QUATERNION';o.keyframe_insert(data_path='rotation_quaternion',frame=1260)
  wheels.append((o,o.matrix_basis.copy(),1 if o.matrix_basis.to_3x3().col[2].x>0 else -1))
# Cup remains visible throughout the seated scene, then leaves the skating shot.
mug=bpy.data.objects['Mug | Mug']
for f,hide in [(1260,False),(1261,True)]:
 mug.hide_render=hide;mug.hide_viewport=hide;mug.keyframe_insert(data_path='hide_render',frame=f);mug.keyframe_insert(data_path='hide_viewport',frame=f)
rx=rail.matrix_world.translation.x
zrail=max((rail.matrix_world@Vector(v)).z for v in rail.bound_box)
# frame, lateral offset to rail, distance along rail, root height, board yaw, nose pitch, pelvis height, arms out
keys=[(1261,-.56,-5.0,.004,0,0,.88,.05),(1310,-.56,-1.35,.004,0,0,.83,.10),
 (1333,-.54,.0,.004,0,0,.59,.1),(1340,-.53,.32,.004,0,0,.57,.25),
 (1345,-.50,.57,.052,8,-18,.77,.7),(1352,-.33,.93,.48,43,-8,.65,1),
 (1357,-.12,1.17,.56,78,0,.61,1),(1363,0,1.45,zrail-.075,90,0,.68,.95),
 (1383,0,2.60,zrail-.075,90,0,.75,.9),(1392,0,3.12,zrail-.075,90,0,.72,.9),
 (1397,-.06,3.42,.44,65,3,.73,.8),(1404,-.18,3.85,.18,14,2,.66,.55),
 (1410,-.25,4.18,.004,0,0,.60,.4),(1420,-.25,4.75,.004,0,0,.76,.25),
 (1460,-.25,6.80,.004,0,0,.88,.1),(1500,-.25,8.15,.004,0,0,.90,.05)]
camera_data=bpy.data.cameras.new('Truco | seguimiento');cam=bpy.data.objects.new('CAM TRUCO | Nollie BS Lipslide',camera_data);s.collection.objects.link(cam);cam.rotation_mode='QUATERNION';camera_data.lens=38;camera_data.clip_start=.05;camera_data.clip_end=300
for f in range(1261,1501):
 s.frame_set(f)
 x,y,z,yaw,pitch,hipheight,spread=[mixvalue(f,keys,i) for i in range(1,8)]
 yaw=math.radians(yaw);pitch=math.radians(pitch)
 board.matrix_world=Matrix.Translation((rx+x,y,z))@Matrix.Rotation(yaw,4,'Z')@Matrix.Rotation(pitch,4,'X')
 for path in ('location','rotation_quaternion'):board.keyframe_insert(data_path=path,frame=f)
 distance=(y+5) if f<=1345 else (5.57+max(0,y-4.18) if f>=1410 else 5.57)
 for wheel,rest,sign in wheels:
  wheel.matrix_basis=rest@Matrix.Rotation(-sign*distance/.027,4,'Z');wheel.keyframe_insert(data_path='rotation_quaternion',frame=f)
 r.location=(rx+x,y,z+.09);r.rotation_euler=(0,0,yaw-math.pi/2)
 for p in r.pose.bones:p.matrix_basis=Matrix.Identity(4);p.rotation_mode='QUATERNION'
 hip=r.pose.bones['Hips'];m=hip.bone.matrix_local.copy();m.translation=Vector((-.035 if 1333<=f<=1352 else 0,.025,hipheight));hip.matrix=m
 bpy.context.view_layer.update()
 # The right foot stays on the nose: goofy nollie. The tail crosses over the rail during +90 degrees yaw.
 for side,b_y in [('Left',-.235),('Right',.285)]:
  ankle_world=board.matrix_world@Vector((0,b_y,.185))
  ankle=r.matrix_world.inverted()@ankle_world
  ik(side+'UpLeg',side+'Leg',ankle,((.24 if side=='Left' else -.29),-.50,hipheight-.22))
  aim(side+'Foot',r.pose.bones[side+'Foot'].head+Vector((0,-.14,-.076)))
 # Crouch and shoulder wind-up, then arms counterbalance the slide.
 lean=math.radians(5+18*(.9-hipheight)/.32)
 p=r.pose.bones['Spine'];m=p.matrix.copy();p.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(lean,4,'X')@m.to_3x3().to_4x4();bpy.context.view_layer.update()
 for side,sign in [('Left',1),('Right',-1)]:
  wrist=Vector((sign*(.27+.32*spread),-.12+.1*spread,hipheight+.06+.50*spread))
  ik(side+'Arm',side+'ForeArm',wrist,(sign*.55,.05,hipheight+.22))
  fore=r.pose.bones[side+'ForeArm'];hand_direction=(fore.tail-fore.head).normalized()*.07+Vector((0,0,-.012))
  aim(side+'Hand',r.pose.bones[side+'Hand'].head+hand_direction)
 # Head checks the landing while the shoulders remain sideways to the deck.
 p=r.pose.bones['Head'];m=p.matrix.copy();p.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(math.radians(-35 if f<1340 or f>1410 else -10),4,'Z')@Matrix.Rotation(math.radians(10),4,'X')@m.to_3x3().to_4x4()
 for path in ('location','rotation_euler'):r.keyframe_insert(data_path=path,frame=f)
 for p in r.pose.bones:
  p.keyframe_insert(data_path='rotation_quaternion',frame=f)
  if p.name=='Hips':p.keyframe_insert(data_path='location',frame=f)
 # Tracking view from the open side shows both the deck and the bar contact.
 target=Vector((rx+x,y,z+.85));cam.location=Vector((rx-4.1,y-3.7,1.75+z*.35));cam.rotation_quaternion=(target-cam.location).to_track_quat('-Z','Y')
 cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_quaternion',frame=f)
# Dense motion samples use linear interpolation; the prior seated scene remains intact.
for ob in (r,board,cam,mug,*[item[0] for item in wheels]):
 if ob.animation_data and ob.animation_data.action:
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:
       if k.co.x==1260:k.interpolation='CONSTANT'
       elif k.co.x>1260:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
s.timeline_markers.new('TRUCO | aproximacion goofy',frame=1261).camera=cam
for label,f in [('NOLLIE | compresion',1333),('NOLLIE | pop del nose',1345),('BS LIPSLIDE | contacto',1363),('BS LIPSLIDE | salida',1392),('ATERRIZAJE | flexion',1410),('FINAL | rodada',1500)]:s.timeline_markers.new(label,frame=f)
s.frame_end=1500;s.frame_preview_end=1500;s.frame_set(1375);s.camera=cam
if bpy.app.background:bpy.ops.wm.save_as_mainfile(filepath=str(out/'nollie_revision.blend'))
else:
 area=bpy.context.area
 def finish():
  area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
  bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);return None
 bpy.app.timers.register(finish,first_interval=1)
print('NOLLIE BS LIPSLIDE CREADO 1261-1500')
