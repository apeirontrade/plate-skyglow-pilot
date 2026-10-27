import json,csv,io,math,datetime,os
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","data")
SYN=29.530588853; NEW_MOON=datetime.datetime(2000,1,6,18,14)  # reference new moon (UTC)
def load(path):
    rows=json.load(open(path))
    out=[]
    for x in csv.DictReader(io.StringIO("\n".join(rows))):
        try:
            if not (x['limMagApass'] and x['exptime'] and x['expdate'][:4].isdigit()): continue
            t=datetime.datetime.fromisoformat(x['expdate'].rstrip('Z')[:19])
            ed=float(x['edgedist']) if x['edgedist'] else -1
            x.update(t=t, year=t.year+(t.timetuple().tm_yday-1)/365.25, lim=float(x['limMagApass']),
                     exp=float(x['exptime']), edge=ed,
                     ct=float(x['medianColortermApass']) if x['medianColortermApass'] else None)
            age=((t-NEW_MOON).total_seconds()/86400)%SYN
            x['moon_age']=age; x['illum']=(1-math.cos(2*math.pi*age/SYN))/2  # 0 new, 1 full
            out.append(x)
        except Exception: pass
    return out
def filt(rows, series=None, edge=2.0, imwcs=True):
    return [x for x in rows if (series is None or x['series']==series) and x['edge']>=edge and (not imwcs or x['wcssource']=='imwcs')]
def linfit(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxx=sum((a-mx)**2 for a in xs); sxy=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    b=sxy/sxx; a=my-b*mx
    res=[y-(a+b*x) for x,y in zip(xs,ys)]; s2=sum(r*r for r in res)/(n-2)
    return b, math.sqrt(s2/sxx), n
