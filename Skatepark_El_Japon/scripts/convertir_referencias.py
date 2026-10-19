from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import pillow_heif, imageio_ffmpeg,subprocess,json
pillow_heif.register_heif_opener()
p=Path('Skatepark_El_Japon')
sheet=Image.new('RGB',(1500,1200),'#eeeeee');d=ImageDraw.Draw(sheet)
for k,n in enumerate(range(4333,4342)):
 im=ImageOps.exif_transpose(Image.open(p/'referencias/originales'/f'IMG_{n}.HEIC')).convert('RGB')
 print(n, im.size)
 im.save(p/'referencias/imagenes'/f'IMG_{n}.jpg',quality=94)
 im.thumbnail((490,360));x=(k%3)*500;y=(k//3)*400
 sheet.paste(im,(x,y+30));d.text((x+12,y+10),f'IMG_{n}',fill='black')
sheet.save(p/'referencias/contacto.jpg')
ff=imageio_ffmpeg.get_ffmpeg_exe()
for n in range(4333,4342):
 inp=p/'referencias/originales'/f'IMG_{n}.MOV'
 r=subprocess.run([ff,'-hide_banner','-i',str(inp)],capture_output=True,text=True)
 print(n,r.stderr[:1000])
 subprocess.run([ff,'-y','-ss','1','-i',str(inp),'-frames:v','1','-vf','scale=1000:-1',str(p/'referencias/imagenes'/f'IMG_{n}_video.jpg')],capture_output=True)
