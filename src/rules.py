import re

RULES = [
    {
        "family": "RSA",
        "category": "classical-public-key",
        "severity": "HIGH",
        "pattern": r"\bRSA\b|\brsa\b|EVP_PKEY_RSA|RSA_(?:new|generate_key|public_encrypt|private_decrypt)|RSAEncryption|RSAPublicKey|RSAPrivateKey|PKCS1(?:v15)?|OAEP|PSS",
        "recommendation": "Review encryption and signature use. Assess approved post-quantum key establishment or signature standards according to protocol role."
    },
    {
        "family": "DSA",
        "category": "classical-public-key",
        "severity": "HIGH",
        "pattern": r"(?<!ML-)(?<!SLH-)\bDSA\b|(?<!ML-)(?<!SLH-)\bdsa\b|DSAParameterNumbers|DSAPrivateKey|DSAPublicKey",
        "recommendation": "Review digital-signature use. Assess ML-DSA or SLH-DSA and verify protocol and library compatibility."
    },
    {
        "family": "DIFFIE_HELLMAN",
        "category": "classical-key-establishment",
        "severity": "HIGH",
        "pattern": r"Diffie[-_ ]?Hellman|DHParameterNumbers|DHPrivateNumbers|DHPublicNumbers|\bDHParameters\b",
        "recommendation": "Review key-establishment use. Assess ML-KEM or an approved hybrid approach appropriate to the protocol."
    },
    {
        "family": "ELLIPTIC_CURVE",
        "category": "classical-public-key",
        "severity": "HIGH",
        "pattern": r"ECDH|ECDSA|EllipticCurve|ec\.generate_private_key|SECP(?:256|384|521)R\d+|EllipticCurvePublicKey|EllipticCurvePrivateKey",
        "recommendation": "Review elliptic-curve key exchange and signature use. Assess ML-KEM for key establishment and ML-DSA or SLH-DSA for signatures."
    },
    {
        "family": "ML_KEM",
        "category": "post-quantum-indicator",
        "severity": "INFO",
        "pattern": r"\bML[-_ ]?KEM\b|\bKyber(?:[-_ ]?(?:512|768|1024))?\b",
        "recommendation": "Post-quantum key-encapsulation indicator. Verify standardized parameter set, vetted implementation and protocol integration."
    },
    {
        "family": "ML_DSA",
        "category": "post-quantum-indicator",
        "severity": "INFO",
        "pattern": r"\bML[-_ ]?DSA\b|\bDilithium(?:[-_ ]?(?:2|3|5|44|65|87))?\b",
        "recommendation": "Post-quantum signature indicator. Verify standardized parameter set, vetted implementation and protocol integration."
    },
    {
        "family": "SLH_DSA",
        "category": "post-quantum-indicator",
        "severity": "INFO",
        "pattern": r"\bSLH[-_ ]?DSA\b|\bSPHINCS\+?\b",
        "recommendation": "Post-quantum hash-based signature indicator. Review signature size, performance and implementation requirements."
    }
]

COMPILED_RULES = [(rule, re.compile(rule["pattern"], re.IGNORECASE)) for rule in RULES]
