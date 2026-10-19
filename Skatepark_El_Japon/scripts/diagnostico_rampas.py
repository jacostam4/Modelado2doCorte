import bpy,json
s=bpy.context.scene
for o in s.objects:
 if any(t in o.name.lower() for t in ['quarter','piram','bank','rampa']):
  print(json.dumps({'name':o.name,'hide_render':o.hide_render,'hide_viewport':o.hide_viewport,'hidden':o.hide_get(),'loc':list(o.matrix_world.translation),'collections':[(c.name,c.hide_render,c.hide_viewport) for c in o.users_collection],'animated':bool(o.animation_data)},ensure_ascii=False))
