import bpy,traceback,pathlib
from bl_ext.user_default.keentools.facebuilder.fbloader import FBLoader as L
from bl_ext.user_default.keentools.facebuilder.head import MESH_OT_FBAddHead
from bl_ext.user_default.keentools.addon_config import fb_settings
from bl_ext.user_default.keentools.utils.images import load_rgba
from bl_ext.user_default.keentools.utils.coords import update_head_mesh_non_neutral
base=pathlib.Path(__file__).resolve().parent
try:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 s=fb_settings(); obj=MESH_OT_FBAddHead.new_head();bpy.context.scene.collection.objects.link(obj) if not obj.users_collection else None
 h=s.heads.add();h.headobj=obj;h.reset_sensor_size();s.current_headnum=0
 fb=L.get_builder()
 print('LICENSE',fb.license_manager(),flush=True)
 for n in (4551,):
  cam=L.add_new_camera_with_image(0,str(base/'referencias'/f'IMG_{n}.jpg'))
  img=load_rgba(cam)
  faces=fb.detect_faces(img,fb.pixel_aspect_ratio(cam.get_keyframe()))
  print('DETECTED',n,len(faces),flush=True)
  if faces:
   ok=fb.detect_face_pose(cam.get_keyframe(),faces[0]);print('POSE',ok,flush=True)
   if ok: fb.add_preset_pins_and_solve(cam.get_keyframe())
 update_head_mesh_non_neutral(fb,h)
 L.update_camera_pins_count(0,0);L.place_camera(0,0);L.update_all_camera_focals(0);L.save_fb_serial_and_image_pathes(0)
 print('CAMERA',list(cam.camobj.location),list(cam.camobj.rotation_euler),cam.camobj.data.lens,flush=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(base/'Juan_Rostro_FaceBuilder.blend'))
 print('SUCCESS',flush=True)
except Exception:traceback.print_exc()
