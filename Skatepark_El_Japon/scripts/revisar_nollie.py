import bpy
from pathlib import Path
s=bpy.context.scene;p=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
s.render.engine='CYCLES';s.cycles.samples=10;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
for f in (1333,1357,1375,1410):
 s.frame_set(f);s.camera=bpy.data.objects['CAM TRUCO | Nollie BS Lipslide'];s.render.filepath=str(p/f'nollie_{f}.png');bpy.ops.render.render(write_still=True)
