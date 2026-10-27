"""P1 moon gate: does plate limiting magnitude respond to lunar illumination?"""
import statistics,collections
from common import *
rows=load(os.path.join(DATA,'q_150_40.raw'))
print("[prediction: negative slope — plates shallower near full moon]")
for s in ['ac','ai','fa','dnb','rh','bm']:
    d=filt(rows,s)
    if len(d)<40: print(s,'too few',len(d)); continue
    exps=sorted(x['exp'] for x in d); t1,t2=exps[len(exps)//3],exps[2*len(exps)//3]
    def eb(e): return 0 if e<t1 else 1 if e<t2 else 2
    bins=collections.defaultdict(list)
    for x in d: bins[(int(x['year'])//5, eb(x['exp']))].append(x)
    xs=[];ys=[]
    for b,lst in bins.items():
        if len(lst)<5: continue
        m=statistics.mean(x['lim'] for x in lst)
        for x in lst: xs.append(x['illum']); ys.append(x['lim']-m)
    b,se,n=linfit(xs,ys)
    print(f"{s:4s} n={n:4d}  d(lim)/d(illum) = {b:+.3f} +- {se:.3f} mag  (t={b/se:+.1f})")
