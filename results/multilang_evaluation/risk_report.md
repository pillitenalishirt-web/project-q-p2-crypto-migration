# Cryptographic Inventory Risk Report

- Scope: `data/raw/multilang_demo`
- Files scanned: 3
- Bytes scanned: 505
- Total findings: 5
- High-risk classical indicators: 3
- PQC indicators: 2

## Findings by family

- ELLIPTIC_CURVE: 1
- ML_DSA: 1
- ML_KEM: 1
- RSA: 2

## Interpretation

HIGH findings are classical public-key/key-establishment indicators requiring human review; INFO findings indicate possible PQC adoption and are not proof of secure deployment.

## Limitations

- Static source indicators may be false positives or miss indirect, aliased, dynamically loaded, binary or dependency-mediated cryptography.
- Do not include secret key material in inventory output.
- Migration decisions require protocol and implementation review.
