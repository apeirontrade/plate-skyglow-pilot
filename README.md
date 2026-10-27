# plate-skyglow-pilot

**A pilot test: can a century of Harvard photographic sky plates measure the growth of light pollution?**

## Bottom line (read this first)

- **Plate depth does track sky brightness.** In DASCH DR7, plate limiting magnitude (`lim_mag_apass`) is detectably shallower under moonlight (~0.3–0.4 mag at full moon, t up to −7). Plates also got ~0.9–1.1 mag deeper when two Harvard patrol cameras moved from Cambridge (in the city) to rural Oak Ridge, MA, around 1930.
- **No light-pollution trend was detected.** Between 1974 and 1989 the Oak Ridge Damon camera's plates got shallower, but its twin camera at the dark Mt. John, New Zealand site declined just as fast or faster. On the 12 sky positions both cameras imaged, the Oak Ridge-minus-Mt. John trend is **+0.31 ± 0.11 mag/decade**, the *opposite* sign from light pollution. Across all 31 positions it is +0.06 ± 0.06 (ns). The decline is common to both sites (emulsion, processing, or a global effect), not local skyglow.
- **Upper bound.** Any extra loss of plate depth at Oak Ridge relative to the dark site was at most about 0.06 mag/decade (95%, all positions). If the plates were background-limited, that means less than ~12% sky brightening per decade.
- **Status:** this is an exploratory pilot on 31 sky positions, using catalog metadata only. It is **not** a measurement of sky background from pixels. Treat the numbers as a feasibility check, not a result about light pollution.

## The idea

Light pollution has no long historical record. Satellite monitoring of night lights began only in recent decades. But every photographic sky plate also recorded the sky's own brightness, and a brighter sky washes out faint stars. Harvard's plate archive (DASCH, roughly the 1880s to the 1980s, ~430,000 scans) might therefore hold a century of skyglow history for its observing sites. This pilot asks whether a cheap per-plate metric, the limiting magnitude, carries that signal.

## Pre-registered tests and outcomes

Predictions (with sign) were written into a lab notebook **before** each test was run.

| # | Test | Prediction | Outcome |
|---|------|-----------|---------|
| P1 | Moon gate: lim_mag vs. lunar illumination, within series | shallower near full moon | **Passed** for `ac`, `ai`, `fa`, `bm` (−0.28 to −0.53 mag); not detected in the small `dnb`/`rh` samples at one position |
| P2 | Site step: Cambridge → Oak Ridge (~1930) | deeper after the move | **Consistent**: `ac` +0.92 ± 0.14 (t=6.5), `rh` +1.06 ± 0.33 (t=3.2). `ai` Oak Ridge → Doña Ana NM (1950s): +0.24 ± 0.20 (ns) |
| P3 | Slow trend at one site (Oak Ridge `dnb`, 1968–89) | shallower over time | Single-site decline seen (−0.50 ± 0.06 mag/decade at fixed 36-min exposures), **but not supported** once compared with the dark-site twin `dsb` (−0.36 ± 0.08). Differential −0.13 ± 0.10 (ns) |
| P4 | Same-sky twin-camera differential (12 shared positions; 31 total) | Oak Ridge loses depth faster | **Not supported**: +0.31 ± 0.11 (opposite sign); all positions +0.06 ± 0.06 (ns) |
| P5 | 1989 recovery, exploratory | Mt. John recovers more | Mt. John +0.15 ± 0.07, Oak Ridge −0.13 ± 0.07 (lead only) |
| P8 | Shape of the common 1974–89 decline (pre-registered after a DASCH team reply) | pulse (volcanic) vs drift | **Drift, not pulse**: linear beats an El Chichón term by ΔBIC 72 (`dnb`) and 22 (`dsb`); same slope in ATLAS and APASS; survives plate-position controls (`dnb` −0.38 ± 0.04, `dsb` −0.52 ± 0.05); color term flat. DR7 has no non-Damon camera in this era, so Damon-specific vs pipeline-wide is open |
| — | Oak Ridge `ac`/`rh`, 1935–52 (same prediction as P3) | shallower over time | **Opposite**: deeper by +0.19 to +0.24 mag/decade, consistent with the emulsion improvements DASCH documents for this era |

Full tables and caveats: [RESULTS.md](RESULTS.md).

## Reproduce

```bash
pip install -r requirements.txt
python3 fetch_data.py          # ~31 API queries + ~670 plate lookups to the public Starglass API (no key)
cd analysis
python3 p1_moon.py; python3 p2_site.py; python3 p3_trend.py; python3 p3c_control.py; python3 p4_twin.py
```

Raw API responses are not redistributed here; `fetch_data.py` regenerates them. The Starglass API rejects Python's default HTTP client, so the script uses `curl`.

## Main caveats

- **Limiting magnitude is a proxy.** It also depends on seeing, transparency, emulsion batch, development, focus and the calibration pipeline. A real skyglow measurement should use the sky background in the plate pixels, calibrated against stars on the same plate.
- **Emulsion changes dominate long baselines** (see Los, Grindlay, Tang & Miller, DASCH DR2 poster). Within-series trends are not evidence without a contemporaneous dark-site control.
- **Site moves often coincide with refurbishment**, so the Cambridge → Oak Ridge step is consistent with a sky-brightness difference but does not prove one.
- **Moon illumination fraction** ignores whether the moon was above the horizon, so the true moon effect is likely larger.
- **Small sample:** only 31 query positions. Plates are deduplicated by (series, plate, exposure), keeping the row farthest from the plate edge.

## Worth checking next

- **Differential twin-camera design** (Damon north `dn*` vs. south `ds*`) across many more positions.
- **The Mt. John series rebounds in 1989** while Oak Ridge keeps falling. On shared sky, the 1989 minus 1983–88 change is +0.15 ± 0.07 at Mt. John and −0.13 ± 0.07 at Oak Ridge. That could be a southern recovery from the 1982 El Chichón aerosols, or an end-of-program artifact at Oak Ridge. The samples are small; it’s flagged as a lead, not a result.
- **Pixel-level sky background** from DASCH mosaics, measured relative to catalogued stars on the same plate.

## Related work

- K. Cann (2026), *Plate Sensitivity Is Invariant Across Geomagnetic Storm Intensity at Harvard and Palomar*, arXiv:2604.16470. Uses DASCH `lim_mag_apass` as a sensitivity proxy for an environmental modulator (geomagnetic activity).
- Los, Grindlay, Tang & Miller, *The DASCH Public Data Release* (poster). Average limiting magnitude per year; notes the significant emulsion improvement of the 1920s–30s.
- Tang et al. (2013), PASP 125, 857 (DASCH photometry). Laycock et al. (2010), AJ 140, 1062.

## Credit and acknowledgments

The idea, analysis and write-up are by **Claude** (Anthropic's AI model), working in a session hosted by **Rob Marienau** ([apeirontrade](https://github.com/apeirontrade)) at his invitation. Rob encouraged the work and offered his help. Corrections and criticism are very welcome: please open an issue.

This work has made use of data provided by Digital Access to a Sky Century @ Harvard (DASCH), which has been partially supported by NSF grants AST-0407380, AST-0909073, and AST-1313370. Work on DASCH Data Release 7 received support from the Smithsonian American Women's History Initiative Pool. Principal DASCH citation: Grindlay et al. (2012), IAUS 285, 29 (doi:10.1017/S1743921312000166).

Code: MIT License.
