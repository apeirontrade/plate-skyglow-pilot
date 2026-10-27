# Results (pilot, 2026-10-27)

Data: DASCH DR7 via the public Starglass API, `POST /dasch/dr7/queryexps`, at 15 positions: the dec +40 ring at RA 60, 105, 150, 195, 240, 285 and 330; (150, +20); (150, +60); and the dec −40 ring at RA 0, 60, 120, 180, 240 and 300.

Filters: requires `limMagApass`, `exptime` > 0 and a parseable date; `edgedist` ≥ 2.0 cm; `wcssource == imwcs`. Exposures are deduplicated by (series, platenum, expnum), keeping the row with the largest edge distance.

Observing sites come from `GET /plates/p/{id}` → `location`.

## Pre-registration (written before each test)

> Main confounder: emulsion speed improved ~1890–1950, so raw lim_mag DEEPENS with time (opposite sign to light pollution). Raw trends are NOT evidence.
>
> **P1 MOON GATE:** within one series and a short window, lim_mag is SHALLOWER near full moon than near new moon. If no moon effect is detectable, the method can't see sky brightness and the pilot STOPS.
>
> **P2 SITE STEP:** lim_mag DEEPENS after the ac/rh move Cambridge → Oak Ridge (~1930) and after the ai move Oak Ridge → Doña Ana NM (~1950), within ±5-yr windows and exptime bins.
>
> **P3 SLOW TREND:** dnb at Oak Ridge 1968–1989: lim_mag SHALLOWS with year within exptime bins (Boston suburban growth). Report the slope ± uncertainty.

The dark-site comparison (Mt. John `dsb`) was added after the P3 single-site result, as a control. It was not part of the original pre-registration.

## P1 — moon gate (`analysis/p1_moon.py`, position RA 150 / Dec +40)

Model: lim_mag residual (after subtracting 5-yr × exposure-tercile bin means) regressed on lunar illuminated fraction (0 = new moon, 1 = full moon).

| series | n | slope (mag per unit illumination) | t |
|---|---|---|---|
| ac | 999 | −0.371 ± 0.069 | −5.4 |
| ai | 989 | −0.437 ± 0.062 | −7.0 |
| fa | 370 | −0.283 ± 0.112 | −2.5 |
| bm | 76 | −0.526 ± 0.246 | −2.1 |
| dnb | 176 | +0.169 ± 0.166 | +1.0 (ns) |
| rh | 125 | +0.051 ± 0.228 | +0.2 (ns) |

With all 15 positions combined, `dnb` and `dsb` do show a moon term (−0.14 to −0.30; see P3).

**If** the plates are background-limited, then Δm_lim ≈ −1.25 log10(B₂/B₁), which follows from limiting flux ∝ √(sky background). On that assumption, the full-moon effect corresponds to roughly a 2× brighter sky.

## P2 — site step (`analysis/p2_site.py`)

Model: OLS of lim ~ site + year + log10(exptime) + moon illumination, within series.

| series | comparison | years | n (dark/bright) | site effect (dark − bright) | t |
|---|---|---|---|---|---|
| ac | Oak Ridge − Cambridge | 1922–41 | 342 (124/218) | **+0.92 ± 0.14** | +6.5 |
| rh | Oak Ridge − Cambridge | 1922–41 | 101 (69/32) | **+1.06 ± 0.33** | +3.2 |
| ai | Doña Ana NM − Oak Ridge | 1944–58 | 223 (86/137) | +0.24 ± 0.20 | +1.2 (ns) |

Years with both sites operating at once (the cleanest comparison): `ac` 1934 only, n=36, +0.84 ± 0.83 (ns).

Treat the steps as upper bounds on a sky-brightness difference, because equipment changes may coincide with the moves.

## P3 — slow trend (`analysis/p3_trend.py`, `analysis/p3c_control.py`, all 15 positions)

| series | site | years / exposure | n | trend (mag/decade) | t |
|---|---|---|---|---|---|
| dnb | Oak Ridge | 1968–89, all exp | 1437 | −0.335 ± 0.038 | −8.7 |
| dnb | Oak Ridge | 1974–89, 36 min only | 561 | **−0.496 ± 0.055** | −9.0 |
| dsb | Mt. John NZ (dark) | 1974–89, 30 min only | 468 | **−0.362 ± 0.079** | −4.6 |
| **dnb − dsb** | | | | **−0.13 ± 0.10** | ns |
| ac | Oak Ridge | 1935–52 | 2678 | +0.190 ± 0.035 (+0.231 with colorterm) | +5.4 |
| rh | Oak Ridge | 1933–52 | 988 | +0.197 ± 0.058 (+0.237 with colorterm) | +3.4 |

The 95% interval for the Oak Ridge-specific excess is about −0.32 to +0.05 mag/decade. Under the background-limited assumption, that is less than ~1.8× sky brightening per decade.

### Median lim_mag in 3-year bins

The first number in each cell is the median limiting magnitude; n is the number of plates; exp is the median exposure in minutes.

| | 1968 | 1971 | 1974 | 1977 | 1980 | 1983 | 1986 | 1989 |
|---|---|---|---|---|---|---|---|---|
| dnb (Oak Ridge) | 14.73, n=3, exp 125 | 14.21, n=6, exp 121 | 14.84, n=128, exp 36 | 14.69, n=196, exp 36 | 14.71, n=227, exp 36 | 14.59, n=423, exp 36 | 14.37, n=397, exp 36 | 14.27, n=57, exp 36 |
| dsb (Mt. John) | 15.16, n=34, exp 120 | 15.09, n=40, exp 120 | — | 15.06, n=47, exp 60 | 14.99, n=66, exp 30 | 14.73, n=187, exp 30 | 14.51, n=192, exp 30 | 14.91, n=29, exp 30 |

**Lead, not a result:** in 1989 the Mt. John series rebounds (14.51 → 14.91) while Oak Ridge keeps falling (14.37 → 14.27). That is the pattern recovery from the 1982 El Chichón aerosols plus a residual Oak Ridge decline would leave. The samples are too small to test it here.

## Interpretation

Limiting magnitude is sensitive to sky brightness: it responds to the moon, and the Cambridge → Oak Ridge step goes the right way. But common-mode effects (emulsion, processing, global atmospheric transparency) are as large as the effect sought. **Any light-pollution reconstruction from these plates needs a differential design** (a contemporaneous dark-site twin) and ideally pixel-level sky background, not limiting magnitude alone.
