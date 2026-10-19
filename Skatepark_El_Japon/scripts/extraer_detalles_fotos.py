from pathlib import Path
from PIL import Image
p=Path('Skatepark_El_Japon')
def patch(n,name,q,size):
 im=Image.open(p/'referencias/imagenes'/f'IMG_{n}.jpg');w,h=im.size
 im=im.transform(size,Image.Transform.QUAD,[v for xy in q for v in (xy[0]*w,xy[1]*h)],Image.Resampling.BICUBIC)
 im.save(p/'texturas'/name,quality=96)
patch(4336,'cajon_ladrillo_foto.jpg',[(.19,.488),(.19,.54),(.739,.545),(.739,.495)],(2048,256))
patch(4337,'manualpad_frente_foto.jpg',[(.327,.594),(.327,.620),(.795,.616),(.795,.58)],(2048,192))
patch(4336,'fachada_verde_grafitis_foto.jpg',[(.245,.257),(.245,.347),(.975,.364),(.975,.256)],(4096,600))
patch(4338,'caseta_foto.jpg',[(.739,.346),(.741,.452),(.937,.458),(.934,.344)],(1536,1024))
