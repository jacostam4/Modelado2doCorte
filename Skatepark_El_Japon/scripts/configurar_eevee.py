import bpy
from pathlib import Path
s=bpy.context.scene
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_respaldo_Cycles.blend')),copy=True)
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.eevee.taa_samples=16;s.eevee.use_raytracing=False
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_motion_blur=False
s.render.fps=30;s.render.fps_base=1;s.frame_start=1;s.frame_end=1800
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.audio_codec='AAC';s.render.ffmpeg.audio_bitrate=192
s.render.filepath=str(Path(bpy.data.filepath).parent/'El_Japon_EEVEE_720p_con_audio.mp4')
a=bpy.context.area
def done():
 a.type='VIEW_3D'
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.app.timers.register(done,first_interval=1)
print('EEVEE 720p 32 samples 30fps audio AAC listo')
