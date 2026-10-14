# Project Q — Crypto Inventory & Migration Planner

**Selected problem:** P2 — Crypto Inventory & Migration Planner  
**Track:** Post-Quantum Cryptography  
**Stage:** Phase 1

## Purpose

This project statically scans source and configuration files for indicators of quantum-vulnerable public-key cryptography and post-quantum cryptography (PQC). Each finding includes a relative path, line number, algorithm family, evidence snippet, review priority, and migration guidance. CSV/JSON findings and a separate risk report are generated.

This is a source-level triage tool, not a cryptographic certification or proof that an application is secure/insecure. It does not read private key material, change source files, or perform cryptographic operations.

## Features

- Pattern-based scanning across common source/configuration extensions, including Python, Java, C/C++, JavaScript/TypeScript, Go, Rust, and configuration files.
- Python AST checks for selected asymmetric-cryptography imports.
- Indicators for RSA, DSA, Diffie–Hellman, elliptic-curve cryptography, ML-KEM/Kyber, ML-DSA/Dilithium, and SLH-DSA/SPHINCS+.
- CSV and JSON findings plus a risk summary in Markdown and JSON.
- Labelled-corpus precision/recall/F1 evaluation.
- Repeated runtime benchmark, peak Python allocation estimate, file coverage, and comparison charts.
- Platform A/B resource-budget profiles, clearly labelled local emulations rather than official physical-platform measurements.

## Quick start

Python 3.10+ is recommended. The core scanner uses the Python standard library.

```bash
python -m unittest discover -s tests -v
python main.py --self-test
python main.py --scan data/raw/labeled_corpus --out results/local_scan
python main.py --benchmark data/processed/benchmark_corpus --out results/final_platform_benchmark --repeats 30
```

Test the small Python/Java/C demonstration corpus:

```bash
python main.py --evaluate data/raw/multilang_demo --labels tests/multilang_expected_findings.json --out results/multilang_evaluation
```

## Scan a real public repository

The organizer's P2 materials ask participants to scan a public repository and report precision, recall, and scan time. Clone a repository on your own machine and record the exact commit and date. Example using Requests:

```bash
git clone --depth 1 https://github.com/psf/requests.git external/requests
git -C external/requests rev-parse HEAD
python main.py --scan external/requests --out results/requests
python main.py --benchmark external/requests --out results/requests_benchmark --repeats 30
```

To compute precision and recall on that repository, create independent labels after manually reviewing the code. Do not use scanner output as ground truth. If no independent labels are available, report findings and runtime only; do not claim measured precision/recall for the public repository.

## Platform interpretation

This Phase 1 package is configured for **Platform A and Platform B only**, following the A/B-only scope stated in the Phase 1 Participant Instructions and Master Challenge Guide. The PQC documents supplied with the project conflict on whether Platform D is required: the later `Updated_Challenge_Kit.pdf` asks PQC participants to design Platform D. This ZIP follows the A/B-only Phase 1 interpretation requested for this build; confirm the conflict with the organizers before final submission if possible.

The profiles are transparent *same-host resource-budget emulations*:
- **A:** scan all eligible files.
- **B:** at most 50 files and 64 KiB per file.

These profiles demonstrate how a scan budget affects runtime, allocation and coverage. They do not simulate a physically slower CPU or enforce a total RAM cap. Replace/supplement them with organizer-provided exact settings if available.

## Standards and migration direction

- **ML-KEM:** NIST FIPS 203, key encapsulation/key establishment.
- **ML-DSA:** NIST FIPS 204, digital signatures.
- **SLH-DSA:** NIST FIPS 205, hash-based digital signatures.

These are migration review directions, not drop-in substitutions. Validate protocol role, libraries, interoperability, parameter sets, and the applicable security policy before migrating.

## Generated outputs

Each scan output folder contains findings in CSV/JSON and a `risk_report.md` / `risk_report.json`. Benchmark output contains CSV/JSON tables and SVG charts for runtime, finding count, Python allocation estimate and files scanned. Runtime and `tracemalloc` values depend on the host, filesystem cache, Python version, and selected source tree. `tracemalloc` measures Python-traced allocations, not total resident memory (RSS).

## Limitations

- Source-line patterns can create false positives and miss indirect calls, aliases, wrappers, dynamically loaded modules, binaries, and dependency-mediated cryptography.
- A match is a lead for human review, not proof of algorithm execution.
- The included labelled examples are tiny and hand-labelled; their scores are not generalizable.
- The benchmark corpus is synthetic and is useful for repeatability, not a substitute for an organizer sample repository or a public real-world repository.
- No organizer ground-truth file was present in the supplied project ZIP. Precision/recall against organizer ground truth remains pending until that file/repository is supplied.

## References

See `sources.md`, `ONLINE_RESEARCH.md`, and `CHALLENGE_REQUIREMENTS.md`.
