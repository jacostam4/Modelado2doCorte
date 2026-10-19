import bpy,json
from pathlib import Path
s=bpy.context.scene
bpy.ops.wm.save_as_mainfile(filepath=str(Path(bpy.data.filepath).with_name('El_Japon_antes_config_GPU.blend')),copy=True)
p=bpy.context.preferences.addons['cycles'].preferences
p.compute_device_type='CUDA';p.get_devices()
for d in p.devices:d.use=d.type=='CUDA' and '1650' in d.name
assert any(d.use for d in p.devices),'GTX 1650 CUDA no disponible'
s.render.engine='CYCLES';s.cycles.device='GPU';s.cycles.samples=32;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.05;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE'
s.cycles.preview_samples=32
s.cycles.max_bounces=6;s.cycles.diffuse_bounces=3;s.cycles.glossy_bounces=3;s.cycles.transmission_bounces=4
s.render.use_motion_blur=False;s.render.use_persistent_data=False
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=30;s.render.fps_base=1;s.frame_start=1;s.frame_end=1800;s.frame_set(1)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.audio_codec='AAC';s.render.ffmpeg.audio_bitrate=192
bpy.ops.wm.save_userpref()
a=bpy.context.area
def finish():
 a.type='VIEW_3D';a.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.app.timers.register(finish,first_interval=1)
print('CONFIGURADO GTX1650 CUDA 1080p 32 samples denoise')
