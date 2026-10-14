from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import dsa
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
curve_key = ec.generate_private_key(ec.SECP256R1())
signature_key = dsa.generate_private_key(key_size=2048)
exchange_name = "Diffie-Hellman"

module_number = 28
