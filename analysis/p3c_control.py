import os
import glob,collections,numpy as np
from common import *
best={}
for f in sorted(glob.glob(os.path.join(DATA,'q_*.raw'))):
    for x in filt(load(f)):
        if x['exp']<=0: continue
        k=(x['series'],x['platenum'],x['expnum'])
        if k not in best or x['edge']>best[k]['edge']: best[k]=x
rows=list(best.values())
late=[x for x in rows if 1965<=x['year']<1990]
print("1965-89 series:",collections.Counter(x['series'] for x in late).most_common(8))
def ols(X,y):
    X=np.column_stack([np.ones(len(y))]+X); b,*_=np.linalg.lstsq(X,y,rcond=None)
    r=y-X@b; s2=r@r/(len(y)-X.shape[1]); cov=s2*np.linalg.inv(X.T@X); return b,np.sqrt(np.diag(cov))
for s in ['dnb','dsb']:
    for lo,hi,fixexp in [(1974,1990,True),(1968,1990,False)]:
        d=[x for x in rows if x['series']==s and lo<=x['year']<hi]
        if fixexp:
            exps=collections.Counter(round(x['exp']) for x in d); mode=exps.most_common(1)[0][0] if exps else None
            d=[x for x in d if round(x['exp'])==mode]
        if len(d)<30: print(s,lo,hi,'too few',len(d)); continue
        y=np.array([x['lim'] for x in d]); yr=np.array([x['year'] for x in d])
        X=[yr-yr.mean(),np.array([x['illum'] for x in d])]
        if not fixexp: X.append(np.log10([x['exp'] for x in d]))
        b,se=ols(X,y)
        ct=[x['ct'] for x in d if x['ct'] is not None]
        print(f"{s} {lo}-{hi} {'exp='+str(mode)+'min only' if fixexp else 'all exp'}: n={len(d)} YEAR {b[1]*10:+.3f} +- {se[1]*10:.3f} mag/decade (t={b[1]/se[1]:+.1f}); moon {b[2]:+.2f}+-{se[2]:.2f}; median colorterm {sorted(ct)[len(ct)//2] if ct else 'na'}")
    d=[x for x in rows if x['series']==s and 1968<=x['year']<1990]
    bins=collections.defaultdict(list)
    for x in d: bins[int(x['year'])//3*3].append(x)
    print(f"  {s} 3-yr bins (median lim / n / median exp):", "  ".join(f"{b}:{sorted(x['lim'] for x in l)[len(l)//2]:.2f}/{len(l)}/{sorted(x['exp'] for x in l)[len(l)//2]:.0f}" for b,l in sorted(bins.items())))
