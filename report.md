# Technical Report — P2 Crypto Inventory & Migration Planner

## 1. Problem and approach

P2 asks for a static scanner that discovers classical cryptographic indicators, assesses quantum migration risk, and recommends post-quantum review paths. The scanner examines source/configuration lines, supplements selected Python imports with AST analysis, and exports findings with path, line, family, evidence, severity, a simple priority score, and a review recommendation.

The priority score is intentionally heuristic: `HIGH` classical public-key/key-establishment indicators receive 90; PQC indicators receive 10 because they are positive inventory signals, not evidence of a vulnerability. These values are prioritization labels, not calibrated probabilities.

## 2. Migration mapping

- RSA, DSA, Diffie–Hellman and elliptic-curve indicators should be reviewed in their protocol role.
- NIST FIPS 203 defines ML-KEM for key establishment.
- NIST FIPS 204 defines ML-DSA for digital signatures.
- NIST FIPS 205 defines SLH-DSA for hash-based digital signatures.

The mapping is a starting point only. Algorithm replacement must account for protocol compatibility, validated implementations, parameter sets, performance, interoperability and organizational policy.

## 3. Validation

The project includes:
- A small labelled Python corpus with 14 expected line/family findings.
- A small cross-language demonstration corpus containing Python, Java and C examples, with five expected line/family labels.
- Seven unit tests covering labelled metrics, missing paths, neutral files, Python AST import recognition, resource limits, cross-language examples and risk metadata.

The included corpora are intentionally small, controlled examples. Their precision/recall do not estimate real-world performance. The cross-language fixtures are project-created examples, not the organizer-provided ground truth.

## 4. Benchmark method

The benchmark runs each profile repeatedly with `time.perf_counter()`. It records mean, median, min/max runtime, files and bytes scanned, findings, throughput, and median peak Python-traced allocation using `tracemalloc`. The latter is not total process memory/RSS.

### Latest local synthetic-corpus run

Environment: Linux x86-64, Python 3.13.5. Dataset: the bundled generated benchmark corpus (150 generated modules plus the generator file), not an external public repository. Repetitions: 30 per profile.

| Profile | Files scanned | Bytes scanned | Findings | Mean time (s) | Median traced allocation (bytes) |
|---|---:|---:|---:|---:|---:|
| Platform A — all eligible files | 151 | 48,063 | 900 | 0.11324364 | 449,563 |
| Platform B — max 50 files / 64 KiB per file | 50 | 15,885 | 295 | 0.04076672 | 184,597 |

These are reproducible local results from one host and a synthetic corpus. Lower runtime and allocation under B result primarily from scanning fewer files/bytes; they do **not** show that a constrained device is faster. Detection counts are not accuracy scores, and the scan budget reduces coverage. Raw results and charts are in `results/final_platform_benchmark/`.

## 5. Phase 1 platform scope

This project now includes Platform A, B and custom Platform D profiles. The supplied documents conflict: earlier participant instructions describe an A/B-only Phase 1 scope, while the later `Updated_Challenge_Kit.pdf` specifically asks PQC participants to design and benchmark Platform D. The D result below is a same-host resource-budget emulation, not an official physical-platform measurement.

## 6. Public repository and organizer ground truth

The official P2 descriptions refer to scanning a public repository and evaluating precision/recall against organizer ground truth. The supplied ZIP did not contain the organizer's planted multi-language repository or ground-truth labels. This environment could not clone GitHub because outbound network resolution was unavailable, so no public repository scan is claimed in this build. The README contains exact commands to run the scanner against Requests after cloning it locally.

Before submission, scan the organizer-provided Python/Java/C repository if available. Use its ground-truth labels for the official precision/recall calculation. If the organizers have not provided labels, independently review a labelled subset and clearly state its scope. Never infer ground truth from the scanner's own predictions.

## 7. Limitations

- Text/regex indicators can match comments or strings and may miss aliases, wrappers, dependency APIs, runtime-loaded modules and binaries.
- Python AST analysis is limited to selected import patterns; Java and C currently use source-line patterns rather than full language ASTs.
- Heuristic risk scores are not calibrated probabilities.
- The local Platform A/B configurations are resource-budget emulations, not official physical targets or hard RAM/CPU enforcement.
- The consolidated kit and earlier participant instructions differ on whether custom Platform D is part of Phase 1. This project includes D to address the newer kit; confirm the governing instructions with organizers if possible.

## 8. Reproducibility

Run the commands in README.md from the project root. Record Python version, OS, source repository URL and commit, scan date, command, repetition count, labels source, and whether platform profiles are official or emulated. Rerun tests and benchmarks after any change. Do not publish secrets or private key material.


## 9. Custom Platform D benchmark ? Windows 11

Environment: Windows 11, Python 3.12.10. Dataset: `data/raw/labeled_corpus` (4 files, 732 bytes). Repetitions: 30 per profile. Platform D uses a proposed custom scan budget of 16 KiB per file and 20 files. This is a same-host emulation, not a separate device.

| Profile | Files scanned | Bytes scanned | Findings | Mean time (s) | Median time (s) | Median traced Python allocation (bytes) |
|---|---:|---:|---:|---:|---:|---:|
| Platform A | 4 | 732 | 14 | 0.00539140 | 0.00403285 | 49,885 |
| Platform B | 4 | 732 | 14 | 0.00420866 | 0.00413345 | 49,885 |
| Platform D | 4 | 732 | 14 | 0.00425228 | 0.00412625 | 49,885 |

The custom D limits were not reached by this small corpus. The results therefore do not demonstrate a meaningful resource or coverage trade-off. Runtime differences are small and may reflect normal timing variation on one host. The figures and raw tables are in `results/platform_d_benchmark/`. These results are separate from the earlier Linux synthetic-corpus benchmark above.
