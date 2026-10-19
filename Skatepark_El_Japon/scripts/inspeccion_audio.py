import bpy,json
s=bpy.context.scene
q=s.sequence_editor
print('AUDIO_INSPECT',json.dumps({'fps':s.render.fps,'fps_base':s.render.fps_base,'start':s.frame_start,'end':s.frame_end,'sequence':[(a.name,a.type) for a in q.strips] if q else [],'audio_codec':s.render.ffmpeg.audio_codec,'ffmpeg_format':s.render.ffmpeg.format,'image_format':s.render.image_settings.file_format,'markers':[(m.name,m.frame) for m in s.timeline_markers if m.frame>=1260]}))
q=s.sequence_editor_create();print('NEW_SOUND_DOC',q.strips.bl_rna.functions['new_sound'].description)
print('SOUND_PACK',hasattr(bpy.types.Sound,'pack'))
