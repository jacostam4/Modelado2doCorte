# Guía de uso y proceso

## Requisitos

El proyecto se trabajó en Blender 5.2. La compatibilidad con otras versiones no está comprobada; algunas propiedades y APIs internas pueden cambiar. `bpy`, `mathutils` y `bpy_extras` pertenecen a Blender: no instalar un paquete homónimo con pip para ejecutar estos scripts como Python normal.

Las utilidades externas usan Python 3 y las bibliotecas indicadas en `requirements-tools.txt`. Para instalarlas en un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-tools.txt
```

Pillow procesa imágenes; pillow-heif lee referencias HEIC; imageio-ffmpeg proporciona el ejecutable FFmpeg; NumPy realiza cálculos de síntesis de sonido. Los scripts de audio necesitan NumPy en el intérprete que los ejecuta.

Los scripts de `Avatar_Juan` son pruebas iniciales. `construir_rostro.py` requiere KeenTools FaceBuilder, sus APIs internas y una licencia aplicable. No es un requisito para usar el avatar final de Avaturn.

## Preparar archivos y rutas

1. Guardar una copia del `.blend` que se vaya a modificar.
2. Consultar la entrada del script en el catálogo y comprobar los objetos esperados.
3. Revisar las rutas `C:\Users\...` conservadas del equipo original. Adaptarlas en una copia del script a los archivos disponibles en el equipo de destino.
4. Comprobar carpetas de salida, imágenes, modelos y pistas de audio antes de ejecutar. Algunos scripts crean carpetas y otros suponen que existen.

`Skatepark_El_Japon/scripts/crear_escenario.py` calcula su carpeta base desde `__file__`; conservar esa estructura al utilizarlo. Otras utilidades usan rutas relativas al directorio de trabajo, como `preparar_texturas.py`, que espera la carpeta `Skatepark_El_Japon` desde donde se ejecute.

Los recursos grandes de la entrega original están en carpetas como `Escenario`, `tabla`, `Avatar`, `texturas` y `audio`. No asumir que cada entrada del catálogo puede ejecutarse con cualquier `.blend`: los nombres y versiones de los objetos importan.

## Ejecutar scripts de Blender

Para los scripts dependientes de la interfaz, abrir Blender y el archivo de trabajo; cambiar un área a Python Console e indicar la ruta absoluta real:

```python
from pathlib import Path
script = Path('D:/proyecto/Skatepark_El_Japon/scripts/animar_kickflip.py')
exec(compile(script.read_text(encoding='utf-8-sig'), str(script), 'exec'), {'__file__': str(script), '__name__': '__main__'})
```

Este ejemplo es ilustrativo: `animar_kickflip.py` requiere el estado posterior al lipslide y los nombres indicados en el catálogo. `__file__` se incluye porque varios scripts lo necesitan. Los callbacks con `bpy.app.timers` pueden guardar unos instantes después; revisar consola y archivo antes de cerrar Blender.

Los archivos sin dependencia de un área de interfaz pueden evaluarse individualmente para ejecución en segundo plano:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b 'D:\proyecto\copia.blend' --python 'D:\proyecto\Skatepark_El_Japon\scripts\diagnostico_rampas.py'
```

No convertir este ejemplo en una ejecución masiva. Los scripts que usan `bpy.context.area` o `bpy.context.window` pueden necesitar la interfaz y un contexto determinado.

## Mapa de etapas

Este mapa explica el proceso, no garantiza una reconstrucción lineal de todas las versiones.

| Etapa | Scripts principales | Insumos y resultado |
|---|---|---|
| Referencias | `convertir_referencias.py`, `preparar_texturas.py` | Fotos y videos originales; genera conversiones y recortes |
| Escenario base | `crear_escenario.py` | Fotografías/texturas preparadas; geometría, materiales, luces y colecciones |
| Corrección de distribución | `corregir_planta_satelital.py`, `complementar_fotos_satelite.py` | Escenario de la etapa anterior; ajusta posiciones y detalles |
| Ajustes de rampas | `mural_y_media_piramide.py`, `unificar_quarter_abierto.py`, `conectar_tres_rampas.py` | Versiones específicas de la geometría |
| Tabla | `armar_skate.py`, `corregir_trucks.py` | Componentes ya modelados; ensamblaje y correcciones |
| Objetos | `agregar_objetos_escenario.py`, `modelar_maletin_rojo.py` | Bibliotecas blend existentes y geometría adicional |
| Introducción y recorrido | `crear_intro.py`, `suavizar_intro.py`, `crear_ronda_patinando.py` | Escenario y cámaras; claves de recorrido |
| Personaje y mug | `crear_cierre_avatar.py` | Armature final y mug ya presentes; posturas, vínculo y cámara |
| Nollie BS lipslide | `animar_nollie_lipslide.py` | Personaje, tabla y baranda; fotogramas 1261–1500 |
| Kickflip | `animar_kickflip.py` | Estado posterior al lipslide; fotogramas 1501–1800 |
| Audio | `crear_audio.py`, `integrar_audio.py`, `finalizar_audio.py` | Síntesis de WAV y colocación de pistas |
| Salida | `configurar_eevee.py` | Configura 720p/30 fps/1800 fotogramas; no inicia por sí solo el render completo |
| Revisión de rampas | `diagnostico_rampas.py`, `reparar_visibilidad_rampas.py`, `verificar_rampas.py` | Diagnóstico, visibilidad y render de comprobación |
| Créditos | `agregar_creditos.py` | MP4 con audio; crea pantalla de seis segundos y un nuevo MP4 |

## Cómo se generan los movimientos

Las cámaras reciben claves de posición y orientación. El recorrido ovalado utiliza muestreo por longitud de arco para controlar su velocidad.

Los trucos se dividen en preparación, salto, ejecución, contacto y salida. Los scripts calculan transformaciones y posturas, e insertan claves en el personaje, la tabla y la cámara. La cinemática inversa de dos segmentos permite dirigir las extremidades hacia objetivos. El giro de las ruedas se relaciona con la distancia recorrida. El mug se vincula al hueso de la mano para mantener la relación durante el gesto.

El audio se sintetiza con señales y ruido filtrado. Las pistas separan base instrumental, rodadura y efectos de trucos. Es una producción sintetizada; no debe describirse como grabación de campo.

## Qué no está automatizado en esta colección

No hay un script maestro que reconstruya todos los assets desde cero ni un registro completo de cada operación de modelado original del madero, ruedas y trucks. La creación del personaje final en Avaturn es externa a estos scripts. La disponibilidad de rutas y nombres no garantiza el estado correcto de una escena. Consultar el catálogo y verificar cada resultado en una copia.
