import bpy
from mathutils import Vector
def mat(name,color,rough):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
 return m
white=mat('Nieve | blanco',(.92,.95,1),.8)
black=mat('Sombrero ojos botones | negro',(.008,.008,.01),.55)
orange=mat('Nariz | naranja',(.95,.19,.008),.55)
red=mat('Bufanda | roja',(.65,.008,.018),.8)
ceramic=mat('Mug | ceramica roja completa',(.65,.008,.015),.22)
objs=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 if o.name.startswith('Mug |'):m=ceramic
 elif o.name.startswith('Muneco de nieve | '):
  part=o.name.split(' | ',1)[1]
  m=orange if part=='Cone' else red if part in ('Circle.001','Circle.002') else black if part in ('Circle','Sphere.002','Sphere.003','Sphere.004','Sphere.005') else white
 else:continue
 o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(m)
 for f in o.data.polygons:f.material_index=0
 objs.append(o)
area=bpy.context.area
def finish():
 area.type='VIEW_3D';sp=area.spaces.active;sp.shading.type='MATERIAL'
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);return None
bpy.app.timers.register(finish,first_interval=.7)
print('COLORES APLICADOS',len(objs))
