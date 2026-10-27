import os
import glob,collections,numpy as np
from common import *
# load all positions, dedupe exposures (wide-field plates appear in several queries): keep row with max edge distance
best={}
for f in sorted(glob.glob(os.path.join(DATA,'q_*.raw'))):
    for x in filt(load(f)):
        if x['exp']<=0: continue
        k=(x['series'],x['platenum'],x['expnum'])
        if k not in best or x['edge']>best[k]['edge']: best[k]=x
rows=list(best.values()); print("unique exposures (filtered):",len(rows))
def ols(X,y):
    X=np.column_stack([np.ones(len(y))]+X); b,*_=np.linalg.lstsq(X,y,rcond=None)
    r=y-X@b; s2=r@r/(len(y)-X.shape[1]); cov=s2*np.linalg.inv(X.T@X); return b,np.sqrt(np.diag(cov))
def trend(s,lo,hi,label):
    d=[x for x in rows if x['series']==s and lo<=x['year']<hi]
    if len(d)<40: print(label,'too few',len(d)); return
    y=np.array([x['lim'] for x in d]); yr=np.array([x['year'] for x in d]); yc=yr-yr.mean()
    lexp=np.log10([x['exp'] for x in d]); ill=np.array([x['illum'] for x in d])
    b,se=ols([yc,lexp,ill],y)
    msg=f"{label}: n={len(d)}  YEAR slope {b[1]*10:+.3f} +- {se[1]*10:.3f} mag/decade (t={b[1]/se[1]:+.1f}); moon {b[3]:+.2f}+-{se[3]:.2f}; log-exp {b[2]:+.2f}"
    ct=[x for x in d if x['ct'] is not None]
    if len(ct)>=40:
        y2=np.array([x['lim'] for x in ct]); yr2=np.array([x['year'] for x in ct]); 
        b2,se2=ols([yr2-yr2.mean(),np.log10([x['exp'] for x in ct]),np.array([x['illum'] for x in ct]),np.array([x['ct'] for x in ct])],y2)
        msg+=f"\n      + colorterm (emulsion) control: n={len(ct)} YEAR {b2[1]*10:+.3f} +- {se2[1]*10:.3f} mag/decade (t={b2[1]/se2[1]:+.1f})"
    print(msg)
print("[prediction for single-site Oak Ridge trends: NEGATIVE year slope (shallower as suburbs grow)]")
trend('dnb',1968,1990,'dnb  Oak Ridge 1968-89')
trend('ac',1935,1953,'ac   Oak Ridge 1935-52')
trend('rh',1933,1953,'rh   Oak Ridge 1933-52')
