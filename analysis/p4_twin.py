import glob,os,collections,numpy as np
from common import *
best={}
for f in sorted(glob.glob(os.path.join(DATA,'q_*.raw'))):
    pos=os.path.basename(f)[2:-4]
    for x in filt(load(f)):
        if x['exp']<=0 or x['series'] not in ('dnb','dsb'): continue
        k=(x['series'],x['platenum'],x['expnum'])
        x['pos']=pos
        if k not in best or x['edge']>best[k]['edge']: best[k]=x
d=[x for x in best.values() if 1974<=x['year']<1990]
print("n by series:",collections.Counter(x['series'] for x in d))
both=[p for p in set(x['pos'] for x in d) if len({x['series'] for x in d if x['pos']==p})==2]
print("positions with both cameras:",len(both),sorted(both))
def fit(rows,label):
    pos=sorted(set(x['pos'] for x in rows)); pi={p:i for i,p in enumerate(pos)}
    y=np.array([x['lim'] for x in rows]); yr=np.array([x['year'] for x in rows]); yc=yr-1981.5
    site=np.array([1.0 if x['series']=='dnb' else 0.0 for x in rows])
    cols=[site,yc,site*yc,np.array([x['illum'] for x in rows]),np.log10([x['exp'] for x in rows])]
    for p in pos[1:]: cols.append(np.array([1.0 if x['pos']==p else 0.0 for x in rows]))
    X=np.column_stack([np.ones(len(y))]+cols); b,*_=np.linalg.lstsq(X,y,rcond=None)
    r=y-X@b; s2=r@r/(len(y)-X.shape[1]); se=np.sqrt(np.diag(s2*np.linalg.pinv(X.T@X)))
    print(f"{label}: n={len(rows)} (dnb {int(site.sum())}, dsb {len(rows)-int(site.sum())}), positions {len(pos)}")
    print(f"   Mt John trend {b[2]*10:+.3f}+-{se[2]*10:.3f} mag/dec; INTERACTION (OakRidge-MtJohn) {b[3]*10:+.3f}+-{se[3]*10:.3f} mag/dec (t={b[3]/se[3]:+.1f}); 95% [{(b[3]-1.96*se[3])*10:+.2f},{(b[3]+1.96*se[3])*10:+.2f}]; site offset@1981.5 {b[1]:+.2f}; moon {b[4]:+.2f}+-{se[4]:.2f}")
    return b,se
fit([x for x in d if x['pos'] in both],"P4 same-sky positions only")
fit(d,"P4 all positions")
print("P5 recovery (mean lim 1989 - mean lim 1983-88), same-sky positions:")
for s in ('dnb','dsb'):
    a=[x['lim'] for x in d if x['series']==s and x['pos'] in both and 1983<=x['year']<1989]
    c=[x['lim'] for x in d if x['series']==s and x['pos'] in both and x['year']>=1989]
    if a and c: print(f"   {s}: {np.mean(c)-np.mean(a):+.3f} (n89={len(c)}, n83-88={len(a)}; se~{np.sqrt(np.var(c)/len(c)+np.var(a)/len(a)):.3f})")
