import os
import json,collections,numpy as np
from common import *
rows=filt(load(os.path.join(DATA,'q_150_40.raw')))
loc=json.load(open(os.path.join(DATA,'plate_locations_transition.json')))
def pid(x): return f"{x['series']}{int(x['platenum']):05d}"
def ols(X,y):
    X=np.column_stack([np.ones(len(y))]+X); b,*_=np.linalg.lstsq(X,y,rcond=None)
    r=y-X@b; s2=r@r/(len(y)-X.shape[1]); cov=s2*np.linalg.inv(X.T@X); return b,np.sqrt(np.diag(cov))
for s,dark,bright,lo,hi in [('ac','Oak Ridge','Cambridge',1922,1942),('rh','Oak Ridge','Cambridge',1922,1942),('ai','Oak Ridge','Cambridge',1922,1942),('ai','Dona Ana, NM','Oak Ridge',1944,1959)]:
    d=[x for x in rows if x['series']==s and lo<=x['year']<hi and loc.get(pid(x)) in (dark,bright)]
    if len(d)<30: print(s,dark,'vs',bright,'too few',len(d)); continue
    site=np.array([1.0 if loc[pid(x)]==dark else 0.0 for x in d])
    by=collections.defaultdict(lambda:[0,0])
    for x,sv in zip(d,site): by[int(x['year'])][int(sv)]+=1
    overlap=[y for y,(b_,d_) in sorted(by.items()) if b_>0 and d_>0]
    y=np.array([x['lim'] for x in d]); yrs=np.array([x['year'] for x in d]); year=yrs-yrs.mean()
    lexp=np.log10([x['exp'] for x in d]); ill=np.array([x['illum'] for x in d])
    b,se=ols([site,year,lexp,ill],y)
    print(f"{s}: {dark} vs {bright} {lo}-{hi}: n={len(d)} (dark {int(site.sum())}, bright {len(d)-int(site.sum())}); overlap years {overlap}")
    print(f"   SITE (dark-bright) {b[1]:+.3f} +- {se[1]:.3f} mag (t={b[1]/se[1]:+.1f}) [pred +]; year {b[2]:+.4f}/yr; log-exp {b[3]:+.2f}; moon {b[4]:+.2f}")
    if overlap:
        o=[i for i,x in enumerate(d) if int(x['year']) in overlap]
        bo,seo=ols([site[o],year[o],lexp[o],ill[o]],y[o])
        print(f"   overlap-years only (contemporaneous): n={len(o)} SITE {bo[1]:+.3f} +- {seo[1]:.3f} (t={bo[1]/seo[1]:+.1f})")
