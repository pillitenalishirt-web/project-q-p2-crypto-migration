#include <openssl/evp.h>
EVP_PKEY *make_key(void) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    return NULL;
}
