import bpy,json
s=bpy.context.scene
print('SETTINGS',json.dumps({'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'samples':s.cycles.samples,'device':s.cycles.device,'denoising':s.cycles.use_denoising}))
