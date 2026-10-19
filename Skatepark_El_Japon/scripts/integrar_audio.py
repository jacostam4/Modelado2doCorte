import bpy,json
from pathlib import Path
s=bpy.context.scene
folder=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\audio')
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_antes_audio.blend')),copy=True)
assert abs(s.render.fps/s.render.fps_base-30)<.001
q=s.sequence_editor_create()
assert not any(a.name.startswith('AUDIO |') for a in q.strips),'Audio ya incorporado'
base=max([a.channel for a in q.strips]+[0])
for i,(name,file) in enumerate([
 ('Boom bap original 88 BPM','01_BoomBap_88BPM_60s.wav'),
 ('Ruedas sobre concreto','02_Ruedas_sincronizadas_60s.wav'),
 ('Pop slide flip aterrizajes','03_Trucos_sincronizados_60s.wav')],1):
 strip=q.strips.new_sound('AUDIO | '+name,str(folder/file),channel=base+i,frame_start=1)
 strip.volume=1;strip.sound.filepath=bpy.path.relpath(str(folder/file));strip.show_waveform=True
 if hasattr(strip.sound,'pack'):strip.sound.pack()
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

