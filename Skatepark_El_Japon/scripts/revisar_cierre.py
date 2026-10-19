import bpy
from pathlib import Path
s=bpy.context.scene;out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
s.render.engine='CYCLES';s.cycles.samples=12
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
for f in (960,1018,1260):
 s.frame_set(f);s.camera=bpy.data.objects['CAM CIERRE | Juan taza y tabla'];s.render.filepath=str(out/f'cierre_{f}.png');bpy.ops.render.render(write_still=True)
