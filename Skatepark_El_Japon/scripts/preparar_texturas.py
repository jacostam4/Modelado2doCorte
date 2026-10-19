from PIL import Image,ImageOps
from pathlib import Path
p=Path('Skatepark_El_Japon')
def patch(n,name,quad,size):
 im=Image.open(p/'referencias/imagenes'/f'IMG_{n}.jpg');w,h=im.size
 q=[v for xy in quad for v in (xy[0]*w,xy[1]*h)]
 im=im.transform(size,Image.Transform.QUAD,q,Image.Resampling.BICUBIC)
 im.save(p/'texturas'/name,quality=96)
# Ordered upper-left, lower-left, lower-right, upper-right.
patch(4340,'mural_fotografico.jpg',[(.008,.397),(.008,.529),(.789,.447),(.789,.286)],(4096,900))
patch(4338,'concreto_fotografico.jpg',[(.05,.695),(.015,.94),(.39,.94),(.36,.695)],(1536,1536))
patch(4337,'ladrillo_perimetral.jpg',[(.26,.408),(.26,.451),(.45,.444),(.45,.403)],(2048,256))
