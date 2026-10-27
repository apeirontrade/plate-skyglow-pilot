# P8: pulse vs drift, other series, and APASS vs ATLAS, on the 1974-89 common-mode decline.
import os, glob, collections, numpy as np
from common import *
best = {}
for f in sorted(glob.glob(os.path.join(DATA, 'q_*.raw'))):
    for x in filt(load(f)):
        if x['exp'] <= 0: continue
        k = (x['series'], x['platenum'], x['expnum'])
        if k not in best or x['edge'] > best[k]['edge']: best[k] = x
rows = list(best.values())

def ols(X, y):
    X = np.column_stack([np.ones(len(y))] + X); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; n, k = X.shape; s2 = r @ r / (n - k)
    cov = s2 * np.linalg.inv(X.T @ X); bic = n * np.log(r @ r / n) + k * np.log(n)
    return b, np.sqrt(np.diag(cov)), bic

def fixed_exp(d):
    exps = collections.Counter(round(x['exp']) for x in d)
    mode = exps.most_common(1)[0][0]; return [x for x in d if round(x['exp']) == mode], mode

def pulse(yr):  # El Chichon: eruption 1982.27, stratospheric aerosol e-folding ~1 yr
    return np.where(yr >= 1982.27, np.exp(-(yr - 1982.27) / 1.0), 0.0)

print("=== (a) pulse vs drift, 1974-89, fixed exposure ===")
for s in ['dnb', 'dsb']:
    d, mode = fixed_exp([x for x in rows if x['series'] == s and 1974 <= x['year'] < 1990])
    y = np.array([x['lim'] for x in d]); yr = np.array([x['year'] for x in d]); il = np.array([x['illum'] for x in d])
    yc = yr - yr.mean()
    bL, sL, bicL = ols([yc, il], y)
    bP, sP, bicP = ols([pulse(yr), il], y)
    bB, sB, bicB = ols([yc, pulse(yr), il], y)
    print(f"{s} exp={mode}min n={len(d)}")
    print(f"  linear : slope {bL[1]*10:+.3f}±{sL[1]*10:.3f} mag/dec   BIC {bicL:.1f}")
    print(f"  pulse  : pulse {bP[1]:+.3f}±{sP[1]:.3f} mag           BIC {bicP:.1f}  (ΔBIC pulse−linear {bicP-bicL:+.1f})")
    print(f"  both   : slope {bB[1]*10:+.3f}±{sB[1]*10:.3f}  pulse {bB[2]:+.3f}±{sB[2]:.3f}   BIC {bicB:.1f}")
    # yearly medians for eyeballing
    yb = collections.defaultdict(list)
    for x in d: yb[int(x['year'])].append(x['lim'])
    print("  yearly medians:", " ".join(f"{k}:{np.median(v):.2f}({len(v)})" for k, v in sorted(yb.items())))

print("\n=== (b) other series with 1974-89 coverage (fixed exposure, n>=100) ===")
late = [x for x in rows if 1974 <= x['year'] < 1990]
for s, n in collections.Counter(x['series'] for x in late).most_common():
    if n < 100: break
    d, mode = fixed_exp([x for x in late if x['series'] == s])
    if len(d) < 100: print(f"{s}: n={n} but only {len(d)} at modal exp {mode}min; skipped"); continue
    y = np.array([x['lim'] for x in d]); yr = np.array([x['year'] for x in d]); il = np.array([x['illum'] for x in d])
    b, se, _ = ols([yr - yr.mean(), il], y)
    yrs = f"{min(x['year'] for x in d):.0f}-{max(x['year'] for x in d):.0f}"
    print(f"{s} exp={mode}min n={len(d)} {yrs}: slope {b[1]*10:+.3f}±{se[1]*10:.3f} mag/dec (t={b[1]/se[1]:+.1f})")

print("\n=== (c) APASS vs ATLAS limiting mags, same plates ===")
for s in ['dnb', 'dsb']:
    d, mode = fixed_exp([x for x in rows if x['series'] == s and 1974 <= x['year'] < 1990 and x.get('limMagAtlas')])
    yr = np.array([x['year'] for x in d]); il = np.array([x['illum'] for x in d])
    for key in ['limMagApass', 'limMagAtlas']:
        y = np.array([float(x[key]) for x in d])
        b, se, _ = ols([yr - yr.mean(), il], y)
        print(f"{s} {key}: n={len(d)} slope {b[1]*10:+.3f}±{se[1]*10:.3f} mag/dec")
    diff = np.array([float(x['limMagAtlas']) - float(x['limMagApass']) for x in d])
    b, se, _ = ols([yr - yr.mean()], diff)
    print(f"{s} ATLAS−APASS: mean {diff.mean():+.3f}, slope {b[1]*10:+.3f}±{se[1]*10:.3f} mag/dec")

print("\n=== (d) drift with plate-position controls and diagnostics ===")
for s in ['dnb', 'dsb']:
    d, mode = fixed_exp([x for x in rows if x['series'] == s and 1974 <= x['year'] < 1990])
    y = np.array([x['lim'] for x in d]); yr = np.array([x['year'] for x in d]); il = np.array([x['illum'] for x in d])
    cd = np.array([float(x['centerdist']) for x in d]); ed = np.array([x['edge'] for x in d])
    pos = [(round(float(x['ra']) / 15), round(float(x['dec']) / 15)) for x in d]
    keys = sorted(set(pos)); FE = [np.array([1.0 if p == k else 0.0 for p in pos]) for k in keys[1:]]
    for lab, X in [('year+moon', [yr - yr.mean(), il]), ('+centerdist+edgedist', [yr - yr.mean(), il, cd - cd.mean(), ed - ed.mean()]),
                   ('+centerdist+edgedist+15deg position FE', [yr - yr.mean(), il, cd - cd.mean(), ed - ed.mean()] + FE)]:
        b, se, _ = ols(X, y); print(f"{s} {lab}: slope {b[1]*10:+.3f}±{se[1]*10:.3f} mag/dec")
    for key, lab in [('medianColortermApass', 'colorterm'), ('centerdist', 'centerdist cm')]:
        v = np.array([float(x[key]) for x in d]); b, se, _ = ols([yr - yr.mean()], v)
        print(f"  {s} {lab} vs year: mean {v.mean():.3f}, slope {b[1]*10:+.3f}±{se[1]*10:.3f} per decade")
    sc = np.array([float(x['scandate'][:4]) + (int(x['scandate'][5:7]) - 1) / 12 for x in d])
    b, se, _ = ols([yr - yr.mean(), sc - sc.mean()], y)
    print(f"  {s} lim ~ exposure year + scan year: exposure {b[1]*10:+.3f}±{se[1]*10:.3f}/dec, scan {b[2]:+.3f}±{se[2]:.3f}/yr")
