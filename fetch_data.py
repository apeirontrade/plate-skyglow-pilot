"""Reproduce the data pulls used in this pilot from the public DASCH DR7 Starglass API (no key needed).
Writes data/q_<ra>_<dec>.raw and data/plate_locations_transition.json. Uses curl (the API rejects Python's default client).
Please be gentle with the API: this makes 31 position queries + ~670 plate lookups with pauses."""
import json,os,subprocess,sys,time
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'analysis'))
from common import load, filt, DATA
API='https://api.starglass.cfa.harvard.edu/public'
POS=[(ra,40) for ra in (60,105,150,195,240,285,330)]+[(150,20),(150,60)]+[(ra,-40) for ra in (0,60,120,180,240,300)]\
    +[(ra,dec) for dec in (0,-15) for ra in (0,45,90,135,180,225,270,315)]
os.makedirs(DATA,exist_ok=True)
def curl(args): 
    p=subprocess.run(['curl','-s','-f','--max-time','60']+args,capture_output=True,text=True); return p.stdout if p.returncode==0 else None
for ra,dec in POS:
    f=os.path.join(DATA,f'q_{ra}_{dec}.raw')
    if os.path.exists(f) and os.path.getsize(f)>1000: continue
    out=curl(['-X','POST',f'{API}/dasch/dr7/queryexps','-H','Content-Type: application/json','-d',json.dumps({'ra_deg':ra,'dec_deg':dec})])
    open(f,'w').write(out or ''); print('fetched',f,len(out or '')); time.sleep(1)
rows=filt(load(os.path.join(DATA,'q_150_40.raw')))
targets=[x for x in rows if (x['series'] in ('ac','rh') and 1922<=x['year']<1942) or (x['series']=='ai' and 1944<=x['year']<1959)]
locf=os.path.join(DATA,'plate_locations_transition.json')
loc=json.load(open(locf)) if os.path.exists(locf) else {}
for x in targets:
    pid=f"{x['series']}{int(x['platenum']):05d}"
    if pid in loc: continue
    j=curl([f'{API}/plates/p/{pid}'])
    try: loc[pid]=(json.loads(j).get('location') or {}).get('name','')
    except Exception: loc[pid]='ERR'
    time.sleep(0.35)
json.dump(loc,open(locf,'w'),indent=0); print('plate locations:',len(loc))
