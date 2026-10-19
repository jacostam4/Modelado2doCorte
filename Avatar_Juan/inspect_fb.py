import bpy,traceback
try:
 from bl_ext.user_default.keentools.facebuilder.fbloader import FBLoader
 fb=FBLoader.get_builder()
 print('FB_METHODS',dir(fb))
 print('MESH',len(fb.applied_args_vertices()))
except Exception: traceback.print_exc()
