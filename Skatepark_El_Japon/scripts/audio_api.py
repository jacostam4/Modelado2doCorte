import bpy
s=bpy.context.scene
for ob in [s.render,s.render.image_settings,s.render.ffmpeg]:
 for p in ob.bl_rna.properties:
  if p.type=='ENUM': print(type(ob).__name__,p.identifier,[(i.identifier,i.name) for i in p.enum_items])
