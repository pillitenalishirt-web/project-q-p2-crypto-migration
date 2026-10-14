# Final Build Test Record

Test date: 2026-10-14  
Python: 3.13.5  
Host: Linux-6.18.44-x86_64-with-glibc2.41

## Automated checks

- `python -m unittest discover -s tests -v`: **7 tests passed**.
- `python main.py --self-test --out results`: **passed**; 14 TP, 0 FP, 0 FN on the bundled 14-label corpus.
- `python main.py --evaluate data/raw/multilang_demo --labels tests/multilang_expected_findings.json --out results/multilang_evaluation`: **passed**; 5 TP, 0 FP, 0 FN on the five hand-authored fixture labels.
- `python main.py --benchmark data/processed/benchmark_corpus --out results/final_platform_benchmark --repeats 30`: **passed**; A/B-only output tables and four SVG charts generated after removing Platform D.
- `python -m compileall -q main.py src tests tools`: **passed**.

## Benchmark interpretation

The generated benchmark corpus contains synthetic files. A/B are same-host resource-budget profiles. Platform D is intentionally excluded from this build based on the A/B-only Phase 1 interpretation; the conflicting later kit requirement is documented in CHALLENGE_REQUIREMENTS.md. These results are reproducible for the local build environment but are not official target hardware results.

## Remaining external validation

The organizer-provided planted Python/Java/C repository and ground-truth labels were not present in the input ZIP. A public GitHub clone was attempted but network DNS was unavailable in the build environment. The project includes commands for running a real repository scan locally; no external repository scan or organizer-ground-truth result is claimed here.
