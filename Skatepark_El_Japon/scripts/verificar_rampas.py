import bpy
s=bpy.context.scene;s.frame_set(121)
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.render.filepath=r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\rampas_render_corregido.png'
bpy.ops.render.render(write_still=True)
