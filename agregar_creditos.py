from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import imageio_ffmpeg, subprocess
root=Path(r'C:\Users\juan_\OneDrive\Documentos\ChatGPT\Segundo corte')
card=root/'creditos_skate.png'
im=Image.new('RGB',(1280,720),'black'); d=ImageDraw.Draw(im)
font=r'C:\Windows\Fonts\arial.ttf'
lines=[('Cinemática "Skate en el Japon"',62,44),('Autor: Juan Camilo Acosta Mahecha',230,36),('Editor: Magister Ingeniero Carlos Iván Pinzón Romero',300,36),('Código: UCMV-10',370,36),('Universidad: Universidad Central',440,36)]
for text,y,size in lines:
 f=ImageFont.truetype(font,size)
 while d.textlength(text,font=f)>1160:
  size-=1; f=ImageFont.truetype(font,size)
 d.text((60,y),text,font=f,fill='white')
im.save(card)
src=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\Escenario\El_Japon_EEVEE_720p_con_audio.mp4')
out=src.with_name('Skate_en_el_Japon_con_creditos.mp4')
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loop','1','-framerate','30','-t','6','-i',str(card),'-i',str(src),'-f','lavfi','-t','6','-i','anullsrc=r=48000:cl=stereo','-filter_complex','[0:v]format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[2:a]asetpts=PTS-STARTPTS[a0];[1:a]asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
with open(root/'video_edicion.log','w') as log:
 subprocess.run(cmd,stdout=log,stderr=log,check=True)
print(out)
