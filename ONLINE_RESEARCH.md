# Online Research Notes

Research checked while preparing this project. Challenge-specific requirements are taken from the supplied QFF PDFs; public references below inform standards context and migration design.

## NIST PQC standards

- **NIST FIPS 203 — ML-KEM:** https://csrc.nist.gov/pubs/fips/203/final
  Defines a standardized key-encapsulation mechanism for establishing shared secrets. The scanner's recommendation is a review direction for key-establishment use, not an automatic code rewrite.
- **NIST FIPS 204 — ML-DSA:** https://csrc.nist.gov/pubs/fips/204/final
  Defines the module-lattice-based digital signature standard.
- **NIST FIPS 205 — SLH-DSA:** https://csrc.nist.gov/pubs/fips/205/final
  Defines a stateless hash-based digital signature standard.
- **NIST PQC overview:** https://www.nist.gov/pqc
  Summarizes finalized standards and the need to identify where quantum-vulnerable algorithms are used before migration.
- **NIST NCCoE Migration to PQC FAQ:** https://pages.nist.gov/nccoe-migration-post-quantum-cryptography/
  Describes cryptographic inventory, risk management, CBOM concepts and migration planning resources. It notes that inventory can include algorithms, libraries, protocols, keys, certificates and system dependencies; this project currently scans source-level indicators only.
- **NIST IR 8547 draft:** https://csrc.nist.gov/pubs/ir/8547/ipd
  Discusses transition from quantum-vulnerable cryptographic standards to post-quantum standards.

## Public repository for a real-world scan

- **Requests source repository:** https://github.com/psf/requests
  A public Python HTTP library repository. The README contains commands to clone and scan it locally. This build does not claim to have scanned it because the build environment could not resolve GitHub.
- **Flask source repository:** https://github.com/pallets/flask
  An alternative public Python repository.

## Qiskit Fall Fest portal

- **Official Phase 1 hackathon workspace:** https://qffsrmap2026.com/learning/hackathon
  The supplied challenge PDFs remain the source of truth for this project's specific requirements. The portal may require a registered participant login.

## Interpretation boundaries

- Standards references are factual context; they do not mean that a source-text match proves actual algorithm use.
- ML-KEM is for key establishment; ML-DSA and SLH-DSA are signature schemes. A scanner should not recommend one interchangeable replacement for every use of RSA/ECC without understanding the protocol role.
- NIST's cryptographic inventory guidance covers more than source-code grep. This project is a limited source-level starting point and discloses that limitation.
