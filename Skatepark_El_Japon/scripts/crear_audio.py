import numpy as np
import wave, json
from pathlib import Path

SR=48000
N=60*SR
rng=np.random.default_rng(16026)
out=Path(r'C:\Users\juan_\OneDrive\Escritorio\2do corte\audio')
out.mkdir(parents=True,exist_ok=True)
def time(d): return np.arange(round(d*SR))/SR
def band(x,lo,hi):
    f=np.fft.rfftfreq(len(x),1/SR)
    gain=(1-np.exp(-(f/max(lo,1))**4))*np.exp(-(f/hi)**4)
    return np.fft.irfft(np.fft.rfft(x)*gain,n=len(x))
def noise(d,lo=100,hi=9000): return band(rng.normal(0,1,round(d*SR)),lo,hi)
def norm(x,peak=1): return x/max(np.max(np.abs(x)),1e-8)*peak
def edge(x,a=.003,b=.025):
    x=x.copy();na=min(len(x),round(a*SR));nb=min(len(x),round(b*SR))
    x[:na]*=np.linspace(0,1,na);x[-nb:]*=np.linspace(1,0,nb)
    return x
def add(dst,x,sec,gain=1,pan=0):
    i=round(sec*SR);n=min(len(x),len(dst)-i)
    if n<=0:return
    gains=np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
    dst[i:i+n]+=x[:n,None]*gain*gains
def write(name,x):
    assert np.max(np.abs(x))<1.0
    data=(x*32767).astype('<i2')
    with wave.open(str(out/name),'wb') as w:
        w.setnchannels(1 if x.ndim==1 else 2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(data.tobytes())
def hz(m):return 440*2**((m-69)/12)

# Original 88 BPM instrumental: swung hats, dry snare, warm keys and bass.
music=np.zeros((N,2),dtype=np.float64)
t=time(.55);freq=49+100*np.exp(-t/0.026)
kick=edge(norm(np.sin(2*np.pi*np.cumsum(freq)/SR)*np.exp(-t/0.12)+.18*noise(.55,1600,6000)*np.exp(-t/.008)))
t=time(.30)
snare=edge(norm(.65*noise(.30,900,8500)*np.exp(-t/.055)+.45*np.sin(2*np.pi*185*t)*np.exp(-t/.045)+.2*np.sin(2*np.pi*320*t)*np.exp(-t/.025)))
t=time(.09);hat=edge(norm(noise(.09,6500,14000)*np.exp(-t/.017)),.001,.008)
t=time(.26);openhat=edge(norm(noise(.26,6000,13000)*np.exp(-t/.065)),.001,.02)
beat=60/88;bar=beat*4
chords=[(48,55,58,62),(44,51,55,58),(46,53,56,60),(43,50,53,57)]
for k in range(23):
    at=k*bar
    if at>=58.7:break
    strength=.72 if k<2 else (0.85 if k>=20 else 1)
    for b,g in [(0,1),(1.75,.72),(2.5,.88),(3.5,.55)]:
        if k%4==3 and b==3.5:continue
        add(music,kick,at+b*beat,.30*g*strength)
    for b in [1,3]:add(music,snare,at+b*beat+.014,.22*strength)
    if k%4==3:add(music,snare,at+2.75*beat,.065)
    for h in range(8):
        off=h*.5*beat+(.042 if h%2 else 0)
        add(music,openhat if h==7 and k%2 else hat,at+off,.055*(.70 if h%2 else 1),-.24 if h%2 else .2)
    notes=chords[(k//2)%4]
    t=time(2.3);keys=np.zeros(len(t))
    for j,n in enumerate(notes):
        f=hz(n+12)
        keys+=(np.sin(2*np.pi*f*t+.9*np.sin(2*np.pi*f*2*t)*np.exp(-t/.22))+.18*np.sin(2*np.pi*f*2.003*t))*np.exp(-t/(.8+j*.16))
    keys=edge(norm(keys),.012,.2)
    add(music,keys,at,.12,-.22)
    add(music,keys,at+beat*.75,.025,.35)
    for b,ln,g in [(0,1.25,1),(2,1.1,.9),(3.5,.40,.65)]:
        t=time(ln);f=hz(notes[0]-12)
        bass=edge(norm((np.sin(2*np.pi*f*t)+.23*np.sin(2*np.pi*2*f*t)+.08*np.sin(2*np.pi*3*f*t))*np.exp(-t/1.1)),.015,.12)
        add(music,bass,at+b*beat,.20*g)
# Short room reflections for the keys/drums, low enough to keep the beat dry.
for delay,gain in [(int(.083*SR),.065),(int(.139*SR),.035)]:music[delay:]+=music[:-delay,::-1]*gain
fade=np.minimum(1,np.arange(N)/(SR*1.2))*np.minimum(1,(N-1-np.arange(N))/(SR*2.4))
music*=fade[:,None]

# Synthesized skateboard foley: wood resonances, urethane rattle and metal scrape.
def wood(d=.28,heavy=False):
    t=time(d);x=noise(d,450,11500)*np.exp(-t/.012)*.7
    for freq,decay,amp in [(164,.06,.4),(410,.042,.4),(890,.025,.3),(1730,.018,.17),(2800,.012,.11)]:
        x+=amp*np.sin(2*np.pi*freq*t+rng.uniform(0,6))*np.exp(-t/decay)
    if heavy:x+=.8*np.sin(2*np.pi*79*t)*np.exp(-t/.055)
    return edge(norm(x),.0002,.035)
pop=wood();landing=wood(.42,True)
landing[int(.017*SR):]+=wood(.42-.017)*.33
landing=norm(landing)
railhit=edge(norm(wood(.33)*.7+sum(.14*np.sin(2*np.pi*f*time(.33))*np.exp(-time(.33)/.10) for f in [1100,2370,3780])),.0005,.05)
t=time(.73);grind=noise(.73,300,7200)*(.5+.2*np.sin(2*np.pi*31*t)+.12*np.sin(2*np.pi*71*t))
grind+=.11*np.sin(2*np.pi*1920*t+4*np.sin(2*np.pi*27*t))+.05*np.sin(2*np.pi*3150*t)
grind=edge(norm(grind),.03,.06)
t=time(.55);flip=edge(norm(noise(.55,750,8500)*np.sin(np.pi*t/.55)**2+.12*np.sin(2*np.pi*(680*t+650*t*t))*np.sin(np.pi*t/.55)**2),.015,.08)
flick=edge(norm(noise(.12,1700,11000)*np.exp(-time(.12)/.026)),.001,.02)
events=np.zeros((N,2));rolling=np.zeros((N,2));manifest=[]
def event(name,frame,sample,gain,pan=0):
    add(events,sample,(frame-1)/30,gain,pan)
    manifest.append({'effect':name,'frame':frame,'seconds':round((frame-1)/30,4)})
event('nollie_pop_nose',1345,pop,.58,-.1)
event('lipslide_contacto',1363,railhit,.42,0)
# Length of slide is 29 frames, followed by a small exit scrape.
gdur=(1392-1363)/30;t=time(gdur)
scrape=edge(norm(noise(gdur,350,7200)*(.6+.15*np.sin(2*np.pi*39*t))+.08*np.sin(2*np.pi*1820*t)),.015,.055)
event('lipslide_deslizamiento',1363,scrape,.24,.08)
event('lipslide_salida',1392,pop,.23,.1)
event('lipslide_aterrizaje',1410,landing,.66,.12)
event('kickflip_pop_tail',1549,pop,.6,0)
event('kickflip_flick',1555,flick,.20,-.1)
event('kickflip_giro',1555,flip,.25,0)
event('kickflip_catch',1574,pop,.19,.1)
event('kickflip_aterrizaje',1583,landing,.68,.1)
for a,b,g in [(1261,1345,.13),(1410,1549,.13),(1583,1680,.11)]:
    dur=(b-a)/30;t=time(dur)
    roll=noise(dur,110,4500)*(.65+.15*np.sin(2*np.pi*44*t))+.12*np.sin(2*np.pi*120*t)*noise(dur,30,400)
    for at in np.arange(.15,dur,.36):
        idx=int(at*SR);clack=wood(.07)*.45;n=min(len(clack),len(roll)-idx);roll[idx:idx+n]+=clack[:n]
    roll=edge(norm(roll),.08,.12)
    if a==1583:roll*=np.linspace(1,0,len(roll))
    add(rolling,roll,(a-1)/30,g,0)
# Subtle music ducking around skateboard transients, with a smooth recovery.
duck=np.ones(N)
for e in manifest:
    if 'deslizamiento' in e['effect'] or 'giro' in e['effect']:continue
    center=round(e['seconds']*SR);a=max(0,center-int(.035*SR));b=min(N,center+int(.30*SR))
    env=np.exp(-np.abs(np.arange(a,b)-center)/(SR*.11))
    duck[a:b]=np.minimum(duck[a:b],1-.28*env)
music*=duck[:,None]
mix=music+rolling+events
gain=min(1,.89/np.max(np.abs(mix)))
music*=gain;rolling*=gain;events*=gain;mix*=gain
write('01_BoomBap_88BPM_60s.wav',music)
write('02_Ruedas_sincronizadas_60s.wav',rolling)
write('03_Trucos_sincronizados_60s.wav',events)
write('El_Japon_Mezcla_60s.wav',mix)
for name,x in [('Pop_madera.wav',pop),('Aterrizaje.wav',landing),('Contacto_baranda.wav',railhit),('Deslizamiento_baranda.wav',scrape),('Kickflip_giro.wav',flip)]:write(name,x*.8)
report={'sample_rate':SR,'duration_seconds':60,'bpm':88,'peak_dbfs':float(20*np.log10(np.max(np.abs(mix)))),'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(mix**2)))),'events':manifest,'source':'Original procedural synthesis; no external samples.'}
(out/'Sincronizacion_audio.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
