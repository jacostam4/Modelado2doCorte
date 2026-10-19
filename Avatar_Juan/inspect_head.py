import bpy,json
from mathutils import Vector
r=[]
for o in bpy.context.scene.objects:
 r.append({'name':o.name,'type':o.type,'loc':list(o.location),'rot':list(o.rotation_euler),'dim':list(o.dimensions),'min':[min((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)],'max':[max((o.matrix_world@Vector(v))[i] for v in o.bound_box) for i in range(3)]})
print('DATA',json.dumps(r))
