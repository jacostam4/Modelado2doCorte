# Catálogo de scripts

Cada entrada documenta el archivo conservado, sus importaciones, referencias directas a objetos y efectos detectables por análisis estático. Las listas de objetos y rutas pueden ser parciales: también existen referencias calculadas dinámicamente. No constituyen una prueba de ejecución.

## Skatepark_El_Japon/scripts/agregar_objetos_escenario.py

Integra la colección del skate y objetos mug/muñeco de nieve desde archivos blend existentes.

- Código: [abrir](../Skatepark_El_Japon/scripts/agregar_objetos_escenario.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `CAJON FS 50-50 | tapa`, `Caseta del parque`.
- Funciones: `bounds`, `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\tabla\STYX_Skate_Armado.blend`
  - `C:\Users\juan_\OneDrive\Escritorio\universidad\MUÑECO DE NIEVE.blend`

## Skatepark_El_Japon/scripts/ajustar_cierre_piso.py

Ajuste específico conservado del proceso: ajustar cierre piso. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/ajustar_cierre_piso.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `CAM FINAL | Kickflip y piso`.
- Funciones: `done`.

## Skatepark_El_Japon/scripts/ajustar_detalle_caseta.py

Ajuste específico conservado del proceso: ajustar detalle caseta. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/ajustar_detalle_caseta.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `CAM 02 | Mural y quarters`, `CAM 03 | Cajones y barandas`, `CAM 04 | Planta`, `Cajon inclinado paralelo a bank`, `Caseta del parque`.

## Skatepark_El_Japon/scripts/alargar_obstaculos_piso.py

Ajuste específico conservado del proceso: alargar obstaculos piso. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/alargar_obstaculos_piso.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `BARANDA BAJA | BS-FS boardslide`, `CAJON FS 50-50 | cuerpo`.
- Funciones: `axis_center`, `length`, `stretch`, `finish`.

## Skatepark_El_Japon/scripts/animar_kickflip.py

Anima salto, giro longitudinal completo de la tabla, postura del personaje, ruedas y cámara.

- Código: [abrir](../Skatepark_El_Japon/scripts/animar_kickflip.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Armature`, `BARANDA BAJA | BS-FS boardslide`, `CAM TRUCO | Nollie BS Lipslide`, `SKATE | control general`.
- Funciones: `smooth`, `mixvalue`, `aim`, `ik`, `value`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/animar_nollie_lipslide.py

Calcula poses, trayectoria de tabla, giro de ruedas y cámara para el nollie BS lipslide.

- Código: [abrir](../Skatepark_El_Japon/scripts/animar_nollie_lipslide.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Armature`, `BARANDA BAJA | BS-FS boardslide`, `Mug | Mug`, `SKATE | control general`.
- Funciones: `smooth`, `mixvalue`, `aim`, `ik`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/armar_skate.py

Ensambla madero, trucks y ruedas existentes bajo un control general; prepara lija, rodamientos y separadores.

- Código: [abrir](../Skatepark_El_Japon/scripts/armar_skate.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`, `shutil`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `STYX | TABLA 8.25 x 31.875`, `TR144 v2 | Complete truck 8.002`.
- Funciones: `link`, `material`, `ring`, `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\AppData\Local\Temp\codex-clipboard-55bb50d9-1512-46d8-b189-dab175961432.png`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\STYX_Skate_Armado.blend`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas`

## Skatepark_El_Japon/scripts/audio_api.py

Inspecciona las opciones enumeradas de formato de salida y audio en Blender.

- Código: [abrir](../Skatepark_El_Japon/scripts/audio_api.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/cajon_inclinado_negro.py

Construye o ajusta el cajón inclinado y su acabado negro.

- Código: [abrir](../Skatepark_El_Japon/scripts/cajon_inclinado_negro.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Cajon inclinado paralelo a bank`.
- Funciones: `worn`, `finish`.

## Skatepark_El_Japon/scripts/colorear_mug_nieve.py

Asigna acabados de color al mug y al muñeco de nieve.

- Código: [abrir](../Skatepark_El_Japon/scripts/colorear_mug_nieve.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `mat`, `finish`.

## Skatepark_El_Japon/scripts/complementar_fotos_satelite.py

Añade ajustes y detalles de las fotografías a la planta del escenario.

- Código: [abrir](../Skatepark_El_Japon/scripts/complementar_fotos_satelite.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `BARANDA BAJA | BS-FS boardslide`, `CAJON FS 50-50 | cuerpo`, `CAJON FS 50-50 | tapa`, `CAM 02 | Mural y quarters`, `CAM 03 | Cajones y barandas`, `CAM 04 | Planta`, `Caseta del parque`.
- Funciones: `assign`, `box`, `photo`, `mesh`, `rod`, `camera`.

## Skatepark_El_Japon/scripts/comprobar_fbx.py

Utilidad de inspección, extracción o revisión: comprobar fbx. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/comprobar_fbx.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`, `sys`.
- Efectos relevantes: reinicia o elimina objetos de la escena.

## Skatepark_El_Japon/scripts/conectar_tres_rampas.py

Ajusta la unión de los módulos de rampa.

- Código: [abrir](../Skatepark_El_Japon/scripts/conectar_tres_rampas.py)
- Entorno: Python de Blender.
- Importaciones: `bmesh`, `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Media piramide | skatepark - cancha`, `Quarter central bajo | mural`, `Quarter central bajo | mural | coping`, `Quarter derecho y lateral | esquina curva`.
- Funciones: `mix`, `finish`.

## Skatepark_El_Japon/scripts/configurar_eevee.py

Configura EEVEE, 720p, 30 fps, 1800 fotogramas y salida de video con audio.

- Código: [abrir](../Skatepark_El_Japon/scripts/configurar_eevee.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `done`.

## Skatepark_El_Japon/scripts/configurar_gpu.py

Configura Cycles para la GTX 1650 mediante CUDA y guarda preferencias de usuario.

- Código: [abrir](../Skatepark_El_Japon/scripts/configurar_gpu.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; guarda preferencias de Blender; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/consultar_render.py

Utilidad de inspección, extracción o revisión: consultar render. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/consultar_render.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/convertir_referencias.py

Convierte referencias HEIC y extrae imágenes de videos con FFmpeg.

- Código: [abrir](../Skatepark_El_Japon/scripts/convertir_referencias.py)
- Entorno: Python externo.
- Importaciones: `PIL`, `imageio_ffmpeg`, `json`, `pathlib`, `pillow_heif`, `subprocess`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/corregir_planta_satelital.py

Ajusta la distribución del parque a la referencia satelital.

- Código: [abrir](../Skatepark_El_Japon/scripts/corregir_planta_satelital.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `BARANDA BAJA | BS-FS boardslide`, `CAJON FS 50-50 | cuerpo`.
- Funciones: `move_group`, `orient`.

## Skatepark_El_Japon/scripts/corregir_trucks.py

Corrige orientación de trucks y componentes asociados alrededor de un pivote local.

- Código: [abrir](../Skatepark_El_Japon/scripts/corregir_trucks.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `SKATE | control general`.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/crear_audio.py

Sintetiza una base instrumental de 88 BPM y efectos de skate; produce pistas WAV sincronizadas.

- Código: [abrir](../Skatepark_El_Japon/scripts/crear_audio.py)
- Entorno: Python externo.
- Importaciones: `json`, `numpy`, `pathlib`, `wave`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.
- Funciones: `time`, `band`, `noise`, `norm`, `edge`, `add`, `write`, `hz`, `wood`, `event`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\audio`

## Skatepark_El_Japon/scripts/crear_cierre_avatar.py

Genera poses del personaje, gesto del mug, vínculo a la mano y cámara de la secuencia.

- Código: [abrir](../Skatepark_El_Japon/scripts/crear_cierre_avatar.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`, `pathlib`, `sys`.
- Efectos relevantes: guarda archivos .blend; borra animación de objetos seleccionados por el script; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Armature`, `CAM RONDA | patinando por Japon`, `Mug | Mug`, `TABLA | montada con lija`.
- Funciones: `smooth`, `bones_key`, `aim`, `ik`, `pose`, `curves`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/crear_escenario.py

Genera suelo, perfiles de rampas, obstáculos, cerramientos, contexto, luces y escenas de construcción; inicia una escena vacía.

- Código: [abrir](../Skatepark_El_Japon/scripts/crear_escenario.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `math`, `mathutils`, `pathlib`, `random`.
- Efectos relevantes: guarda archivos .blend; reinicia o elimina objetos de la escena; ejecuta render.
- Objetos requeridos por nombre: `Quarter del fondo frontal`, `Quarter del fondo frontal | coping`.
- Funciones: `place`, `mat`, `photo_mat`, `mesh`, `box`, `rod`, `linked`, `profile_ramp`, `quarter`, `wire_quad`, `line`, `building`, `light`, `camera`.

## Skatepark_El_Japon/scripts/crear_intro.py

Inserta claves de posición y orientación para presentar el parque con una cámara animada.

- Código: [abrir](../Skatepark_El_Japon/scripts/crear_intro.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `bpy_extras`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/crear_ronda_patinando.py

Genera un recorrido de cámara ovalado con muestreo por longitud de arco para mantener velocidad.

- Código: [abrir](../Skatepark_El_Japon/scripts/crear_ronda_patinando.py)
- Entorno: Python de Blender.
- Importaciones: `bisect`, `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `pos`, `finish`.

## Skatepark_El_Japon/scripts/diagnostico_rampas.py

Utilidad de inspección, extracción o revisión: diagnostico rampas. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/diagnostico_rampas.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/eevee_api.py

Inspecciona propiedades de muestreo y trazado disponibles en EEVEE.

- Código: [abrir](../Skatepark_El_Japon/scripts/eevee_api.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/exportar_fbx_completo.py

Exporta el conjunto del escenario a formato FBX.

- Código: [abrir](../Skatepark_El_Japon/scripts/exportar_fbx_completo.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/extraer_detalles_fotos.py

Utilidad de inspección, extracción o revisión: extraer detalles fotos. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/extraer_detalles_fotos.py)
- Entorno: Python externo.
- Importaciones: `PIL`, `pathlib`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.
- Funciones: `patch`.

## Skatepark_El_Japon/scripts/extraer_rampas.py

Utilidad de inspección, extracción o revisión: extraer rampas. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/extraer_rampas.py)
- Entorno: Python externo.
- Importaciones: `imageio_ffmpeg`, `pathlib`, `subprocess`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\Escenario\El_Japon_EEVEE_720p_con_audio.mp4`

## Skatepark_El_Japon/scripts/finalizar_audio.py

Configura exportación MPEG4/H264 con audio AAC estéreo y registra las pistas integradas.

- Código: [abrir](../Skatepark_El_Japon/scripts/finalizar_audio.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\audio`

## Skatepark_El_Japon/scripts/finalizar_planta_corregida.py

Ajuste específico conservado del proceso: finalizar planta corregida. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/finalizar_planta_corregida.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `Bank frontal | plataforma inclinada`, `CAJON FS 50-50 | cuerpo`, `CAM 01 | Vista general`, `CAM 04 | Planta`, `Mural fotografico | despliegue UV`.

## Skatepark_El_Japon/scripts/inspeccionar_cierre.py

Utilidad de inspección, extracción o revisión: inspeccionar cierre. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/inspeccionar_cierre.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend.
- Objetos requeridos por nombre: `Armature`.
- Funciones: `ob`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/inspeccionar_truco.py

Utilidad de inspección, extracción o revisión: inspeccionar truco. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/inspeccionar_truco.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/inspeccion_audio.py

Utilidad de inspección, extracción o revisión: inspeccion audio. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/inspeccion_audio.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Skatepark_El_Japon/scripts/integrar_audio.py

Integra pistas de sonido en el editor de secuencias de Blender.

- Código: [abrir](../Skatepark_El_Japon/scripts/integrar_audio.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\audio`

## Skatepark_El_Japon/scripts/intercambiar_extremos_abierto.py

Ajuste específico conservado del proceso: intercambiar extremos abierto. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/intercambiar_extremos_abierto.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Caseta del parque`.
- Funciones: `bounds`, `finish`.

## Skatepark_El_Japon/scripts/modelar_maletin_rojo.py

Construye el obstáculo rojo a partir de un contorno con aberturas y rotura.

- Código: [abrir](../Skatepark_El_Japon/scripts/modelar_maletin_rojo.py)
- Entorno: Python de Blender.
- Importaciones: `bmesh`, `bpy`, `json`, `mathutils`, `pathlib`, `shutil`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Barrera roja observada`.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\AppData\Local\Temp\codex-clipboard-78f9e171-cb56-42b3-bb80-324ca89e0c35.png`

## Skatepark_El_Japon/scripts/mostrar_componentes.py

Utilidad de inspección, extracción o revisión: mostrar componentes. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/mostrar_componentes.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`.
- Efectos relevantes: depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `reveal`, `finish`.

## Skatepark_El_Japon/scripts/mural_y_media_piramide.py

Ajusta el mural e incorpora la media pirámide.

- Código: [abrir](../Skatepark_El_Japon/scripts/mural_y_media_piramide.py)
- Entorno: Python de Blender.
- Importaciones: `bmesh`, `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Bank del mural | plano inclinado`, `Cancha contigua | asfalto`.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/preparar_texturas.py

Recorta y rectifica regiones de fotografías mediante transformaciones de Pillow para crear imágenes de textura.

- Código: [abrir](../Skatepark_El_Japon/scripts/preparar_texturas.py)
- Entorno: Python externo.
- Importaciones: `PIL`, `pathlib`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.
- Funciones: `patch`.

## Skatepark_El_Japon/scripts/prueba_gpu.py

Renderiza un fotograma de prueba con Cycles y registra tiempo y configuración.

- Código: [abrir](../Skatepark_El_Japon/scripts/prueba_gpu.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`, `time`.
- Efectos relevantes: ejecuta render.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\prueba_GPU.json`
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\prueba_GPU_1080.png`

## Skatepark_El_Japon/scripts/reparar_cabeza.py

Ajuste específico conservado del proceso: reparar cabeza. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/reparar_cabeza.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Muneco de nieve | Sphere`, `Muneco de nieve | Sphere.001`.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/reparar_cabeza_persistente.py

Ajuste específico conservado del proceso: reparar cabeza persistente. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/reparar_cabeza_persistente.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`.
- Efectos relevantes: guarda archivos .blend; borra animación de objetos seleccionados por el script; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `Muneco de nieve | Sphere`, `Muneco de nieve | Sphere.001`.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/reparar_visibilidad_rampas.py

Activa hide_render=False para las rampas identificadas y guarda el escenario.

- Código: [abrir](../Skatepark_El_Japon/scripts/reparar_visibilidad_rampas.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `done`.

## Skatepark_El_Japon/scripts/restaurar_ladrillo.py

Restaura el material de ladrillo del escenario.

- Código: [abrir](../Skatepark_El_Japon/scripts/restaurar_ladrillo.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `CAJON FS 50-50 | cuerpo`.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas\cajon_ladrillo_foto.jpg`

## Skatepark_El_Japon/scripts/revisar_cierre.py

Utilidad de inspección, extracción o revisión: revisar cierre. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/revisar_cierre.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: ejecuta render.
- Objetos requeridos por nombre: `CAM CIERRE | Juan taza y tabla`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/revisar_kickflip.py

Utilidad de inspección, extracción o revisión: revisar kickflip. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/revisar_kickflip.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: ejecuta render.
- Objetos requeridos por nombre: `CAM FINAL | Kickflip y piso`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/revisar_nollie.py

Utilidad de inspección, extracción o revisión: revisar nollie. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/revisar_nollie.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: ejecuta render.
- Objetos requeridos por nombre: `CAM TRUCO | Nollie BS Lipslide`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/suavizar_intro.py

Revisa y suaviza la trayectoria de la introducción.

- Código: [abrir](../Skatepark_El_Japon/scripts/suavizar_intro.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `bpy_extras`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/texturizar_cajon_y_exportar.py

Ajuste específico conservado del proceso: texturizar cajon y exportar. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/texturizar_cajon_y_exportar.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`, `pathlib`, `shutil`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `CAJON FS 50-50 | cuerpo`, `CAJON FS 50-50 | tapa`.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\texturas`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas`

## Skatepark_El_Japon/scripts/transicion_camaras.py

Ajuste específico conservado del proceso: transicion camaras. Requiere el estado previo correspondiente del proyecto.

- Código: [abrir](../Skatepark_El_Japon/scripts/transicion_camaras.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Objetos requeridos por nombre: `CAM INTRO | recorrido general 8s`, `CAM RONDA | patinando por Japon`.
- Funciones: `finish`.

## Skatepark_El_Japon/scripts/unificar_quarter_abierto.py

Unifica la geometría del quarter abierto.

- Código: [abrir](../Skatepark_El_Japon/scripts/unificar_quarter_abierto.py)
- Entorno: Python de Blender.
- Importaciones: `bmesh`, `bpy`, `json`, `math`, `mathutils`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.

## Skatepark_El_Japon/scripts/verificar_audio.py

Utilidad de inspección, extracción o revisión: verificar audio. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/verificar_audio.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`.
- Efectos relevantes: ejecuta render.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon`

## Skatepark_El_Japon/scripts/verificar_rampas.py

Utilidad de inspección, extracción o revisión: verificar rampas. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/verificar_rampas.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`.
- Efectos relevantes: ejecuta render.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon\rampas_render_corregido.png`

## Skatepark_El_Japon/scripts/verificar_y_exportar.py

Utilidad de inspección, extracción o revisión: verificar y exportar. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Skatepark_El_Japon/scripts/verificar_y_exportar.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `pathlib`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `AREA | cielo difuso original`, `AREA | instancia vinculada`, `BARANDA BAJA | BS-FS boardslide`, `CAJON FS 50-50 | cuerpo`, `CAJON FS 50-50 | tapa`, `CAM 01 | Vista general`, `CAM 02 | Mural y quarters`, `LAB | Alt D - cambia ambas`, `LAB | Shift D - color independiente`, `LAB | area original`, `Ladrillo lateral | UV fotografico`.

## Avatar_Juan/construir_rostro.py

Prueba inicial de construcción facial con las API internas de KeenTools FaceBuilder.

- Código: [abrir](../Avatar_Juan/construir_rostro.py)
- Entorno: Python de Blender.
- Importaciones: `bl_ext`, `bpy`, `pathlib`, `traceback`.
- Efectos relevantes: guarda archivos .blend; reinicia o elimina objetos de la escena.

## Avatar_Juan/crear_avatar.py

Construye el avatar inicial sobre una cabeza FaceBuilder existente, con ropa, partes y vínculos.

- Código: [abrir](../Avatar_Juan/crear_avatar.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `bpy_extras`, `math`, `mathutils`, `pathlib`, `random`.
- Efectos relevantes: guarda archivos .blend; ejecuta render.
- Objetos requeridos por nombre: `FBHead`, `fbCamera`.
- Funciones: `register`, `material`, `mesh`, `loft`, `sphere`, `tube`, `bone`, `studio_obj`.

## Avatar_Juan/incorporar_avatar.py

Integra el avatar inicial en el escenario; no representa el avatar final creado en Avaturn.

- Código: [abrir](../Avatar_Juan/incorporar_avatar.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `math`, `mathutils`.
- Efectos relevantes: guarda archivos .blend; depende de un área de la interfaz; no asumir ejecución en background.
- Funciones: `finish`.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\Avatar\Juan_Avatar_Inicial.blend`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\texturas\Juan_referencia_frontal.jpg`

## Avatar_Juan/inspect_fb.py

Utilidad de inspección, extracción o revisión: inspect fb. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Avatar_Juan/inspect_fb.py)
- Entorno: Python de Blender.
- Importaciones: `bl_ext`, `bpy`, `traceback`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## Avatar_Juan/inspect_head.py

Utilidad de inspección, extracción o revisión: inspect head. Consultar las operaciones detectadas antes de ejecutarla.

- Código: [abrir](../Avatar_Juan/inspect_head.py)
- Entorno: Python de Blender.
- Importaciones: `bpy`, `json`, `mathutils`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.

## agregar_creditos.py

Genera una tarjeta de título y concatena seis segundos iniciales con el MP4 y su audio.

- Código: [abrir](../agregar_creditos.py)
- Entorno: Python externo.
- Importaciones: `PIL`, `imageio_ffmpeg`, `pathlib`, `subprocess`.
- Efectos relevantes: revisar el código; puede escribir informes o imágenes aun sin guardar el blend.
- Rutas originales que deben revisarse:
  - `C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte`
  - `C:\Users\juan_\OneDrive\Escritorio\2do corte\Escenario\El_Japon_EEVEE_720p_con_audio.mp4`
  - `C:\Windows\Fonts\arial.ttf`
