import bpy,time,json
from pathlib import Path
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='CUDA';p.get_devices()
for d in p.devices:d.use=d.type=='CUDA' and '1650' in d.name
print('DEVICES',[(d.name,d.type,d.use) for d in p.devices],flush=True)
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.frame_set(1);s.render.filepath=r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\prueba_GPU_1080.png'
t=time.perf_counter();bpy.ops.render.render(write_still=True)
Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\prueba_GPU.json').write_text(json.dumps({'seconds':time.perf_counter()-t,'device':s.cycles.device,'samples':s.cycles.samples,'resolution':[s.render.resolution_x,s.render.resolution_y]}))
