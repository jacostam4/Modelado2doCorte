import bpy,json
from pathlib import Path
s=bpy.context.scene
q=s.sequence_editor
folder=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\audio')
s.render.use_sequencer=True
s.render.image_settings.media_type='VIDEO'
s.render.image_settings.file_format='FFMPEG'
s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264'
s.render.ffmpeg.audio_codec='AAC';s.render.ffmpeg.audio_bitrate=192
s.render.ffmpeg.audio_mixrate=48000;s.render.ffmpeg.audio_channels='STEREO'
s.render.ffmpeg.constant_rate_factor='HIGH'
s.render.filepath=str(Path(bpy.data.filepath).parent/'El_Japon_Final_con_audio.mp4')
s.sync_mode='AUDIO_SYNC'
if hasattr(s,'use_audio'):s.use_audio=True
if hasattr(s,'use_audio_scrub'):s.use_audio_scrub=True
s.frame_set(1261)
report={'fps':s.render.fps,'end':s.frame_end,'audio_codec':s.render.ffmpeg.audio_codec,'video_format':s.render.image_settings.file_format,'strips':[(a.name,a.frame_final_start,a.frame_final_end,a.sound.filepath) for a in q.strips if a.type=='SOUND']}
(folder/'Blender_audio_integrado.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
area=bpy.context.area
def finish():
 area.type='VIEW_3D';area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.app.timers.register(finish,first_interval=1)
print('AUDIO INTEGRADO: 3 pistas, 60 segundos, exportacion MP4 con AAC')

