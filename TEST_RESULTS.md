# Test and Benchmark Results

- Automated unit tests: **passed** (see the terminal output from the final run).
- Labelled-corpus self-test: completed against the bundled 4-file/732-byte corpus. Its 14/14 metrics are fixture-only and are not generalizable.
- Cross-language demonstration evaluation: completed against the included participant-created Python/Java/C fixtures, not organizer ground truth.
- A/B/C/D benchmark: completed with 30 repetitions per profile on `data/processed/benchmark_corpus`; raw tables and four SVG charts are under `results/final_platform_abcd_benchmark/`.
- Environment: Windows-11-10.0.26300-SP0; Python 3.12.10; timestamp 2026-10-14T21:52:58+05:30.

All platform profiles are same-host input-budget emulations, not official physical-target measurements. Official precision/recall against organizer ground truth remains pending until the organizer sample and labels are available.
