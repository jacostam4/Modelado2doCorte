import bpy
from pathlib import Path
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_antes_reparar_visibilidad.blend')),copy=True)
for name in ['Media piramide | skatepark - cancha','Quarter central bajo | mural','Quarter central bajo | mural | coping','Quarter derecho y lateral | esquina curva']:
 o=bpy.data.objects[name];o.hide_render=False
 print('VISIBLE EN RENDER',name)
a=bpy.context.area
def done():
 a.type='VIEW_3D'
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.app.timers.register(done,first_interval=1)
