import bpy,math,json
from mathutils import Vector
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene;c=s.camera;checks=[]
for f in range(1,241):
 t=(f-1)/239;u=t*t*(3-2*t);a=math.radians(52-30*u);r=39-8*u;target=Vector((0,0,.8))
 c.location=target+(Vector((r*math.cos(a),r*math.sin(a),32-8*u))-target)*1.2
 c.rotation_quaternion=(target-c.location).to_track_quat('-Z','Y')
 c.keyframe_insert(data_path='location',frame=f,group='Recorrido suave')
 bpy.context.view_layer.update()
 checks.append(all(0<v.x<1 and 0<v.y<1 for v in [world_to_camera_view(s,c,Vector((x,y,z))) for x in (-8.5,8.5) for y in (-16,15.5) for z in (0,4)]))
s.frame_set(1)
p=Path(bpy.data.filepath);(p.parent/'animacion_intro'/'verificacion.json').write_text(json.dumps({'frames':240,'fps':30,'encuadre_completo_todos_frames':all(checks),'movimiento':'curva continua smoothstep'},indent=2))
area=bpy.context.area
def finish():
 area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.ops.wm.save_as_mainfile(filepath=str(p));return None
bpy.app.timers.register(finish,first_interval=.7)
