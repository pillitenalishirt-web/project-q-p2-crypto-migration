# Technical Report — PS-P2 Crypto Inventory & Migration Planner

## 1. Problem and approach

PS-P2 asks for a scanner that discovers classical cryptographic usage in a multi-language codebase, classifies quantum migration risk, and recommends post-quantum review paths. This implementation uses source-line rules across common code/configuration extensions and selected Python AST import checks. Findings include path, line, algorithm family, evidence, severity/priority and review guidance.

## 2. Migration mapping

- RSA and elliptic-curve key establishment: review whether ML-KEM or an approved hybrid key-establishment design fits the protocol.
- DSA/ECDSA and other classical signatures: review ML-DSA or SLH-DSA according to protocol, policy and library support.
- Diffie–Hellman: review key-establishment role and hybrid migration options.
- ML-KEM is standardized in NIST FIPS 203; ML-DSA in FIPS 204; SLH-DSA in FIPS 205.

These are review directions, not drop-in replacements. The correct migration depends on protocol role, interoperability, parameter sets, vetted libraries and organizational requirements.

## 3. Validation

The included labelled corpus has 14 expected line/family findings across four small files. The cross-language demo contains participant-created Python/Java/C examples with five hand-authored labels. These are development fixtures, not organizer ground truth, and their scores are not generalizable to real repositories.

## 4. Benchmark method

Each profile is run 30 times using `time.perf_counter()`. The output records mean/median/min/max runtime, eligible files scanned, bytes scanned, findings, throughput and median peak Python-traced allocation (`tracemalloc`). Traced allocation is not total process memory/RSS.

### Current local A/B/C/D benchmark

Environment: Windows-11-10.0.26300-SP0; Python 3.12.10. Dataset: `data/processed/benchmark_corpus` (synthetic generated corpus). Repetitions: 30 per profile. Measurement timestamp: 2026-10-14T21:52:58+05:30.

| Profile | Files scanned | Bytes scanned | Findings | Mean time (s) | Median time (s) | Median traced allocation (bytes) |
|---|---:|---:|---:|---:|---:|---:|
| Platform A — all eligible files | 151 | 48063 | 900 | 0.32140681 | 0.26205115 | 496,987 |
| Platform B — up to 50 files / 64 KiB each | 50 | 15885 | 295 | 0.09206985 | 0.09095375 | 197,916 |
| Platform C — up to 10 files / 64 KiB each (embedded-style proxy) | 10 | 3033 | 54 | 0.02667599 | 0.02648635 | 144,561 |
| Platform D — up to 20 files / 16 KiB each (custom proxy) | 20 | 6315 | 115 | 0.04367638 | 0.04329100 | 144,561 |

These are same-host scan-budget emulations, not separate physical devices or official organizer measurements. B/C/D scan limits can reduce coverage; a lower runtime or lower finding count is not evidence of better scanner accuracy or a faster physical device. The exact profile configuration and raw results are in `platforms/platform_profiles.json` and `results/final_platform_abcd_benchmark/`.

### Figures

![Runtime comparison](results/final_platform_abcd_benchmark/figures/runtime_comparison.svg)

![Finding count comparison](results/final_platform_abcd_benchmark/figures/finding_count_comparison.svg)

![Traced allocation comparison](results/final_platform_abcd_benchmark/figures/memory_comparison.svg)

![Files scanned comparison](results/final_platform_abcd_benchmark/figures/coverage_comparison.svg)

## 5. Platform interpretation and D rationale

The latest consolidated `Updated_Challenge_Kit.pdf` defines the PQC track as classical software measured on target Platforms A/B/C followed by a custom Platform D. The P2-specific numeric CPU/RAM limits were not fully specified in the PDFs reviewed. This project therefore proposes reproducible input-budget proxies: A scans all eligible files; B scans at most 50 files up to 64 KiB each; C scans at most 10 files up to 64 KiB each; D scans at most 20 files up to 16 KiB each. D is custom because it selects an intermediate bounded-scan budget; it is not a separate physical device and does not enforce a total RAM cap.

## 6. Organizer ground truth and external validation

The official kit describes an organizer-provided Python/Java/C sample with planted cryptographic usages and says ground truth is withheld until judging. That sample and its labels were not present in the files reviewed for this build. Therefore, official precision/recall remains pending. The bundled demo is not a substitute. Run the official sample and evaluate against the organizer labels if/when provided. A public repository scan may be added as optional exploratory evidence; without independently reviewed labels, report findings and runtime only.

## 7. Limitations

- Text rules can match comments/strings and may miss aliases, wrappers, runtime-loaded modules, binaries and dependency-mediated cryptography.
- Python AST support covers selected imports; Java and C use source-line patterns, not full language ASTs.
- Risk scores are heuristic prioritization labels, not calibrated probabilities.
- The included corpora are small; perfect fixture metrics are not a real-world performance estimate.
- A/B/C/D results are same-host input-budget emulations. They are not official CPU/RAM measurements.
- Older general participant instructions/quantum guides say Phase 1 is A/B only, while the later consolidated kit explicitly specifies A/B/C and custom D for PQC. This project follows the newer PQC-specific section and records the conflict in `CHALLENGE_REQUIREMENTS.md`.

## 8. Reproducibility

From the project root run `python -m unittest discover -s tests -v`, `python main.py --self-test`, and `python main.py --benchmark data/processed/benchmark_corpus --out results/final_platform_abcd_benchmark --repeats 30`. Record OS, Python version, date, command, profile configuration and data source. Do not publish secrets or private key material.
