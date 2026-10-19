import subprocess,imageio_ffmpeg
from pathlib import Path
p=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte\Skatepark_El_Japon')
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-ss','4','-i',r'C:\Users\juan_\OneDrive\Escritorio\2do corte\Escenario\El_Japon_EEVEE_720p_con_audio.mp4','-frames:v','1',str(p/'video_rampas_4s.png')],capture_output=True)
