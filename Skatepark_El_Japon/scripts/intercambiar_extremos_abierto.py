import bpy, math, json
from pathlib import Path
from mathutils import Matrix, Vector
p=Path(bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p.with_name('El_Japon_antes_intercambio_extremos.blend')),copy=True)
ap=('Caseta del parque','Caseta |','Bank frontal |','Quarter del fondo frontal','BARANDA INCLINADA |','Baranda inclinada |','Cajon inclinado','Escalon bajo transversal')
bp=('Quarter derecho y lateral |','Quarter esquina curva |','Quarter central bajo |','Bank del mural |')
a=[o for o in bpy.context.scene.objects if o.name.startswith(ap)]
b=[o for o in bpy.context.scene.objects if o.name.startswith(bp)]
assert len(a)>=10 and len(b)>=4
def bounds(obs):
 pts=[o.matrix_world@Vector(v) for o in obs for v in o.bound_box]
 return [[min(v[i] for v in pts),max(v[i] for v in pts)] for i in range(3)]
beforeA=bounds(a); beforeB=bounds(b)
offset=beforeA[1][0]+beforeB[1][1]
T=Matrix.Translation((0,offset,0))@Matrix.Rotation(math.pi,4,'Z')
obs=a+b; saved={o:o.matrix_world.copy() for o in obs}
# Parent transforms carry children such as the continuous coping exactly once.
for o in obs:
 if o.parent not in saved: o.matrix_world=T@saved[o]
bpy.context.view_layer.update()
errors={o.name:max(abs(o.matrix_world[i][j]-(T@saved[o])[i][j]) for i in range(4) for j in range(4)) for o in obs}
assert max(errors.values())<.0001,errors
for o in bpy.context.selected_objects:o.select_set(False)
for o in obs:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Caseta del parque']
report={'grupo_caseta':[o.name for o in a],'grupo_quarters':[o.name for o in b],'antes_caseta':beforeA,'antes_quarters':beforeB,'despues_caseta':bounds(a),'despues_quarters':bounds(b),'error_transformacion_maximo':max(errors.values())}
p.with_name('intercambio_extremos_verificacion.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
area=bpy.context.area
# Restore viewport and save after the console command has returned.
def finish():
 area.type='VIEW_3D'; sp=area.spaces.active; r=sp.region_3d
 target=Vector((0,0,.5)); eye=Vector((24,-29,27))
 r.view_rotation=(target-eye).to_track_quat('-Z','Y'); r.view_location=target; r.view_distance=39
 sp.overlay.show_extras=False
 bpy.ops.wm.save_as_mainfile(filepath=str(p))
 return None
bpy.app.timers.register(finish,first_interval=.7)
print('INTERCAMBIO VERIFICADO:',len(obs),'objetos; guardando escena')
