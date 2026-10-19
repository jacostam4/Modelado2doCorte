import bpy
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
for ob in [s,s.eevee] if hasattr(s,'eevee') else [s]:
 print(type(ob).__name__,[p.identifier for p in ob.bl_rna.properties if any(t in p.identifier for t in ['sample','ray','taa'])])
