# Challenge Requirements Audit — PS-P2

## Applicable task

The latest consolidated `Updated_Challenge_Kit.pdf`, Section 10 and PS-P2 entry, defines this as a classical software task, not a quantum-circuit task. It asks for a scanner that discovers classical cryptographic usage in a provided multi-language sample, classifies quantum risk, recommends PQC review paths, produces a risk report, evaluates precision/recall against organizer ground truth and benchmarks scan time/memory on target platforms.

## Platform policy and document precedence

The latest consolidated kit states that the PQC track uses target Platforms A/B/C followed by custom Platform D; Section 11.2 asks participants to choose a D resource budget/configuration, rerun the benchmark and explain the trade-off. Earlier general participant instructions and older quantum-focused guides describe A/B-only Phase 1 and reserve D for Phase 2. The IBM quantum-hardware guideline and quantum processor coupling-map documents are general quantum-track material; their quantum circuits, qubit maps and Bell-correlation requirements do not apply to this classical P2 scanner. This project follows the newer PQC-specific section and explicitly records the conflict.

## Current implementation and evidence

- Scanner: source-line rules across common source/configuration extensions, plus selected Python AST import checks.
- Risk report: Markdown and JSON with finding families, high-risk classical indicators and limitations.
- Migration review mapping: RSA/ECC/DH/DSA findings include protocol-role-specific review guidance toward ML-KEM and/or ML-DSA/SLH-DSA as appropriate.
- Validation: bundled hand-labelled fixtures and unit tests; these are not organizer ground truth.
- Benchmark: A/B/C/D same-host input-budget emulations. They are not separate physical devices and do not enforce a hard system RAM cap.
- Figures: runtime, finding count, traced Python allocation and file coverage charts are generated with the benchmark tables.

## Proposed local platform budgets

The reviewed PDFs do not supply complete numeric P2-specific CPU/RAM caps. Therefore the project uses transparent proposed scan-budget proxies: A scans all eligible files; B scans at most 50 files of up to 64 KiB; C scans at most 10 files of up to 64 KiB; D scans at most 20 files of up to 16 KiB. These limits must not be described as official hardware measurements.

## Pending organizer-dependent validation

- The official planted Python/Java/C sample repository and ground-truth labels were not present in the files reviewed. Official precision/recall cannot be claimed until the organizers provide the labels.
- Public repository scans are optional additional evidence unless the organizer separately instructs otherwise; independent labels are required for precision/recall on such a repository.
- Any platform budgets supplied later by organizers should replace these proposed proxies and be rerun reproducibly.
