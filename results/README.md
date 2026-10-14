# Results

- `tables/validation_metrics.json` is the bundled labelled-corpus self-test.
- `multilang_evaluation/tables/evaluation_metrics.json` evaluates five hand-authored labels in the included Python/Java/C demonstration corpus.
- `final_platform_benchmark/tables/platform_comparison.json` contains 30-repeat measurements on the bundled synthetic corpus for same-host resource-budget profiles A and B only.
- `final_platform_benchmark/figures/` contains runtime, finding-count, traced-allocation and scanned-file charts.

These are local results on the recorded environment. The profiles are not official physical target-platform measurements, the corpora are not organizer ground truth, and the synthetic-corpus findings count is not a precision/recall score. Rerun the commands in README.md after changing the project or test data.
