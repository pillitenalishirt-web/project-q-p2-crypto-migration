# Challenge Requirements Audit — P2

This file records how the supplied challenge documents were interpreted for this project.

## P2 requirements extracted from the supplied documents

- Problem: Crypto Inventory & Migration Planner / cryptographic inventory and migration scanner.
- Identify classical cryptography indicators including RSA, DSA, Diffie–Hellman and elliptic-curve cryptography.
- Recommend review/migration paths toward standardized post-quantum cryptography.
- Produce a risk-rated report.
- Measure scan time and resource use.
- Evaluate precision and recall against organizer ground truth when supplied.
- Use Python/Java/C sample code with planted cryptographic usages if the organizer-provided sample repository is available.
- Keep the project reproducible and document commands, assumptions, data and results.
- This build is configured for Platform A and Platform B only, following the A/B-only Phase 1 instructions.

## Important document conflict

The Phase 1 Participant Instructions and `QFF_2026_Phase1_Master_Challenge_Guide.pdf` describe Phase 1 as A/B only and say custom D is not required. However, the later `Updated_Challenge_Kit.pdf` specifically includes `11.2 PQC track — Platform D` and asks PQC participants to design it. This ZIP follows the A/B-only Phase 1 interpretation requested for this build. The documents conflict; confirm with the organizers before final submission if possible.

## Platform definitions and limitations

The Problem Statement Details describe Platform A as a resource-rich single-core x86-64 laptop/cloud baseline and Platform B as a constrained server with limited RAM. The supplied documents do not state a complete numerical RAM cap for the P2 platform profile. This project labels A/B as same-host resource-budget emulations. The emulation is useful to show how a scan budget changes coverage and resource use, but it is not a measurement on separate physical hardware and does not enforce a system-wide RAM cap.

## Not yet verifiable from the supplied package

- The organizer-provided Python/Java/C planted-usage repository and its ground-truth labels were not present in the ZIP.
- The local environment could not fetch a public GitHub repository, so no public repository scan is claimed in the report.
- Official P2-specific numerical Platform A/B CPU and memory settings were not included in the files available to this build.

These gaps are explicitly disclosed. The included fixtures and generated corpus are development/test assets, not substitutes for organizer ground truth.
