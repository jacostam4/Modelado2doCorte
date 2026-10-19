import bpy,math
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
s=bpy.context.scene;r=bpy.data.objects['Armature'];board=bpy.data.objects['SKATE | control general'];rail=bpy.data.objects['BARANDA BAJA | BS-FS boardslide']
out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')

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

s.frame_set(1500)
start=board.location.copy();oldcam=bpy.data.objects['CAM TRUCO | Nollie BS Lipslide']
cam=bpy.data.objects.get('CAM FINAL | Kickflip y piso');cam.rotation_mode='QUATERNION';cam.matrix_world=oldcam.matrix_world.copy()
camstart=cam.location.copy();qstart=cam.rotation_quaternion.copy()
wheels=[(o,o.matrix_basis.copy(),1 if o.matrix_basis.to_3x3().col[2].x>0 else -1) for o in board.children if o.name.startswith('RUEDA ')]
# frame, z, pitch, roll, hip height, arm spread, foot clearance, flick
keys=[(1500,.004,0,0,.90,.05,0,0),(1535,.004,0,0,.61,.15,0,0),(1544,.004,0,0,.57,.25,0,0),(1549,.065,23,0,.77,.6,0,0),(1555,.32,9,45,.70,.95,.14,.14),(1562,.49,0,180,.68,1,.22,.18),(1569,.43,0,320,.67,1,.13,.08),(1574,.29,0,360,.68,.85,0,0),(1583,.004,0,360,.59,.5,0,0),(1596,.004,0,360,.77,.25,0,0),(1645,.004,0,360,.90,.05,0,0),(1800,.004,0,360,.90,.05,0,0)]
def value(f,i):
 for a,b in zip(keys,keys[1:]):
  if f<=b[0]:
   t=smooth((f-a[0])/(b[0]-a[0]));return a[i]+(b[i]-a[i])*t
 return keys[-1][i]
for f in range(1501,1801):
 s.frame_set(f)
 z,pitch,roll,hipheight,spread,clearance,flick=[value(f,i) for i in range(1,8)]
 # Continue forward, then gently slow before the hut.
 t=min(1,(f-1500)/180);travel=3.05*(2*t-t*t)
 pos=Vector((start.x,start.y+travel,z))
 board.matrix_world=Matrix.Translation(pos)@Matrix.Rotation(math.radians(pitch),4,'X')@Matrix.Rotation(math.radians(-roll),4,'Y')
 for path in ('location','rotation_quaternion'):board.keyframe_insert(data_path=path,frame=f)
 for wheel,rest,sign in wheels:
  wheel.matrix_basis=rest@Matrix.Rotation(-sign*travel/.027,4,'Z');wheel.keyframe_insert(data_path='rotation_quaternion',frame=f)
 r.location=(pos.x,pos.y,z+.09);r.rotation_euler=(0,0,-math.pi/2)
 for p in r.pose.bones:p.matrix_basis=Matrix.Identity(4);p.rotation_mode='QUATERNION'
 hip=r.pose.bones['Hips'];m=hip.bone.matrix_local.copy();m.translation=Vector((0,.025,hipheight));hip.matrix=m;bpy.context.view_layer.update()
 # Feet leave the deck during its longitudinal flip; right foot flicks off the edge.
 footframe=Matrix.Translation(pos)@Matrix.Rotation(math.radians(pitch),4,'X')
 for side,by in [('Left',-.235),('Right',.285)]:
  ankleworld=footframe@Vector((-flick if side=='Right' else .025*spread,by,.185+clearance))
  ankle=r.matrix_world.inverted()@ankleworld
  ik(side+'UpLeg',side+'Leg',ankle,((.24 if side=='Left' else -.29),-.50,hipheight-.22))
  aim(side+'Foot',r.pose.bones[side+'Foot'].head+Vector((0,-.14,-.076)))
 lean=math.radians(5+18*(.9-hipheight)/.32)
 p=r.pose.bones['Spine'];m=p.matrix.copy();p.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(lean,4,'X')@m.to_3x3().to_4x4();bpy.context.view_layer.update()
 for side,sign in [('Left',1),('Right',-1)]:
  ik(side+'Arm',side+'ForeArm',(sign*(.27+.32*spread),-.12+.1*spread,hipheight+.06+.50*spread),(sign*.55,.05,hipheight+.22))
  fore=r.pose.bones[side+'ForeArm'];aim(side+'Hand',r.pose.bones[side+'Hand'].head+(fore.tail-fore.head).normalized()*.07+Vector((0,0,-.012)))
 p=r.pose.bones['Head'];m=p.matrix.copy();p.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(math.radians(-35),4,'Z')@Matrix.Rotation(math.radians(10),4,'X')@m.to_3x3().to_4x4()
 for path in ('location','rotation_euler'):r.keyframe_insert(data_path=path,frame=f)
 for p in r.pose.bones:
  p.keyframe_insert(data_path='rotation_quaternion',frame=f)
  if p.name=='Hips':p.keyframe_insert(data_path='location',frame=f)
 cam.location=camstart+Vector((0,travel,0))
 target=Vector((pos.x,pos.y,z+.85))
 q=(target-cam.location).to_track_quat('-Z','Y')
 # Last four seconds tilt progressively toward the pavement, finishing with a hold.
 u=smooth(max(0,min(1,(f-1650)/120)))
 down=(Vector((cam.location.x+.12,cam.location.y+.12,.02))-cam.location).to_track_quat('-Z','Y')
 cam.rotation_quaternion=q.slerp(down,u)
 cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_quaternion',frame=f)
for ob in (r,board,cam,*[x[0] for x in wheels]):
 if ob.animation_data and ob.animation_data.action:
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:
       if k.co.x>=1500:k.interpolation='LINEAR'
s.timeline_markers.new('KICKFLIP | clip final 10s',frame=1501).camera=cam
for name,f in [('KICKFLIP | pop',1549),('KICKFLIP | giro completo',1574),('KICKFLIP | aterrizaje',1583),('CIERRE | camara al piso',1650)]:s.timeline_markers.new(name,frame=f)
s.frame_end=1800;s.frame_preview_end=1800;s.frame_set(1562);s.camera=cam
if not bpy.app.background:
 area=bpy.context.area
 def finish():
  area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
  bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);return None
 bpy.app.timers.register(finish,first_interval=1)
print('KICKFLIP Y CIERRE CREADOS: 1501-1800')

