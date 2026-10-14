# Cryptographic Inventory Risk Report

- Scope: `data/raw/labeled_corpus`
- Files scanned: 4
- Bytes scanned: 732
- Total findings: 14
- High-risk classical indicators: 10
- PQC indicators: 4

## Findings by family

- DIFFIE_HELLMAN: 1
- DSA: 2
- ELLIPTIC_CURVE: 4
- ML_DSA: 1
- ML_KEM: 2
- RSA: 3
- SLH_DSA: 1

## Interpretation

HIGH findings are classical public-key/key-establishment indicators requiring human review; INFO findings indicate possible PQC adoption and are not proof of secure deployment.

## Limitations

- Static source indicators may be false positives or miss indirect, aliased, dynamically loaded, binary or dependency-mediated cryptography.
- Do not include secret key material in inventory output.
- Migration decisions require protocol and implementation review.
