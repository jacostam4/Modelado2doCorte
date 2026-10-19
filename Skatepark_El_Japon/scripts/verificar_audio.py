import bpy,json
from pathlib import Path
s=bpy.context.scene
out=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
print('SOUND_CHECK',[(x.name,x.volume,x.frame_final_start,x.frame_final_end) for x in s.sequence_editor.strips])
bpy.ops.sound.mixdown(filepath=str(out/'audio_verificacion_blender.wav'),container='WAV',codec='PCM',format='S16',mixrate=48000)
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.resolution_x=480;s.render.resolution_y=270;s.render.resolution_percentage=100
s.render.engine='CYCLES';s.cycles.samples=4;s.frame_set(1375)
s.render.filepath=str(out/'audio_render_verificacion.png');bpy.ops.render.render(write_still=True)
print('VERIFICACION_AUDIO_COMPLETA')
