# Results (pilot, 2026-10-27)

Data: DASCH DR7 via the public Starglass API, `POST /dasch/dr7/queryexps`, at 31 positions: the dec +40 ring at RA 60, 105, 150, 195, 240, 285 and 330; (150, +20); (150, +60); the dec −40 ring at RA 0, 60, 120, 180, 240 and 300; and the dec 0 and dec −15 rings at RA 0–315 in steps of 45 (added for P4).

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

**Lead, not a result:** in 1989 the Mt. John series rebounds (14.51 → 14.91) while Oak Ridge keeps falling (14.37 → 14.27). That could be a southern recovery from the 1982 El Chichón aerosols, or an end-of-program artifact at Oak Ridge (P4 finds no Oak Ridge-specific decline). The samples are too small to test it here.

## P4/P5 — same-sky twin-camera differential (`analysis/p4_twin.py`, 31 positions)

Pre-registered before running. Model: lim ~ site + year + site×year + moon + log10(exptime) + position fixed effects, 1974–89.

| sample | n (dnb / dsb) | Mt. John trend (mag/dec) | **Oak Ridge − Mt. John trend** | 95% |
|---|---|---|---|---|
| 12 positions imaged by both cameras | 1068 / 402 | −0.51 ± 0.10 | **+0.31 ± 0.11** (t=2.8, opposite to prediction) | [+0.09, +0.52] |
| all 31 positions | 2416 / 1250 | −0.35 ± 0.05 | +0.06 ± 0.06 (ns) | [−0.06, +0.17] |

The Oak Ridge plates are ~1 mag shallower than Mt. John on the same stars, but that offset is confounded by exposure time, airmass (Oak Ridge sees dec −15° low in the sky) and extinction. Don't read it as skyglow.

P5 (exploratory), 1989 minus 1983–88 mean, shared positions: Mt. John +0.15 (≈0.07, n=24), Oak Ridge −0.13 (≈0.07, n=37).

## Interpretation

Limiting magnitude is sensitive to sky brightness: it responds to the moon, and the Cambridge → Oak Ridge step goes the right way. But common-mode effects (emulsion, processing, global atmospheric transparency) are as large as the effect sought. **Any light-pollution reconstruction from these plates needs a differential design** (a contemporaneous dark-site twin) and ideally pixel-level sky background, not limiting magnitude alone.

## P8 — what shape is the 1974–89 decline? (`analysis/p8_shape.py`, all 31 positions, fixed exposure: dnb 36 min n=935 over 1976–89, dsb 30 min n=1152 over 1981–89 plus 11 plates in 1979)

Note on sample: the P3 table used the original 15 positions (dnb n=561, dsb n=468); P8 uses all 31. With the larger sample and position fixed effects the Oak Ridge slope comes out slightly shallower than Mt John's, which is the same direction as the P4 differential (+0.31 ± 0.11 on shared positions). The two tables are consistent; neither shows an Oak Ridge excess.

Pre-registered 2026-10-27 after Peter Williams (DASCH DR7) replied that emulsions "generally got better with time," which removes the most natural plate-side explanation. Three candidates, three tests. Thresholds fixed in advance: ΔBIC 6; "same slope" = overlapping 2σ.

**(a) Pulse vs drift.** A volcanic-aerosol pulse (El Chichón, April 1982, 1-yr e-folding) against a linear drift:

| series | linear slope (mag/decade) | ΔBIC pulse − linear | both: slope | both: pulse |
|---|---|---|---|---|
| dnb | −0.422 ± 0.048 | +71.7 (linear wins) | −0.419 ± 0.049 | +0.03 ± 0.11 (nil) |
| dsb | −0.449 ± 0.050 | +22.0 (linear wins) | −0.347 ± 0.055 | +0.29 ± 0.07 (wrong sign for dimming) |

Yearly medians fall steadily on both cameras; there is no 1982–85 dip. **Volcanic pulse rejected.** The drift persists in every model.

**(b) Non-Damon series.** In 1974–89 the dataset contains only Damon cameras (dnb 2416, dsb 1250, dnr 182, dsr 121, dny 35) plus 16 `mc` plates. The Damon-specific vs DR7-wide test is **not feasible** with DR7: nothing else was running. (dsr, 1982–84 only, n=118 at 40 min: −1.03 ± 0.47, same sign.)

**(c) Catalog check.** limMagAtlas on the same plates: dnb −0.391 ± 0.048, dsb −0.438 ± 0.047 mag/decade, versus APASS −0.423 ± 0.048 and −0.457 ± 0.050. ATLAS − APASS drifts by only +0.03 ± 0.01 and +0.02 ± 0.01 per decade. **Not a catalog-specific artifact.** Both catalogs see the same plate photometry, so this does not clear the upstream pipeline.

**(d) Controls and diagnostics.**
- Plate position: on dnb my sampled positions sit farther from plate center after 1982 (median 5–6 cm → 7.3 cm). Adding centerdist + edgedist: dnb −0.400 ± 0.048, dsb −0.461 ± 0.049. Adding 15° position fixed effects as well: dnb −0.382 ± 0.044, dsb −0.520 ± 0.048. **Drift survives.**
- Color term (medianColortermApass) vs year: flat on both cameras (slope 0.000 ± 0.005 per decade). No sign of an emulsion or filter change.
- Scan date (2008–2020) explains nothing: lim ~ exposure year + scan year gives scan −0.006 ± 0.005 (dnb) and −0.011 ± 0.004 (dsb) mag per scan-year, with the exposure-year slope unchanged.

**Interpretation.** The 1974–89 decline is a steady drift, common to both hemispheres, present in both calibration catalogs, with a flat color term, independent of scan epoch and plate position. That leaves (i) Damon plate stock, developing, or exposure practice changing over the decade, or (ii) an epoch-dependent term in the DR7 plate photometry upstream of the catalog match. DR7 has no non-Damon camera in this era to separate them. This is the question for the DASCH list.
